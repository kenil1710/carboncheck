/**
 * Drives every path on the DEMO deployment (CarbonCheckDemo: 3 filings per
 * sender per 10 minutes; OffsetGateDemo: max_age 10 minutes) with real Toucan
 * batches, and appends a plain log to docs/demo-run.log: each verdict
 * (DOUBLE_CLAIMED via interval overlap), each refusal, the consumer's allow,
 * refuse and stale refusal.
 *   node demo_paths.mjs
 */
import { readFileSync, appendFileSync, existsSync } from "node:fs";
import { connect, returnedJson } from "./harness.mjs";

const root = new URL("..", import.meta.url);
const dep = JSON.parse(readFileSync(new URL("deployments.json", root), "utf8")).contracts;
const CC = dep.CarbonCheckDemo.address;
const CANON = dep.CarbonCheck.address;
const GATE = dep.OffsetGateDemo.address;
const BATCHES = "0x8A4d7458dDe3023A3B24225D62087701A88b09DD";
const TCO2_1000 = "0xCcAcC6099debD9654C6814fCb800431Ef7549b10";
const logFile = new URL("docs/demo-run.log", root);
const log = (line) => { console.log(line); appendFileSync(logFile, line + "\n"); };

async function finalized() {
  const got = [];
  for (const url of ["https://polygon.drpc.org", "https://gateway.tenderly.co/public/polygon"]) {
    for (let i = 1; ; i++) {
      try {
        const r = await fetch(url, { method: "POST", headers: { "content-type": "application/json" }, signal: AbortSignal.timeout(20_000), body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "eth_getBlockByNumber", params: ["finalized", false] }) });
        got.push(parseInt((await r.json()).result.number, 16));
        break;
      } catch (e) { if (i >= 6) throw e; await new Promise((r) => setTimeout(r, 4000 * i)); }
    }
  }
  return Math.min(...got);
}

async function step(label, address, role, fn, args, expect) {
  const { send } = connect({ address, role });
  const r = await send(fn, args);
  const ret = returnedJson(r);
  const got = r.ok ? (ret ? JSON.stringify(ret) : String(r.returned)) : `REVERTED ${String(r.revertReason).slice(0, 160)}`;
  const pass = expect(r, ret);
  log(`[${new Date().toISOString()}] ${pass ? "PASS" : "FAIL"} ${label}`);
  log(`    ${role} -> ${fn}(${JSON.stringify(args).slice(0, 300)})`);
  log(`    tx ${r.hash} status ${r.status} ${r.seconds?.toFixed?.(1)}s`);
  log(`    => ${got}`);
  return { r, ret, pass };
}
const verdict = (v, code) => (r, ret) => r.ok && ret?.verdict === v && (!code || ret?.code === code);
const refused = (code) => (r) => !r.ok && String(r.revertReason).includes("REFUSED: " + code);

