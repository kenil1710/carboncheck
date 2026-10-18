"""Markdown table of the batches in feasibility/onchain.json (two RPCs, one
block) joined with their Verra records from feasibility/deep.json."""
import json
from pathlib import Path
d = Path(__file__).parent
on = json.loads((d / "onchain.json").read_text())
deep = json.loads((d / "deep.json").read_text())
print("| Batch | Status | Fractionalized | Serial | Qty | TCO2 project / vintage | Verra (exact serial) |")
print("|---|---|---|---|---|---|---|")
names = ["Pending", "Rejected", "Confirmed", "DetokReq", "Detokenized", "RetireReq", "RetireFinal"]
for b in on["batches"]:
    v = deep["verra"].get(b["serial"])
    if v and v["entities"] != "ERROR" and v["entities"]:
        e = [x for x in v["entities"] if x["serialNo"] == b["serial"]]
        vt = ("%s %s, %d units, VCS-%s, vintage %s, remark `%s`" % (v["report"], e[0]["stateCode"], e[0]["holdingQuantity"], e[0]["vcsProjectId"], e[0]["vintage"], (e[0]["remark"] or "")[:34])) if e else "not found"
    elif v:
        vt = "not found (retirements and holdings)"
    else:
        vt = "not looked up (not Confirmed)" if b["status"] != 2 else "-"
    a = b.get("attrs")
    at = "%s / %s..%s" % (a["projectId"], __import__("time").strftime("%Y-%m-%d", __import__("time").gmtime(a["startTime"])), __import__("time").strftime("%Y-%m-%d", __import__("time").gmtime(a["endTime"]))) if a else "no TCO2 from the factory"
    s = b["serial"] if len(b["serial"]) < 80 else b["serial"][:76] + "..."
    print("| [%s](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/%s) | %s | %s | `%s` | %s | %s | %s |" % (b["id"], b["id"], names[b["status"]] if b["status"] < 7 else b["status"], "yes" if b["fractionalized"] else "no", s or "(empty)", b["quantity"], at, vt))
