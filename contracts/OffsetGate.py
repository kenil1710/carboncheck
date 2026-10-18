# v0.3.0
# { "Depends": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng" }
import genlayer as gl
from genlayer import *
from dataclasses import dataclass
import typing

# OffsetGate - a consumer of CarbonCheck.
#
# Accepts an offset claim for a Toucan batch only if CarbonCheck's LATEST
# verdict for that batch (the one that read the newest Polygon block) is
# MATCHED, was ruled at most `max_age` seconds ago, and read a Polygon block
# at most `max_age` seconds old. Anything else is refused and nothing is stored. Each batch can back
# one accepted claim, so the same credits are never counted twice here.
# The CarbonCheck address and max_age are frozen at deploy; no owner, no
# setter, no funds.

VERSION = "1.0.0"
MAX_NOTE = 140
MAX_PAGE_LIST = 50


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


def decide(lv: typing.Any, now: int, max_age: int) -> dict:
    """CarbonCheck.latest_verdict(batch) -> {"ok": True} or {"refuse": CODE}."""
    if not isinstance(lv, dict):
        return {"refuse": "REGISTRY_UNREADABLE"}
    v = lv.get("verdict")
    if v == "NONE" or v is None:
        return {"refuse": "NO_VERDICT"}
    if v != "MATCHED":
        return {"refuse": "NOT_MATCHED_" + str(v)[:20]}
    try:
        at = int(lv.get("filed_at"))
    except Exception:
        return {"refuse": "REGISTRY_UNREADABLE"}
    if at <= 0 or at > now:
        return {"refuse": "REGISTRY_UNREADABLE"}
    if now - at > max_age:
        return {"refuse": "STALE_VERDICT"}
    try:
        bt = int(lv.get("block_time"))
    except Exception:
        return {"refuse": "REGISTRY_UNREADABLE"}
    if bt <= 0 or now - bt > max_age:
        return {"refuse": "STALE_BLOCK"}
    return {"ok": True}


@gl.storage.allow
@dataclass
class Claim:
    claim_id: u64
    batch_id: u64
    check_id: u64
    verdict_at: u64
    claimant: str
    note: str
    accepted_at: u64


class OffsetGate(gl.contract.Contract):
    registry: Address
    max_age: u64
    n: u64
    claims: gl.storage.TreeMap[u64, Claim]
    by_batch: gl.storage.TreeMap[u64, u64]

    def __init__(self, registry: str, max_age: int) -> None:
        if int(max_age) < 60 or int(max_age) > 86400 * 365:
            raise gl.vm.UserError("bad max_age")
        self.registry = Address(registry)
        self.max_age = u64(int(max_age))
        self.n = u64(0)

    def _now(self) -> int:
        return iso_epoch(gl.message.raw.get("datetime", ""))

    def _latest(self, batch_id: int) -> typing.Any:
        try:
            return gl.contract.get_at(self.registry).view().latest_verdict(batch_id)
        except Exception:
            return None

    @gl.public.write
    def claim_offset(self, batch_id: int, note: str) -> typing.Any:
        now = self._now()
        if now <= 0:
            raise gl.vm.UserError("REFUSED: NO_CLOCK")
        bid = batch_id if isinstance(batch_id, int) and not isinstance(batch_id, bool) else None
        if bid is None or bid < 1 or bid > 10 ** 9:
            raise gl.vm.UserError("REFUSED: BAD_BATCH_ID")
        nt = str(note) if isinstance(note, str) else ""
        if len(nt) > MAX_NOTE:
            raise gl.vm.UserError("REFUSED: BAD_NOTE")
        for ch in nt:
            if ord(ch) < 32 or ord(ch) > 126:
                raise gl.vm.UserError("REFUSED: BAD_NOTE")
        prev = int(self.by_batch.get(u64(bid)) or 0)
        if prev != 0:
            raise gl.vm.UserError("REFUSED: ALREADY_CLAIMED_IN_" + str(prev))
        lv = self._latest(bid)
        d = decide(lv, now, int(self.max_age))
        if "refuse" in d:
            raise gl.vm.UserError("REFUSED: " + d["refuse"])
        k = int(self.n) + 1
        self.claims[u64(k)] = Claim(claim_id=u64(k), batch_id=u64(bid), check_id=u64(int(lv["check_id"])),
                                    verdict_at=u64(int(lv["filed_at"])),
                                    claimant=gl.message.sender_address.as_hex.lower(), note=nt,
                                    accepted_at=u64(now))
        self.by_batch[u64(bid)] = u64(k)
        self.n = u64(k)
        return {"claim_id": k, "batch_id": bid, "check_id": int(lv["check_id"]), "age_s": now - int(lv["filed_at"])}

    @gl.public.view
    def check_offset(self, batch_id: int) -> typing.Any:
        """What claim_offset would answer right now, without storing anything."""
        bid = int(batch_id)
        prev = int(self.by_batch.get(u64(bid)) or 0) if bid > 0 else 0
        if prev != 0:
            return {"batch_id": bid, "accept": False, "reason": "ALREADY_CLAIMED_IN_" + str(prev)}
        lv = self._latest(bid)
        d = decide(lv, self._now(), int(self.max_age))
        return {"batch_id": bid, "accept": "ok" in d, "reason": d.get("refuse", "MATCHED_AND_FRESH"),
                "latest": lv}

    def _view(self, c: Claim) -> dict:
        return {"claim_id": int(c.claim_id), "batch_id": int(c.batch_id), "check_id": int(c.check_id),
                "verdict_at": int(c.verdict_at), "claimant": c.claimant, "note": c.note,
                "accepted_at": int(c.accepted_at)}

    @gl.public.view
    def get_claim(self, claim_id: int) -> typing.Any:
        c = self.claims.get(u64(int(claim_id))) if int(claim_id) > 0 else None
        if c is None:
            return {"found": False, "claim_id": int(claim_id)}
        out = self._view(c)
        out["found"] = True
        return out

    @gl.public.view
    def list_claims(self, start: int, count: int) -> typing.Any:
        s = max(1, int(start))
        k = max(0, min(int(count), MAX_PAGE_LIST))
        out = []
        i = s
        while i <= int(self.n) and len(out) < k:
            out.append(self._view(self.claims[u64(i)]))
            i += 1
        return {"total": int(self.n), "start": s, "claims": out}

    @gl.public.view
    def get_config(self) -> typing.Any:
        return {"version": VERSION, "registry": self.registry.as_hex, "max_age": int(self.max_age),
                "claims": int(self.n)}
