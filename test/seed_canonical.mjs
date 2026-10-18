/**
 * Files every seed in test/seeds.json on the CANONICAL CarbonCheck, all pinned
 * at ONE finalized Polygon block, and records each final check in
 * docs/seeds.onchain.json. Resumable: a seed already on chain at that block is
 * read back, not filed again. A seed that ends on a transport code (a source
 * did not answer) is filed again at the next block, up to 3 times.
 *   node seed_canonical.mjs
 */
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { connect, returnedJson } from "./harness.mjs";

const root = new URL("..", import.meta.url);
const dep = JSON.parse(readFileSync(new URL("deployments.json", root), "utf8"));
const seeds = JSON.parse(readFileSync(new URL("./seeds.json", import.meta.url), "utf8")).seeds;
const outPath = new URL("docs/seeds.onchain.json", root);
const address = dep.contracts.CarbonCheck.address;
const BATCHES = "0x8A4d7458dDe3023A3B24225D62087701A88b09DD";
const TRANSPORT = ["RPC_UNAVAILABLE", "RPC_DISAGREE", "BLOCK_NOT_FINALIZED", "VERRA_UNAVAILABLE", "VERRA_UNREADABLE", "INTERNAL"];
const roles = Array.from({ length: 10 }, (_, i) => "s" + String(i + 1).padStart(2, "0")).flatMap((r) => [r, r, r, r, r]);
const spare = ["s11", "s11", "s11", "s11", "s11", "s12", "s12", "s12", "s12", "s12"];

async function finalized() {
  const got = [];
  for (const url of ["https://polygon.drpc.org", "https://gateway.tenderly.co/public/polygon"]) {
    const r = await fetch(url, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "eth_getBlockByNumber", params: ["finalized", false] }) });
    got.push(parseInt((await r.json()).result.number, 16));
  }
  return Math.min(...got);
}

const prev = existsSync(outPath) ? JSON.parse(readFileSync(outPath, "utf8")) : null;
const BLOCK = prev?.contract === address && prev?.block ? prev.block : await finalized();
console.log(`CarbonCheck ${address}, seed block ${BLOCK}`);
const reader = connect({ address, role: "filer" });
async function onChain() {
  const all = [];
  for (let s = 1; ; s += 50) {
    const raw = await reader.view("list_checks", [s, 50]);
    const page = typeof raw === "string" ? JSON.parse(raw) : raw;
    all.push(...(page.checks ?? []));
    if ((page.checks ?? []).length < 50) break;
  }
  return all;
}
const results = prev?.contract === address ? prev.seeds : [];
const known = Object.fromEntries(results.map((r) => [r.id, r]));
for (let i = 0; i < seeds.length; i++) {
  const s = seeds[i];
  if (known[s.id] && !TRANSPORT.includes(known[s.id].code)) continue;
  const latest = async (blk) => (await onChain()).filter((c) => c.batch_id === s.batch && c.block === blk).pop();
  let blk = BLOCK, found = await latest(blk), tx = known[s.id]?.tx ?? null;
  if (!found) {
    const { send } = connect({ address, role: roles[i] ?? "s12" });
    const r = await send("file_check", [BATCHES, s.batch, blk]);
    console.log(`${s.id} batch ${s.batch}: ${r.status} ok=${r.ok} ${r.seconds}s ${r.hash}`, JSON.stringify(returnedJson(r) ?? r.revertReason?.slice(0, 200)));
    tx = r.hash;
    found = await latest(blk);
  }
  for (let k = 1; k <= 3 && found && TRANSPORT.includes(found.code); k++) {
    blk = BLOCK + k;
    const role = spare.shift();
    console.log(`${s.id} check #${found.check_id} was ${found.code}; filing again at block ${blk} as ${role}`);
    await new Promise((r) => setTimeout(r, 30_000));
    const { send } = connect({ address, role });
    const r = await send("file_check", [BATCHES, s.batch, blk]);
    tx = r.hash;
    found = await latest(blk);
  }
  if (!found) { console.log(`${s.id} NOT ON CHAIN`); continue; }
  const rec = { id: s.id, batch: s.batch, expect: s.expect, expect_code: s.expect_code, why_chosen: s.why_chosen, tx, ...found };
  const at = results.findIndex((r) => r.id === s.id);
  if (at >= 0) results[at] = rec; else results.push(rec);
  console.log(`${s.id} batch ${s.batch} check #${found.check_id} ${found.verdict} ${found.code}${found.verdict === s.expect && found.code === s.expect_code ? "" : `  (research said ${s.expect} ${s.expect_code})`}`);
  writeFileSync(outPath, JSON.stringify({ contract: address, block: BLOCK, seeds: results }, null, 1) + "\n");
}
