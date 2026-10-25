"""
title: Open WebUI Agent Continuity Engine (ACE)
author: Joseph Tingiris / Jun
description: Session-scoped continuity tools for inspecting, locating, and reopening exact evidence from the current Open WebUI chat.
version: 0.1.0
"""

from __future__ import annotations

import re
from typing import Any, Optional

from open_webui.models.chats import Chats
from open_webui.models.users import Users
from open_webui.utils.misc import get_message_list


class Tools:
    """Agent-facing continuity tools for the current Open WebUI chat."""

    # ---------- private helpers: not exposed to the model ----------

    @staticmethod
    def _text(value: Any) -> str:
        """Return a conservative text representation for stored message content."""
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            parts: list[str] = []
            for item in value:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    text = item.get("text") or item.get("content")
                    if isinstance(text, str):
                        parts.append(text)
            return "\n".join(parts)
        return str(value)

    @staticmethod
    def _excerpt(text: str, query: str = "", limit: int = 360) -> str:
        """Create a bounded excerpt, centered near a query when possible."""
        clean = re.sub(r"\s+", " ", text or "").strip()
        if len(clean) <= limit:
            return clean

        center = 0
        if query:
            match = re.search(re.escape(query), clean, flags=re.IGNORECASE)
            if match:
                center = match.start()

        start = max(0, center - limit // 3)
        end = min(len(clean), start + limit)
        start = max(0, end - limit)
        prefix = "..." if start else ""
        suffix = "..." if end < len(clean) else ""
        return f"{prefix}{clean[start:end]}{suffix}"

    @staticmethod
    def _public_message(message: dict, *, query: str = "") -> dict:
        """Return a small, provenance-bearing message representation."""
        content = Tools._text(message.get("content"))
        return {
            "message_id": message.get("id"),
            "parent_id": message.get("parentId"),
            "role": message.get("role"),
            "created_at": message.get("timestamp") or message.get("created_at"),
            "excerpt": Tools._excerpt(content, query=query),
        }

    async def _load_current_chat(
        self,
        __chat_id__: Optional[str],
        __user__: Optional[dict],
    ) -> tuple[Any, dict[str, dict], list[dict]]:
        """Load the invoking user's current chat through Open WebUI access control."""
        if not __chat_id__:
            raise ValueError("Open WebUI did not inject a current chat ID.")

        user_id = (__user__ or {}).get("id")
        if not user_id:
            raise ValueError("Open WebUI did not inject an authenticated user ID.")

        user = await Users.get_user_by_id(user_id)
        if user is None:
            raise PermissionError("The invoking Open WebUI user could not be resolved.")

        chat = await Chats.get_accessible_chat_by_id(
            __chat_id__, user, permission="read"
        )
        if chat is None:
            raise PermissionError("The current chat is unavailable or not readable.")

        messages_map = await Chats.get_messages_map_by_chat_id(__chat_id__) or {}
        history = (chat.chat or {}).get("history") or {}
        current_id = history.get("currentId")

        # Prefer the exact current branch. If currentId is unavailable, provide a
        # deterministic fallback ordered by stored timestamps and IDs.
        chain = get_message_list(messages_map, current_id) if current_id else []
        if not chain:
            chain = sorted(
                messages_map.values(),
                key=lambda message: (
                    message.get("timestamp") or message.get("created_at") or 0,
                    message.get("id") or "",
                ),
            )

        return chat, messages_map, chain

    # ---------- public ACE API: exposed to the model ----------

    async def ace_check_context(
        self,
        __chat_id__: Optional[str] = None,
        __message_id__: Optional[str] = None,
        __metadata__: Optional[dict] = None,
        __messages__: Optional[list] = None,
        __user__: Optional[dict] = None,
        __model__: Optional[dict] = None,
    ) -> dict:
        """
        Check your present continuity position and the safe structure Open WebUI
        supplied to ACE. Use this diagnostic when validating ACE or comparing
        active request context with persisted chat history.
        """
        metadata = __metadata__ or {}
        user = __user__ or {}
        model = __model__ or {}
        messages = __messages__ or []

        return {
            "chat_id": __chat_id__,
            "message_id": __message_id__,
            "visible_message_count": len(messages),
            "metadata_keys": sorted(metadata.keys()),
            "user_keys": sorted(user.keys()),
            "model_keys": sorted(model.keys()),
            "chat_model_id": (
                metadata.get("model", {}).get("id")
                if isinstance(metadata.get("model"), dict)
                else metadata.get("model")
            ),
        }

    async def ace_get_chat(
        self,
        __chat_id__: Optional[str] = None,
        __user__: Optional[dict] = None,
        __messages__: Optional[list] = None,
    ) -> dict:
        """
        Get a compact structural account of your current persisted Open WebUI
        chat. Use this to learn what durable history exists here and compare it
        with the messages visible in the current request. This does not dump the
        transcript.
        """
        try:
            chat, messages_map, chain = await self._load_current_chat(
                __chat_id__, __user__
            )
            history = (chat.chat or {}).get("history") or {}
            roles: dict[str, int] = {}
            for message in chain:
                role = message.get("role") or "unknown"
                roles[role] = roles.get(role, 0) + 1

            return {
                "chat_id": chat.id,
                "title": chat.title,
                "owner_user_id": chat.user_id,
                "created_at": chat.created_at,
                "updated_at": chat.updated_at,
                "current_message_id": history.get("currentId"),
                "visible_message_count": len(__messages__ or []),
                "persisted_message_count": len(messages_map),
                "current_branch_message_count": len(chain),
                "current_branch_roles": roles,
                "has_forks": len(messages_map) > len(chain),
            }
        except Exception as error:
            return {
                "error": type(error).__name__,
                "message": str(error),
                "chat_id": __chat_id__,
            }

    async def ace_search_transcript(
        self,
        query: str,
        limit: int = 10,
        __chat_id__: Optional[str] = None,
        __user__: Optional[dict] = None,
    ) -> dict:
        """
        Search your current persisted chat for earlier exact text when something
        relevant may have fallen outside active context. Returns candidate
        coordinates and bounded excerpts, not reconstructed memories.
        :param query: Text to locate case-insensitively in stored user and assistant messages.
        :param limit: Maximum candidate coordinates to return, from 1 to 25.
        """
        query = (query or "").strip()
        if not query:
            return {"error": "query_required", "message": "Provide text to search for."}

        limit = max(1, min(int(limit), 25))
        try:
            chat, _messages_map, chain = await self._load_current_chat(
                __chat_id__, __user__
            )
            results: list[dict] = []
            for position, message in enumerate(chain):
                content = self._text(message.get("content"))
                if query.casefold() in content.casefold():
                    candidate = self._public_message(message, query=query)
                    candidate["position"] = position
                    results.append(candidate)
                    if len(results) >= limit:
                        break

            return {
                "chat_id": chat.id,
                "query": query,
                "match_type": "case_insensitive_substring",
                "result_count": len(results),
                "results": results,
                "target_unresolved": not results,
            }
        except Exception as error:
            return {
                "error": type(error).__name__,
                "message": str(error),
                "chat_id": __chat_id__,
            }

    async def ace_get_message(
        self,
        message_id: str,
        __chat_id__: Optional[str] = None,
        __user__: Optional[dict] = None,
    ) -> dict:
        """
        Get one exact persisted message from your current chat after you know its
        coordinate. Use this to replace recollection or a search excerpt with
        source evidence.
        :param message_id: Exact message coordinate returned by another ACE operation.
        """
        try:
            chat, messages_map, chain = await self._load_current_chat(
                __chat_id__, __user__
            )
            message = messages_map.get(message_id)
            if message is None:
                return {
                    "chat_id": chat.id,
                    "message_id": message_id,
                    "found": False,
                }

            result = self._public_message(message)
            result["content"] = self._text(message.get("content"))
            result["found"] = True
            result["chat_id"] = chat.id
            result["on_current_branch"] = any(
                item.get("id") == message_id for item in chain
            )
            return result
        except Exception as error:
            return {
                "error": type(error).__name__,
                "message": str(error),
                "chat_id": __chat_id__,
            }

    async def ace_get_context(
        self,
        message_id: str,
        before: int = 3,
        after: int = 3,
        __chat_id__: Optional[str] = None,
        __user__: Optional[dict] = None,
    ) -> dict:
        """
        Revisit the exact conversation surrounding a known historical message.
        Use this after finding a promising coordinate when you need to understand
        what led to it and what followed on the current branch.
        :param message_id: Exact message coordinate to center in the returned neighborhood.
        :param before: Number of earlier branch messages to include, from 0 to 20.
        :param after: Number of later branch messages to include, from 0 to 20.
        """
        before = max(0, min(int(before), 20))
        after = max(0, min(int(after), 20))
        try:
            chat, messages_map, chain = await self._load_current_chat(
                __chat_id__, __user__
            )
            positions = {
                message.get("id"): index
                for index, message in enumerate(chain)
                if message.get("id")
            }
            position = positions.get(message_id)
            if position is None:
                return {
                    "chat_id": chat.id,
                    "message_id": message_id,
                    "found": message_id in messages_map,
                    "on_current_branch": False,
                    "message": "The coordinate is not on the current branch.",
                }

            start = max(0, position - before)
            end = min(len(chain), position + after + 1)
            neighborhood = []
            for index in range(start, end):
                item = self._public_message(chain[index])
                item["position"] = index
                item["is_target"] = index == position
                item["content"] = self._text(chain[index].get("content"))
                neighborhood.append(item)

            return {
                "chat_id": chat.id,
                "message_id": message_id,
                "found": True,
                "on_current_branch": True,
                "start_position": start,
                "end_position": end - 1,
                "messages": neighborhood,
            }
        except Exception as error:
            return {
                "error": type(error).__name__,
                "message": str(error),
                "chat_id": __chat_id__,
            }
