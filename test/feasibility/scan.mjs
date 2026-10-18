/**
 * Feasibility (d): scan every batch NFT (nftList) at one block on ONE RPC to find
 * candidate non-MATCHED cases (serial overlaps, odd statuses, quantity vs serial width).
 * Candidates are then re-read on two RPCs by onchain.mjs. Writes feasibility/scan.json.
 */
import { encodeFunctionData, decodeFunctionResult, parseAbi } from "viem";
import { writeFileSync } from "node:fs";
const abi = parseAbi(["function nftList(uint256) view returns (uint256 projectVintageTokenId, string serialNumber, uint256 quantity, uint8 status, string uri)"]);
const RPC = "https://polygon-bor-rpc.publicnode.com";
const BATCHES = "0x8A4d7458dDe3023A3B24225D62087701A88b09DD";
const block = "0x" + BigInt(process.argv[2]).toString(16);
const max = Number(process.argv[3]);
const rows = [];
async function one(id) {
  for (let i = 0; i < 5; i++) {
    try {
      const r = await fetch(RPC, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ jsonrpc: "2.0", id, method: "eth_call", params: [{ to: BATCHES, data: encodeFunctionData({ abi, functionName: "nftList", args: [BigInt(id)] }) }, block] }), signal: AbortSignal.timeout(20000) });
      const j = await r.json();
      if (j.error) throw new Error(JSON.stringify(j.error));
      const d = decodeFunctionResult({ abi, functionName: "nftList", data: j.result });
      return { id, pvId: Number(d[0]), serial: d[1], quantity: Number(d[2]), status: d[3] };
    } catch (e) { await new Promise((r) => setTimeout(r, 1000 * (i + 1))); }
  }
  return { id, error: true };
}
for (let s = 1; s <= max; s += 20) {
  const ids = []; for (let i = s; i < s + 20 && i <= max; i++) ids.push(i);
  rows.push(...(await Promise.all(ids.map(one))));
}
writeFileSync(new URL("./scan.json", import.meta.url), JSON.stringify(rows) + "\n");
const st = {}; for (const r of rows) st[r.status ?? "err"] = (st[r.status ?? "err"] ?? 0) + 1;
console.log("rows", rows.length, "by status", JSON.stringify(st));
