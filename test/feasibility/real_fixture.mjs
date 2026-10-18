// Builds test/real_batches.json from feasibility/deep.json: raw Polygon answers
// (nftList, getAttributes) plus viem's independent decoding, for the offline suite.
import { readFileSync, writeFileSync } from "node:fs";
import { decodeFunctionResult, parseAbi } from "viem";
const abi = parseAbi(["function getAttributes() view returns ((string projectId,string standard,string methodology,string region,string storageMethod,string method,string emissionType,string category,string uri,address beneficiary),(string name,uint64 startTime,uint64 endTime,uint256 projectTokenId,uint64 totalVintageQuantity,bool isCorsiaCompliant,bool isCCPcompliant,string coBenefits,string correspAdjustment,string additionalCertification,string uri,string registry))"]);
const deep = JSON.parse(readFileSync(new URL("./deep.json", import.meta.url), "utf8"));
const rows = Object.values(deep.batches).filter((b) => b.nft);
const pick = rows.filter((_, i) => i % Math.max(1, Math.floor(rows.length / 60)) === 0).slice(0, 60);
const out = pick.map((b) => {
  let ad = null;
  if (b.attrs) {
    const [p, v] = decodeFunctionResult({ abi, functionName: "getAttributes", data: b.attrs });
    ad = { projectId: p.projectId, startTime: Number(v.startTime), endTime: Number(v.endTime), name: v.name };
  }
  return { id: b.id, pvId: b.pvId, serial: b.serial, quantity: String(b.quantity), status: b.status, nft: b.nft, attrs: b.attrs, attrs_decoded: ad };
});
writeFileSync(new URL("../real_batches.json", import.meta.url), JSON.stringify({ block: deep.block, source: "Polygon via dRPC/Tenderly, CarbonOffsetBatches 0x8A4d7458dDe3023A3B24225D62087701A88b09DD", batches: out }, null, 1) + "\n");
console.log("wrote", out.length);
