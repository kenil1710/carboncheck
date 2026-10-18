# v0.3.0
# { "Depends": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng" }
import genlayer as gl
from genlayer import *
from dataclasses import dataclass
import json
import typing

# CarbonCheck - checks ONE tokenized carbon credit batch against the public
# Verra registry.
#
# A filing names a Toucan batch NFT (the official CarbonOffsetBatches contract
# on Polygon, frozen below) and a finalized Polygon block. Code decides
# everything; no model is called anywhere:
#
#   1. two independent Polygon RPCs must answer byte-identically at the block:
#      the batch (serial, quantity, status, owner), its TCO2 from the official
#      factory, and the TCO2's project id and vintage;
#   2. the batch must be Confirmed and fractionalized (held by its own TCO2);
#   3. code parses the Verra serial (unit range, project id, vintage dates)
#      and checks it against the TCO2 attributes and the on-chain quantity;
#   4. code reads the serial's record from the public Verra registry and
#      compares status, unit count, project id and vintage field by field;
#   5. a range that overlaps a range of the same Verra project already MATCHED
#      for a different batch is DOUBLE_CLAIMED (interval overlap on unit numbers;
#      Verra reuses unit numbers across projects, so the project scopes them).
#
# Verdicts: MATCHED, MISMATCH, DOUBLE_CLAIMED, UNVERIFIABLE. Anything that
# cannot be established ends UNVERIFIABLE. Verra is a live registry: every
# verdict is "as of" its fetch time and Polygon block; recheck() files anew.
# Holds no funds; has no owner and no setter.

VERSION = "1.0.0"

MATCHED = "MATCHED"
MISMATCH = "MISMATCH"
DOUBLE_CLAIMED = "DOUBLE_CLAIMED"
UNVERIFIABLE = "UNVERIFIABLE"
VERDICTS = (MATCHED, MISMATCH, DOUBLE_CLAIMED, UNVERIFIABLE)

POLYGON = 137
# Two archive RPCs run by different operators; both answer GenVM
# (docs/FEASIBILITY.md).
RPCS = ("https://polygon.drpc.org", "https://gateway.tenderly.co/public/polygon")
# Toucan's own deployment records (github.com/ToucanProtocol/contracts,
# deployments/production/matic/*.json). Frozen: no setter exists.
TOUCAN_BATCHES = "0x8a4d7458dde3023a3b24225d62087701a88b09dd"
TOUCAN_TCO2_FACTORY = "0x2359677e513bc83106268514c5b2de3c29c849ea"
POLYGONSCAN = "https://polygonscan.com"

SEL_NFT_LIST = "0x75bea166"       # nftList(uint256)
SEL_OWNER_OF = "0x6352211e"       # ownerOf(uint256)
SEL_PV_TO_ERC20 = "0x5e813d3c"    # pvIdtoERC20(uint256)
SEL_ATTRIBUTES = "0x152583de"     # getAttributes()

# BatchStatus in Toucan's CarbonOffsetBatchesTypes.sol
BATCH_STATUS = ("Pending", "Rejected", "Confirmed", "DetokenizationRequested",
                "DetokenizationFinalized", "RetirementRequested", "RetirementFinalized")
CONFIRMED = 2

# The JSON endpoints registry.verra.org's own Retirements and Holdings reports call. The
# header values are the public ones the site ships to every browser in
# registry.verra.org/config/environment.config.json.
VERRA_API = "https://prod-us.api.platts.com/ci-raas-prod/raas-report-api/es/public/"
VERRA_SEARCH = VERRA_API + "retirements/publicReportPageSearch"
# Units still active (not retired) are listed only in the Holdings report.
VERRA_HOLDINGS = VERRA_API + "holdings/publicReportPageSearch"
VERRA_HEADERS = {
    "Content-Type": "application/json", "Accept": "application/json", "language": "en",
    "standardId": "150000000000001", "standardAcronym": "VCS", "registry": "VERRA",
    "appkey": "wOKHFGuxKApQaujPSKgF", "application": "Markit",
    "X-XSRF-TOKEN": "t20", "Cookie": "XSRF-TOKEN=t20",
}
VERRA_RETIRED = "RETIRED"
VERRA_PAGE = "https://registry.verra.org/verra/public/program/VCS"

MIN_BLOCK = 19_000_000      # before Toucan's batch contract existed
MAX_BLOCK = 10 ** 10
MAX_TOKEN_ID = 10 ** 9
MAX_SERIAL = 120
MAX_UNIT = 10 ** 15
TRIES = 3
MAX_PAGE_LIST = 50

# reason codes
C_MATCH = "ALL_FIELDS_MATCH"
C_DOUBLE = "RANGE_ALREADY_CLAIMED"
M_PROJECT = "SERIAL_PROJECT_MISMATCH"
M_VINTAGE = "SERIAL_VINTAGE_MISMATCH"
M_QUANTITY = "QUANTITY_MISMATCH"
M_V_STATUS = "VERRA_STATUS_MISMATCH"
M_V_QUANTITY = "VERRA_QUANTITY_MISMATCH"
M_V_PROJECT = "VERRA_PROJECT_MISMATCH"
M_V_VINTAGE = "VERRA_VINTAGE_MISMATCH"
U_RPC = "RPC_UNAVAILABLE"
U_RPC_DIFF = "RPC_DISAGREE"
U_NOT_FINAL = "BLOCK_NOT_FINALIZED"
U_NO_BATCH = "BATCH_NOT_FOUND"
U_NOT_CONFIRMED = "BATCH_NOT_CONFIRMED"
U_NO_TCO2 = "TCO2_NOT_FOUND"
U_NOT_FRACTIONALIZED = "BATCH_NOT_FRACTIONALIZED"
U_TCO2 = "TCO2_UNREADABLE"
U_NOT_VCS = "NOT_A_VERRA_CREDIT"
U_SERIAL = "SERIAL_UNPARSABLE"
U_VERRA = "VERRA_UNAVAILABLE"
U_VERRA_BAD = "VERRA_UNREADABLE"
U_NOT_FOUND = "VERRA_NOT_FOUND"
U_AMBIGUOUS = "VERRA_AMBIGUOUS"
U_INTERNAL = "INTERNAL"
# failures of a transport a validator may not reproduce; the leader's
# UNVERIFIABLE for one of these is accepted (it asserts nothing).
TRANSPORT_CODES = (U_RPC, U_RPC_DIFF, U_NOT_FINAL, U_VERRA, U_VERRA_BAD, U_INTERNAL)


