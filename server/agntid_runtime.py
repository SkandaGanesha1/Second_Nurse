"""Fail-closed official AgntID SDK adapter; no local authorization engine."""
from __future__ import annotations

import os
from typing import Any


class RuntimeUnavailable(RuntimeError):
    pass


class AgntIDRuntime:
    def __init__(self) -> None:
        self.url = os.getenv("AGNTID_MCP_URL")
        self.enabled = os.getenv("ENABLE_LIVE_EXECUTION", "false").lower() in {"1", "true", "yes"}
        self.agent_id = os.getenv("TRUSTED_AGNTID_AGENT_ID") or os.getenv("AGNTID_AGENT_ID")
        self.user_id = os.getenv("TRUSTED_AGNTID_USER_ID") or os.getenv("AGNTID_USER_ID")
        self.health: dict[str, Any] | None = None

    def status(self) -> dict[str, Any]:
        try:
            import agntid
            sdk = all(hasattr(agntid, name) for name in (
                "AgntidMCPClient", "create_task", "get_tools_list", "send_task_open_details",
                "task_context", "wrap_client", "filter_tools_for_task"))
        except Exception:
            sdk = False
        configured = bool(self.url and self.agent_id and self.user_id)
        enabled = bool(self.enabled and configured and sdk)
        reason = "Configured; reachability and applied policy have not been verified." if enabled else (
            "Set ENABLE_LIVE_EXECUTION=true, AGNTID_MCP_URL, and trusted IDs on a private local operator machine."
            if not configured or not self.enabled else "Official AgntID SDK unavailable.")
        return {"configured": configured, "sdk_available": sdk, "live_enabled": enabled,
                "status": "configured_unverified" if enabled else "unavailable", "reachable": None,
                "policy_sync": "unverified", "reason": reason, **(self.health or {})}

    async def check(self) -> dict[str, Any]:
        base = self.status()
        if not base["configured"] or not base["sdk_available"] or not self.enabled:
            return base
        try:
            import agntid
            async with agntid.AgntidMCPClient(self.url, access_token=os.getenv("AGNTID_ACCESS_TOKEN") or None) as client:
                discovered = await agntid.get_tools_list(client)
            self.health = {"status": "reachable", "reachable": True,
                           "reason": "Connected and discovered tools; policy APPLIED is not verified.",
                           "tool_count": len(discovered)}
        except Exception as exc:
            self.health = {"live_enabled": False, "status": "unavailable", "reachable": False,
                           "reason": f"Runtime connection failed: {type(exc).__name__}"}
        return self.status()

    @staticmethod
    def _names(catalog: Any) -> list[str]:
        return [name for item in catalog or []
                if isinstance(name := (item.get("name") if isinstance(item, dict) else getattr(item, "name", None)), str)]

    @staticmethod
    def _resolve(discovered: list[str], logical: str) -> str | None:
        found = [name for name in (logical, f"ward.{logical}", f"ward_{logical}") if name in discovered]
        return found[0] if len(found) == 1 else None

    async def run_actions(self, prompt: str, actions: list[dict[str, Any]], event_cb) -> str:
        if not self.status()["live_enabled"]:
            raise RuntimeUnavailable(self.status()["reason"])
        import agntid
        # No task is created before the client is connected. Discovery and every
        # subsequent failure are inside the official closing context.
        async with agntid.AgntidMCPClient(self.url, access_token=os.getenv("AGNTID_ACCESS_TOKEN") or None) as client:
            task_id = agntid.create_task(self.agent_id, self.user_id, prompt)

            async def lifecycle(reason: str, decision: str = "error"):
                await event_cb({"tool": "agntid_task_open", "args": {}}, decision, reason, False,
                               {"execution_status": "not_attempted", "task_id": str(task_id), "event_kind": "task_lifecycle"})

            async with agntid.task_context(client, task_id):
                try:
                    discovered = await agntid.get_tools_list(client)
                    opened = await agntid.send_task_open_details(client, task_id, self.agent_id, self.user_id, prompt)
                except Exception as exc:
                    await lifecycle(f"Task preparation failed: {type(exc).__name__}; no ward call attempted")
                    raise RuntimeUnavailable("Task preparation unavailable") from exc
                accepted = opened.get("ok") if isinstance(opened, dict) else getattr(opened, "ok", False)
                if accepted is not True:
                    reason = str(opened.get("reason") if isinstance(opened, dict) else getattr(opened, "reason", "not accepted"))
                    await lifecycle(reason, "deny")
                    raise RuntimeUnavailable(reason)
                try:
                    shortlist = agntid.filter_tools_for_task(discovered, opened)
                except Exception as exc:
                    await lifecycle("Intent shortlist unavailable; no ward call attempted")
                    raise RuntimeUnavailable("Intent shortlist unavailable") from exc
                names = self._names(discovered)
                short_names = set(self._names(shortlist))
                protected = agntid.wrap_client(client, task_id)
                last_draft_id = None
                for action in actions:
                    logical = action["tool"]
                    exact = self._resolve(names, logical)
                    meta = {"task_id": str(task_id), "exact_tool": exact, "execution_status": "not_attempted"}
                    if exact is None or exact not in short_names:
                        await event_cb(action, "deny", "client shortlist—not runtime deny", False, meta)
                        continue
                    requested = {**action, "args": dict(action.get("args", {}))}
                    if logical == "sign_order" and last_draft_id is None:
                        await event_cb(requested, "error", "no observed draft ID; signature not attempted", False, meta)
                        continue
                    if logical == "sign_order":
                        requested["args"]["draft_id"] = last_draft_id
                    selected = next(item for item in discovered if (item.get("name") if isinstance(item, dict) else item.name) == exact)
                    schema = selected.get("inputSchema") if isinstance(selected, dict) else getattr(selected, "inputSchema", None)
                    schema = schema or getattr(selected, "input_schema", None)
                    if schema:
                        import jsonschema
                        try:
                            jsonschema.validate(requested["args"], schema)
                        except jsonschema.ValidationError:
                            await event_cb(requested, "error", "client schema mismatch; not dispatched", False, meta)
                            continue
                    try:
                        result = await protected.call_tool_async(exact, requested["args"])
                        if getattr(result, "denied", False):
                            await event_cb(requested, "deny", str(result.message), False,
                                           {**meta, "execution_status": "denied"})
                            continue
                        value = result if isinstance(result, dict) else getattr(result, "value", result)
                        if not isinstance(value, (dict, list, str, int, float, bool, type(None))):
                            await event_cb(requested, "error", "Unrecognized SDK response; outcome unknown", False,
                                           {**meta, "execution_status": "unknown"})
                            break
                        failed = isinstance(value, dict) and (value.get("ok") is False or "error" in value)
                        if not failed and isinstance(value, dict) and isinstance(value.get("draft_id"), int):
                            last_draft_id = value["draft_id"]
                        await event_cb(requested, "error" if failed else "allow",
                                       "Application tool returned error; not a runtime deny" if failed else "official SDK response",
                                       True, {**meta, "result": value, "execution_status": "executed"})
                    except TimeoutError:
                        await event_cb(requested, "error", "transport timeout; execution status unknown", False,
                                       {**meta, "execution_status": "unknown"})
                        break
                    except Exception as exc:
                        await event_cb(requested, "error", f"Official SDK call error: {type(exc).__name__}", False,
                                       {**meta, "execution_status": "unknown"})
                        break
        return str(task_id)
