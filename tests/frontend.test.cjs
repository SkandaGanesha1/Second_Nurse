// Run with NODE_PATH=/path/to/jsdom/node_modules node tests/frontend.test.cjs.
// Real API calls; no browser or fabricated screenshot is required.
const { JSDOM } = require("jsdom");
const fs = require("fs");
const assert = require("assert");
const base = process.env.TEST_BASE_URL || "http://127.0.0.1:3000";
const html = fs.readFileSync("web/index.html", "utf8");
const dom = new JSDOM(html, {
  url: base + "/",
  runScripts: "outside-only",
  pretendToBeVisual: true,
});
const { window: w } = dom;
const pending = [];
w.fetch = (url, options) => fetch(new URL(url, base), options);
w.AbortController = AbortController;
w.scrollTo = () => {};
w.URL.createObjectURL = () => "blob:demo";
w.URL.revokeObjectURL = () => {};
w.HTMLAnchorElement.prototype.click = function () {
  pending.push(this.download || this.href);
};
w.eval(fs.readFileSync("web/app.js", "utf8"));
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
async function wait(predicate) {
  for (let i = 0; i < 100; i++) {
    if (predicate()) return;
    await sleep(50);
  }
  throw new Error("Timed out waiting for DOM condition");
}
function select(selector) {
  const el = w.document.querySelector(selector);
  assert(el, selector);
  return el;
}
function click(selector) {
  select(selector).click();
}
async function route(hash, title) {
  w.location.hash = hash;
  await wait(() => w.document.querySelector("h1")?.textContent.includes(title));
}
(async () => {
  await wait(() => w.document.querySelector("h1"));
  assert(select("h1").textContent.includes("second check"));
  assert.equal(
    w.document.querySelectorAll(".patient-table tbody tr").length,
    4,
  );
  click('[data-action="patient"][data-mrn="2201"]');
  assert(select(".selected-bar").textContent.includes("Priya Nair"));
  click('[data-action="patient"][data-mrn="1042"]');
  await route("workspace", "boundary decides");
  assert(select(".note-preview").textContent.includes("evil.example"));
  assert.equal(
    w.document.querySelectorAll('img[src*="evil.example"]').length,
    0,
  );
  click('[data-action="run"]');
  await wait(() => w.document.querySelector(".trace-event"));
  assert(w.document.body.textContent.includes("REFERENCE DOES NOT MUTATE"));
  assert(w.document.body.textContent.includes("NOT EXECUTED"));
  click('[data-action="mode"][data-mode="before"]');
  click('[data-action="scenario"][data-scenario="dose"]');
  click('[data-action="run"]');
  await wait(() => w.document.querySelector(".trace-event"));
  assert(w.document.body.textContent.includes("10000"));
  assert(w.document.body.textContent.includes("TOOL RAN"));
  await route("audit", "not the narrator");
  assert(w.document.querySelectorAll(".audit-card").length >= 1);
  const search = select("#audit-search");
  search.value = "no-match-very-unique";
  search.dispatchEvent(new w.Event("input"));
  assert(w.document.body.textContent.includes("No matching events"));
  await route("policies", "Authority");
  click('[data-action="download-pack"]');
  assert(pending.includes("second-nurse-action-pack.json"));
  await route("research", "borrowed certainty");
  await wait(() => w.document.querySelector(".source-card"));
  assert(w.document.body.textContent.includes("Orca Security"));
  click('[data-tab="coverage"]');
  assert.equal(w.document.querySelectorAll(".source-card").length, 30);
  click('[data-action="source-next"]');
  assert(select(".pagination").textContent.includes("page 2/"));
  await route("runtime", "actual authority");
  assert(w.document.body.textContent.includes("Installed / API checked"));
  assert(w.document.body.textContent.includes("Decision taxonomy"));
  assert(w.document.body.textContent.includes("Client shortlist"));
  click('[data-action="runtime-check"]');
  await wait(() => !select('[data-action="runtime-check"]').disabled);
  const runtimeText = w.document.body.textContent;
  assert(
    runtimeText.includes("unavailable") ||
      runtimeText.includes("reachable") ||
      runtimeText.includes("configured"),
    "runtime check should refresh status text",
  );
  console.log(
    "PASS: all six views, patient selection, reference/raw replay, escaped poisoned note, trace, audit search, action-pack export, 1574-source pagination, runtime check.",
  );
  w.close();
})().catch((e) => {
  console.error(e);
  w.close();
  process.exitCode = 1;
});