# ---- pure helpers (no storage, no network) ----------------------------------

def _canon(v: typing.Any) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"))


def _days_in(y: int, m: int) -> int:
    if m == 2:
        return 29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28
    return 30 if m in (4, 6, 9, 11) else 31


def epoch_of(y: int, m: int, d: int, hh: int, mm: int, ss: int) -> int:
    y2 = y - (1 if m <= 2 else 0)
    era = (y2 if y2 >= 0 else y2 - 399) // 400
    yoe = y2 - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return (era * 146097 + doe - 719468) * 86400 + hh * 3600 + mm * 60 + ss


def iso_epoch(value: typing.Any) -> int:
    if not isinstance(value, str) or len(value) < 19:
        return 0
    try:
        return epoch_of(int(value[0:4]), int(value[5:7]), int(value[8:10]),
                        int(value[11:13]), int(value[14:16]), int(value[17:19]))
    except Exception:
        return 0


def iso_of(epoch: int) -> str:
    days = epoch // 86400
    rem = epoch - days * 86400
    z = days + 719468
    era = (z if z >= 0 else z - 146096) // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = mp + (3 if mp < 10 else -9)
    if m <= 2:
        y += 1
    return "%04d-%02d-%02dT%02d:%02d:%02dZ" % (y, m, d, rem // 3600, (rem % 3600) // 60, rem % 60)


def _digits(s: str) -> bool:
    if s == "":
        return False
    for ch in s:
        if ch < "0" or ch > "9":
            return False
    return True


def as_int(v: typing.Any) -> typing.Any:
    """An integer argument: a Python int (not bool) or a string of ASCII
    digits. Anything else (floats, hex, signs, bools) -> None."""
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, str) and 0 < len(v) <= 20 and _digits(v):
        return int(v)
    return None


def _canon_int(s: str) -> bool:
    """ASCII digits with no leading zero (a serial's numbers are written so)."""
    return _digits(s) and (s == "0" or s[0] != "0")


def parse_date8(s: str) -> typing.Any:
    """DDMMYYYY -> (y, m, d), or None."""
    if len(s) != 8 or not _digits(s):
        return None
    d, m, y = int(s[0:2]), int(s[2:4]), int(s[4:8])
    if y < 1990 or y > 2100 or m < 1 or m > 12 or d < 1 or d > _days_in(y, m):
        return None
    return (y, m, d)


SERIAL_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-"


def parse_serial(s: typing.Any) -> typing.Any:
    """A Verra VCU serial -> dict, or None.

    <issuance>-<first unit>-<last unit>-...VCU...-<project id>-<DDMMYYYY>-<DDMMYYYY>-<0|1>

      8367-10851650-10851650-VCS-VCU-1423-VER-IN-1-1418-01012020-29022020-0
      7236-378945246-378945248-VCU-034-APX-IN-1-1190-01012018-31052018-0

    Upper-case ASCII letters, digits and single hyphens only; numbers with no
    leading zero; first unit >= 1 and <= last unit; real calendar dates with
    the vintage start on or before its end."""
    if not isinstance(s, str) or len(s) < 30 or len(s) > MAX_SERIAL:
        return None
    for ch in s:
        if ch not in SERIAL_CHARS:
            return None
    parts = s.split("-")
    if len(parts) < 9 or len(parts) > 16:
        return None
    for p in parts:
        if p == "":
            return None
    if not (_canon_int(parts[0]) and _canon_int(parts[1]) and _canon_int(parts[2])):
        return None
    start, end = int(parts[1]), int(parts[2])
    if start < 1 or end < start or end >= MAX_UNIT:
        return None
    if parts[-1] not in ("0", "1"):
        return None
    vs, ve = parse_date8(parts[-3]), parse_date8(parts[-2])
    if vs is None or ve is None:
        return None
    vs_e = epoch_of(vs[0], vs[1], vs[2], 0, 0, 0)
    ve_e = epoch_of(ve[0], ve[1], ve[2], 0, 0, 0)
    if vs_e > ve_e:
        return None
    if not _canon_int(parts[-4]) or parts[-4] == "0":
        return None
    middle = parts[3:-4]
    if "VCU" not in middle:
        return None
    return {"issuance": parts[0], "start": start, "end": end, "units": end - start + 1,
            "project": int(parts[-4]), "vintage_start": "%04d-%02d-%02d" % vs,
            "vintage_end": "%04d-%02d-%02d" % ve, "vs_day": vs_e // 86400, "ve_day": ve_e // 86400,
            "vintage_year": str(vs[0]),
            # how the Verra registry writes this vintage: "2009", or "2008 - 2009"
            # when the monitoring period spans two calendar years
            "verra_vintage": str(vs[0]) if vs[0] == ve[0] else str(vs[0]) + " - " + str(ve[0])}


