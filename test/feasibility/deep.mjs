/**
 * Feasibility (d): for every batch with a serial, read owner, TCO2 (official
 * factory) and TCO2 getAttributes() raw at the scan block, then look the
 * serial(s) up in the Verra Retirements report (and Holdings if not retired).
 *   node feasibility/deep.mjs 95733573
 * Writes feasibility/deep.json (raw hex + Verra entities) for analysis with the
 * contract's own parser (deep_report.py).
 */
import { readFileSync, writeFileSync, existsSync } from "node:fs";
const RPCS = ["https://polygon.drpc.org", "https://gateway.tenderly.co/public/polygon"];
const BATCHES = "0x8A4d7458dDe3023A3B24225D62087701A88b09DD";
const FACTORY = "0x2359677E513Bc83106268514c5B2De3C29C849ea";
const block = "0x" + BigInt(process.argv[2]).toString(16);
const scan = JSON.parse(readFileSync(new URL("./scan.json", import.meta.url), "utf8"));
const outPath = new URL("./deep.json", import.meta.url);
const out = existsSync(outPath) ? JSON.parse(readFileSync(outPath, "utf8")) : { block: Number(BigInt(process.argv[2])), batches: {}, verra: {} };
// the public header values registry.verra.org ships to every browser
const cfg = await (await fetch("https://registry.verra.org/config/environment.config.json")).json();
const H = { "Content-Type": "application/json", Accept: "application/json", language: "en", standardId: "150000000000001", standardAcronym: "VCS", registry: "VERRA", appkey: cfg.uris.common.DEFAULT_HEADERS.appkey, application: "Markit", "X-XSRF-TOKEN": "t20", Cookie: "XSRF-TOKEN=t20" };
const w = (n) => BigInt(n).toString(16).padStart(64, "0");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let k = 0;
async function call(to, data) {
  for (let i = 0; i < 6; i++) {
    try {
      const r = await fetch(RPCS[(k++) % 2], { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "eth_call", params: [{ to, data }, block] }), signal: AbortSignal.timeout(20000) });
      const j = await r.json();
      if (j.error) return j.error.code === 3 || /revert/i.test(j.error.message ?? "") ? null : Promise.reject(new Error(JSON.stringify(j.error)));
      return j.result;
    } catch (e) { await sleep(1000 * (i + 1)); }
  }
  throw new Error("rpc failed");
}
async function verra(report, serial) {
  for (let i = 0; i < 4; i++) {
    try {
      const r = await fetch(`https://prod-us.api.platts.com/ci-raas-prod/raas-report-api/es/public/${report}/publicReportPageSearch`, { method: "POST", headers: H, body: JSON.stringify({ searchFilter: { pagination: { start: 0, limit: 5, sortOptions: [] }, filterModel: { serialNo: { columnFilters: [{ filterType: "Text", type: "equals", filter: serial }] } } } }), signal: AbortSignal.timeout(40000) });
      if (r.status !== 200) throw new Error("http " + r.status);
      const j = await r.json();
      return (j.entities ?? []).map((e) => ({ serialNo: e.serialNo, stateCode: e.stateCode, holdingQuantity: e.holdingQuantity, vcsProjectId: e.vcsProjectId, vintage: e.vintage, retiredDate: e.retiredDate, remark: e.publicRetirementReasonDetails, beneficiary: e.publicBeneficialOwner }));
    } catch (e) { await sleep(2000 * (i + 1)); }
  }
  return "ERROR";
}
const pvCache = {};
const todo = scan.filter((r) => !r.error && r.serial && !out.batches[r.id]);
let n = 0;
async function one(r) {
  const owner = await call(BATCHES, "0x6352211e" + w(r.id));
  if (!(r.pvId in pvCache)) {
    const t = await call(FACTORY, "0x5e813d3c" + w(r.pvId));
    const addr = t ? "0x" + t.slice(26) : null;
    const attrs = addr && !/^0x0+$/.test(addr) ? await call(addr, "0x152583de") : null;
    pvCache[r.pvId] = { tco2: t, attrs };
  }
  const nft = await call(BATCHES, "0x75bea166" + w(r.id));
  out.batches[r.id] = { ...r, nft, owner, ...pvCache[r.pvId] };
  if (r.status === 2) {
    for (const s of r.serial.split(",")) {
      if (out.verra[s]) continue;
      let ents = await verra("retirements", s);
      let report = "retirements";
      if (Array.isArray(ents) && ents.filter((e) => e.serialNo === s).length === 0) { ents = await verra("holdings", s); report = "holdings"; }
      out.verra[s] = { report, entities: ents };
    }
  }
  if (++n % 50 === 0) { writeFileSync(outPath, JSON.stringify(out) + "\n"); console.log("done", n, "/", todo.length); }
}
const queue = [...todo];
await Promise.all(Array.from({ length: 6 }, async () => { while (queue.length) await one(queue.shift()); }));
writeFileSync(outPath, JSON.stringify(out) + "\n");
console.log("finished", Object.keys(out.batches).length, "batches,", Object.keys(out.verra).length, "serials");
