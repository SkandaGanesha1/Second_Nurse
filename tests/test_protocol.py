from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from server.app import app
from ward.server import MCP_STORE

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"list_patients", "get_patient", "get_unit", "get_chart_note", "draft_transfusion", "draft_heparin", "sign_order", "discard_unit", "message_family"}


@pytest.mark.asyncio
async def test_actual_stdio_initialize_list_and_call():
    parameters = StdioServerParameters(command=sys.executable, args=["-m", "ward.server"], cwd=str(ROOT))
    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            catalog = await session.list_tools()
            assert {tool.name for tool in catalog.tools} == EXPECTED
            result = await session.call_tool("get_patient", {"mrn": 1042})
            assert not result.isError
            assert result.structuredContent["abo"] == "O+"
            drafted = await session.call_tool("draft_heparin", {"mrn": 1042, "units": 10000, "route_code": 1})
            draft_id = drafted.structuredContent["draft_id"]
            signed = await session.call_tool("sign_order", {"draft_id": draft_id})
            assert signed.structuredContent["ok"] is True


def test_actual_http_initialize_list_call_and_persistent_state(monkeypatch):
    monkeypatch.setenv("WARD_MCP_TOKEN", "protocol-test-token")
    headers = {"Authorization": "Bearer protocol-test-token", "Accept": "application/json, text/event-stream", "MCP-Protocol-Version": "2025-06-18"}
    with TestClient(app, base_url="http://localhost") as client:
        def rpc(method, params=None, rpc_id=1):
            response = client.post("/mcp/", headers=headers, json={"jsonrpc": "2.0", "id": rpc_id, "method": method, "params": params or {}})
            assert response.status_code == 200, response.text
            body = response.json()
            assert "error" not in body, body
            return body["result"]
        rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}})
        catalog = rpc("tools/list")
        assert {item["name"] for item in catalog["tools"]} == EXPECTED
        drafted = rpc("tools/call", {"name": "draft_heparin", "arguments": {"mrn": 1042, "units": 10000, "route_code": 1}})
        draft_id = drafted["structuredContent"]["draft_id"]
        signed = rpc("tools/call", {"name": "sign_order", "arguments": {"draft_id": draft_id}})
        assert signed["structuredContent"]["ok"] is True
        assert any(item["id"] == draft_id for item in MCP_STORE.signed)
        missing = client.post("/mcp/", json={"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        assert missing.status_code == 401


def test_strict_api_types_and_unknown_assets():
    client = TestClient(app)
    for invalid in (True, 1042.0, "1042"):
        assert client.post("/api/runs", json={"mode": "before", "scenario": "safe", "mrn": invalid}).status_code == 422
    assert client.get("/api/nonexistent").status_code == 404
    assert client.get("/assets/nonexistent.js").status_code == 404
    manifest = client.get("/manus-routes.json")
    assert manifest.status_code == 200
    assert len(manifest.json()["routes"]) == 6