def overlaps(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    """Closed unit ranges [a_start, a_end] and [b_start, b_end] share a unit.
    Touching ranges (a_end + 1 == b_start) do not."""
    return a_start <= b_end and b_start <= a_end


# ---- ABI ---------------------------------------------------------------------

class ReadFailed(Exception):
    pass


def _hexdata(r: typing.Any) -> bytes:
    if not isinstance(r, str) or not r.startswith("0x") or len(r) % 2 != 0:
        raise ReadFailed("not hex")
    try:
        return bytes.fromhex(r[2:])
    except Exception:
        raise ReadFailed("not hex")


def _w(b: bytes, off: int) -> int:
    if off < 0 or off + 32 > len(b):
        raise ReadFailed("short return")
    return int.from_bytes(b[off:off + 32], "big")


def _str_at(b: bytes, off: int) -> str:
    n = _w(b, off)
    if n > 4096 or off + 32 + n > len(b):
        raise ReadFailed("bad string")
    try:
        return b[off + 32:off + 32 + n].decode("utf-8")
    except Exception:
        raise ReadFailed("bad utf-8")


def _addr_word(b: bytes, off: int) -> str:
    v = _w(b, off)
    if v >> 160 != 0:
        raise ReadFailed("not an address")
    return "0x" + ("%040x" % v)


def decode_nft(r: str) -> dict:
    """nftList(uint256) -> (uint256 pvId, string serial, uint256 quantity, uint8 status, string uri)"""
    b = _hexdata(r)
    st = _w(b, 96)
    if st > 255:
        raise ReadFailed("bad status")
    return {"pv_id": _w(b, 0), "serial": _str_at(b, _w(b, 32)), "quantity": _w(b, 64), "status": st}


def decode_attributes(r: str) -> dict:
    """getAttributes() -> (ProjectData, VintageData); both tuples are dynamic.
    ProjectData.projectId is its first field; VintageData starts with
    (string name, uint64 startTime, uint64 endTime, ...)."""
    b = _hexdata(r)
    p = _w(b, 0)
    v = _w(b, 32)
    if p > len(b) or v > len(b):
        raise ReadFailed("bad tuple offset")
    pid = _str_at(b, p + _w(b, p))
    name = _str_at(b, v + _w(b, v))
    return {"project_id": pid, "vintage_name": name, "start": _w(b, v + 32), "end": _w(b, v + 64)}


def _arg(n: int) -> str:
    return "%064x" % n


def _addr_arg(a: str) -> str:
    return "0" * 24 + a[2:]


# ---- network ---------------------------------------------------------------

def _status(res: typing.Any) -> int:
    s = getattr(res, "status", None)
    if s is None:
        s = getattr(res, "status_code", None)
    return 0 if s is None else int(s)


def _body(res: typing.Any) -> bytes:
    b = getattr(res, "body", None)
    if b is None:
        return b""
    if isinstance(b, bytes):
        return b
    return str(b).encode("utf-8")


def _post(url: str, body: str, headers: dict) -> typing.Any:
    """One POST with retries on transport errors, 429 and 5xx. The response, or None."""
    res = None
    for _ in range(TRIES):
        try:
            res = gl.nondet.web.request(url, method="POST", body=body, headers=headers)
        except Exception:
            res = None
            continue
        st = _status(res)
        if st == 200:
            return res
        if st != 429 and st < 500:
            return res
        res = None
    return res


def rpc_one(url: str, method: str, params: list) -> typing.Any:
    """One JSON-RPC call. ["ok", result] | ["revert", None]; raises ReadFailed."""
    res = _post(url, json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}),
                {"Content-Type": "application/json"})
    if res is None or _status(res) != 200:
        raise ReadFailed("transport")
    try:
        doc = json.loads(_body(res).decode("utf-8", errors="replace"))
    except Exception:
        raise ReadFailed("json")
    if not isinstance(doc, dict):
        raise ReadFailed("shape")
    err = doc.get("error")
    if err is not None:
        msg = str(err.get("message", "")).lower() if isinstance(err, dict) else ""
        code = err.get("code") if isinstance(err, dict) else None
        if code == 3 or msg.find("revert") >= 0:
            return ["revert", None]
        raise ReadFailed("rpc error")
    if "result" not in doc:
        raise ReadFailed("no result")
    return ["ok", doc["result"]]


def _call(url: str, to: str, data: str, tag: str) -> typing.Any:
    """eth_call -> hex string, or None if it reverted (or answered empty)."""
    r = rpc_one(url, "eth_call", [{"to": to, "data": data}, tag])
    if r[0] == "revert":
        return None
    if not isinstance(r[1], str) or not r[1].startswith("0x"):
        raise ReadFailed("bad eth_call result")
    if r[1] == "0x":
        return None
    return r[1].lower()


def read_rpc(url: str, token_id: int, block: int) -> dict:
    """Every raw answer the verdict needs, from ONE endpoint, at `block`."""
    tag = hex(block)
    cid = rpc_one(url, "eth_chainId", [])
    if cid[0] != "ok" or not isinstance(cid[1], str) or int(cid[1], 16) != POLYGON:
        raise ReadFailed("wrong chain")
    fin = rpc_one(url, "eth_getBlockByNumber", ["finalized", False])
    if fin[0] != "ok" or not isinstance(fin[1], dict):
        raise ReadFailed("no finalized block")
    fin_n = int(str(fin[1].get("number")), 16)
    out = {"finalized": fin_n}
    if fin_n < block:
        return out
    blk = rpc_one(url, "eth_getBlockByNumber", [tag, False])
    if blk[0] != "ok" or not isinstance(blk[1], dict):
        raise ReadFailed("no such block")
    out["hash"] = str(blk[1].get("hash", "")).lower()
    out["time"] = int(str(blk[1].get("timestamp")), 16)
    out["nft"] = _call(url, TOUCAN_BATCHES, SEL_NFT_LIST + _arg(token_id), tag)
    out["owner"] = _call(url, TOUCAN_BATCHES, SEL_OWNER_OF + _arg(token_id), tag)
    out["tco2"] = None
    out["attrs"] = None
    if out["nft"] is not None:
        pv = decode_nft(out["nft"])["pv_id"]
        if pv > 0:
            out["tco2"] = _call(url, TOUCAN_TCO2_FACTORY, SEL_PV_TO_ERC20 + _arg(pv), tag)
            if out["tco2"] is not None:
                t = _addr_word(_hexdata(out["tco2"]), 0)
                if t != "0x" + "0" * 40:
                    out["attrs"] = _call(url, t, SEL_ATTRIBUTES, tag)
    return out


