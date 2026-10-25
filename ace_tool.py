"""
title: Open WebUI Agent Continuity Engine (ACE)
author: Joseph Tingiris / Jun
description: ACE 0.3.0 · Continuity tools for finding and replaying preserved evidence from the current Open WebUI chat.
version: 0.3.0
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Literal, Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, Field

from open_webui.models.chats import Chats
from open_webui.models.users import Users
from open_webui.utils.misc import get_message_list


ACE_VERSION = "0.3.0"
ACE_CONTRACT = "continuity-v1"
ACE_TURN_CONTRACT = "turn-v1"
ACE_COORDINATE_CONTRACT = "trajectory-v1"
ACE_CANARY = "trustworthy recall beats plausible reconstruction"


class Tools:
    """Agent-facing continuity tools for the current Open WebUI chat."""

    class UserValves(BaseModel):
        find_order: Literal["oldest_first", "newest_first"] = Field(
            default="oldest_first",
            description="Order independent ACE find results by sacred source time.",
        )

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
    def _source_timestamp(message: dict) -> Optional[float]:
        value = message.get("timestamp")
        if value is None:
            value = message.get("created_at")
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _timezone_context(metadata: Optional[dict], user: Optional[dict]) -> tuple[timezone | ZoneInfo, str, str]:
        metadata = metadata or {}
        variables = metadata.get("variables") or {}
        candidates = [
            (variables.get("{{CURRENT_TIMEZONE}}") or variables.get("CURRENT_TIMEZONE"), "browser"),
            ((user or {}).get("timezone"), "profile"),
        ]
        for name, source in candidates:
            if not name or name in {"CURRENT_TIMEZONE", "{{CURRENT_TIMEZONE}}"}:
                continue
            try:
                return ZoneInfo(str(name)), str(name), source
            except (ZoneInfoNotFoundError, ValueError):
                continue
        return timezone.utc, "UTC", "fallback"

    @staticmethod
    def _display_time(message: dict, tz: timezone | ZoneInfo) -> str:
        stamp = Tools._source_timestamp(message)
        if stamp is None:
            return "time unavailable"
        dt = datetime.fromtimestamp(stamp, tz=tz)
        hour = dt.hour % 12 or 12
        return f"{dt.strftime('%b')} {dt.day}, {hour}:{dt.strftime('%M %p %Z')}"

    @staticmethod
    def _turn_header(position: int, message: dict, tz: timezone | ZoneInfo) -> str:
        return f"{Tools._handle(position)} · {Tools._display_time(message, tz)} · {Tools._role(message.get('role'))}:"

    @staticmethod
    def _find_order(user: Optional[dict]) -> str:
        valves = (user or {}).get("valves")
        value = getattr(valves, "find_order", None) if valves is not None else None
        return value if value in {"oldest_first", "newest_first"} else "oldest_first"

    @staticmethod
    def _integrity(chain: list[dict]) -> list[dict]:
        findings: list[dict] = []
        prior_stamp: Optional[float] = None
        prior_role: Optional[str] = None
        for position, message in enumerate(chain):
            stamp = Tools._source_timestamp(message)
            if stamp is None:
                findings.append({"kind": "temporal.missing_source_timestamp", "coordinate": Tools._handle(position)})
            elif prior_stamp is not None and stamp < prior_stamp:
                findings.append({"kind": "temporal.non_monotonic_trajectory", "coordinate": Tools._handle(position)})
            if stamp is not None:
                prior_stamp = stamp
            role = message.get("role")
            if role in {"user", "assistant"}:
                if prior_role == role:
                    findings.append({"kind": "conversation.role_sequence", "coordinate": Tools._handle(position), "role": role})
                prior_role = role
        return findings

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
    def _replay(messages: list[dict], start_position: int, tz: timezone | ZoneInfo) -> str:
        blocks: list[str] = []
        for offset, message in enumerate(messages):
            content = Tools._text(message.get("content"))
            blocks.append(f"{Tools._turn_header(start_position + offset, message, tz)}\n{content}")
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
        _tz, timezone_name, timezone_source = self._timezone_context(metadata, __user__)
        return {
            "ace_version": ACE_VERSION,
            "semantic_contract": ACE_CONTRACT,
            "historical_turn_contract": ACE_TURN_CONTRACT,
            "coordinate_contract": ACE_COORDINATE_CONTRACT,
            "semantic_canary": ACE_CANARY,
            "timezone": timezone_name,
            "timezone_source": timezone_source,
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
        __metadata__: Optional[dict] = None,
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
            findings = self._integrity(chain)
            _tz, tz_name, tz_source = self._timezone_context(__metadata__, __user__)
            summary = (
                f"ACE {ACE_VERSION} | visible {len(__messages__ or [])} | "
                f"current trajectory {len(chain)} | persisted {len(messages_map)} | "
                f"forks {fork_note} | integrity findings {len(findings)} | "
                f"timezone {tz_name} ({tz_source})"
            )
            if findings:
                detail = "\n".join(
                    f"{item['coordinate']} {item['kind']}" + (f" role={item['role']}" if item.get('role') else "")
                    for item in findings[:20]
                )
                return f"{summary}\n{detail}"
            return summary
        except Exception as error:
            return f"ACE error: {type(error).__name__}: {error}"

    async def ace_search_transcript(
        self,
        query: str = "",
        limit: int = 8,
        after: Optional[float] = None,
        before: Optional[float] = None,
        __chat_id__: Optional[str] = None,
        __user__: Optional[dict] = None,
        __metadata__: Optional[dict] = None,
    ) -> str:
        """
        Find preserved turns in the current conversation by remembered text, by
        source-time bounds, or by both. Use this when earlier history matters and
        is not confidently present. Findings use canonical historical-turn
        headers; exact message/context replay remains the source-evidence path.
        :param query: Optional remembered wording. Leave empty for a purely temporal find.
        :param limit: Maximum candidate turns to return, from 1 to 20.
        :param after: Optional inclusive source timestamp lower bound (Unix seconds).
        :param before: Optional exclusive source timestamp upper bound (Unix seconds).
        """
        query = (query or "").strip()
        limit = max(1, min(int(limit), 20))
        try:
            _chat, _messages_map, chain = await self._load_current_chat(__chat_id__, __user__)
            tz, _tz_name, _tz_source = self._timezone_context(__metadata__, __user__)
            matches: list[tuple[int, dict, float]] = []
            for position, message in enumerate(chain):
                content = self._text(message.get("content"))
                stamp = self._source_timestamp(message)
                if query and query.casefold() not in content.casefold():
                    continue
                if after is not None and (stamp is None or stamp < float(after)):
                    continue
                if before is not None and (stamp is None or stamp >= float(before)):
                    continue
                if query or after is not None or before is not None:
                    matches.append((position, message, stamp if stamp is not None else float("inf")))
            if not matches:
                kind = "lexical/temporal" if query and (after is not None or before is not None) else ("lexical" if query else "temporal")
                return f"unresolved: no {kind} match"
            reverse = self._find_order(__user__) == "newest_first"
            matches.sort(key=lambda item: (item[2], item[0]), reverse=reverse)
            blocks: list[str] = []
            for position, message, _stamp in matches[:limit]:
                excerpt = self._excerpt(self._text(message.get("content")), query=query)
                blocks.append(f"{self._turn_header(position, message, tz)}\n{excerpt}")
            return "\n\n".join(blocks)
        except Exception as error:
            return f"ACE error: {type(error).__name__}: {error}"

    async def ace_get_message(
        self,
        coordinate: str,
        __chat_id__: Optional[str] = None,
        __user__: Optional[dict] = None,
        __metadata__: Optional[dict] = None,
    ) -> str:
        """
        Reopen one exact preserved historical turn at an ACE coordinate. Use this
        to establish source evidence after a find rather than relying on an excerpt.
        :param coordinate: ACE coordinate such as @16, or an exact persisted ID for forensic retrieval.
        """
        try:
            _chat, messages_map, chain = await self._load_current_chat(__chat_id__, __user__)
            message, position = self._resolve_coordinate(coordinate, messages_map, chain)
            if message is None:
                return f"unresolved: coordinate {coordinate!r} was not found"
            if position is None:
                return f"unresolved: coordinate {coordinate!r} is not on the current trajectory"
            tz, _tz_name, _tz_source = self._timezone_context(__metadata__, __user__)
            return f"{self._turn_header(position, message, tz)}\n{self._text(message.get('content'))}"
        except Exception as error:
            return f"ACE error: {type(error).__name__}: {error}"

    async def ace_get_context(
        self,
        coordinate: str,
        before: int = 3,
        after: int = 3,
        __chat_id__: Optional[str] = None,
        __user__: Optional[dict] = None,
        __metadata__: Optional[dict] = None,
    ) -> str:
        """
        Replay the exact source trajectory around a historical ACE coordinate.
        Replay preserves topology order and pristine persisted content; display
        time is projected only for navigation.
        :param coordinate: ACE coordinate such as @16, or an exact persisted message ID.
        :param before: Number of earlier turns to replay, from 0 to 20.
        :param after: Number of later turns to replay, from 0 to 20.
        """
        before = max(0, min(int(before), 20))
        after = max(0, min(int(after), 20))
        try:
            _chat, messages_map, chain = await self._load_current_chat(__chat_id__, __user__)
            message, position = self._resolve_coordinate(coordinate, messages_map, chain)
            if message is None:
                return f"unresolved: coordinate {coordinate!r} was not found"
            if position is None:
                return f"unresolved: coordinate {coordinate!r} is not on the current trajectory"
            start = max(0, position - before)
            end = min(len(chain), position + after + 1)
            tz, _tz_name, _tz_source = self._timezone_context(__metadata__, __user__)
            replay = self._replay(chain[start:end], start, tz)
            findings = [f for f in self._integrity(chain[start:end])]
            if findings:
                replay += f"\n\n[continuity notice: {len(findings)} integrity finding(s); inspect ace_get_chat diagnostics]"
            return replay
        except Exception as error:
            return f"ACE error: {type(error).__name__}: {error}"

