/**
 * docs/SEEDS.md and the README seed and address tables, from
 * docs/seeds.onchain.json (what the canonical contract stored),
 * test/seeds.json (the research) and deployments.json.
 *   node tools/seeds_md.mjs
 */
import { readFileSync, writeFileSync } from "node:fs";
const root = new URL("..", import.meta.url).pathname;
const on = JSON.parse(readFileSync(root + "docs/seeds.onchain.json", "utf8"));
const dep = JSON.parse(readFileSync(root + "deployments.json", "utf8")).contracts;
const BATCHES = "0x8A4d7458dDe3023A3B24225D62087701A88b09DD";
const EXP = "https://explorer-studio-dev.genlayer.com";
const nft = (id) => `https://polygonscan.com/nft/${BATCHES}/${id}`;
const verraUrl = "https://registry.verra.org/verra/public/program/VCS";
const short = (c) => (c.verdict === "MATCHED" ? `${c.units} units, VCS-${c.serial_project}, ${c.vintage_start.slice(0, 4)}` : `${c.code}: ${c.why}`).replace(/\|/g, "/");
const rows = on.seeds.map((c) => `| ${c.id} | [${c.batch}](${nft(c.batch)}) | **${c.verdict}** | ${short(c).slice(0, 150)} | [#${c.check_id}](${EXP}/tx/${c.tx}) |`);
const table = ["| Seed | Batch | Verdict | Reason (decided by code) | Check / tx |", "|---|---|---|---|---|", ...rows].join("\n");
const mix = {};
for (const c of on.seeds) mix[c.verdict] = (mix[c.verdict] ?? 0) + 1;
const detail = on.seeds.map((c) => [
  `## ${c.id}: batch ${c.batch}, ${c.verdict}`, "",
  `- Why chosen: ${c.why_chosen}`,
  `- Batch: [Polygonscan NFT ${c.batch}](${nft(c.batch)}), status ${c.batch_status || "(not read)"}, quantity ${c.quantity || "-"}, held by \`${c.owner || "-"}\``,
  `- TCO2: ${c.tco2 ? `[\`${c.tco2}\`](https://polygonscan.com/address/${c.tco2}), ${c.project_id}, vintage ${c.vintage_start}..${c.vintage_end}` : "(none)"}`,
  `- Serial: \`${c.serial || "(empty)"}\`${c.unit_start ? ` (units ${c.unit_start}..${c.unit_end}, ${c.units}, project ${c.serial_project})` : ""}`,
  `- Polygon block: [${c.block}](https://polygonscan.com/block/${c.block})${c.block_hash ? `, hash \`${c.block_hash}\`, time ${new Date(c.block_time * 1000).toISOString()}` : ""}`,
  `- Verra (exact serial, ${verraUrl}, Retirements report): ${c.verra.found ? `${c.verra.source}: ${c.verra.status}, ${c.verra.quantity} units, project ${c.verra.project}, vintage ${c.verra.vintage}, retired ${c.verra.retired_on || "-"}, remark \`${c.verra.remark || "-"}\`` : (c.stage === "verra" ? "no record with this exact serial" : "not looked up (the check ended before the Verra stage)")}`,
  `- Verdict: **${c.verdict}** / \`${c.code}\`: ${c.why}`,
  `- As of: ${c.as_of} (fetch) and block ${c.block}`,
  `- Research (block 95733573): ${c.expect} / \`${c.expect_code}\`${c.verdict === c.expect && c.code === c.expect_code ? " (same)" : " (DIFFERENT, see why above)"}`,
  `- On chain: CarbonCheck \`${on.contract}\` check #${c.check_id}, tx [\`${c.tx}\`](${EXP}/tx/${c.tx}), filed by \`${c.filer}\``,
  ""].join("\n"));
writeFileSync(root + "docs/SEEDS.md", [
  "# Seeds", "",
  `Every real batch from [FEASIBILITY.md](FEASIBILITY.md) and every real non-MATCHED case found among Confirmed Toucan batches, plus one batch of each non-Confirmed status and one id that does not exist, filed on the canonical CarbonCheck [\`${dep.CarbonCheck.address}\`](${EXP}/address/${dep.CarbonCheck.address}), all at Polygon block [${on.block}](https://polygonscan.com/block/${on.block}). Every verdict is final. Mix: ${Object.entries(mix).map(([k, v]) => `${v} ${k}`).join(", ")}. The real data has no DOUBLE_CLAIMED case (FEASIBILITY.md, section d); the demo deployment shows that path ([demo-run.log](demo-run.log)).`, "",
  `Each verdict is "as of" its fetch time and block. The raw records (\`get_check\` output) are in [seeds.onchain.json](seeds.onchain.json).`, "",
  table, "", ...detail].join("\n"));
const addr = [
  "| Contract | Address | Mode | Constructor |", "|---|---|---|---|",
  ...Object.entries(dep).map(([k, d]) => `| ${k} | [\`${d.address}\`](${EXP}/address/${d.address}) | ${d.mode} | \`${JSON.stringify(d.constructor_args)}\` |`),
  "",
  `All four from commit \`${Object.values(dep)[0].commit.slice(0, 10)}\` on GenLayer Studio Dev (chain 61997, https://studio-dev.genlayer.com/api). Frozen inside CarbonCheck: Toucan CarbonOffsetBatches \`${BATCHES}\` and ToucanCarbonOffsetsFactory \`0x2359677E513Bc83106268514c5B2De3C29C849ea\` on Polygon (chain 137).`,
].join("\n");
let readme = readFileSync(root + "README.md", "utf8");
const swap = (marker, start, text) => {
  if (readme.includes(marker)) { readme = readme.replace(marker, text); return; }
  const i = readme.indexOf(start);
  const j = readme.indexOf("\n\n", readme.indexOf("\n\n", i) + 2);
  readme = readme.slice(0, i) + text + readme.slice(start.startsWith("| Seed") ? readme.indexOf("\n\n", i) : j);
};
swap("SEEDS_TABLE", "| Seed | Batch |", table);
swap("ADDRESSES_TABLE", "| Contract | Address |", addr);
writeFileSync(root + "README.md", readme);
console.log(JSON.stringify(mix));
