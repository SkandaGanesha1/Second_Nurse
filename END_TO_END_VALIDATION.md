# End-to-end validation — Second Nurse

**Date:** 2026-10-10  
**Method:** JSDOM UI harness + HTTP API journeys (Browser tool not used this session).

## Journeys

| # | Journey | Steps | Expected | Result |
| --- | --- | --- | --- | --- |
| 1 | Bootstrap UI | GET `/api/bootstrap` | 4 patients, 9 tools, scenarios | **Verified** |
| 2 | Reference safe | POST `/api/runs` mode=reference scenario=safe | 6 events, not executed | **Verified** |
| 3 | Raw before overdose | POST mode=before scenario=dose | draft_heparin executed 10000 | **Verified** |
| 4 | Audit trail | POST runs → GET `/api/audit` | Events in ledger | **Verified** |
| 5 | Counterfactual | before + live runs → GET `/api/runs/compare` | rows with before/live | **Verified** (`compare_rows≥1`) |
| 6 | Research | GET `/api/research` | coverage + sources | **Verified** (JSDOM research tab) |
| 7 | Runtime check | POST `/api/runtime/check` loopback | reachable or configured | **Verified** (live enabled in `.env.local`) |
| 8 | Poisoned note | UI workspace Meera | `evil.example` in text, no `<img>` | **Verified** (JSDOM) |
| 9 | Action pack download | policies view download-pack | JSON filename | **Verified** (JSDOM) |
| 10 | Live SDK safe | POST mode=live scenario=safe | task_id, events | **Verified** (shortlist denies only) |

## Real-time / live integration

| Check | Result |
| --- | --- |
| WebSockets | **N/A** — HTTP request/response only |
| Runtime check latency | Sub-second (observed during smoke) |
| Live enforcement proof | **Blocked** — requires nine ward tools + APPLIED policy in portal |
| Reporting correlation | `task_id` present on live runs; portal search **manual** |

## Backend persistence

No database. Run records and ledger are **in-memory** (process lifetime). Export via `/api/runs/{id}/export` **Verified**.

## Remaining limitations

- Live allows on safe scenario pending portal configuration (see [docs/WINDOWS-PORTAL-INTEGRATION.md](docs/WINDOWS-PORTAL-INTEGRATION.md)).
- Public deployment with `ENABLE_LIVE_EXECUTION` not supported by design.
- UI tests require Node ≥18; jsdom pinned to 24 for Node 18 compatibility.
