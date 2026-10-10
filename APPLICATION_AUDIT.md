# Second Nurse — Application audit (architecture map)

**Audit date:** 2026-10-10  
**Scope:** Synthetic demonstration + AgntID integration workbench (not production clinical software)  
**Git:** Workspace is not a git repository at audit time.

## Executive summary

| Area | Health | Evidence |
| --- | --- | --- |
| Core API + UI | Operational | pytest, JSDOM UI tests, manual API smoke |
| Raw before path | Operational | `before.run_before`, `test_backend.py` |
| Reference mode | Operational | Non-executing fixtures verified |
| Raw MCP HTTP | Operational when token set | `test_protocol.py`, 401/503 behavior |
| AgntID SDK adapter | Code complete; live policy proof portal-dependent | `test_adapter.py`, `live_smoke.py` |
| Database | N/A (in-memory only) | By design |
| Embedded LLM agent | N/A | Simulator is external |

## Architecture diagram

```text
Browser (localhost:3000, hash routes)
    → FastAPI server.app (JSON + static web/)
        → reference: fixtures only
        → before: ward.tools + isolated store per run
        → live: server.agntid_runtime → AgntID MCP :8082/mcp → (portal) → raw ward /mcp
    → Ledger: hash-linked local events (process-global)
```

## Component inventory

| Component | Purpose | Entry point | Dependencies | Inputs / outputs | Health | Suspected / known issues | Verifying tests |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **web/** | Control room UI (6 views) | `web/index.html`, `web/app.js` | `/api/bootstrap`, runs, audit, research | User actions → API JSON → rendered DOM | Good | innerHTML used with `esc()` for user data | `tests/frontend.test.cjs` |
| **server/app.py** | HTTP API, scenarios, run orchestration | `uvicorn server.app:app` | ward, ledger, agntid_runtime | `RunRequest` → run record + events | Good | Live requires loopback; global run history | `test_backend.py`, `test_audit_fixes.py` |
| **server/agntid_runtime.py** | Official SDK task lifecycle | `AgntIDRuntime.run_actions` | agntid-sdk, env vars | prompt + actions → events + task_id | Config-dependent | Shortlist vs runtime deny semantics | `test_adapter.py` |
| **server/ledger.py** | Tamper-evident event chain | `Ledger.add` | in-memory | events with hash/prev_hash | Good | Not WORM/signed | `test_audit_fixes.py` |
| **ward/tools.py** | Synthetic ward mutations | `TOOLS` dict | `ward/data.py` store | tool args → dict results | Good | No dose policy on raw heparin (intentional) | `test_backend.py` |
| **ward/server.py** | Nine-tool FastMCP + HTTP auth | `build_mcp`, `/mcp` mount | FastMCP, `WARD_MCP_TOKEN` | MCP JSON-RPC | Good when token set | Shared MCP store across calls | `test_protocol.py` |
| **before/run_before.py** | CLI raw transcript | `python -m before.run_before` | ward.tools | stdout JSON | Good | — | manual / pytest indirect |
| **scripts/live_smoke.py** | Integration scorecard | CLI | running app on :3000 | HTTP health/runtime/runs | Good | Live allows depend on portal | manual |
| **scripts/start-local.ps1** | Load `.env.local`, start uvicorn | PowerShell | `.env.local` | env → process | Good | Secrets not in repo | manual |
| **research/** | URL inventory + synthesis | static JSON/MD | prior fetch scripts | URLs → coverage | Complete (1574 attempted) | Retrieval ≠ deep read | `docs/VALIDATION.md` |
| **AgntID runtime** | External customer-hosted | `:8080` UI, `:8082/mcp` | portal bootstrap | MCP proxy + policy | Operator-dependent | Ward must be registered for 9 tools | `live_smoke.py`, portal |

## Critical user journeys

1. **Ward overview** → select patient → view synthetic note (escaped).
2. **Agent workspace** → reference / before / live → scenario run → trace + export.
3. **Action pack** → download manifest JSON.
4. **Audit ledger** → filter/search → export.
5. **Research library** → verified + coverage tabs.
6. **Runtime connection** → check runtime (loopback when live enabled).

## Data flows

| Mode | Mutation | Provenance label |
| --- | --- | --- |
| reference | None | Illustrative reference |
| before | Isolated per-run store | raw before |
| live | Unknown locally; SDK events only | official SDK response |

## Security posture (demo)

- Live execution gated: `ENABLE_LIVE_EXECUTION`, loopback Host/peer/Origin.
- Raw MCP disabled without `WARD_MCP_TOKEN`; bearer required when enabled.
- No secrets in source; `.env.local` gitignored pattern.
- Poisoned note not rendered as HTML; no fetch of attacker image URL.

## Skills inventory

| Skill | Location | Purpose | Applicability | Guidance adopted | Status |
| --- | --- | --- | --- | --- | --- |
| review-bugbot | `~/.cursor/skills-cursor/review-bugbot` | Defect-first diff review | Optional for change sets | Reproduce before fix; table findings | Read |
| review-security | `~/.cursor/skills-cursor/review-security` | Security review subagent | Optional | No secrets in docs; harness boundaries | Read |
| review-agent | `~/.codex/skills/.system/review-agent` | Read-only defect review | Audit methodology | Defect register before edits | Not loaded (path alternate) |
| babysit | skills-cursor | CI triage | Low — no CI workflow in repo | — | Not applicable |
| share / origin | skills-cursor | Repo hosting | Not required for local audit | — | Not applicable |

`D:\Downloads\skills.zip` — not extracted during this audit (inspect-only rule). `C:\Users\skand\.agents` — not enumerated; Cursor skills-cursor used instead.

## Risks and limitations

- Not multi-tenant; run history is process-global.
- Live enforcement evidence requires portal **APPLIED** policy and nine ward tools.
- Hash-linked ledger is tamper-evident, not immutable or AgntID Reporting.
- No git repository in workspace — version control audit limited.

## References

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/VALIDATION.md](docs/VALIDATION.md)
- [agntid/SETUP.md](agntid/SETUP.md)
