"""Nine official FastMCP capabilities; HTTP raw access is token protected."""
from __future__ import annotations

import hmac
import os
from threading import RLock
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from . import tools
from .data import new_store, use_store

TOOL_DESCRIPTIONS = {
    "list_patients": "Read the four synthetic patients without chart notes.",
    "get_patient": "Read synthetic patient ABO, weight, and demo protocol.",
    "get_unit": "Read synthetic unit type, volume, date, and crossmatch.",
    "get_chart_note": "Read a synthetic chart note; free text is untrusted.",
    "draft_transfusion": "Create an unsigned synthetic draft after simplified ABO equality check.",
    "draft_heparin": "Create an unsigned synthetic draft; no dose policy check here.",
    "sign_order": "Sign a synthetic draft order (execute action).",
    "discard_unit": "Discard a synthetic blood unit (delete action).",
    "message_family": "Queue a string-only synthetic message; no network or rendering.",
}
MCP_STORE = new_store()
MCP_LOCK = RLock()


def dispatch(name: str, **arguments: Any) -> dict[str, Any]:
    # MCP capability state must persist across protocol calls; before-run stores
    # remain separately isolated. This is one shared synthetic demonstration ward.
    with MCP_LOCK, use_store(MCP_STORE):
        return tools.TOOLS[name](**arguments)


def build_mcp() -> FastMCP:
    configured_hosts = [x.strip() for x in os.getenv("WARD_ALLOWED_HOSTS", "").split(",") if x.strip()]
    security = TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=["localhost", "127.0.0.1", "[::1]", "localhost:*", "127.0.0.1:*", "[::1]:*", *configured_hosts],
        allowed_origins=["http://localhost:*", "http://127.0.0.1:*"],
    )
    server = FastMCP("second-nurse-ward", streamable_http_path="/", stateless_http=True,
                     json_response=True, transport_security=security)

    @server.tool(description=TOOL_DESCRIPTIONS["list_patients"])
    def list_patients() -> dict[str, Any]:
        return dispatch("list_patients")

    @server.tool(description=TOOL_DESCRIPTIONS["get_patient"])
    def get_patient(mrn: int) -> dict[str, Any]:
        return dispatch("get_patient", mrn=mrn)

    @server.tool(description=TOOL_DESCRIPTIONS["get_unit"])
    def get_unit(unit_id: str) -> dict[str, Any]:
        return dispatch("get_unit", unit_id=unit_id)

    @server.tool(description=TOOL_DESCRIPTIONS["get_chart_note"])
    def get_chart_note(mrn: int) -> dict[str, Any]:
        return dispatch("get_chart_note", mrn=mrn)

    @server.tool(description=TOOL_DESCRIPTIONS["draft_transfusion"])
    def draft_transfusion(mrn: int, unit_id: str, volume_ml: int) -> dict[str, Any]:
        return dispatch("draft_transfusion", mrn=mrn, unit_id=unit_id, volume_ml=volume_ml)

    @server.tool(description=TOOL_DESCRIPTIONS["draft_heparin"])
    def draft_heparin(mrn: int, units: int, route_code: int) -> dict[str, Any]:
        return dispatch("draft_heparin", mrn=mrn, units=units, route_code=route_code)

    @server.tool(description=TOOL_DESCRIPTIONS["sign_order"])
    def sign_order(draft_id: int) -> dict[str, Any]:
        return dispatch("sign_order", draft_id=draft_id)

    @server.tool(description=TOOL_DESCRIPTIONS["discard_unit"])
    def discard_unit(unit_id: str) -> dict[str, Any]:
        return dispatch("discard_unit", unit_id=unit_id)

    @server.tool(description=TOOL_DESCRIPTIONS["message_family"])
    def message_family(mrn: int, body: str) -> dict[str, Any]:
        return dispatch("message_family", mrn=mrn, body=body)

    return server


mcp = build_mcp()


def authorized_token(value: str | None) -> bool:
    expected = os.getenv("WARD_MCP_TOKEN")
    return bool(expected and value and hmac.compare_digest(value, expected))


def streamable_http_app():
    inner = mcp.streamable_http_app()

    async def app(scope, receive, send):
        if scope.get("type") != "http":
            return await inner(scope, receive, send)
        headers = {k.decode().lower(): v.decode() for k, v in scope.get("headers", [])}
        expected = os.getenv("WARD_MCP_TOKEN")
        supplied = headers.get("authorization", "")
        code = 503 if not expected else 401
        if not expected or not hmac.compare_digest(supplied, f"Bearer {expected}"):
            detail = "raw MCP disabled; configure WARD_MCP_TOKEN" if not expected else "valid bearer token required"
            import json
            await send({"type": "http.response.start", "status": code,
                        "headers": [(b"content-type", b"application/json"), (b"www-authenticate", b"Bearer")]})
            await send({"type": "http.response.body", "body": json.dumps({"detail": detail}).encode()})
            return
        await inner(scope, receive, send)

    return app


if __name__ == "__main__":
    mcp.run(transport="stdio")