def read_chain(token_id: int, block: int) -> dict:
    """Both RPCs, identical answers required. {"raw": {...}} or {"code","why"}."""
    got = []
    for u in RPCS:
        try:
            got.append(read_rpc(u, token_id, block))
        except ReadFailed as e:
            return {"code": U_RPC, "why": u[8:] + ": " + str(e)}
        except Exception:
            return {"code": U_RPC, "why": u[8:] + ": unreadable answer"}
    for r, u in zip(got, RPCS):
        if r["finalized"] < block:
            return {"code": U_NOT_FINAL, "why": u[8:] + " has finalized only up to block " + str(r["finalized"])}
    keep = ["hash", "time", "nft", "owner", "tco2", "attrs"]
    pa = {k: got[0].get(k) for k in keep}
    pb = {k: got[1].get(k) for k in keep}
    if _canon(pa) != _canon(pb):
        diff = [k for k in keep if _canon(pa.get(k)) != _canon(pb.get(k))]
        return {"code": U_RPC_DIFF, "why": "the two RPCs differ on " + ",".join(diff)}
    return {"raw": pa}


def verra_body(serial: str) -> str:
    return json.dumps({"searchFilter": {
        "pagination": {"start": 0, "limit": 5, "sortOptions": []},
        "filterModel": {"serialNo": {"columnFilters": [{"filterType": "Text", "type": "equals", "filter": serial}]}}}},
        sort_keys=True, separators=(",", ":"))


def _qty(v: typing.Any) -> int:
    """Verra sends unit counts as JSON numbers (5000.0). Whole, non-negative only."""
    if isinstance(v, bool):
        return -1
    if isinstance(v, int):
        return v if v >= 0 else -1
    if isinstance(v, float):
        if v < 0 or v != v or v > 1e15 or v != int(v):
            return -1
        return int(v)
    return -1


def _text(v: typing.Any, n: int) -> str:
    if v is None:
        return ""
    return str(v)[:n]


def normalize_verra(doc: typing.Any, serial: str, source: str) -> dict:
    """The registry answer -> {"found": False} | {"found": True, "record": {...}}
    | {"code","why"}. Only records whose serialNo equals the serial exactly count."""
    if not isinstance(doc, dict) or not isinstance(doc.get("entities"), list):
        return {"code": U_VERRA_BAD, "why": "the registry answer has no entities list"}
    hits = [e for e in doc["entities"] if isinstance(e, dict) and e.get("serialNo") == serial]
    if len(hits) == 0:
        return {"found": False}
    if len(hits) > 1:
        return {"code": U_AMBIGUOUS, "why": "the registry lists " + str(len(hits)) + " records for this serial"}
    e = hits[0]
    rec = {
        "source": source,
        "serial": serial,
        "status": _text(e.get("stateCode"), 40),
        "quantity": _qty(e.get("holdingQuantity")),
        "project": _text(e.get("vcsProjectId"), 20),
        "vintage": _text(e.get("vintage"), 20),
        "retired_on": _text(e.get("retiredDate"), 10),
        "remark": _text(e.get("publicRetirementReasonDetails"), 240),
        "beneficiary": _text(e.get("publicBeneficialOwner"), 100),
    }
    return {"found": True, "record": rec}


def _verra_one(url: str, serial: str, source: str) -> dict:
    res = _post(url, verra_body(serial), VERRA_HEADERS)
    if res is None:
        return {"code": U_VERRA, "why": "the Verra registry did not answer"}
    if _status(res) != 200:
        return {"code": U_VERRA, "why": "the Verra registry answered HTTP " + str(_status(res))}
    try:
        doc = json.loads(_body(res).decode("utf-8", errors="replace"))
    except Exception:
        return {"code": U_VERRA_BAD, "why": "the Verra registry answer is not JSON"}
    return normalize_verra(doc, serial, source)


def read_verra(serial: str) -> dict:
    """The serial's record: the Retirements report first; only if it is not
    there, the Holdings report (active units), so a serial that was never
    retired ends MISMATCH on status rather than "not found"."""
    r = _verra_one(VERRA_SEARCH, serial, "retirements")
    if "code" in r or r["found"]:
        return r
    return _verra_one(VERRA_HOLDINGS, serial, "holdings")


# ---- the decision ------------------------------------------------------------

def unv(stage: str, code: str, why: str, extra: typing.Any = None) -> dict:
    out = {"verdict": UNVERIFIABLE, "code": code, "why": why, "stage": stage}
    if extra:
        out.update(extra)
    return out


