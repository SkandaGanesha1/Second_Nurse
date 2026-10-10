# Windows portal integration (AgntID + Second Nurse)

Use this checklist after [agntid/SETUP.md](../agntid/SETUP.md). Runtime UI is at `http://localhost:8080`; protected MCP is `http://localhost:8082/mcp`.

## 1. Ward MCP server (Remote HTTP)

| Field | Value |
| --- | --- |
| Connection | Remote HTTP |
| URL | `http://host.docker.internal:3000/mcp` |
| Bearer | Same value as `WARD_MCP_TOKEN` on the host (store on runtime as env var, reference as `${WARD_MCP_TOKEN}` in portal) |
| Server ID | `ward` (or stable name) |
| Prefix | `ward` (adapter accepts `draft_heparin`, `ward.draft_heparin`, `ward_draft_heparin`) |

Start the app with token enabled:

```powershell
copy .env.local.example .env.local
# Edit .env.local — set WARD_MCP_TOKEN to a long random secret
.\scripts\start-local.ps1
```

**Test Connection** → Save → wait until **Runtime sync: Applied**.

## 2. Tool review (nine tools)

In **Access Control → Tools**, classify:

- **Read:** `list_patients`, `get_patient`, `get_unit`, `get_chart_note`
- **Normal write:** `draft_transfusion`, `draft_heparin`
- **Execute:** `sign_order`, `message_family`
- **Delete:** `discard_unit`

## 3. Policy (Medium / READ_WRITE + numeric bounds)

**Access Control → Access Policies → Baseline Allow Policy:**

| Tool | Input | Min | Max |
| --- | --- | --- | --- |
| draft_heparin | units | 800 | 1200 |
| draft_heparin | route_code | 1 | 1 |
| draft_transfusion | volume_ml | 200 | 350 |

Confirm execute/delete are excluded by profile. Wait for **APPLIED** after each save.

## 4. Second Nurse live mode

In `.env.local`:

```
AGNTID_MCP_URL=http://localhost:8082/mcp
ENABLE_LIVE_EXECUTION=true
```

Restart `.\scripts\start-local.ps1`. Open `http://localhost:3000` → **Runtime connection** → **Check runtime** (loopback only).

## 5. Simulator evidence

Enable **Simulation System** (Operations → Configuration). In **Simulator**, run the Meera task from SETUP.md, then attack matrix (10000 units, sign, etc.). Capture **Reporting** correlation IDs — authoritative evidence.

## 6. Runtime container bearer secret

If the runtime cannot reach the ward URL, verify Docker can resolve `host.docker.internal` and that the runtime process has the bearer token env var matching your host `WARD_MCP_TOKEN`.
