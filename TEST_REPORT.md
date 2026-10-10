# Test report — Second Nurse audit 2026-10-10

## Environment

| Item | Value |
| --- | --- |
| OS | Windows |
| Python | 3.11.9 (`.venv`) |
| Node | 18.20.5 / 23.11.0 (shell may switch via nvm) |
| App URL | `http://localhost:3000` |
| AgntID runtime | localhost:8080 / :8082 (operator machine) |
| Git | Not a repository |

## Commands and results

| Command | Result | Notes |
| --- | --- | --- |
| `python -m pytest -q` | **PASS** (24 tests) | Includes compare API, adapter, MCP protocol |
| `node --check web/app.js` | **PASS** | |
| `python -m before.run_before` | **PASS** | JSON transcript to stdout |
| `npm ci --ignore-scripts` + `npm run test:ui` | **PASS** (after jsdom pin) | Failed on jsdom 29 + Node 18 before D-006 |
| `python scripts/live_smoke.py` | **PASS** (HTTP) | `tool_count=6`; live allows=0 (portal ward pending) |

### Excerpts

```
24 passed in 12.87s
```

```
PASS: all six views, patient selection, reference/raw replay, ...
```

```
[OK] runtime check reachable=True tool_count=6
[OK] live/safe http=200 ... allow=0 deny=6 task_id=...
```

## Skipped / blocked

| Test | Reason |
| --- | --- |
| Real Browser (@Browser) | Tool not invoked in this session; API + JSDOM used instead |
| Full live policy allow/deny | Blocked: portal ward MCP + APPLIED policy (D-002) |
| Simulator / Reporting screenshots | Manual portal workflow |

## Regression after fixes

All listed commands re-run after D-005–D-007 fixes: **PASS**.
