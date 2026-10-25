"""
title: Open WebUI Agent Continuity Engine (ACE)
author: Joseph Tingiris / Jun
description: Session-scoped continuity tools for locating and replaying exact evidence from the current Open WebUI chat.
version: 0.2.1
"""

from __future__ import annotations

import re
from typing import Any, Optional

from open_webui.models.chats import Chats
from open_webui.models.users import Users
from open_webui.utils.misc import get_message_list


ACE_VERSION = "0.2.1"
ACE_CONTRACT = "continuity-v1"
ACE_CANARY = "trustworthy recall beats plausible reconstruction"


class Tools:
    """Agent-facing continuity tools for the current Open WebUI chat."""

    @staticmethod
    def _text(value: Any) -> str:
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
    def _role(role: Optional[str]) -> str:
        """Project storage roles into a compact conversational replay voice."""
        return {
            "user": "you",
            "assistant": "me",
            "system": "system",
            "tool": "tool",
        }.get(role or "", role or "unknown")

    @staticmethod
    def _excerpt(text: str, query: str = "", limit: int = 240) -> str:
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
        return f"{'...' if start else ''}{clean[start:end]}{'...' if end < len(clean) else ''}"

    @staticmethod
    def _handle(position: int) -> str:
        return f"@{position}"

    @staticmethod
    def _position_from_handle(handle: str) -> Optional[int]:
        match = re.fullmatch(r"@?(\d+)", (handle or "").strip())
        return int(match.group(1)) if match else None

    async def _load_current_chat(
        self,
        __chat_id__: Optional[str],
        __user__: Optional[dict],
    ) -> tuple[Any, dict[str, dict], list[dict]]:
        if not __chat_id__:
            raise ValueError("Open WebUI did not inject a current chat ID.")
        user_id = (__user__ or {}).get("id")
        if not user_id:
            raise ValueError("Open WebUI did not inject an authenticated user ID.")
        user = await Users.get_user_by_id(user_id)
        if user is None:
            raise PermissionError("The invoking Open WebUI user could not be resolved.")
        chat = await Chats.get_accessible_chat_by_id(__chat_id__, user, permission="read")
        if chat is None:
            raise PermissionError("The current chat is unavailable or not readable.")
        messages_map = await Chats.get_messages_map_by_chat_id(__chat_id__) or {}
        history = (chat.chat or {}).get("history") or {}
        current_id = history.get("currentId")
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

    @staticmethod
    def _resolve_coordinate(
        coordinate: str,
        messages_map: dict[str, dict],
        chain: list[dict],
    ) -> tuple[Optional[dict], Optional[int]]:
        """Resolve a lightweight @position or durable UUID below deck."""
        position = Tools._position_from_handle(coordinate)
        if position is not None:
            if 0 <= position < len(chain):
                return chain[position], position
            return None, None
        message = messages_map.get((coordinate or "").strip())
        if message is None:
            return None, None
        for index, item in enumerate(chain):
            if item.get("id") == message.get("id"):
                return message, index
        return message, None

    @staticmethod
    def _replay(messages: list[dict]) -> str:
        blocks: list[str] = []
        for message in messages:
            role = Tools._role(message.get("role"))
            content = Tools._text(message.get("content"))
            blocks.append(f"{role}:\n{content}")
        return "\n\n".join(blocks)

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
        Diagnose ACE's present continuity position and runtime contract. Use this
        when validating installation, tool visibility, active context, or which
        ACE generation is actually running. Continuity cue: trustworthy recall
        beats plausible reconstruction.
        """
        metadata = __metadata__ or {}
        return {
            "ace_version": ACE_VERSION,
            "semantic_contract": ACE_CONTRACT,
            "semantic_canary": ACE_CANARY,
            "chat_id": __chat_id__,
            "message_id": __message_id__,
            "visible_message_count": len(__messages__ or []),
            "metadata_keys": sorted(metadata.keys()),
            "user_keys": sorted((__user__ or {}).keys()),
            "model_keys": sorted((__model__ or {}).keys()),
        }

    async def ace_get_chat(
        self,
        __chat_id__: Optional[str] = None,
        __user__: Optional[dict] = None,
        __messages__: Optional[list] = None,
    ) -> str:
        """
        Inspect continuity coverage for this current chat. Use ACE for this, not
        web access or URL fetching. This reports how much persisted conversation
        exists compared with active request context; it does not dump history.
        Continuity cue: trustworthy recall beats plausible reconstruction.
        """
        try:
            _chat, messages_map, chain = await self._load_current_chat(__chat_id__, __user__)
            fork_note = "yes" if len(messages_map) > len(chain) else "no"
            return (
                f"ACE {ACE_VERSION} | visible {len(__messages__ or [])} | "
                f"current branch {len(chain)} | persisted {len(messages_map)} | "
                f"forks {fork_note}"
            )
        except Exception as error:
            return f"ACE error: {type(error).__name__}: {error}"

    async def ace_search_transcript(
        self,
        query: str,
        limit: int = 8,
        __chat_id__: Optional[str] = None,
        __user__: Optional[dict] = None,
    ) -> str:
        """
        Search your own preserved conversation when earlier context may matter.
        Use this when the user asks whether you remember something, refers to an
        earlier discussion, asks what was said or happened before, asks you to
        look back, or when relevant history may no longer be confidently present.
        Prefer ACE retrieval over guessing, web access, URL fetching, or a
        plausible reconstruction. Search returns compact clues; replay exact
        evidence before making strong historical claims. Continuity cue:
        trustworthy recall beats plausible reconstruction.
        :param query: Distinctive text from the earlier conversation to locate. Use remembered wording or a short phrase likely to occur in the preserved chat.
        :param limit: Maximum compact candidate clues to return, from 1 to 20.
        """
        query = (query or "").strip()
        if not query:
            return "unresolved: no search text provided"
        limit = max(1, min(int(limit), 20))
        try:
            _chat, _messages_map, chain = await self._load_current_chat(__chat_id__, __user__)
            lines: list[str] = []
            for position, message in enumerate(chain):
                content = self._text(message.get("content"))
                if query.casefold() in content.casefold():
                    excerpt = self._excerpt(content, query=query)
                    lines.append(f"{self._handle(position)} {self._role(message.get('role'))}: {excerpt}")
                    if len(lines) >= limit:
                        break
            if not lines:
                return f'unresolved: no lexical match for "{query}"'
            return "\n".join(lines)
        except Exception as error:
            return f"ACE error: {type(error).__name__}: {error}"

    async def ace_get_message(
        self,
        coordinate: str,
        __chat_id__: Optional[str] = None,
        __user__: Optional[dict] = None,
    ) -> str:
        """
        Reopen one exact preserved conversational turn after ACE search gives you
        a promising coordinate such as @16. Use this for source evidence instead
        of relying on the search excerpt or on recollection. A durable message ID
        is also accepted below deck when needed. Continuity cue: trustworthy
        recall beats plausible reconstruction.
        :param coordinate: Lightweight ACE coordinate such as @16 returned by search, or an exact persisted message ID when performing forensic retrieval.
        """
        try:
            _chat, messages_map, chain = await self._load_current_chat(__chat_id__, __user__)
            message, position = self._resolve_coordinate(coordinate, messages_map, chain)
            if message is None:
                return f"unresolved: coordinate {coordinate!r} was not found"
            label = self._handle(position) if position is not None else "@off-branch"
            return f"{label} {self._role(message.get('role'))}:\n{self._text(message.get('content'))}"
        except Exception as error:
            return f"ACE error: {type(error).__name__}: {error}"

    async def ace_get_context(
        self,
        coordinate: str,
        before: int = 3,
        after: int = 3,
        __chat_id__: Optional[str] = None,
        __user__: Optional[dict] = None,
    ) -> str:
        """
        Replay the exact local conversation around a historical ACE coordinate.
        Use this after search finds a promising place, or whenever understanding
        what led to a recovered turn and what followed matters more than a single
        excerpt. Replay is source evidence: it stays close to the original
        you/me conversation and hides database machinery. Continuity cue:
        trustworthy recall beats plausible reconstruction.
        :param coordinate: Lightweight ACE coordinate such as @16 returned by search, or an exact persisted message ID.
        :param before: Number of earlier conversational turns to replay, from 0 to 20.
        :param after: Number of later conversational turns to replay, from 0 to 20.
        """
        before = max(0, min(int(before), 20))
        after = max(0, min(int(after), 20))
        try:
            _chat, messages_map, chain = await self._load_current_chat(__chat_id__, __user__)
            message, position = self._resolve_coordinate(coordinate, messages_map, chain)
            if message is None:
                return f"unresolved: coordinate {coordinate!r} was not found"
            if position is None:
                return f"unresolved: coordinate {coordinate!r} is not on the current branch"
            start = max(0, position - before)
            end = min(len(chain), position + after + 1)
            return self._replay(chain[start:end])
        except Exception as error:
            return f"ACE error: {type(error).__name__}: {error}"
