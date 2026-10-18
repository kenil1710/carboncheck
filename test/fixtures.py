"""Builders for the offline suite: two mock Polygon RPCs holding Toucan batch
NFTs, TCO2 factory entries and TCO2 attributes (ABI-encoded exactly as the
real contracts answer), a mock Verra registry (Retirements and Holdings
reports) and a wired deployment (CarbonCheck canonical + demo, OffsetGate)."""
import hashlib
import json

import stub
import world

CC = world.module("CarbonCheck")
OG = world.module("OffsetGate")

NOW_ISO = "2026-10-18T12:00:00Z"
NOW = CC.iso_epoch(NOW_ISO)
FIN = 95_733_573
BLOCK = 95_700_000
BLOCK_TS = NOW - 60
HOUR = 3600
DAY = 86400
RPC_A, RPC_B = CC.RPCS
BATCHES = CC.TOUCAN_BATCHES
FACTORY = CC.TOUCAN_TCO2_FACTORY


def addr(n):
    return "0x" + hashlib.sha256(b"addr%d" % n).hexdigest()[:40]


FILER = addr(0xf11e)
FILER2 = addr(0xf11f)
FILER3 = addr(0xf120)
USER = addr(0x05e)

# ---- ABI encoding -------------------------------------------------------------


def w(n):
    return "%064x" % n


def a_word(a):
    return "0" * 24 + a[2:].lower()


def enc_str(s):
    b = s.encode("utf-8")
    pad = (32 - len(b) % 32) % 32
    return w(len(b)) + (b + b"\x00" * pad).hex()


def enc_nft(pv, serial, qty, status, uri=""):
    """(uint256, string, uint256, uint8, string)"""
    s1 = enc_str(serial)
    off1 = 5 * 32
    off2 = off1 + len(s1) // 2
    return "0x" + w(pv) + w(off1) + w(qty) + w(status) + w(off2) + s1 + enc_str(uri)


def enc_addr(a):
    return "0x" + a_word(a)


