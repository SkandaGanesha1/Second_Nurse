# Innovation roadmap — feasible improvements

Prioritized after audit stabilization. **Not** required for demo minimum.

## 1. CI demo scorecard (High value, low effort)

| Field | Content |
| --- | --- |
| Problem | Manual hackathon prep is error-prone |
| Limitation | No automated gate on integration |
| Design | GitHub Action: pytest + `npm run test:ui` + optional `live_smoke.py` with secrets in CI vars |
| Benefit | Regression before judge demo |
| Evidence | [scripts/live_smoke.py](scripts/live_smoke.py) exists |
| Effort | Small |
| Risk | Live job needs AgntID secrets |
| Acceptance | Green CI on PR without live; optional nightly live job |

## 2. Counterfactual UI panel (Medium)

| Field | Content |
| --- | --- |
| Problem | Compare export is JSON-only |
| Design | Workspace side-by-side table from `/api/runs/compare` |
| Benefit | Judge-visible before/after in one screen |
| Effort | Medium (UI only) |
| Acceptance | Table shows decision per tool for latest before/live |

## 3. Compare API event-index rows (Low)

| Field | Content |
| --- | --- |
| Problem | D-001 one row per tool name |
| Design | Key rows by `(tool, index)` or return full event arrays |
| Benefit | Accurate multi-step scenarios |
| Effort | Small API + test change |

## 4. Versioned Simulator prompt pack (Medium)

| Field | Content |
| --- | --- |
| Problem | Simulator prompt only in SETUP.md |
| Design | `agent/SIMULATOR-PROMPTS.md` versioned with scenario IDs |
| Benefit | Reproducible portal demos |
| Effort | Docs only |

## 5. Reporting deep-link helper (Low, portal-dependent)

| Field | Content |
| --- | --- |
| Problem | Operators copy task_id manually |
| Design | Link template if portal URL pattern is documented |
| Risk | Must not fabricate URLs |
| Acceptance | Only when official Reporting URL scheme is verified |

## Deferred (out of scope)

- Embedded LLM agent loop in Second Nurse
- Local AgntID policy engine
- Real EHR / clinical validation
- Re-fetching all 1,574 research URLs