def judge_chain(raw: dict) -> dict:
    """Decoded on-chain facts {"batch": {...}} or a final result (rules 1-3)."""
    try:
        nft = decode_nft(raw["nft"]) if raw.get("nft") is not None else None
    except ReadFailed:
        return unv("chain", U_NO_BATCH, "nftList() answered something that is not a batch")
    if nft is None or raw.get("owner") is None:
        return unv("chain", U_NO_BATCH, "the batch contract has no such token at this block")
    try:
        owner = _addr_word(_hexdata(raw["owner"]), 0)
    except ReadFailed:
        return unv("chain", U_NO_BATCH, "ownerOf() answered something that is not an address")
    st = nft["status"]
    name = BATCH_STATUS[st] if st < len(BATCH_STATUS) else "status " + str(st)
    batch = {"serial": nft["serial"], "quantity": nft["quantity"], "status": name, "pv_id": nft["pv_id"],
             "owner": owner, "tco2": "", "block_hash": raw.get("hash", ""), "block_time": raw.get("time", 0)}
    if st != CONFIRMED:
        return unv("chain", U_NOT_CONFIRMED, "the batch is " + name + ", not Confirmed", {"batch": batch})
    tco2 = ""
    if raw.get("tco2") is not None:
        try:
            tco2 = _addr_word(_hexdata(raw["tco2"]), 0)
        except ReadFailed:
            tco2 = ""
    if tco2 == "" or tco2 == "0x" + "0" * 40:
        return unv("chain", U_NO_TCO2, "the official factory maps this batch's vintage to no TCO2", {"batch": batch})
    batch["tco2"] = tco2
    if owner != tco2:
        return unv("chain", U_NOT_FRACTIONALIZED, "the batch is held by " + owner + ", not by its TCO2", {"batch": batch})
    if raw.get("attrs") is None:
        return unv("chain", U_TCO2, "getAttributes() on the TCO2 reverted", {"batch": batch})
    try:
        a = decode_attributes(raw["attrs"])
    except ReadFailed:
        return unv("chain", U_TCO2, "getAttributes() on the TCO2 is unreadable", {"batch": batch})
    batch["project_id"] = a["project_id"][:40]
    batch["vintage_start"] = iso_of(a["start"])[:10] if a["start"] < 10 ** 11 else ""
    batch["vintage_end"] = iso_of(a["end"])[:10] if a["end"] < 10 ** 11 else ""
    if not a["project_id"].startswith("VCS-"):
        return unv("chain", U_NOT_VCS, "the TCO2 project id " + a["project_id"][:40] + " is not a VCS project", {"batch": batch})
    s = parse_serial(nft["serial"])
    if s is None:
        return unv("serial", U_SERIAL, "the batch serial is not a well-formed Verra VCU serial", {"batch": batch})
    batch["start"] = s["start"]
    batch["end"] = s["end"]
    batch["units"] = s["units"]
    batch["serial_project"] = s["project"]
    batch["serial_vintage_start"] = s["vintage_start"]
    batch["serial_vintage_end"] = s["vintage_end"]
    if a["project_id"] != "VCS-" + str(s["project"]):
        return {"verdict": MISMATCH, "code": M_PROJECT, "stage": "serial", "batch": batch,
                "why": "the serial names project VCS-" + str(s["project"]) + ", the TCO2 says " + a["project_id"][:40]}
    if a["start"] // 86400 != s["vs_day"] or a["end"] // 86400 != s["ve_day"]:
        return {"verdict": MISMATCH, "code": M_VINTAGE, "stage": "serial", "batch": batch,
                "why": "the serial's vintage is " + s["vintage_start"] + ".." + s["vintage_end"] + ", the TCO2 says "
                + batch["vintage_start"] + ".." + batch["vintage_end"]}
    if s["units"] != nft["quantity"]:
        return {"verdict": MISMATCH, "code": M_QUANTITY, "stage": "serial", "batch": batch,
                "why": "the serial spans " + str(s["units"]) + " units, the batch holds " + str(nft["quantity"])}
    return {"batch": batch, "parsed": s}


def judge_verra(batch: dict, parsed: dict, v: dict) -> dict:
    """Rule 4: the Verra record against the batch, field by field."""
    if "code" in v:
        return unv("verra", v["code"], v["why"], {"batch": batch})
    if not v["found"]:
        return unv("verra", U_NOT_FOUND, "the Verra registry lists no retired or active units with this exact serial", {"batch": batch})
    r = v["record"]
    diffs = []
    if r["status"] != VERRA_RETIRED:
        diffs.append([M_V_STATUS, "Verra status is " + (r["status"] or "empty") + ", not RETIRED"])
    if r["quantity"] != parsed["units"]:
        diffs.append([M_V_QUANTITY, "Verra lists " + str(r["quantity"]) + " units, the serial spans " + str(parsed["units"])])
    if r["project"] != str(parsed["project"]):
        diffs.append([M_V_PROJECT, "Verra lists project " + (r["project"] or "none") + ", the serial names " + str(parsed["project"])])
    if r["vintage"] != parsed["verra_vintage"]:
        diffs.append([M_V_VINTAGE, "Verra lists vintage " + (r["vintage"] or "none") + ", the serial's vintage is "
                      + parsed["verra_vintage"]])
    if len(diffs) > 0:
        return {"verdict": MISMATCH, "code": diffs[0][0], "stage": "verra", "batch": batch, "verra": r,
                "why": "; ".join(d[1] for d in diffs)}
    return {"verdict": MATCHED, "code": C_MATCH, "stage": "verra", "batch": batch, "verra": r,
            "why": "Retired on Verra; " + str(parsed["units"]) + " units, project VCS-" + str(parsed["project"])
            + ", vintage " + parsed["vintage_start"] + ".." + parsed["vintage_end"] + " match the batch and its TCO2"}


def evaluate(p: dict) -> dict:
    """The whole check on one node. Every failure becomes UNVERIFIABLE; nothing raises."""
    try:
        ch = read_chain(p["token_id"], p["block"])
        if "code" in ch:
            return unv("chain", ch["code"], ch["why"])
        j = judge_chain(ch["raw"])
        if "verdict" in j:
            return j
        return judge_verra(j["batch"], j["parsed"], read_verra(j["batch"]["serial"]))
    except Exception:
        return unv("internal", U_INTERNAL, "a read failed unexpectedly")


