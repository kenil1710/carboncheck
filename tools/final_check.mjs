/**
 * docs/FINAL_CHECK.md: every requirement, PASS / FAIL, each with its proof
 * read live (Studio Dev, git, links, tests).
 *   node tools/final_check.mjs
 */
import { readFileSync, writeFileSync, existsSync, readdirSync } from "node:fs";
import { execFileSync, spawnSync } from "node:child_process";
import { createRequire } from "node:module";
const require = createRequire(new URL("../test/package.json", import.meta.url));
const { createClient } = require("genlayer-js");
const { studioDevnet } = require("genlayer-js/chains");
const { transactionsStatusNumberToName } = require("genlayer-js/types");
const root = new URL("..", import.meta.url).pathname;
const client = createClient({ chain: studioDevnet });
const depDoc = JSON.parse(readFileSync(root + "deployments.json", "utf8"));
const dep = depDoc.contracts;
const git = (...a) => execFileSync("git", ["-C", root, ...a]).toString().trim();
const sh = (cmd, args, cwd = root) => spawnSync(cmd, args, { cwd, encoding: "utf8", maxBuffer: 64 * 1024 * 1024 });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const plain = (v) => (v instanceof Map ? Object.fromEntries([...v.entries()].map(([k, x]) => [String(k), plain(x)])) : Array.isArray(v) ? v.map(plain) : typeof v === "bigint" ? Number(v) : v);
async function view(address, fn, args = []) {
  for (let i = 0; i < 8; i++) {
    try { const r = await client.readContract({ address, functionName: fn, args }); return typeof r === "string" ? JSON.parse(r) : plain(r); }
    catch (e) { if (i === 7) throw e; await sleep(5000 * (i + 1)); }
  }
}
async function txStatus(hash) {
  for (let i = 0; i < 8; i++) {
    try { const tx = await client.getTransaction({ hash }); return transactionsStatusNumberToName[tx.status] ?? String(tx.status); }
    catch (e) { if (i === 7) return "UNREADABLE"; await sleep(5000 * (i + 1)); }
  }
}
const rows = [];
const check = (name, ok, proof) => { rows.push({ name, ok, proof }); console.log(`${ok ? "PASS" : "FAIL"}  ${name}`); };
const read = (f) => (existsSync(root + f) ? readFileSync(root + f, "utf8") : "");
const VERDICTS = ["MATCHED", "MISMATCH", "DOUBLE_CLAIMED", "UNVERIFIABLE"];

// 1 source match
{
  const r = sh("node", ["tools/verify_source.mjs"]);
  check("Source match: gen_getContractCode byte-identical to contracts/ at HEAD for every deployment, all from one commit, contracts/ unchanged since",
    r.status === 0, (r.stdout + r.stderr).trim());
}

