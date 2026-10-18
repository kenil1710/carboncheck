"""Runs the contract's own decision code (judge_chain, normalize_verra,
judge_verra) over the raw answers in feasibility/deep.json: what CarbonCheck
would rule for every real Toucan batch at block 95733573 (before rule 5).

    cd test && python3 feasibility/deep_report.py > feasibility/deep_report.txt
"""
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import stub  # noqa: E402

stub._install_stub()
CC = stub.load_full(Path(__file__).resolve().parents[2] / "contracts" / "CarbonCheck.py", "CarbonCheck")
deep = json.loads((Path(__file__).parent / "deep.json").read_text())

out = []
for bid, b in sorted(deep["batches"].items(), key=lambda kv: int(kv[0])):
    raw = {"hash": "", "time": 0, "nft": b["nft"].lower() if b.get("nft") else None,
           "owner": b["owner"].lower() if b.get("owner") else None,
           "tco2": b["tco2"].lower() if b.get("tco2") and b["tco2"] != "0x" else None,
           "attrs": b["attrs"].lower() if b.get("attrs") and b["attrs"] != "0x" else None}
    if raw["tco2"] is not None and int(raw["tco2"], 16) == 0:
        raw["attrs"] = None
    j = CC.judge_chain(raw)
    if "verdict" not in j:
        v = deep["verra"].get(b["serial"])
        if v is None or v["entities"] == "ERROR":
            j = CC.unv("verra", "VERRA_UNAVAILABLE", "lookup failed during research")
        else:
            j = CC.judge_verra(j["batch"], j["parsed"], CC.normalize_verra({"entities": v["entities"]}, b["serial"], v["report"]))
    out.append((int(bid), b["status"], j["verdict"], j["code"], j.get("why", "")))

c = collections.Counter((v, code) for _, _, v, code, _ in out)
print("batches with a serial:", len(out))
for (v, code), n in sorted(c.items(), key=lambda kv: -kv[1]):
    print("  %-13s %-26s %d" % (v, code, n))
print()
for bid, st, v, code, why in out:
    if st == 2 and not (v == "MATCHED"):
        print("%5d  %-13s %-26s %s" % (bid, v, code, why[:150]))
