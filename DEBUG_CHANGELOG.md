# Debug changelog — audit pass 2026-10-10

| File | Defect | Change | Tests |
| --- | --- | --- | --- |
| [tests/frontend.test.cjs](tests/frontend.test.cjs) | D-005 | Assert Decision taxonomy + Client shortlist on runtime view | `npm run test:ui` PASS |
| [tests/frontend.test.cjs](tests/frontend.test.cjs) | D-007 (brittle runtime assert) | Accept reachable/configured when live env enabled | `npm run test:ui` PASS |
| [package.json](package.json) | D-006 | Pin `jsdom@24.1.3`; add `engines.node` | `npm run test:ui` on Node 18/23 |
| [server/app.py](server/app.py) | D-001 | Clarify compare API notice (one row per tool name) | `test_compare_runs_counterfactual` |

No application logic changes to AgntID adapter or ward tools in this pass.