def agree(p: dict, theirs: typing.Any) -> bool:
    """A validator's check of the leader's result: recompute and compare all of it."""
    if not isinstance(theirs, dict) or theirs.get("verdict") not in (MATCHED, MISMATCH, UNVERIFIABLE):
        return False
    if theirs.get("verdict") == UNVERIFIABLE and theirs.get("code") in TRANSPORT_CODES:
        return True
    mine = evaluate(p)
    if mine.get("verdict") == UNVERIFIABLE and mine.get("code") in TRANSPORT_CODES:
        return False
    return _canon(mine) == _canon(theirs)


@gl.storage.allow
@dataclass
class Check:
    check_id: u64
    project: u64
    batch_id: u64
    block: u64
    filer: str
    filed_at: u64
    recheck_of: u64
    verdict: str
    code: str
    why: str
    stage: str
    serial: str
    unit_start: u64
    unit_end: u64
    units: u64
    quantity: str
    batch_status: str
    owner: str
    tco2: str
    project_id: str
    vintage_start: str
    vintage_end: str
    block_hash: str
    block_time: u64
    verra_found: bool
    verra_source: str
    verra_status: str
    verra_quantity: str
    verra_project: str
    verra_vintage: str
    verra_retired_on: str
    verra_remark: str
    verra_beneficiary: str
    conflict_check: u64
    conflict_batch: u64


@gl.storage.allow
@dataclass
class Claimed:
    project: u64
    unit_start: u64
    unit_end: u64
    batch_id: u64
    check_id: u64
    label: str