const B = await finalized();
log(`\n=== demo run ${new Date().toISOString()}  CarbonCheckDemo ${CC}  OffsetGateDemo ${GATE}  CarbonCheck ${CANON} ===`);
log(`pinned Polygon block ${B} (finalized on both RPCs)`);
let fails = 0;
const t = async (...a) => { const o = await step(...a); if (!o.pass) fails++; return o; };
const id1000 = (await t("verdict MATCHED (batch 1000, project 191, 5000 units)", CC, "demo", "file_check", [BATCHES, 1000, B], verdict("MATCHED", "ALL_FIELDS_MATCH"))).ret?.check_id;
await t("verdict MISMATCH (batch 68: serial is project 1477, its TCO2 is VCS-981)", CC, "demo", "file_check", [BATCHES, 68, B], verdict("MISMATCH", "SERIAL_PROJECT_MISMATCH"));
await t("verdict UNVERIFIABLE BATCH_NOT_FRACTIONALIZED (batch 3: Confirmed, held by a wallet)", CC, "demo", "file_check", [BATCHES, 3, B], verdict("UNVERIFIABLE", "BATCH_NOT_FRACTIONALIZED"));
await t("refusal RATE_LIMITED (4th filing by one sender in 10 min)", CC, "demo", "file_check", [BATCHES, 10, B], refused("RATE_LIMITED_UNTIL_"));
const id23 = await (async () => {
  await t("verdict MATCHED (batch 9, project 535, units 48565492..48567831)", CC, "demo2", "file_check", [BATCHES, 9, B], verdict("MATCHED"));
  return (await t("verdict MATCHED (batch 23, project 535, units 48567832..48595400: TOUCHES batch 9, no overlap)", CC, "demo2", "file_check", [BATCHES, 23, B], verdict("MATCHED"))).ret?.check_id;
})();
await t("demo range (project 1418, units 10851600..10851700, labelled; DEMO deployment only)", CC, "demo2", "demo_claim_range", [1418, 10851600, 10851700, "claimed on another registry"], (r, ret) => r.ok && ret?.project === 1418);
await t("verdict DOUBLE_CLAIMED (batch 2, project 1418, unit 10851650 inside the claimed range)", CC, "demo2", "file_check", [BATCHES, 2, B], verdict("DOUBLE_CLAIMED", "RANGE_ALREADY_CLAIMED"));
await t("verdict UNVERIFIABLE VERRA_NOT_FOUND (batch 1213: exact serial not on Verra)", CC, "filer", "file_check", [BATCHES, 1213, B], verdict("UNVERIFIABLE", "VERRA_NOT_FOUND"));
await t("verdict UNVERIFIABLE SERIAL_UNPARSABLE (batch 7: two serials joined by a comma)", CC, "filer", "file_check", [BATCHES, 7, B], verdict("UNVERIFIABLE", "SERIAL_UNPARSABLE"));
await t("verdict UNVERIFIABLE BATCH_NOT_CONFIRMED (batch 244: Rejected)", CC, "filer", "file_check", [BATCHES, 244, B], verdict("UNVERIFIABLE", "BATCH_NOT_CONFIRMED"));
await t("verdict UNVERIFIABLE BATCH_NOT_FOUND (batch 2000 does not exist)", CC, "filer2", "file_check", [BATCHES, 2000, B], verdict("UNVERIFIABLE", "BATCH_NOT_FOUND"));
await t("verdict UNVERIFIABLE BLOCK_NOT_FINALIZED (a block a day ahead)", CC, "filer2", "file_check", [BATCHES, 1000, B + 43200], verdict("UNVERIFIABLE", "BLOCK_NOT_FINALIZED"));
await t("recheck (batch 1000 again at the next block: a fresh as-of verdict)", CC, "filer2", "recheck", [id1000, B + 1], verdict("MATCHED"));
await t("refusal NOT_TOUCAN_BATCH_CONTRACT (batch 1000's TCO2 passed as the batch contract)", CC, "filer3", "file_check", [TCO2_1000, 1000, B], refused("NOT_TOUCAN_BATCH_CONTRACT"));
await t("refusal BAD_TOKEN_ID (0)", CC, "filer3", "file_check", [BATCHES, 0, B], refused("BAD_TOKEN_ID"));
await t("refusal BAD_BLOCK (before Toucan existed)", CC, "filer3", "file_check", [BATCHES, 1000, 100], refused("BAD_BLOCK"));
await t("refusal DUPLICATE (batch 1000 at the same block)", CC, "filer3", "file_check", [BATCHES, 1000, B], refused("DUPLICATE_OF_"));
await t("refusal NO_SUCH_CHECK (recheck of check 999)", CC, "filer3", "recheck", [999, B + 2], refused("NO_SUCH_CHECK"));
await t("refusal DEMO_ONLY (demo_claim_range on the canonical CarbonCheck)", CANON, "filer3", "demo_claim_range", [191, 1, 2, "should be refused"], refused("DEMO_ONLY"));
await t("gate ALLOW (batch 1000: latest verdict MATCHED, fresh)", GATE, "demo", "claim_offset", [1000, "demo offset, 5000 t"], (r, ret) => r.ok && ret?.batch_id === 1000);
await t("gate REFUSE ALREADY_CLAIMED (batch 1000 a second time)", GATE, "demo2", "claim_offset", [1000, "again"], refused("ALREADY_CLAIMED_IN_"));
await t("gate REFUSE NOT_MATCHED_MISMATCH (batch 68)", GATE, "demo", "claim_offset", [68, "x"], refused("NOT_MATCHED_MISMATCH"));
await t("gate REFUSE NOT_MATCHED_DOUBLE_CLAIMED (batch 2)", GATE, "demo", "claim_offset", [2, "x"], refused("NOT_MATCHED_DOUBLE_CLAIMED"));
await t("gate REFUSE NOT_MATCHED_UNVERIFIABLE (batch 3)", GATE, "demo", "claim_offset", [3, "x"], refused("NOT_MATCHED_UNVERIFIABLE"));
await t("gate REFUSE NO_VERDICT (batch 10: never filed)", GATE, "demo", "claim_offset", [10, "x"], refused("NO_VERDICT"));
// stale: batch 23's MATCHED becomes older than OffsetGateDemo's max_age (600 s)
const { view } = connect({ address: CC, role: "filer" });
const c23 = await view("get_check", [id23]).catch(() => null);
const waitMs = Math.max(0, ((c23?.filed_at ?? 0) + 600 + 30) * 1000 - Date.now());
log(`waiting ${Math.round(waitMs / 1000)} s until batch 23's MATCHED (check ${id23}) is older than 600 s`);
await new Promise((r) => setTimeout(r, waitMs));
await t("gate REFUSE STALE_VERDICT (batch 23: MATCHED, but older than max_age 600 s)", GATE, "demo2", "claim_offset", [23, "late"], refused("STALE_VERDICT"));
log(`=== demo run done: ${fails === 0 ? "ALL PASS" : fails + " FAIL"} ===`);
process.exit(fails ? 1 : 0);
