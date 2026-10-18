/**
 * Feasibility (a): read real Toucan batch NFTs from two independent Polygon RPCs
 * at one pinned finalized block and require the raw eth_call results to agree.
 *   node feasibility/onchain.mjs [--ids=1,2,3] [--block=N]
 * Writes feasibility/onchain.json.
 */
import { encodeFunctionData, decodeFunctionResult, parseAbi } from "viem";
import { writeFileSync } from "node:fs";

export const RPCS = ["https://polygon.drpc.org", "https://gateway.tenderly.co/public/polygon"];
export const BATCHES = "0x8A4d7458dDe3023A3B24225D62087701A88b09DD";
export const FACTORY = "0x2359677E513Bc83106268514c5B2De3C29C849ea";
const abi = parseAbi([
  "function batchTokenCounter() view returns (uint256)",
  "function nftList(uint256) view returns (uint256 projectVintageTokenId, string serialNumber, uint256 quantity, uint8 status, string uri)",
  "function ownerOf(uint256) view returns (address)",
  "function pvIdtoERC20(uint256) view returns (address)",
  "function getAttributes() view returns ((string projectId,string standard,string methodology,string region,string storageMethod,string method,string emissionType,string category,string uri,address beneficiary),(string name,uint64 startTime,uint64 endTime,uint256 projectTokenId,uint64 totalVintageQuantity,bool isCorsiaCompliant,bool isCCPcompliant,string coBenefits,string correspAdjustment,string additionalCertification,string uri,string registry))",
]);
const arg = (n, d) => (process.argv.find((a) => a.startsWith(`--${n}=`)) ?? `=${d ?? ""}`).split("=")[1];

async function rpc(url, method, params) {
  for (let i = 0; i < 4; i++) {
    try {
      const r = await fetch(url, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }), signal: AbortSignal.timeout(20000) });
      const j = await r.json();
      if (j.error) throw new Error(JSON.stringify(j.error));
      return j.result;
    } catch (e) { if (i === 3) throw e; await new Promise((r) => setTimeout(r, 1500 * (i + 1))); }
  }
}
async function call2(to, fn, args, block) {
  const data = encodeFunctionData({ abi, functionName: fn, args });
  const tag = "0x" + block.toString(16);
  const [a, b] = await Promise.all(RPCS.map((u) => rpc(u, "eth_call", [{ to, data }, tag])));
  if (a !== b) throw new Error(`RPC disagreement on ${fn}`);
  return decodeFunctionResult({ abi, functionName: fn, data: a });
}

if (import.meta.url === `file://${process.argv[1]}`) {
  let block = arg("block") ? BigInt(arg("block")) : null;
  if (!block) {
    const fins = await Promise.all(RPCS.map((u) => rpc(u, "eth_getBlockByNumber", ["finalized", false])));
    block = BigInt(Math.min(...fins.map((f) => Number(f.number))));
  }
  const hashes = await Promise.all(RPCS.map((u) => rpc(u, "eth_getBlockByNumber", ["0x" + block.toString(16), false])));
  if (hashes[0].hash !== hashes[1].hash) throw new Error("block hash disagreement");
  const counter = await call2(BATCHES, "batchTokenCounter", [], block);
  console.log(`block ${block} hash ${hashes[0].hash} ts ${Number(hashes[0].timestamp)} batchTokenCounter ${counter}`);
  const ids = arg("ids") ? arg("ids").split(",").map(BigInt) : [];
  const out = { block: block.toString(), block_hash: hashes[0].hash, block_time: Number(hashes[0].timestamp), rpcs: RPCS, batches_contract: BATCHES, factory: FACTORY, counter: counter.toString(), batches: [] };
  for (const id of ids) {
    try {
      const n = await call2(BATCHES, "nftList", [id], block);
      const owner = await call2(BATCHES, "ownerOf", [id], block).catch((e) => "ERR " + String(e.message).slice(0, 80));
      const tco2 = await call2(FACTORY, "pvIdtoERC20", [n[0]], block);
      let attrs = null;
      if (tco2 !== "0x0000000000000000000000000000000000000000") {
        const [p, v] = await call2(tco2, "getAttributes", [], block);
        attrs = { projectId: p.projectId, standard: p.standard, vintageName: v.name, startTime: Number(v.startTime), endTime: Number(v.endTime), registry: v.registry };
      }
      const row = { id: id.toString(), pvId: n[0].toString(), serial: n[1], quantity: n[2].toString(), status: n[3], owner, tco2, fractionalized: owner === tco2, attrs };
      out.batches.push(row);
      console.log(JSON.stringify(row));
    } catch (e) { console.log(id.toString(), "ERR", String(e.message).slice(0, 120)); out.batches.push({ id: id.toString(), error: String(e.message).slice(0, 200) }); }
  }
  writeFileSync(new URL("./onchain.json", import.meta.url), JSON.stringify(out, null, 2) + "\n");
}