class CarbonCheck(gl.contract.Contract):
    mode: str
    rate_max: u64
    rate_window: u64
    n: u64
    n_matched: u64
    n_mismatch: u64
    n_double: u64
    n_unverifiable: u64
    checks: gl.storage.TreeMap[u64, Check]
    by_key: gl.storage.TreeMap[str, u64]
    by_batch: gl.storage.TreeMap[u64, str]
    claimed: gl.storage.TreeMap[u64, Claimed]
    n_claimed: u64
    claimed_batch: gl.storage.TreeMap[u64, u64]
    rate_start: gl.storage.TreeMap[str, u64]
    rate_count: gl.storage.TreeMap[str, u64]

    def __init__(self, mode: str, rate_max: int, rate_window: int) -> None:
        m = str(mode).strip().upper()
        if m not in ("CANONICAL", "DEMO"):
            raise gl.vm.UserError("mode must be CANONICAL or DEMO")
        if int(rate_max) < 1 or int(rate_max) > 100 or int(rate_window) < 60 or int(rate_window) > 86400 * 7:
            raise gl.vm.UserError("bad rate limit")
        self.mode = m
        self.rate_max = u64(int(rate_max))
        self.rate_window = u64(int(rate_window))
        self.n = u64(0)
        self.n_matched = u64(0)
        self.n_mismatch = u64(0)
        self.n_double = u64(0)
        self.n_unverifiable = u64(0)
        self.n_claimed = u64(0)

    def _now(self) -> int:
        return iso_epoch(gl.message.raw.get("datetime", ""))

    @gl.public.write
    def file_check(self, batch_contract: str, token_id: int, block: int) -> typing.Any:
        return self._file(batch_contract, token_id, block, 0)

    @gl.public.write
    def recheck(self, check_id: int, block: int) -> typing.Any:
        """A fresh check of the same batch at a newer block: Verra is live, so
        an old verdict is only true as of its own fetch."""
        cid = as_int(check_id)
        old = self.checks.get(u64(cid)) if cid is not None and 0 < cid < 2 ** 63 else None
        if old is None:
            raise gl.vm.UserError("REFUSED: NO_SUCH_CHECK")
        return self._file(TOUCAN_BATCHES, int(old.batch_id), block, cid)

    def _file(self, batch_contract: typing.Any, token_id: typing.Any, block: typing.Any, recheck_of: int) -> typing.Any:
        now = self._now()
        if now <= 0:
            raise gl.vm.UserError("REFUSED: NO_CLOCK")
        # --- door: format checks; a refusal stores nothing
        bc = str(batch_contract).strip().lower() if isinstance(batch_contract, str) else ""
        if bc != TOUCAN_BATCHES:
            raise gl.vm.UserError("REFUSED: NOT_TOUCAN_BATCH_CONTRACT")
        tid = as_int(token_id)
        if tid is None or tid < 1 or tid > MAX_TOKEN_ID:
            raise gl.vm.UserError("REFUSED: BAD_TOKEN_ID")
        blk = as_int(block)
        if blk is None or blk < MIN_BLOCK or blk >= MAX_BLOCK:
            raise gl.vm.UserError("REFUSED: BAD_BLOCK")
        key = str(tid) + "@" + str(blk)
        if int(self.by_key.get(key) or 0) != 0:
            raise gl.vm.UserError("REFUSED: DUPLICATE_OF_" + str(int(self.by_key.get(key))))
        sender = gl.message.sender_address.as_hex.lower()
        start = int(self.rate_start.get(sender) or 0)
        count = int(self.rate_count.get(sender) or 0)
        if now - start >= int(self.rate_window):
            start = now
            count = 0
        if count >= int(self.rate_max):
            raise gl.vm.UserError("REFUSED: RATE_LIMITED_UNTIL_" + str(start + int(self.rate_window)))

        p = {"token_id": tid, "block": blk}

        def leader() -> dict:
            return evaluate(p)

        def validator(res: gl.vm.Result) -> bool:
            if not isinstance(res, gl.vm.Return):
                return False
            return agree(p, res.calldata)

        r = gl.vm.run_nondet(leader, validator)
        if not isinstance(r, dict) or r.get("verdict") not in (MATCHED, MISMATCH, UNVERIFIABLE):
            r = unv("internal", U_INTERNAL, "no readable result")
        b = r.get("batch") if isinstance(r.get("batch"), dict) else {}
        v = r.get("verra") if isinstance(r.get("verra"), dict) else {}
        verdict = str(r["verdict"])
        code = str(r.get("code", ""))[:40]
        why = str(r.get("why", ""))[:400]
        conflict = None
        u_start = int(b.get("start") or 0)
        u_end = int(b.get("end") or 0)
        u_project = int(b.get("serial_project") or 0)
        # --- rule 5: interval overlap with a range MATCHED for another batch
        if verdict == MATCHED:
            i = 1
            while i <= int(self.n_claimed):
                c = self.claimed[u64(i)]
                if int(c.batch_id) != tid and int(c.project) == u_project and overlaps(u_start, u_end, int(c.unit_start), int(c.unit_end)):
                    conflict = c
                    break
                i += 1
            if conflict is not None:
                verdict = DOUBLE_CLAIMED
                code = C_DOUBLE
                why = ("project " + str(u_project) + " units " + str(u_start) + ".." + str(u_end) + " overlap units " + str(int(conflict.unit_start))
                       + ".." + str(int(conflict.unit_end)) + " already MATCHED for "
                       + (("batch " + str(int(conflict.batch_id)) + " in check " + str(int(conflict.check_id)))
                          if int(conflict.batch_id) != 0 else conflict.label))
        # --- writes (nothing below can refuse)
        new_id = int(self.n) + 1
        self.checks[u64(new_id)] = Check(
            check_id=u64(new_id), project=u64(u_project), batch_id=u64(tid), block=u64(blk), filer=sender, filed_at=u64(now),
            recheck_of=u64(recheck_of), verdict=verdict, code=code, why=why, stage=str(r.get("stage", ""))[:20],
            serial=str(b.get("serial", ""))[:MAX_SERIAL + 8], unit_start=u64(u_start), unit_end=u64(u_end),
            units=u64(int(b.get("units") or 0)), quantity=str(b.get("quantity", ""))[:40],
            batch_status=str(b.get("status", ""))[:40], owner=str(b.get("owner", ""))[:42],
            tco2=str(b.get("tco2", ""))[:42], project_id=str(b.get("project_id", ""))[:40],
            vintage_start=str(b.get("vintage_start", ""))[:10], vintage_end=str(b.get("vintage_end", ""))[:10],
            block_hash=str(b.get("block_hash", ""))[:66], block_time=u64(int(b.get("block_time") or 0)),
            verra_found=len(v) > 0, verra_source=str(v.get("source", "")), verra_status=str(v.get("status", "")), verra_quantity=str(v.get("quantity", "")),
            verra_project=str(v.get("project", "")), verra_vintage=str(v.get("vintage", "")),
            verra_retired_on=str(v.get("retired_on", "")), verra_remark=str(v.get("remark", "")),
            verra_beneficiary=str(v.get("beneficiary", "")),
            conflict_check=u64(int(conflict.check_id) if conflict is not None else 0),
            conflict_batch=u64(int(conflict.batch_id) if conflict is not None else 0))
        self.by_key[key] = u64(new_id)
        prev = self.by_batch.get(u64(tid)) or ""
        self.by_batch[u64(tid)] = (prev + "," if prev else "") + str(new_id)
        if verdict == MATCHED and int(self.claimed_batch.get(u64(tid)) or 0) == 0:
            self._claim(u_project, u_start, u_end, tid, new_id, "")
        self.rate_start[sender] = u64(start)
        self.rate_count[sender] = u64(count + 1)
        self.n = u64(new_id)
        if verdict == MATCHED:
            self.n_matched = u64(int(self.n_matched) + 1)
        elif verdict == MISMATCH:
            self.n_mismatch = u64(int(self.n_mismatch) + 1)
        elif verdict == DOUBLE_CLAIMED:
            self.n_double = u64(int(self.n_double) + 1)
        else:
            self.n_unverifiable = u64(int(self.n_unverifiable) + 1)
        return {"check_id": new_id, "verdict": verdict, "code": code, "why": why}

    def _claim(self, project: int, u_start: int, u_end: int, batch_id: int, check_id: int, label: str) -> None:
        k = int(self.n_claimed) + 1
        self.claimed[u64(k)] = Claimed(project=u64(project), unit_start=u64(u_start), unit_end=u64(u_end), batch_id=u64(batch_id),
                                       check_id=u64(check_id), label=label)
        self.n_claimed = u64(k)
        if batch_id != 0:
            self.claimed_batch[u64(batch_id)] = u64(k)

    @gl.public.write
    def demo_claim_range(self, project: int, unit_start: int, unit_end: int, label: str) -> typing.Any:
        """DEMO deployment only: enters a labelled range as if MATCHED by a
        non-Toucan source, so the DOUBLE_CLAIMED path can be shown with real
        Toucan batches (which Toucan itself never let overlap). The canonical
        deployment refuses it."""
        if self.mode != "DEMO":
            raise gl.vm.UserError("REFUSED: DEMO_ONLY")
        try:
            pj, s, e = int(project), int(unit_start), int(unit_end)
        except Exception:
            raise gl.vm.UserError("REFUSED: BAD_RANGE")
        if pj < 1 or pj >= 10 ** 9 or s < 1 or e < s or e >= MAX_UNIT:
            raise gl.vm.UserError("REFUSED: BAD_RANGE")
        lb = str(label)[:60]
        for ch in lb:
            if ord(ch) < 32 or ord(ch) > 126:
                raise gl.vm.UserError("REFUSED: BAD_LABEL")
        if len(lb) < 3:
            raise gl.vm.UserError("REFUSED: BAD_LABEL")
        self._claim(pj, s, e, 0, 0, "DEMO range '" + lb + "'")
        return {"claimed_id": int(self.n_claimed), "project": pj, "unit_start": s, "unit_end": e}

    # --- views (storage only) -------------------------------------------------

    def _view(self, c: Check) -> dict:
        return {"found": True, "check_id": int(c.check_id), "batch_contract": TOUCAN_BATCHES,
                "batch_id": int(c.batch_id), "block": int(c.block), "filer": c.filer,
                "filed_at": int(c.filed_at), "as_of": iso_of(int(c.filed_at)), "recheck_of": int(c.recheck_of),
                "verdict": c.verdict, "code": c.code, "why": c.why, "stage": c.stage,
                "serial": c.serial, "serial_project": int(c.project), "unit_start": int(c.unit_start), "unit_end": int(c.unit_end),
                "units": int(c.units), "quantity": c.quantity, "batch_status": c.batch_status,
                "owner": c.owner, "tco2": c.tco2, "project_id": c.project_id,
                "vintage_start": c.vintage_start, "vintage_end": c.vintage_end,
                "block_hash": c.block_hash, "block_time": int(c.block_time),
                "verra": {"found": bool(c.verra_found), "source": c.verra_source, "status": c.verra_status, "quantity": c.verra_quantity,
                          "project": c.verra_project, "vintage": c.verra_vintage,
                          "retired_on": c.verra_retired_on, "remark": c.verra_remark,
                          "beneficiary": c.verra_beneficiary},
                "conflict_check": int(c.conflict_check), "conflict_batch": int(c.conflict_batch),
                "batch_url": POLYGONSCAN + "/token/" + TOUCAN_BATCHES + "?a=" + str(int(c.batch_id)),
                "block_url": POLYGONSCAN + "/block/" + str(int(c.block)),
                "tco2_url": (POLYGONSCAN + "/token/" + c.tco2) if c.tco2 else "",
                "verra_url": VERRA_PAGE}

    @gl.public.view
    def get_check(self, check_id: int) -> typing.Any:
        c = self.checks.get(u64(int(check_id))) if int(check_id) > 0 else None
        if c is None:
            return {"found": False, "check_id": int(check_id)}
        return self._view(c)

    @gl.public.view
    def list_checks(self, start: int, count: int) -> typing.Any:
        s = max(1, int(start))
        k = max(0, min(int(count), MAX_PAGE_LIST))
        out = []
        i = s
        while i <= int(self.n) and len(out) < k:
            out.append(self._view(self.checks[u64(i)]))
            i += 1
        return {"total": int(self.n), "start": s, "checks": out}

    @gl.public.view
    def latest_verdict(self, batch_id: int) -> typing.Any:
        """The filing that read the NEWEST Polygon block for the batch (ties
        cannot happen: one filing per batch and block). A filing pinned to an
        older block can never mask a newer one, whatever order they were
        filed in. Carries both "as of" times: the fetch and the block."""
        ids = (self.by_batch.get(u64(int(batch_id))) or "").split(",") if int(batch_id) > 0 else []
        last = None
        counts = {MATCHED: 0, MISMATCH: 0, DOUBLE_CLAIMED: 0, UNVERIFIABLE: 0}
        for s in ids:
            if s == "":
                continue
            c = self.checks[u64(int(s))]
            counts[c.verdict] += 1
            if last is None or (int(c.block), int(c.check_id)) > (int(last.block), int(last.check_id)):
                last = c
        if last is None:
            return {"batch_id": int(batch_id), "verdict": "NONE", "check_id": 0, "filed_at": 0,
                    "as_of": "", "block": 0, "block_time": 0, "counts": counts}
        return {"batch_id": int(batch_id), "verdict": last.verdict, "code": last.code,
                "check_id": int(last.check_id), "filed_at": int(last.filed_at),
                "as_of": iso_of(int(last.filed_at)), "block": int(last.block),
                "block_time": int(last.block_time), "counts": counts}

    @gl.public.view
    def is_matched(self, batch_id: int) -> bool:
        return self.latest_verdict(batch_id)["verdict"] == MATCHED

    @gl.public.view
    def list_claimed(self, start: int, count: int) -> typing.Any:
        s = max(1, int(start))
        k = max(0, min(int(count), MAX_PAGE_LIST))
        out = []
        i = s
        while i <= int(self.n_claimed) and len(out) < k:
            c = self.claimed[u64(i)]
            out.append({"id": i, "project": int(c.project), "unit_start": int(c.unit_start), "unit_end": int(c.unit_end),
                        "batch_id": int(c.batch_id), "check_id": int(c.check_id), "label": c.label})
            i += 1
        return {"total": int(self.n_claimed), "start": s, "ranges": out}

    @gl.public.view
    def get_stats(self) -> typing.Any:
        return {"version": VERSION, "mode": self.mode, "checks": int(self.n), "matched": int(self.n_matched),
                "mismatch": int(self.n_mismatch), "double_claimed": int(self.n_double),
                "unverifiable": int(self.n_unverifiable), "claimed_ranges": int(self.n_claimed),
                "rate_max": int(self.rate_max), "rate_window": int(self.rate_window)}

    @gl.public.view
    def get_rules(self) -> typing.Any:
        return {"version": VERSION, "verdicts": list(VERDICTS), "chain_id": POLYGON, "rpcs": list(RPCS),
                "batch_contract": TOUCAN_BATCHES, "tco2_factory": TOUCAN_TCO2_FACTORY,
                "required_batch_status": BATCH_STATUS[CONFIRMED], "fractionalized": "ownerOf(batch) == its TCO2",
                "verra_search": [VERRA_SEARCH, VERRA_HOLDINGS], "verra_retired_status": VERRA_RETIRED,
                "min_block": MIN_BLOCK, "model": "none"}

    @gl.public.view
    def rate_status(self, sender: str) -> typing.Any:
        s = str(sender).strip().lower()
        now = self._now()
        start = int(self.rate_start.get(s) or 0)
        count = int(self.rate_count.get(s) or 0)
        if now - start >= int(self.rate_window):
            count = 0
        return {"sender": s, "used": count, "max": int(self.rate_max), "window": int(self.rate_window)}
