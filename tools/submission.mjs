/**
 * docs/SUBMISSION.md: title and description, plain ASCII, each with its
 * character count checked against its limit.
 *   node tools/submission.mjs <offline test count>
 */
import { readFileSync, writeFileSync } from "node:fs";
const root = new URL("..", import.meta.url).pathname;
const dep = JSON.parse(readFileSync(root + "deployments.json", "utf8")).contracts;
const on = JSON.parse(readFileSync(root + "docs/seeds.onchain.json", "utf8"));
const tests = Number(process.argv[2] || 0);
const mix = { MATCHED: 0, MISMATCH: 0, DOUBLE_CLAIMED: 0, UNVERIFIABLE: 0 };
for (const s of on.seeds) mix[s.verdict]++;

const title = "CarbonCheck: does a tokenized carbon credit batch match real retired credits on Verra?";
const description = [
  "CarbonCheck checks one Toucan carbon credit batch on Polygon against the public Verra registry.",
  "Code reads the batch on Polygon and the public Verra record, compares them field by field and decides; no model decides anything.",
  "Two RPCs must agree at one finalized block on the batch's serial, quantity and status and on its TCO2's project and vintage.",
  "Code parses the serial and requires a Verra record with that exact serial that is RETIRED with the same unit count, project and vintage.",
  "Verdicts: MATCHED, MISMATCH, DOUBLE_CLAIMED (units overlap a range already matched for another batch of the same project) or UNVERIFIABLE.",
  "Each verdict is final and as of its fetch time and block.",
  `Seeds: ${on.seeds.length} real batches, ${mix.MATCHED} MATCHED, ${mix.MISMATCH} MISMATCH, ${mix.UNVERIFIABLE} UNVERIFIABLE.`,
  "OffsetGate accepts an offset claim only on a fresh MATCHED.",
].join(" ");
const items = [["Title", title, 100], ["Description", description, 1000]];
const bad = items.filter(([, t, max]) => t.length > max || !/^[\x20-\x7e]*$/.test(t));
if (bad.length) { console.error("over limit or not ASCII:", bad.map(([n, t]) => `${n} ${t.length}`)); process.exit(1); }
writeFileSync(root + "docs/SUBMISSION.md", [
  "# Submission", "",
  "Plain ASCII. Character counts are measured by `tools/submission.mjs`.", "",
  ...items.flatMap(([n, t, max]) => [`## ${n} (${t.length} / ${max} characters)`, "", "```", t, "```", ""]),
  "## Links", "",
  "- Repository: https://github.com/kenil1710/carboncheck",
  `- CarbonCheck (canonical): ${dep.CarbonCheck.address}`,
  `- CarbonCheckDemo: ${dep.CarbonCheckDemo.address}`,
  `- OffsetGate: ${dep.OffsetGate.address}`,
  `- OffsetGateDemo: ${dep.OffsetGateDemo.address}`,
  "- Network: GenLayer Studio Dev, chain id 61997, https://studio-dev.genlayer.com/api",
  `- Offline tests: ${tests}`,
  "- Seeds: https://github.com/kenil1710/carboncheck/blob/main/docs/SEEDS.md",
  "- Demo run: https://github.com/kenil1710/carboncheck/blob/main/docs/demo-run.log", "",
].join("\n"));
for (const [n, t, max] of items) console.log(`${n}: ${t.length}/${max}`);