def _tuple(head_words, strings):
    """A dynamic tuple: head_words is a list of either int (static word) or
    str (a string placed in the tail)."""
    head = ""
    tail = ""
    n = len(head_words)
    for h in head_words:
        if isinstance(h, str):
            head += w(n * 32 + len(tail) // 2)
            tail += enc_str(h)
        else:
            head += w(h)
    return head + tail


def enc_attributes(project_id, vintage_name, start, end, beneficiary="0x" + "0" * 40):
    """((string x9, address), (string, uint64, uint64, uint256, uint64, bool, bool, string x5))"""
    p = _tuple([project_id, "VCS", "VM0001", "CN", "", "", "", "", "", int(beneficiary, 16)], [])
    v = _tuple([vintage_name, start, end, 7, 100000, 0, 0, "", "", "", "", ""], [])
    return "0x" + w(64) + w(64 + len(p) // 2) + p + v


# ---- the chain -------------------------------------------------------------------


def chains():
    out = {}
    for url in CC.RPCS:
        ch = stub.MockChain(137, FIN, NOW - 60)
        for i in range(0, 40):
            ch.set_block(BLOCK + i, BLOCK_TS + 2 * i)
        stub.WEB.chains[url] = ch
        out[url] = ch
    return out


_extra = [BLOCK + 100]


def new_block(ts):
    """A new block at time `ts` on both RPCs (finalized moves up to it)."""
    _extra[0] += 1
    n = _extra[0]
    for url in CC.RPCS:
        ch = stub.WEB.chains[url]
        ch.set_block(n, ts)
        ch.finalized = max(ch.finalized, n)
        ch.set_block(ch.finalized, ch.blocks[ch.finalized][1])
    return n


def tco2_of(pv):
    return addr(0x7c0200 + pv)


def ep(y, m, d):
    return CC.epoch_of(y, m, d, 0, 0, 0)


def set_batch(token_id, serial, qty, status=2, pv=None, project="VCS-191", vintage=(ep(2009, 1, 1), ep(2009, 12, 31)),
              owner=None, tco2=None, urls=None, block=None, attrs=True, vintage_name="2009"):
    """A batch NFT, its factory entry and its TCO2 on every RPC (or `urls`),
    optionally only at `block`. By default the batch is Confirmed and held by
    its own TCO2 (fractionalized)."""
    pv = pv if pv is not None else 1000 + token_id
    t = tco2 if tco2 is not None else tco2_of(pv)
    own = owner if owner is not None else t
    for url in urls or CC.RPCS:
        ch = stub.WEB.chains[url]
        st = ch.calls if block is None else ch.at.setdefault(block, {}).setdefault("calls", {})
        st[(BATCHES, CC.SEL_NFT_LIST + w(token_id))] = enc_nft(pv, serial, qty, status)
        st[(BATCHES, CC.SEL_OWNER_OF + w(token_id))] = stub.MockChain.REVERT if own == "REVERT" else enc_addr(own)
        st[(FACTORY, CC.SEL_PV_TO_ERC20 + w(pv))] = enc_addr(t)
        if attrs and t != "0x" + "0" * 40:
            st[(t.lower(), CC.SEL_ATTRIBUTES)] = enc_attributes(project, vintage_name, vintage[0], vintage[1])
        ch.code[BATCHES] = "0x6080"
        ch.code[FACTORY] = "0x6080"
        ch.code[t.lower()] = "0x6080"
    return {"pv": pv, "tco2": t}


# ---- Verra ------------------------------------------------------------------------


class Verra:
    """Retirements and Holdings reports. Answers a serialNo `equals` filter
    with every stored entity whose serialNo equals it."""

    def __init__(self):
        self.retired = {}       # serial -> [entity, ...]
        self.holdings = {}
        self.status = {}        # report -> forced HTTP status
        self.raw = {}           # report -> forced raw body
        self.log = []
        self.headers = []

    def handler(self, report):
        def h(body, headers):
            self.log.append(report)
            self.headers.append(headers)
            if report in self.status:
                return (self.status[report], "{}")
            if report in self.raw:
                return (200, self.raw[report])
            req = json.loads(body)
            f = req["searchFilter"]["filterModel"]["serialNo"]["columnFilters"][0]
            assert f["type"] == "equals" and f["filterType"] == "Text"
            store = self.retired if report == "retirements" else self.holdings
            ents = list(store.get(f["filter"], []))
            return (200, json.dumps({"entities": ents, "totalEntities": len(ents), "start": 0, "limit": 5}))
        return h


VERRA = Verra()


def entity(serial, qty, project, vintage, state="RETIRED", remark="TOUCAN-1.0-137-0xabc-1", retired="2022-01-25T00:00:00"):
    return {"serialNo": serial, "holdingQuantity": float(qty), "stateCode": state, "vcsProjectId": str(project),
            "projectId": int(project) if str(project).isdigit() else None, "vintage": str(vintage),
            "retiredDate": retired if state == "RETIRED" else None, "publicRetirementReasonDetails": remark,
            "publicBeneficialOwner": "0x22270a0b82cbf0bd80c6e0fad85342600518e114", "esUpdatedOn": "2026-10-17T15:19:22"}


def retire(serial, qty, project, vintage, **k):
    VERRA.retired.setdefault(serial, []).append(entity(serial, qty, project, vintage, **k))


def hold(serial, qty, project, vintage, state="ACTIVE"):
    VERRA.holdings.setdefault(serial, []).append(entity(serial, qty, project, vintage, state=state, remark=None))


def reset():
    global VERRA
    stub.WEB.reset()
    stub.MODEL.reset()
    stub.FORGE["payload"] = None
    stub.FORGE["mutate"] = None
    VERRA = Verra()
    stub.WEB.posts[CC.VERRA_SEARCH] = VERRA.handler("retirements")
    stub.WEB.posts[CC.VERRA_HOLDINGS] = VERRA.handler("holdings")


def verra():
    return VERRA


# A real batch (Toucan batch 1000, read 2026-10-18 at Polygon block 95733573).
S1000 = "12078-382273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0"


def real_batch(token_id=1000, serial=S1000, qty=5000, project=191, year=2009, vintage=None, retire_it=True):
    v = vintage or (ep(year, 1, 1), ep(year, 12, 31))
    info = set_batch(token_id, serial, qty, project="VCS-" + str(project), vintage=v, vintage_name=str(year))
    if retire_it:
        retire(serial, qty, project, year)
    return info


def serial_for(start, end, project=191, year=2009, issuance=12078):
    return "%d-%d-%d-VCS-VCU-304-VER-CN-1-%d-0101%d-3112%d-0" % (issuance, start, end, project, year, year)


def deploy(rate_max=5, rate_window=HOUR, demo=False, max_age=30 * DAY):
    reset()
    wd = world.new_world(now_iso=NOW_ISO)
    chains()
    cc = wd.deploy("CarbonCheck", "DEMO" if demo else "CANONICAL", rate_max, rate_window)
    gate = wd.deploy("OffsetGate", cc, max_age)
    return wd, cc, gate