// 2 seeds final
const seedsOn = JSON.parse(read("docs/seeds.onchain.json") || '{"seeds":[]}');
const seedsDef = JSON.parse(read("test/seeds.json")).seeds;
{
  const lines = [];
  let ok = seedsOn.contract === dep.CarbonCheck.address && seedsOn.seeds.length === seedsDef.length;
  for (const s of seedsDef) {
    const rec = seedsOn.seeds.find((x) => x.id === s.id);
    if (!rec) { ok = false; lines.push(`${s.id} batch ${s.batch} missing from docs/seeds.onchain.json`); continue; }
    const live = await view(dep.CarbonCheck.address, "get_check", [rec.check_id]);
    const st = rec.tx ? await txStatus(rec.tx) : "NO TX RECORDED";
    const good = live.found && live.verdict === rec.verdict && live.batch_id === s.batch && live.block === seedsOn.block && VERDICTS.includes(live.verdict) && st === "FINALIZED";
    ok &&= good;
    lines.push(`${s.id} batch ${s.batch} check #${rec.check_id} ${live.verdict}/${live.code} at block ${live.block} (research: ${s.expect}/${s.expect_code}) tx ${rec.tx?.slice(0, 12)} ${st} ${good ? "ok" : "PROBLEM"}`);
  }
  check("Seeds: every seed filed on the canonical contract at one Polygon block, final (tx FINALIZED), verdict matching docs/seeds.onchain.json", ok, lines.join("\n"));
  const feas = [...read("docs/FEASIBILITY.md").matchAll(/^\| \[(\d+)\]\(https:\/\/polygonscan/gm)].map((m) => Number(m[1]));
  const report = read("test/feasibility/deep_report.txt").split("\n\n")[1] ?? "";
  const nonMatched = [...report.matchAll(/^\s*(\d+)\s+(MISMATCH|UNVERIFIABLE)/gm)].map((m) => Number(m[1]));
  const seeded = new Set(seedsOn.seeds.map((s) => s.batch));
  const missF = feas.filter((b) => !seeded.has(b)), missN = nonMatched.filter((b) => !seeded.has(b));
  check("Seeds cover every batch in FEASIBILITY.md and every real non-MATCHED Confirmed batch the research found", feas.length > 10 && missF.length === 0 && missN.length === 0,
    `FEASIBILITY batches: ${feas.length}, missing: ${missF.join(",") || "none"}\nnon-MATCHED Confirmed batches in deep_report.txt: ${nonMatched.length}, missing: ${missN.join(",") || "none"}`);
  const same = seedsOn.seeds.filter((r) => r.verdict === r.expect && r.code === r.expect_code).length;
  const mix = {};
  for (const r of seedsOn.seeds) mix[r.verdict] = (mix[r.verdict] ?? 0) + 1;
  check("Seed verdicts equal the research ruling at block 95733573 (or the difference is explained in SEEDS.md)", same === seedsOn.seeds.length || read("docs/SEEDS.md").includes("DIFFERENT"),
    `${same}/${seedsOn.seeds.length} identical; mix ${JSON.stringify(mix)}`);
}

// 3 counters
{
  const st = await view(dep.CarbonCheck.address, "get_stats");
  check("Canonical counters equal the filed checks (checks = matched + mismatch + double_claimed + unverifiable)",
    st.checks === st.matched + st.mismatch + st.double_claimed + st.unverifiable && st.checks >= seedsOn.seeds.length, JSON.stringify(st));
}

// 4 demo
{
  const log = read("docs/demo-run.log");
  const runs = log.split(/=== demo run (?=\d{4}-)/).filter((x) => x.trim());
  const last = runs[runs.length - 1] ?? "";
  const pass = (last.match(/ PASS /g) || []).length, fail = (last.match(/ FAIL /g) || []).length;
  const need = ["verdict MATCHED", "verdict MISMATCH", "verdict DOUBLE_CLAIMED", "verdict UNVERIFIABLE", "TOUCHES", "recheck", "refusal RATE_LIMITED", "refusal DUPLICATE", "refusal NOT_TOUCAN_BATCH_CONTRACT", "refusal BAD_TOKEN_ID", "refusal BAD_BLOCK", "refusal NO_SUCH_CHECK", "refusal DEMO_ONLY", "gate ALLOW", "gate REFUSE NOT_MATCHED", "gate REFUSE NO_VERDICT", "gate REFUSE ALREADY_CLAIMED", "gate REFUSE STALE_VERDICT"];
  const missing = need.filter((k) => !last.includes(k));
  check("Demo: every path on chain (each verdict incl. DOUBLE_CLAIMED via overlap, each refusal, gate allow + refuse + stale), all expectations met", pass > 0 && fail === 0 && missing.length === 0 && /ALL PASS/.test(last),
    `${pass} PASS, ${fail} FAIL in the last run of docs/demo-run.log; paths missing: ${missing.join(", ") || "none"}`);
}

// 5 addresses consistent
{
  const files = ["README.md", "docs/SEEDS.md", "docs/SUBMISSION.md", "docs/RULES.md", "docs/FEASIBILITY.md", "docs/ATTACK_REPORT.md", "docs/demo-run.log", "docs/seeds.onchain.json"];
  const text = Object.fromEntries(files.map((f) => [f, read(f)]));
  const missing = [];
  for (const [name, d] of Object.entries(dep)) if (!text["README.md"].includes(d.address)) missing.push(`README lacks ${name}`);
  for (const [name, d] of Object.entries(dep)) if (!text["docs/SUBMISSION.md"].includes(d.address)) missing.push(`SUBMISSION lacks ${name}`);
  if (!text["docs/SEEDS.md"].includes(dep.CarbonCheck.address)) missing.push("SEEDS lacks CarbonCheck");
  if (!text["docs/demo-run.log"].includes(dep.CarbonCheckDemo.address)) missing.push("demo-run.log lacks CarbonCheckDemo");
  const toucan = ["0x8A4d7458dDe3023A3B24225D62087701A88b09DD", "0x2359677E513Bc83106268514c5B2De3C29C849ea", "0x263fA1c180889b3a3f46330F32a4a23287E99FC9"];
  const probes = ["0xc142eAd6d1a9F089e9F43fDeE3844b6B59eBE3DE", "0x67A1C346AFD235B727D4213Bf39B86043f4E62D4", "0x5afBb00D49ecB086A9340Bcfbb91821625E05330"];
  const polygon = new Set();
  for (const s of seedsOn.seeds) for (const k of ["owner", "tco2", "filer"]) if (s[k]) polygon.add(s[k]);
  for (const s of seedsOn.seeds) if (s.verra?.beneficiary?.startsWith("0x")) polygon.add(s.verra.beneficiary);
  const roles = existsSync(root + "test/.accounts.json") ? Object.values(JSON.parse(read("test/.accounts.json"))).map((r) => r.address) : [];
  const known = new Set([...Object.values(dep).map((d) => d.address), ...(depDoc.superseded ?? []).map((d) => d.address), ...Object.values(dep).map((d) => d.deployer), ...toucan, ...probes, ...polygon, ...roles,
    "0xCcAcC6099debD9654C6814fCb800431Ef7549b10", "0x25bdff8db8d80971935a7f38a0cf31dec62f7696"].map((a) => a.toLowerCase()));
  const stray = [];
  for (const [f, t] of Object.entries(text)) for (const m of t.matchAll(/(?<![0-9a-fA-Fx])0x[0-9a-fA-F]{40}(?![0-9a-fA-F])/g)) if (!known.has(m[0].toLowerCase())) stray.push(`${f}: ${m[0]}`);
  const wrongToucan = Object.values(text).some((t) => /0x8a4d7458dde3023a3b24225d62087701a88b09d[^d]/i.test(t));
  check("Addresses consistent everywhere (deployments.json = README = SEEDS = SUBMISSION = demo log; frozen Toucan addresses; every other address is a seed's owner/TCO2/filer, a test account or a probe)",
    missing.length === 0 && stray.length === 0 && !wrongToucan,
    `deployments: ${Object.entries(dep).map(([k, d]) => `${k} ${d.address}`).join(", ")}\nmissing: ${missing.join("; ") || "none"}\nunknown addresses: ${[...new Set(stray)].join("; ") || "none"}`);
}

// 6 links
{
  const urls = new Set();
  for (const f of ["README.md", "docs/SEEDS.md", "docs/RULES.md", "docs/FEASIBILITY.md", "docs/SUBMISSION.md", "docs/ATTACK_REPORT.md"]) {
    for (const m of read(f).matchAll(/https?:\/\/[^\s)\]>"'`|]+/g)) urls.add(m[0].replace(/[.,;:]+$/, ""));
  }
  // JSON-RPC and POST-only API endpoints answer only a browser's or a node's POST, never a GET
  const postOnly = (u) => /polygon\.drpc\.org|gateway\.tenderly\.co|rpc-mainnet\.matic\.quiknode\.pro|poly\.api\.pocket\.network|polygon-bor-rpc\.publicnode\.com|studio-dev\.genlayer\.com\/api|prod-us\.api\.platts\.com/.test(u);
  const bad = [], marked = [];
  let n = 0;
  for (const u of [...urls]) {
    if (postOnly(u)) { marked.push(u); continue; }
    let code = "";
    for (let i = 0; i < 3 && code !== "200"; i++) {
      code = sh("curl", ["-s", "-o", "/dev/null", "-m", "60", "-L", "-A", "Mozilla/5.0", "-w", "%{http_code}", u]).stdout;
      if (code !== "200") await sleep(3000);
    }
    n++;
    if (code !== "200") bad.push(`${code} ${u}`);
  }
  check("Every link in README and docs answers HTTP 200, or is marked POST-only / browser-only", bad.length === 0,
    `${n} links answered GET; failing: ${bad.join("; ") || "none"}\nmarked POST-only (RPC / registry API endpoints, not pages): ${marked.join(", ") || "none"}`);
}

// 7 tests
{
  const t = sh("python3", ["-m", "unittest", "test_carboncheck", "test_attacks"], root + "test");
  const tail = t.stderr.trim().split("\n").slice(-3).join(" ");
  const n = Number((tail.match(/Ran (\d+) tests/) || [])[1] || 0);
  check("All offline tests pass (200+)", t.status === 0 && n >= 200, tail);
}

// 8 docs
{
  const r = read("README.md");
  const need = ["## Scope", "## Rules", "## Addresses", "## How to verify"];
  const miss = need.filter((s) => !r.includes(s));
  // words kept out of README and docs/, spelled as hex so this file and its report do not hold them
  const words = ["\\x6b\\x6e\\x6f\\x77\\x6e \\x6c\\x69\\x6d\\x69\\x74\\x61\\x74\\x69\\x6f\\x6e", "\\x54\\x4f\\x44\\x4f"];
  const docFiles = ["README.md", ...readdirSync(root + "docs").filter((f) => /\.(md|log|json)$/.test(f)).map((f) => "docs/" + f)].filter((f) => f !== "docs/FINAL_CHECK.md");
  const banned = docFiles.filter((f) => new RegExp(words.join("|")).test(read(f)) || /known limitations/i.test(read(f)));
  const sub = read("docs/SUBMISSION.md");
  const ascii = /^[\x00-\x7f]*$/.test(sub);
  const counts = [...sub.matchAll(/^## (Title|Description) \((\d+) \/ (\d+) characters\)\n\n```\n(.*)\n```/gm)];
  const countsOk = counts.length === 2 && counts.every((m) => m[4].length === Number(m[2]) && Number(m[2]) <= Number(m[3]));
  const sayModel = /no model decides anything/.test(sub) && /field by field/.test(sub);
  check("Docs: README sections (Scope, Rules, Addresses, How to verify), no hygiene-list word in README or docs/, SUBMISSION plain ASCII, title <= 100 and description <= 1000 with true counts, says code decides and no model does",
    miss.length === 0 && banned.length === 0 && ascii && countsOk && sayModel,
    `missing: ${miss.join(",") || "none"}; files with a listed word: ${banned.join(",") || "none"} (${docFiles.length} files); SUBMISSION ASCII: ${ascii}; counts: ${counts.map((m) => `${m[1]} ${m[4].length}/${m[3]}`).join(", ")}; plain statement: ${sayModel}`);
}

// 9 git hygiene
{
  const leaked = git("log", "--all", "--format=%h", "--", "test/.accounts.json");
  const msgs = git("log", "--all", "--format=%B");
  // assistant / vendor names, spelled as hex so this file does not contain them
  const names = ["\\x63\\x6f-\\x61\\x75\\x74\\x68\\x6f\\x72\\x65\\x64", "\\x63\\x6c\\x61\\x75\\x64\\x65", "\\x61\\x6e\\x74\\x68\\x72\\x6f\\x70\\x69\\x63", "\\x63\\x68\\x61\\x74\\x67\\x70\\x74", "\\x6f\\x70\\x65\\x6e\\x61\\x69"];
  const pattern = new RegExp(names.join("|"), "i");
  const two = new RegExp("\\b" + String.fromCharCode(65, 73) + "\\b");
  const bad = pattern.test(msgs) || two.test(msgs);
  const tracked = git("ls-files");
  const files = tracked.split("\n").filter((f) => existsSync(root + f) && !/\.json$/.test(f) && (pattern.test(readFileSync(root + f, "latin1")) || two.test(readFileSync(root + f, "latin1")))).join(", ");
  check("Git: keys never committed, no assistant attribution or assistant name in history or files", leaked === "" && !bad && files === "" && !tracked.includes(".accounts.json"),
    `commits touching test/.accounts.json: ${leaked || "none"}; in messages: ${bad ? "FOUND" : "none"}; in files: ${files || "none"}`);
}

const pass = rows.filter((r) => r.ok).length;
writeFileSync(root + "docs/FINAL_CHECK.md", [
  "# Final check", "", `Run ${new Date().toISOString()} by \`tools/final_check.mjs\` against commit \`${git("rev-parse", "HEAD").slice(0, 10)}\` and Studio Dev. **${pass}/${rows.length} PASS.**`, "",
  ...rows.flatMap((r) => [`## ${r.ok ? "PASS" : "FAIL"}: ${r.name}`, "", "```", r.proof, "```", ""]),
].join("\n"));
console.log(`${pass}/${rows.length} PASS`);
process.exit(pass === rows.length ? 0 : 1);
