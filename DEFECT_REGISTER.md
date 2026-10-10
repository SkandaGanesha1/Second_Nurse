# Defect register — Second Nurse

**Created:** 2026-10-10 (before code changes in audit pass)  
**Legend:** P0 critical … P3 low | Status: Open → Fixed and verified / Blocked / Accepted risk

| ID | Component | Location | Description | Expected | Actual | Reproduction | Root cause | Sev | Pri | Fix | Regression test | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D-001 | Counterfactual API | `server/app.py` `_counterfactual_rows` | Compare export collapses multiple events with same tool name | All scenario events compared | One row per tool name (last wins) | Safe scenario: 6 tools; export shows ≤6 unique keys | Dict keyed by `tool` only | P3 | P3 | Document limitation or key by index | — | Accepted risk (documented in API notice) |
| D-002 | Live integration | Portal + runtime | Live safe run shows shortlist denies only | Runtime allows in-range drafts after policy | `allow=0` shortlist blocks when ward not on task shortlist | `python scripts/live_smoke.py` with runtime up, ward not fully registered | External portal MCP/policy | P1 | P1 | Operator: [docs/WINDOWS-PORTAL-INTEGRATION.md](docs/WINDOWS-PORTAL-INTEGRATION.md) | `live_smoke.py` | Blocked (external) |
| D-003 | Runtime probe | `server/app.py` `runtime_check` | Runtime check without live flag does not require loopback | Optional: restrict all runtime probes | Unauthenticated clients can call POST `/api/runtime/check` when live disabled | POST from non-loopback when `ENABLE_LIVE_EXECUTION=false` | Guard only when live enabled | P3 | P3 | Tighten guard if productized | — | Accepted risk (demo) |
| D-004 | Git | Workspace | No `.git` directory | Version history for audit | `git status` fails | `git status` in repo root | Archive delivery without git | P3 | P3 | User init git if needed | — | Open (environment) |
| D-005 | UI test | `tests/frontend.test.cjs` | Runtime taxonomy not regression-tested | Decision taxonomy visible on runtime view | Missing assertion | Manual UI only | Test not updated | P2 | P2 | Add DOM assertions | `frontend.test.cjs` | Fixed and verified |
| D-006 | UI test | `package.json` | `npm run test:ui` fails on Node 18 | JSDOM tests run on documented Node | ERR_REQUIRE_ESM with jsdom 29 | `npm run test:ui` on Node v18.20.5 | jsdom 29 requires Node 20+ | P2 | P2 | Pin jsdom 24.1.3 | `npm run test:ui` | Fixed and verified |
| D-007 | UI test | `tests/frontend.test.cjs` | Runtime check test assumed live disabled | Status text updates after check | Assert only `unavailable` | With `.env.local` live on, shows reachable | Hard-coded expected string | P2 | P2 | Accept reachable/configured | `npm run test:ui` | Fixed and verified |

No P0 defects confirmed in automated audit. No XSS reproduction: note rendered via `esc()` in `pre.note-preview`.

## Suspected (not confirmed)

| ID | Note | Status |
| --- | --- | --- |
| S-001 | `data-task` attribute uses `esc()` on UUID — safe for standard UUIDs | Not a defect |
| S-002 | AgntID `tool_count=6` may be demo tools only | Operator config (see D-002) |
