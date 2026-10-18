"""Offline suite for CarbonCheck and OffsetGate.

    cd test && python3 -m unittest -q test_carboncheck test_attacks
"""
import json
import unittest
from pathlib import Path

import fixtures as F
import stub
import world
from fixtures import CC, OG, BATCHES, BLOCK, FILER, FILER2, FILER3, USER, S1000, HOUR, DAY

ROOT = Path(__file__).resolve().parent.parent
REAL = json.loads((Path(__file__).parent / "real_batches.json").read_text())


class Base(unittest.TestCase):
    demo = False
    max_age = 30 * DAY

    def setUp(self):
        self.w, self.cc, self.gate = F.deploy(demo=self.demo, max_age=self.max_age)
        F.real_batch()

    def file(self, token_id=1000, block=BLOCK, contract=BATCHES, sender=FILER, cc=None):
        return self.w.call(cc or self.cc, "file_check", contract, token_id, block, sender=sender)

    def refused(self, code, **k):
        with self.assertRaises(world.Reverted) as cm:
            self.file(**k)
        self.assertTrue(cm.exception.msg.startswith("REFUSED: " + code), cm.exception.msg)
        return cm.exception.msg

    def verdict(self, expect, code=None, **k):
        r = self.file(**k)
        self.assertEqual(r["verdict"], expect, r)
        if code is not None:
            self.assertEqual(r["code"], code, r)
        return r

    def check(self, cid):
        return self.w.view(self.cc, "get_check", cid)

    def stats(self):
        return self.w.view(self.cc, "get_stats")

    def batch(self, token_id, serial, qty, project=191, year=2009, retire=True, **k):
        F.set_batch(token_id, serial, qty, project="VCS-" + str(project),
                    vintage=(F.ep(year, 1, 1), F.ep(year, 12, 31)), vintage_name=str(year), **k)
        if retire:
            F.retire(serial, qty, project, year)


# ------------------------------------------------------------------ serials

REAL_SERIALS = sorted({s for r in REAL["batches"] for s in r["serial"].split(",") if CC.parse_serial(s)})[:60]


class TestRealSerials(unittest.TestCase):
    """Every confirmed single-serial format seen on chain parses, and the
    parsed numbers are the ones written in the serial."""


def _real_serial_test(s):
    def t(self):
        p = CC.parse_serial(s)
        parts = s.split("-")
        self.assertIsNotNone(p, s)
        self.assertEqual(p["start"], int(parts[1]))
        self.assertEqual(p["end"], int(parts[2]))
        self.assertEqual(p["units"], int(parts[2]) - int(parts[1]) + 1)
        self.assertEqual(p["project"], int(parts[-4]))
        self.assertEqual(p["vintage_start"][:4], parts[-3][4:])
        self.assertEqual(p["vintage_end"][:4], parts[-2][4:])
    return t


for _i, _s in enumerate(REAL_SERIALS):
    setattr(TestRealSerials, "test_real_%02d" % _i, _real_serial_test(_s))

MALFORMED = {
    "comma_list": "9380-92545283-92645182-VCS-VCU-263-VER-ID-14-674-01072014-31122014-1,7627-414200938-414229937-VCU-016-MER-ID-14-674-01072014-31122014-1",
    "puro": "643002406801000010000000192331-643002406801000010000000192335",
    "puro_uuid": "926aeaf2-5603-4388-a6fe-53af6108c34a_643002406801000010000000213789-643002406801000010000000213789",
    "tx_hash": "0xe1e28e399de8fc14f9e29824554eb6367aa71f24c606c662091b734a6c91ac41-239",
    "short_number": "1235",
    "zeros": "000",
    "leading_zero_units": "1234-00000001-00001000-VCS-VCU-262-VER-IN-1-1418-01012018-31122018-1",
    "escaped_unicode": "\\u00311015-267732157-267732168-VCS-VCU-279-VER-TR-1-905-01012013-31122013-0",
    "address": "0xd838290e877e0188a4a44700463419ed96c16107",
    "empty": "",
    "lowercase": "12078-382273659-382278658-vcs-vcu-304-ver-cn-1-191-01012009-31122009-0",
    "end_before_start": "12078-382278658-382273659-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0",
    "zero_start": "12078-0-5-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0",
    "double_hyphen": "12078--382273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0",
    "trailing_hyphen": "12078-382273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0-",
    "space": "12078-382273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0 ",
    "no_vcu": "12078-382273659-382278658-VCS-XYZ-304-VER-CN-1-191-01012009-31122009-0",
    "bad_flag": "12078-382273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-2",
    "feb_30": "12078-382273659-382278658-VCS-VCU-304-VER-CN-1-191-30022009-31122009-0",
    "month_13": "12078-382273659-382278658-VCS-VCU-304-VER-CN-1-191-01132009-31122009-0",
    "vintage_reversed": "12078-382273659-382278658-VCS-VCU-304-VER-CN-1-191-31122010-01012009-0",
    "seven_digit_date": "12078-382273659-382278658-VCS-VCU-304-VER-CN-1-191-0101209-31122009-0",
    "project_zero": "12078-382273659-382278658-VCS-VCU-304-VER-CN-1-0-01012009-31122009-0",
    "project_leading_zero": "12078-382273659-382278658-VCS-VCU-304-VER-CN-1-0191-01012009-31122009-0",
    "project_letters": "12078-382273659-382278658-VCS-VCU-304-VER-CN-1-19A-01012009-31122009-0",
    "fullwidth_digit": "12078-３82273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0",
    "arabic_indic_digit": "12078-382273659-38227865٨-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0",
    "unicode_hyphen": "12078‐382273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0",
    "zero_width": "12078-382273659​-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0",
    "cyrillic_vcu": "12078-382273659-382278658-VCS-VСU-304-VER-CN-1-191-01012009-31122009-0",
    "too_long": "12078-382273659-382278658-VCS-VCU-" + "A-" * 60 + "191-01012009-31122009-0",
    "too_few_parts": "12078-382273659-382278658-VCU-191-01012009-31122009-0",
    "units_overflow": "12078-382273659-1000000000000000-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0",
    "not_a_string": 12345,
    "none": None,
    "semicolon_list": "12078-382273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0;1",
    "plus_sign": "12078-+382273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0",
    "negative_range": "12078-382273659--382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0",
    "year_1900": "12078-382273659-382278658-VCS-VCU-304-VER-CN-1-191-01011900-31121900-0",
    "newline": "12078-382273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0\n",
}


class TestMalformedSerials(unittest.TestCase):
    pass


def _bad_serial_test(s):
    def t(self):
        self.assertIsNone(CC.parse_serial(s), repr(s))
    return t


for _k, _s in MALFORMED.items():
    setattr(TestMalformedSerials, "test_rejects_" + _k, _bad_serial_test(_s))


class TestSerialDetails(unittest.TestCase):
    def test_single_unit(self):
        p = CC.parse_serial("8367-10851650-10851650-VCS-VCU-1423-VER-IN-1-1418-01012020-29022020-0")
        self.assertEqual(p["units"], 1)
        self.assertEqual(p["vintage_end"], "2020-02-29")

    def test_old_apx_format(self):
        p = CC.parse_serial("7236-378945246-378945248-VCU-034-APX-IN-1-1190-01012018-31052018-0")
        self.assertEqual((p["start"], p["end"], p["project"]), (378945246, 378945248, 1190))
        self.assertEqual(p["vintage_year"], "2018")

    def test_mer_format(self):
        p = CC.parse_serial("3401-151906516-151907446-VCU-044-MER-ID-1-486-01012011-31122011-1")
        self.assertEqual(p["units"], 931)

    def test_tz1_format(self):
        p = CC.parse_serial("793-36303349-36306753-VCU-001-TZ1-CN-11-439-18072008-19042009-0")
        self.assertEqual((p["vintage_start"], p["vintage_end"]), ("2008-07-18", "2009-04-19"))

    def test_corsia_flag_one(self):
        self.assertIsNotNone(CC.parse_serial("9380-92545283-92645182-VCS-VCU-263-VER-ID-14-674-01072014-31122014-1"))

    def test_leap_day(self):
        self.assertIsNotNone(CC.parse_serial("8367-10851650-10851650-VCS-VCU-1423-VER-IN-1-1418-29022020-29022020-0"))

    def test_non_leap_feb_29(self):
        self.assertIsNone(CC.parse_serial("8367-10851650-10851650-VCS-VCU-1423-VER-IN-1-1418-29022019-31122019-0"))

    def test_same_day_vintage(self):
        self.assertIsNotNone(CC.parse_serial("8367-1-1-VCS-VCU-1423-VER-IN-1-1418-01012020-01012020-0"))

    def test_epoch_days(self):
        p = CC.parse_serial(S1000)
        self.assertEqual(p["vs_day"] * 86400, F.ep(2009, 1, 1))
        self.assertEqual(p["ve_day"] * 86400, F.ep(2009, 12, 31))

    def test_iso_roundtrip(self):
        for e in (0, 951782400, F.ep(2009, 12, 31), F.ep(2024, 2, 29) + 3661, 4102444799):
            self.assertEqual(CC.iso_epoch(CC.iso_of(e)), e)


# ------------------------------------------------------------------ overlap math

class TestOverlapMath(unittest.TestCase):
    def test_identical(self):
        self.assertTrue(CC.overlaps(10, 20, 10, 20))

    def test_contained(self):
        self.assertTrue(CC.overlaps(10, 20, 12, 15))

    def test_containing(self):
        self.assertTrue(CC.overlaps(12, 15, 10, 20))

    def test_left_partial(self):
        self.assertTrue(CC.overlaps(5, 10, 10, 20))

    def test_right_partial(self):
        self.assertTrue(CC.overlaps(20, 30, 10, 20))

    def test_touching_left_is_not_overlap(self):
        self.assertFalse(CC.overlaps(1, 9, 10, 20))

    def test_touching_right_is_not_overlap(self):
        self.assertFalse(CC.overlaps(21, 30, 10, 20))

    def test_disjoint(self):
        self.assertFalse(CC.overlaps(1, 5, 10, 20))

    def test_single_units_same(self):
        self.assertTrue(CC.overlaps(7, 7, 7, 7))

    def test_single_units_adjacent(self):
        self.assertFalse(CC.overlaps(7, 7, 8, 8))

    def test_symmetry(self):
        for a in ((1, 5), (5, 9), (3, 3), (10, 12)):
            for b in ((4, 6), (6, 8), (1, 2), (12, 20)):
                self.assertEqual(CC.overlaps(a[0], a[1], b[0], b[1]), CC.overlaps(b[0], b[1], a[0], a[1]))

    def test_real_apx_ver_collision_is_numeric_overlap(self):
        a = CC.parse_serial("8842-48565492-48567831-VCS-VCU-279-VER-TR-1-535-01012014-31122014-0")
        b = CC.parse_serial("1104-48565711-48569710-VCU-010-APX-CN-1-476-01022008-17022009-0")
        self.assertTrue(CC.overlaps(a["start"], a["end"], b["start"], b["end"]))
        self.assertNotEqual(a["project"], b["project"])


# ------------------------------------------------------------------ ABI decoding

class TestRealAbi(unittest.TestCase):
    """The contract's decoder reads the exact bytes Polygon returned."""

    def test_real_nft_decodes(self):
        n = 0
        for r in REAL["batches"]:
            if not r.get("nft"):
                continue
            d = CC.decode_nft(r["nft"])
            self.assertEqual(d["serial"], r["serial"])
            self.assertEqual(d["quantity"], int(r["quantity"]))
            self.assertEqual(d["status"], r["status"])
            self.assertEqual(d["pv_id"], int(r["pvId"]))
            n += 1
        self.assertGreater(n, 10)

    def test_real_attributes_decode(self):
        n = 0
        for r in REAL["batches"]:
            if not r.get("attrs") or not r.get("attrs_decoded"):
                continue
            a = CC.decode_attributes(r["attrs"])
            self.assertEqual(a["project_id"], r["attrs_decoded"]["projectId"])
            self.assertEqual(a["start"], r["attrs_decoded"]["startTime"])
            self.assertEqual(a["end"], r["attrs_decoded"]["endTime"])
            n += 1
        self.assertGreater(n, 10)

    def test_fixture_encoder_matches_decoder(self):
        h = F.enc_attributes("VCS-191", "2009", 1, 2)
        a = CC.decode_attributes(h)
        self.assertEqual((a["project_id"], a["vintage_name"], a["start"], a["end"]), ("VCS-191", "2009", 1, 2))

    def test_truncated_nft_fails(self):
        with self.assertRaises(CC.ReadFailed):
            CC.decode_nft(F.enc_nft(1, S1000, 5000, 2)[:200])

    def test_bad_hex_fails(self):
        with self.assertRaises(CC.ReadFailed):
            CC.decode_nft("0xzz")

    def test_huge_string_length_fails(self):
        h = "0x" + F.w(1) + F.w(160) + F.w(5) + F.w(2) + F.w(160) + F.w(10 ** 9)
        with self.assertRaises(CC.ReadFailed):
            CC.decode_nft(h)


# ------------------------------------------------------------------ the door

class TestDoor(Base):
    def test_wrong_contract_refused(self):
        self.refused("NOT_TOUCAN_BATCH_CONTRACT", contract=F.addr(1))

    def test_tco2_address_as_contract_refused(self):
        self.refused("NOT_TOUCAN_BATCH_CONTRACT", contract=F.tco2_of(2000))

    def test_factory_as_contract_refused(self):
        self.refused("NOT_TOUCAN_BATCH_CONTRACT", contract=F.FACTORY)

    def test_checksummed_official_accepted(self):
        self.verdict("MATCHED", contract="0x8A4d7458dDe3023A3B24225D62087701A88b09DD")

    def test_padded_official_accepted(self):
        self.verdict("MATCHED", contract="  0x8a4d7458dde3023a3b24225d62087701a88b09dd ")

    def test_contract_without_0x_refused(self):
        self.refused("NOT_TOUCAN_BATCH_CONTRACT", contract=BATCHES[2:])

    def test_contract_not_string_refused(self):
        self.refused("NOT_TOUCAN_BATCH_CONTRACT", contract=12345)

    def test_token_zero_refused(self):
        self.refused("BAD_TOKEN_ID", token_id=0)

    def test_token_negative_refused(self):
        self.refused("BAD_TOKEN_ID", token_id=-5)

    def test_token_huge_refused(self):
        self.refused("BAD_TOKEN_ID", token_id=10 ** 12)

    def test_token_text_refused(self):
        self.refused("BAD_TOKEN_ID", token_id="abc")

    def test_token_float_refused(self):
        self.refused("BAD_TOKEN_ID", token_id=1000.5)

    def test_token_digit_string_accepted(self):
        self.verdict("MATCHED", token_id="1000")

    def test_token_hex_string_refused(self):
        self.refused("BAD_TOKEN_ID", token_id="0x3e8")

    def test_block_float_refused(self):
        self.refused("BAD_BLOCK", block=float(BLOCK))

    def test_token_bool_refused(self):
        self.refused("BAD_TOKEN_ID", token_id=True)

    def test_block_too_old_refused(self):
        self.refused("BAD_BLOCK", block=18_999_999)

    def test_block_huge_refused(self):
        self.refused("BAD_BLOCK", block=10 ** 10)

    def test_block_text_refused(self):
        self.refused("BAD_BLOCK", block="latest")

    def test_block_bool_refused(self):
        self.refused("BAD_BLOCK", block=False)

    def test_duplicate_refused(self):
        self.file()
        self.refused("DUPLICATE_OF_1")

    def test_duplicate_from_other_sender_refused(self):
        self.file()
        self.refused("DUPLICATE_OF_1", sender=FILER2)

    def test_same_batch_new_block_allowed(self):
        self.file()
        self.verdict("MATCHED", block=BLOCK + 1)

    def test_duplicate_after_unverifiable_refused(self):
        stub.WEB.down.add(F.RPC_A)
        self.verdict("UNVERIFIABLE", "RPC_UNAVAILABLE")
        stub.WEB.down.clear()
        self.refused("DUPLICATE_OF_1")

    def test_refusal_stores_nothing(self):
        before = self.stats()
        self.refused("NOT_TOUCAN_BATCH_CONTRACT", contract=F.addr(1))
        self.assertEqual(self.stats(), before)
        self.assertEqual(stub.WEB.log, [])

    def test_no_clock_refused(self):
        self.w.now_iso = ""
        self.refused("NO_CLOCK")


class TestRateLimit(Base):
    def setUp(self):
        self.w, self.cc, self.gate = F.deploy(rate_max=2, rate_window=600)
        F.real_batch()

    def test_third_filing_refused(self):
        self.file(block=BLOCK)
        self.file(block=BLOCK + 1)
        msg = self.refused("RATE_LIMITED_UNTIL_", block=BLOCK + 2)
        self.assertTrue(msg.endswith(str(F.NOW + 600)))

    def test_other_sender_unaffected(self):
        self.file(block=BLOCK)
        self.file(block=BLOCK + 1)
        self.verdict("MATCHED", block=BLOCK + 2, sender=FILER2)

    def test_window_resets(self):
        self.file(block=BLOCK)
        self.file(block=BLOCK + 1)
        self.w.advance(600)
        self.verdict("MATCHED", block=BLOCK + 2)

    def test_refusal_does_not_count(self):
        self.file(block=BLOCK)
        self.refused("NOT_TOUCAN", contract=F.addr(3))
        self.verdict("MATCHED", block=BLOCK + 1)

    def test_rate_status_view(self):
        self.file(block=BLOCK)
        r = self.w.view(self.cc, "rate_status", FILER)
        self.assertEqual((r["used"], r["max"], r["window"]), (1, 2, 600))

    def test_undetermined_round_does_not_count(self):
        stub.FORGE["mutate"] = lambda r: dict(r, verdict="MISMATCH")
        with self.assertRaises(world.Reverted):
            self.file(block=BLOCK)
        stub.FORGE["mutate"] = None
        self.assertEqual(self.w.view(self.cc, "rate_status", FILER)["used"], 0)

    def test_bad_constructor_limits(self):
        for args in (("CANONICAL", 0, 600), ("CANONICAL", 101, 600), ("CANONICAL", 5, 59), ("X", 5, 600)):
            with self.assertRaises(stub._UserError):
                self.w.deploy("CarbonCheck", *args)


# ------------------------------------------------------------------ the chain

class TestChain(Base):
    def test_matched_records_everything(self):
        r = self.verdict("MATCHED", "ALL_FIELDS_MATCH")
        c = self.check(r["check_id"])
        self.assertEqual(c["serial"], S1000)
        self.assertEqual((c["unit_start"], c["unit_end"], c["units"]), (382273659, 382278658, 5000))
        self.assertEqual(c["quantity"], "5000")
        self.assertEqual(c["batch_status"], "Confirmed")
        self.assertEqual(c["owner"], c["tco2"])
        self.assertEqual(c["project_id"], "VCS-191")
        self.assertEqual((c["vintage_start"], c["vintage_end"]), ("2009-01-01", "2009-12-31"))
        self.assertEqual(c["block"], BLOCK)
        self.assertEqual(c["block_time"], F.BLOCK_TS)
        self.assertTrue(c["block_hash"].startswith("0x"))
        self.assertEqual(c["as_of"], F.NOW_ISO)
        self.assertEqual(c["verra"]["status"], "RETIRED")
        self.assertEqual(c["verra"]["source"], "retirements")
        self.assertTrue(c["batch_url"].endswith("?a=1000"))

    def test_rpc_a_down(self):
        stub.WEB.down.add(F.RPC_A)
        self.verdict("UNVERIFIABLE", "RPC_UNAVAILABLE")

    def test_rpc_b_down(self):
        stub.WEB.down.add(F.RPC_B)
        self.verdict("UNVERIFIABLE", "RPC_UNAVAILABLE")

    def test_rpc_http_500(self):
        stub.WEB.rpc_status[F.RPC_B] = 500
        self.verdict("UNVERIFIABLE", "RPC_UNAVAILABLE")

    def test_rpc_429(self):
        stub.WEB.rpc_status[F.RPC_A] = 429
        self.verdict("UNVERIFIABLE", "RPC_UNAVAILABLE")

    def test_rpc_wrong_chain(self):
        stub.WEB.chains[F.RPC_B].chain_id = 1
        self.verdict("UNVERIFIABLE", "RPC_UNAVAILABLE")

    def test_rpc_error_answer(self):
        stub.WEB.chains[F.RPC_A].fail = lambda m, p: {"code": -32000, "message": "header not found"} if m == "eth_call" else None
        self.verdict("UNVERIFIABLE", "RPC_UNAVAILABLE")

    def test_block_not_finalized_on_one(self):
        stub.WEB.chains[F.RPC_B].finalized = BLOCK - 1
        stub.WEB.chains[F.RPC_B].set_block(BLOCK - 1, F.NOW - 99)
        self.verdict("UNVERIFIABLE", "BLOCK_NOT_FINALIZED")

    def test_block_after_finalized(self):
        self.verdict("UNVERIFIABLE", "BLOCK_NOT_FINALIZED", block=F.FIN + 1)

    def test_rpc_disagree_on_serial(self):
        F.set_batch(1000, S1000.replace("382278658", "382278659"), 5000, urls=[F.RPC_B])
        r = self.verdict("UNVERIFIABLE", "RPC_DISAGREE")
        self.assertIn("nft", r["why"])

    def test_rpc_disagree_on_owner(self):
        F.set_batch(1000, S1000, 5000, owner=F.addr(9), urls=[F.RPC_A])
        r = self.verdict("UNVERIFIABLE", "RPC_DISAGREE")
        self.assertIn("owner", r["why"])

    def test_rpc_disagree_on_attributes(self):
        F.set_batch(1000, S1000, 5000, project="VCS-192", urls=[F.RPC_B])
        r = self.verdict("UNVERIFIABLE", "RPC_DISAGREE")
        self.assertIn("attrs", r["why"])

    def test_rpc_disagree_on_block_hash(self):
        stub.WEB.chains[F.RPC_B].blocks[BLOCK] = ("0x" + "ab" * 32, F.BLOCK_TS)
        r = self.verdict("UNVERIFIABLE", "RPC_DISAGREE")
        self.assertIn("hash", r["why"])

    def test_rpc_disagree_on_tco2(self):
        info = F.set_batch(1000, S1000, 5000)
        stub.WEB.chains[F.RPC_A].calls[(F.FACTORY, CC.SEL_PV_TO_ERC20 + F.w(info["pv"]))] = F.enc_addr(F.addr(77))
        self.verdict("UNVERIFIABLE", "RPC_DISAGREE")

    def test_state_read_at_pinned_block(self):
        F.set_batch(1000, S1000, 4999, block=BLOCK + 5)
        self.verdict("MATCHED", block=BLOCK)
        self.verdict("MISMATCH", "QUANTITY_MISMATCH", block=BLOCK + 5)

    def test_batch_not_found(self):
        self.verdict("UNVERIFIABLE", "BATCH_NOT_FOUND", token_id=2000)

    def test_owner_reverts_is_not_found(self):
        F.set_batch(5, S1000, 5000, owner="REVERT")
        self.verdict("UNVERIFIABLE", "BATCH_NOT_FOUND", token_id=5)

    def test_pending(self):
        F.set_batch(6, "", 0, status=0, pv=0)
        self.verdict("UNVERIFIABLE", "BATCH_NOT_CONFIRMED", token_id=6)

    def test_rejected(self):
        F.set_batch(7, S1000, 5000, status=1)
        r = self.verdict("UNVERIFIABLE", "BATCH_NOT_CONFIRMED", token_id=7)
        self.assertIn("Rejected", r["why"])

    def test_detokenization_requested(self):
        F.set_batch(8, S1000, 5000, status=3)
        self.verdict("UNVERIFIABLE", "BATCH_NOT_CONFIRMED", token_id=8)

    def test_detokenized(self):
        F.set_batch(9, S1000, 5000, status=4)
        self.verdict("UNVERIFIABLE", "BATCH_NOT_CONFIRMED", token_id=9)

    def test_retirement_requested(self):
        F.set_batch(10, S1000, 5000, status=5)
        self.verdict("UNVERIFIABLE", "BATCH_NOT_CONFIRMED", token_id=10)

    def test_retirement_finalized(self):
        F.set_batch(11, S1000, 5000, status=6)
        self.verdict("UNVERIFIABLE", "BATCH_NOT_CONFIRMED", token_id=11)

    def test_unknown_status(self):
        F.set_batch(12, S1000, 5000, status=9)
        r = self.verdict("UNVERIFIABLE", "BATCH_NOT_CONFIRMED", token_id=12)
        self.assertIn("status 9", r["why"])

    def test_confirmed_not_fractionalized(self):
        F.set_batch(13, S1000, 5000, owner=F.addr(13))
        self.verdict("UNVERIFIABLE", "BATCH_NOT_FRACTIONALIZED", token_id=13)

    def test_held_by_other_tco2_not_fractionalized(self):
        F.set_batch(14, S1000, 5000, owner=F.tco2_of(999))
        self.verdict("UNVERIFIABLE", "BATCH_NOT_FRACTIONALIZED", token_id=14)

    def test_no_tco2_for_vintage(self):
        F.set_batch(15, S1000, 5000, tco2="0x" + "0" * 40)
        self.verdict("UNVERIFIABLE", "TCO2_NOT_FOUND", token_id=15)

    def test_tco2_attributes_revert(self):
        F.set_batch(16, S1000, 5000, attrs=False)
        self.verdict("UNVERIFIABLE", "TCO2_UNREADABLE", token_id=16)

    def test_tco2_attributes_garbage(self):
        info = F.set_batch(17, S1000, 5000)
        for u in CC.RPCS:
            stub.WEB.chains[u].calls[(info["tco2"].lower(), CC.SEL_ATTRIBUTES)] = "0x" + F.w(64)
        self.verdict("UNVERIFIABLE", "TCO2_UNREADABLE", token_id=17)

    def test_puro_project_not_vcs(self):
        F.set_batch(18, "643002406801000010000000192331-643002406801000010000000192335", 5, project="PURO-12345")
        self.verdict("UNVERIFIABLE", "NOT_A_VERRA_CREDIT", token_id=18)

    def test_unparsable_serial(self):
        F.set_batch(19, MALFORMED["comma_list"], 100000)
        self.verdict("UNVERIFIABLE", "SERIAL_UNPARSABLE", token_id=19)

    def test_empty_serial_confirmed(self):
        F.set_batch(20, "", 0)
        self.verdict("UNVERIFIABLE", "SERIAL_UNPARSABLE", token_id=20)

    def test_unverifiable_never_reaches_verra(self):
        F.set_batch(21, S1000, 5000, status=1)
        self.file(token_id=21)
        self.assertEqual(F.verra().log, [])


# ------------------------------------------------------------------ rule 3

class TestSerialAgainstTco2(Base):
    def test_project_mismatch(self):
        F.set_batch(30, S1000, 5000, project="VCS-192")
        r = self.verdict("MISMATCH", "SERIAL_PROJECT_MISMATCH", token_id=30)
        self.assertIn("VCS-191", r["why"])

    def test_project_prefix_trick(self):
        F.set_batch(31, S1000, 5000, project="VCS-1910")
        self.verdict("MISMATCH", "SERIAL_PROJECT_MISMATCH", token_id=31)

    def test_project_leading_zero_in_tco2(self):
        F.set_batch(32, S1000, 5000, project="VCS-0191")
        self.verdict("MISMATCH", "SERIAL_PROJECT_MISMATCH", token_id=32)

    def test_vintage_start_mismatch(self):
        F.set_batch(33, S1000, 5000, vintage=(F.ep(2009, 1, 2), F.ep(2009, 12, 31)))
        self.verdict("MISMATCH", "SERIAL_VINTAGE_MISMATCH", token_id=33)

    def test_vintage_end_mismatch(self):
        F.set_batch(34, S1000, 5000, vintage=(F.ep(2009, 1, 1), F.ep(2010, 12, 31)))
        self.verdict("MISMATCH", "SERIAL_VINTAGE_MISMATCH", token_id=34)

    def test_vintage_year_mismatch(self):
        F.set_batch(35, S1000, 5000, vintage=(F.ep(2010, 1, 1), F.ep(2010, 12, 31)))
        self.verdict("MISMATCH", "SERIAL_VINTAGE_MISMATCH", token_id=35)

    def test_vintage_end_of_day_same_date_matches(self):
        F.set_batch(36, S1000, 5000, vintage=(F.ep(2009, 1, 1), F.ep(2009, 12, 31) + 86399))
        self.verdict("MATCHED", token_id=36)

    def test_vintage_next_midnight_mismatch(self):
        F.set_batch(37, S1000, 5000, vintage=(F.ep(2009, 1, 1), F.ep(2009, 12, 31) + 86400))
        self.verdict("MISMATCH", "SERIAL_VINTAGE_MISMATCH", token_id=37)

    def test_quantity_one_more(self):
        F.set_batch(38, S1000, 5001)
        r = self.verdict("MISMATCH", "QUANTITY_MISMATCH", token_id=38)
        self.assertIn("5000 units", r["why"])

    def test_quantity_one_less(self):
        F.set_batch(39, S1000, 4999)
        self.verdict("MISMATCH", "QUANTITY_MISMATCH", token_id=39)

    def test_quantity_end_minus_start_trap(self):
        s = F.serial_for(100, 200)
        self.batch(40, s, 100)
        self.verdict("MISMATCH", "QUANTITY_MISMATCH", token_id=40)

    def test_quantity_inclusive_exact(self):
        s = F.serial_for(100, 200)
        self.batch(41, s, 101)
        self.verdict("MATCHED", token_id=41)

    def test_quantity_zero(self):
        F.set_batch(42, S1000, 0)
        self.verdict("MISMATCH", "QUANTITY_MISMATCH", token_id=42)

    def test_mismatch_does_not_reach_verra(self):
        F.set_batch(43, S1000, 4999)
        self.file(token_id=43)
        self.assertEqual(F.verra().log, [])


# ------------------------------------------------------------------ rule 4

class TestVerra(Base):
    def test_not_found(self):
        self.batch(50, F.serial_for(1, 10), 10, retire=False)
        r = self.verdict("UNVERIFIABLE", "VERRA_NOT_FOUND", token_id=50)
        self.assertEqual(F.verra().log, ["retirements", "holdings"] * 2)
        self.assertEqual(self.check(r["check_id"])["verra"]["found"], False)

    def test_active_in_holdings_is_status_mismatch(self):
        s = F.serial_for(1, 10)
        self.batch(51, s, 10, retire=False)
        F.hold(s, 10, 191, 2009)
        r = self.verdict("MISMATCH", "VERRA_STATUS_MISMATCH", token_id=51)
        c = self.check(r["check_id"])
        self.assertEqual((c["verra"]["source"], c["verra"]["status"]), ("holdings", "ACTIVE"))

    def test_status_cancelled(self):
        s = F.serial_for(1, 10)
        self.batch(52, s, 10, retire=False)
        F.retire(s, 10, 191, 2009, state="CANCELLED")
        self.verdict("MISMATCH", "VERRA_STATUS_MISMATCH", token_id=52)

    def test_status_lowercase_retired_is_mismatch(self):
        s = F.serial_for(1, 10)
        self.batch(53, s, 10, retire=False)
        F.retire(s, 10, 191, 2009, state="Retired")
        self.verdict("MISMATCH", "VERRA_STATUS_MISMATCH", token_id=53)

    def test_status_empty(self):
        s = F.serial_for(1, 10)
        self.batch(54, s, 10, retire=False)
        F.retire(s, 10, 191, 2009, state="")
        self.verdict("MISMATCH", "VERRA_STATUS_MISMATCH", token_id=54)

    def test_quantity_off_by_one_up(self):
        s = F.serial_for(1, 10)
        self.batch(55, s, 10, retire=False)
        F.retire(s, 11, 191, 2009)
        self.verdict("MISMATCH", "VERRA_QUANTITY_MISMATCH", token_id=55)

    def test_quantity_off_by_one_down(self):
        s = F.serial_for(1, 10)
        self.batch(56, s, 10, retire=False)
        F.retire(s, 9, 191, 2009)
        self.verdict("MISMATCH", "VERRA_QUANTITY_MISMATCH", token_id=56)

    def test_quantity_fractional(self):
        s = F.serial_for(1, 10)
        self.batch(57, s, 10, retire=False)
        F.retire(s, 10, 191, 2009)
        F.verra().retired[s][0]["holdingQuantity"] = 10.5
        self.verdict("MISMATCH", "VERRA_QUANTITY_MISMATCH", token_id=57)

    def test_quantity_string(self):
        s = F.serial_for(1, 10)
        self.batch(58, s, 10, retire=False)
        F.retire(s, 10, 191, 2009)
        F.verra().retired[s][0]["holdingQuantity"] = "10"
        self.verdict("MISMATCH", "VERRA_QUANTITY_MISMATCH", token_id=58)

    def test_project_mismatch(self):
        s = F.serial_for(1, 10)
        self.batch(59, s, 10, retire=False)
        F.retire(s, 10, 192, 2009)
        self.verdict("MISMATCH", "VERRA_PROJECT_MISMATCH", token_id=59)

    def test_vintage_mismatch(self):
        s = F.serial_for(1, 10)
        self.batch(60, s, 10, retire=False)
        F.retire(s, 10, 191, 2010)
        self.verdict("MISMATCH", "VERRA_VINTAGE_MISMATCH", token_id=60)

    def test_all_fields_differ_lists_all(self):
        s = F.serial_for(1, 10)
        self.batch(61, s, 10, retire=False)
        F.retire(s, 12, 192, 2010, state="CANCELLED")
        r = self.verdict("MISMATCH", "VERRA_STATUS_MISMATCH", token_id=61)
        for word in ("status", "units", "project", "vintage"):
            self.assertIn(word, r["why"])

    def test_two_records_ambiguous(self):
        s = F.serial_for(1, 10)
        self.batch(62, s, 10)
        F.retire(s, 10, 191, 2009)
        self.verdict("UNVERIFIABLE", "VERRA_AMBIGUOUS", token_id=62)

    def test_near_serial_ignored(self):
        s = F.serial_for(1, 10)
        self.batch(63, s, 10, retire=False)
        F.verra().retired[s] = [F.entity(s + "1", 10, 191, 2009)]
        self.verdict("UNVERIFIABLE", "VERRA_NOT_FOUND", token_id=63)

    def test_http_500(self):
        F.verra().status["retirements"] = 500
        self.verdict("UNVERIFIABLE", "VERRA_UNAVAILABLE")

    def test_holdings_http_500_after_not_retired(self):
        self.batch(64, F.serial_for(1, 10), 10, retire=False)
        F.verra().status["holdings"] = 503
        self.verdict("UNVERIFIABLE", "VERRA_UNAVAILABLE", token_id=64)

    def test_not_json(self):
        F.verra().raw["retirements"] = "<html>maintenance</html>"
        self.verdict("UNVERIFIABLE", "VERRA_UNREADABLE")

    def test_no_entities(self):
        F.verra().raw["retirements"] = json.dumps({"errorCode": 500, "messages": ["Please contact support team"]})
        self.verdict("UNVERIFIABLE", "VERRA_UNREADABLE")

    def test_transport_down(self):
        stub.WEB.down.add(CC.VERRA_SEARCH)
        self.verdict("UNVERIFIABLE", "VERRA_UNAVAILABLE")

    def test_headers_sent(self):
        self.file()
        h = F.verra().headers[0]
        self.assertEqual(h["registry"], "VERRA")
        self.assertEqual(h["standardAcronym"], "VCS")

    def test_remark_recorded_not_decisive(self):
        s = F.serial_for(1, 10)
        self.batch(65, s, 10, retire=False)
        F.retire(s, 10, 191, 2009, remark="NOT TOUCAN - sold to someone else - batch 999")
        r = self.verdict("MATCHED", token_id=65)
        self.assertIn("NOT TOUCAN", self.check(r["check_id"])["verra"]["remark"])

    def test_remark_missing_still_matched(self):
        s = F.serial_for(1, 10)
        self.batch(66, s, 10, retire=False)
        F.retire(s, 10, 191, 2009, remark=None)
        self.verdict("MATCHED", token_id=66)

    def test_remark_truncated(self):
        s = F.serial_for(1, 10)
        self.batch(67, s, 10, retire=False)
        F.retire(s, 10, 191, 2009, remark="x" * 5000)
        r = self.file(token_id=67)
        self.assertEqual(len(self.check(r["check_id"])["verra"]["remark"]), 240)

    def test_retired_found_skips_holdings(self):
        self.file()
        self.assertEqual(F.verra().log, ["retirements"] * 2)

    def two_year(self, token_id, verra_vintage):
        s = "8367-10851650-10851650-VCS-VCU-1423-VER-IN-1-1418-01032012-28022013-0"
        F.set_batch(token_id, s, 1, project="VCS-1418", vintage=(F.ep(2012, 3, 1), F.ep(2013, 2, 28)))
        F.retire(s, 1, 1418, verra_vintage)
        return s

    def test_verra_two_year_vintage_format(self):
        self.two_year(68, "2012 - 2013")
        self.verdict("MATCHED", token_id=68)

    def test_verra_two_year_vintage_start_year_only_is_mismatch(self):
        self.two_year(69, "2012")
        self.verdict("MISMATCH", "VERRA_VINTAGE_MISMATCH", token_id=69)

    def test_verra_two_year_vintage_without_spaces_is_mismatch(self):
        self.two_year(70, "2012-2013")
        self.verdict("MISMATCH", "VERRA_VINTAGE_MISMATCH", token_id=70)

    def test_verra_one_year_vintage_with_range_is_mismatch(self):
        s = F.serial_for(1, 10)
        self.batch(71, s, 10, retire=False)
        F.retire(s, 10, 191, "2009 - 2009")
        self.verdict("MISMATCH", "VERRA_VINTAGE_MISMATCH", token_id=71)

    def test_verra_vintage_format_on_real_serials(self):
        self.assertEqual(CC.parse_serial("1104-48565711-48569710-VCU-010-APX-CN-1-476-01022008-17022009-0")["verra_vintage"], "2008 - 2009")
        self.assertEqual(CC.parse_serial(S1000)["verra_vintage"], "2009")


# ------------------------------------------------------------------ rule 5

class TestDoubleClaim(Base):
    def setUp(self):
        super().setUp()
        self.verdict("MATCHED")

    def test_same_range_other_batch(self):
        F.set_batch(70, S1000, 5000)
        r = self.verdict("DOUBLE_CLAIMED", "RANGE_ALREADY_CLAIMED", token_id=70)
        c = self.check(r["check_id"])
        self.assertEqual((c["conflict_batch"], c["conflict_check"]), (1000, 1))

    def test_partial_overlap(self):
        s = F.serial_for(382278000, 382279000)
        self.batch(71, s, 1001)
        self.verdict("DOUBLE_CLAIMED", token_id=71)

    def test_contained_range(self):
        s = F.serial_for(382275000, 382275009)
        self.batch(72, s, 10)
        self.verdict("DOUBLE_CLAIMED", token_id=72)

    def test_touching_after_is_matched(self):
        s = F.serial_for(382278659, 382278700)
        self.batch(73, s, 42)
        self.verdict("MATCHED", token_id=73)

    def test_touching_before_is_matched(self):
        s = F.serial_for(382273600, 382273658)
        self.batch(74, s, 59)
        self.verdict("MATCHED", token_id=74)

    def test_one_unit_overlap(self):
        s = F.serial_for(382278658, 382278700)
        self.batch(75, s, 43)
        self.verdict("DOUBLE_CLAIMED", token_id=75)

    def test_other_project_same_numbers_is_matched(self):
        s = F.serial_for(382273659, 382278658, project=535)
        self.batch(76, s, 5000, project=535)
        self.verdict("MATCHED", token_id=76)

    def test_split_evasion_both_halves_caught(self):
        a = F.serial_for(382273659, 382276000)
        b = F.serial_for(382276001, 382278658)
        self.batch(77, a, 2342)
        self.batch(78, b, 2658)
        self.verdict("DOUBLE_CLAIMED", token_id=77)
        self.verdict("DOUBLE_CLAIMED", token_id=78)

    def test_recheck_of_same_batch_not_double(self):
        r = self.w.call(self.cc, "recheck", 1, BLOCK + 1, sender=FILER2)
        self.assertEqual(r["verdict"], "MATCHED")

    def test_double_claimed_range_not_indexed(self):
        F.set_batch(79, S1000, 5000)
        self.verdict("DOUBLE_CLAIMED", token_id=79)
        self.assertEqual(self.w.view(self.cc, "list_claimed", 1, 10)["total"], 1)

    def test_first_matched_wins_regardless_of_batch_number(self):
        s = F.serial_for(382273659, 382273700)
        self.batch(5, s, 42)
        self.verdict("DOUBLE_CLAIMED", token_id=5)

    def test_mismatch_range_not_indexed(self):
        s = F.serial_for(10, 20)
        F.set_batch(80, s, 99)
        self.verdict("MISMATCH", token_id=80)
        self.batch(81, s, 11)
        self.verdict("MATCHED", token_id=81)

    def test_unverifiable_range_not_indexed(self):
        s = F.serial_for(10, 20)
        self.batch(82, s, 11, retire=False)
        self.verdict("UNVERIFIABLE", token_id=82)
        self.batch(83, s, 11)
        self.verdict("MATCHED", token_id=83)

    def test_counters(self):
        F.set_batch(84, S1000, 5000)
        self.file(token_id=84)
        st = self.stats()
        self.assertEqual((st["matched"], st["double_claimed"], st["checks"]), (1, 1, 2))

    def test_claimed_view(self):
        r = self.w.view(self.cc, "list_claimed", 1, 10)["ranges"][0]
        self.assertEqual((r["project"], r["unit_start"], r["unit_end"], r["batch_id"]), (191, 382273659, 382278658, 1000))

    def test_demo_range_refused_on_canonical(self):
        with self.assertRaises(world.Reverted) as cm:
            self.w.call(self.cc, "demo_claim_range", 191, 1, 5, "x" * 5, sender=FILER)
        self.assertEqual(cm.exception.msg, "REFUSED: DEMO_ONLY")


class TestDemoRange(Base):
    demo = True

    def test_demo_range_then_double(self):
        self.w.call(self.cc, "demo_claim_range", 191, 382278000, 382290000, "other registry", sender=FILER)
        r = self.verdict("DOUBLE_CLAIMED")
        self.assertIn("DEMO range 'other registry'", r["why"])
        self.assertEqual(self.check(r["check_id"])["conflict_batch"], 0)

    def test_demo_range_other_project_no_effect(self):
        self.w.call(self.cc, "demo_claim_range", 192, 382278000, 382290000, "other registry", sender=FILER)
        self.verdict("MATCHED")

    def test_demo_range_bad(self):
        for args in ((191, 0, 5, "abc"), (191, 5, 4, "abc"), (0, 1, 5, "abc"), (191, 1, 5, "ab"), (191, 1, 5, "café!")):
            with self.assertRaises(world.Reverted):
                self.w.call(self.cc, "demo_claim_range", *args, sender=FILER)

    def test_demo_mode_reported(self):
        self.assertEqual(self.stats()["mode"], "DEMO")


# ------------------------------------------------------------------ consensus

class TestConsensus(Base):
    def test_validator_rejects_forged_matched(self):
        F.set_batch(90, S1000, 4999)
        stub.FORGE["mutate"] = lambda r: dict(r, verdict="MATCHED", code="ALL_FIELDS_MATCH")
        with self.assertRaises(world.Reverted) as cm:
            self.file(token_id=90)
        self.assertIn("UNDETERMINED", cm.exception.msg)
        self.assertEqual(self.stats()["checks"], 0)

    def test_validator_rejects_forged_double_claimed(self):
        stub.FORGE["mutate"] = lambda r: dict(r, verdict="DOUBLE_CLAIMED")
        with self.assertRaises(world.Reverted):
            self.file()

    def test_validator_rejects_forged_field(self):
        stub.FORGE["mutate"] = lambda r: dict(r, verra=dict(r["verra"], remark="forged"))
        with self.assertRaises(world.Reverted):
            self.file()

    def test_leader_transport_unverifiable_accepted(self):
        stub.WEB.leader_hook = lambda: stub.WEB.down.add(F.RPC_A)
        stub.WEB.validator_hook = lambda: stub.WEB.down.clear()
        self.verdict("UNVERIFIABLE", "RPC_UNAVAILABLE")

    def test_leader_forges_not_found_rejected(self):
        stub.FORGE["payload"] = CC.unv("verra", "VERRA_NOT_FOUND", "x")
        with self.assertRaises(world.Reverted):
            self.file()

    def test_validator_transport_failure_does_not_confirm(self):
        stub.WEB.validator_hook = lambda: stub.WEB.down.add(CC.VERRA_SEARCH)
        with self.assertRaises(world.Reverted):
            self.file()

    def test_verra_changes_between_leader_and_validator(self):
        def flip():
            F.verra().retired[S1000][0]["stateCode"] = "CANCELLED"
        stub.WEB.validator_hook = flip
        with self.assertRaises(world.Reverted):
            self.file()

    def test_leader_crash_is_internal_unverifiable(self):
        orig = CC.read_chain
        CC.read_chain = lambda t, b: 1 / 0
        try:
            self.verdict("UNVERIFIABLE", "INTERNAL")
        finally:
            CC.read_chain = orig

    def test_non_dict_result_rejected(self):
        stub.FORGE["payload"] = "MATCHED"
        with self.assertRaises(world.Reverted):
            self.file()

    def test_timeout_every_try_unverifiable(self):
        stub.WEB.down.add(CC.VERRA_SEARCH)
        r = self.verdict("UNVERIFIABLE", "VERRA_UNAVAILABLE")
        self.assertEqual(self.check(r["check_id"])["verdict"], "UNVERIFIABLE")
        self.assertEqual(stub.WEB.log.count(CC.VERRA_SEARCH), CC.TRIES)


# ------------------------------------------------------------------ views, recheck

class TestViews(Base):
    def test_get_check_missing(self):
        self.assertEqual(self.check(5), {"found": False, "check_id": 5})
        self.assertEqual(self.check(0)["found"], False)

    def test_list_checks_paging(self):
        for i in range(3):
            self.file(block=BLOCK + i)
        r = self.w.view(self.cc, "list_checks", 2, 5)
        self.assertEqual(r["total"], 3)
        self.assertEqual([c["check_id"] for c in r["checks"]], [2, 3])

    def test_list_checks_cap(self):
        self.assertEqual(self.w.view(self.cc, "list_checks", 1, 1000)["checks"], [])

    def test_latest_verdict_none(self):
        r = self.w.view(self.cc, "latest_verdict", 1000)
        self.assertEqual((r["verdict"], r["check_id"]), ("NONE", 0))

    def test_latest_verdict_after_recheck(self):
        self.file()
        s = S1000
        F.verra().retired[s][0]["stateCode"] = "CANCELLED"
        self.w.advance(HOUR)
        r = self.w.call(self.cc, "recheck", 1, BLOCK + 3, sender=FILER2)
        self.assertEqual(r["verdict"], "MISMATCH")
        lv = self.w.view(self.cc, "latest_verdict", 1000)
        self.assertEqual((lv["verdict"], lv["check_id"], lv["block"]), ("MISMATCH", 2, BLOCK + 3))
        self.assertEqual(lv["counts"], {"MATCHED": 1, "MISMATCH": 1, "DOUBLE_CLAIMED": 0, "UNVERIFIABLE": 0})
        self.assertFalse(self.w.view(self.cc, "is_matched", 1000))

    def test_is_matched(self):
        self.assertFalse(self.w.view(self.cc, "is_matched", 1000))
        self.file()
        self.assertTrue(self.w.view(self.cc, "is_matched", 1000))

    def test_recheck_records_link(self):
        self.file()
        r = self.w.call(self.cc, "recheck", 1, BLOCK + 1, sender=FILER)
        self.assertEqual(self.check(r["check_id"])["recheck_of"], 1)

    def test_recheck_missing(self):
        with self.assertRaises(world.Reverted) as cm:
            self.w.call(self.cc, "recheck", 9, BLOCK + 1, sender=FILER)
        self.assertEqual(cm.exception.msg, "REFUSED: NO_SUCH_CHECK")

    def test_recheck_same_block_duplicate(self):
        self.file()
        with self.assertRaises(world.Reverted) as cm:
            self.w.call(self.cc, "recheck", 1, BLOCK, sender=FILER)
        self.assertEqual(cm.exception.msg, "REFUSED: DUPLICATE_OF_1")

    def test_recheck_is_rate_limited(self):
        self.w, self.cc, self.gate = F.deploy(rate_max=1, rate_window=600)
        F.real_batch()
        self.file()
        with self.assertRaises(world.Reverted) as cm:
            self.w.call(self.cc, "recheck", 1, BLOCK + 1, sender=FILER)
        self.assertTrue(cm.exception.msg.startswith("REFUSED: RATE_LIMITED"))

    def test_stats_counts_each_verdict(self):
        self.file()
        F.set_batch(2, S1000, 1)
        self.file(token_id=2)
        self.file(token_id=2000)
        F.set_batch(3, S1000, 5000)
        self.file(token_id=3)
        st = self.stats()
        self.assertEqual((st["matched"], st["mismatch"], st["unverifiable"], st["double_claimed"], st["checks"]), (1, 1, 1, 1, 4))

    def test_rules_view(self):
        r = self.w.view(self.cc, "get_rules")
        self.assertEqual(r["batch_contract"], BATCHES)
        self.assertEqual(r["model"], "none")
        self.assertEqual(r["chain_id"], 137)
        self.assertEqual(r["verra_retired_status"], "RETIRED")

    def test_as_of_is_fetch_time(self):
        self.w.advance(12345)
        r = self.file()
        self.assertEqual(self.check(r["check_id"])["filed_at"], F.NOW + 12345)

    def test_verdict_is_final_immediately(self):
        r = self.file()
        self.assertEqual(self.check(r["check_id"])["verdict"], "MATCHED")
        self.w.advance(10 * DAY)
        self.assertEqual(self.check(r["check_id"])["verdict"], "MATCHED")


# ------------------------------------------------------------------ OffsetGate

class TestGate(Base):
    def claim(self, batch=1000, note="Scope 1 2026 offset", sender=USER, gate=None):
        return self.w.call(gate or self.gate, "claim_offset", batch, note, sender=sender)

    def gate_refused(self, code, **k):
        with self.assertRaises(world.Reverted) as cm:
            self.claim(**k)
        self.assertTrue(cm.exception.msg.startswith("REFUSED: " + code), cm.exception.msg)

    def test_allow_matched(self):
        self.file()
        r = self.claim()
        self.assertEqual((r["claim_id"], r["batch_id"], r["check_id"], r["age_s"]), (1, 1000, 1, 0))
        c = self.w.view(self.gate, "get_claim", 1)
        self.assertEqual((c["claimant"], c["note"], c["found"]), (USER, "Scope 1 2026 offset", True))

    def test_refuse_no_verdict(self):
        self.gate_refused("NO_VERDICT")

    def test_refuse_mismatch(self):
        F.set_batch(2, S1000, 1)
        self.file(token_id=2)
        self.gate_refused("NOT_MATCHED_MISMATCH", batch=2)

    def test_refuse_unverifiable(self):
        self.file(token_id=2000)
        self.gate_refused("NOT_MATCHED_UNVERIFIABLE", batch=2000)

    def test_refuse_double_claimed(self):
        self.file()
        F.set_batch(3, S1000, 5000)
        self.file(token_id=3)
        self.gate_refused("NOT_MATCHED_DOUBLE_CLAIMED", batch=3)

    def test_refuse_stale(self):
        self.file()
        self.w.advance(30 * DAY + 1)
        self.gate_refused("STALE_VERDICT")

    def test_allow_exactly_max_age(self):
        self.file()
        self.w.advance(30 * DAY - 60)
        self.assertEqual(self.claim()["age_s"], 30 * DAY - 60)

    def test_refuse_one_second_past_block_age(self):
        self.file()
        self.w.advance(30 * DAY - 59)
        self.gate_refused("STALE_BLOCK")

    def test_fresh_filing_of_old_block_is_stale(self):
        self.w.advance(30 * DAY)
        self.file()
        self.gate_refused("STALE_BLOCK")

    def test_old_block_filed_later_cannot_mask_newer(self):
        n = F.new_block(F.NOW)
        F.set_batch(1000, S1000, 5000, status=4, block=n)
        self.verdict("UNVERIFIABLE", "BATCH_NOT_CONFIRMED", block=n)
        self.verdict("MATCHED", block=BLOCK)
        lv = self.w.view(self.cc, "latest_verdict", 1000)
        self.assertEqual((lv["verdict"], lv["block"], lv["check_id"]), ("UNVERIFIABLE", n, 1))
        self.gate_refused("NOT_MATCHED_UNVERIFIABLE")

    def test_stale_then_recheck_allows(self):
        self.file()
        self.w.advance(31 * DAY)
        self.gate_refused("STALE_VERDICT")
        n = F.new_block(self.w.now() - 30)
        self.w.call(self.cc, "recheck", 1, n, sender=FILER)
        self.assertEqual(self.claim()["check_id"], 2)

    def test_latest_mismatch_masks_older_matched(self):
        self.file()
        F.verra().retired[S1000][0]["stateCode"] = "CANCELLED"
        self.w.call(self.cc, "recheck", 1, BLOCK + 1, sender=FILER)
        self.gate_refused("NOT_MATCHED_MISMATCH")

    def test_transport_unverifiable_recheck_does_not_block_gate(self):
        self.file()
        stub.WEB.down.add(F.RPC_A)
        self.w.call(self.cc, "recheck", 1, BLOCK + 1, sender=FILER)
        self.assertEqual(self.claim()["check_id"], 1)

    def test_read_unverifiable_recheck_blocks_gate(self):
        self.file()
        F.set_batch(1000, S1000, 5000, owner=F.addr(77), block=BLOCK + 1)
        self.w.call(self.cc, "recheck", 1, BLOCK + 1, sender=FILER)
        self.gate_refused("NOT_MATCHED_UNVERIFIABLE")

    def test_one_claim_per_batch(self):
        self.file()
        self.claim()
        self.gate_refused("ALREADY_CLAIMED_IN_1", sender=FILER3)

    def test_refusal_stores_nothing(self):
        self.gate_refused("NO_VERDICT")
        self.assertEqual(self.w.view(self.gate, "list_claims", 1, 10)["total"], 0)

    def test_bad_batch_ids(self):
        for b in (0, -1, 10 ** 10, "x", True):
            self.gate_refused("BAD_BATCH_ID", batch=b)

    def test_bad_notes(self):
        self.file()
        for n in ("x" * 141, "café", "line\nbreak"):
            self.gate_refused("BAD_NOTE", note=n)

    def test_check_offset_view(self):
        self.assertFalse(self.w.view(self.gate, "check_offset", 1000)["accept"])
        self.file()
        r = self.w.view(self.gate, "check_offset", 1000)
        self.assertEqual((r["accept"], r["reason"]), (True, "MATCHED_AND_FRESH"))
        self.claim()
        self.assertEqual(self.w.view(self.gate, "check_offset", 1000)["reason"], "ALREADY_CLAIMED_IN_1")

    def test_config(self):
        c = self.w.view(self.gate, "get_config")
        self.assertEqual((c["registry"], c["max_age"]), (self.cc, 30 * DAY))

    def test_bad_max_age(self):
        for a in (59, 86400 * 366):
            with self.assertRaises(stub._UserError):
                self.w.deploy("OffsetGate", self.cc, a)

    def test_decide_pure(self):
        self.assertEqual(OG.decide(None, 100, 10), {"refuse": "REGISTRY_UNREADABLE"})
        self.assertEqual(OG.decide({"verdict": "MATCHED", "filed_at": 200}, 100, 10), {"refuse": "REGISTRY_UNREADABLE"})
        self.assertEqual(OG.decide({"verdict": "MATCHED", "filed_at": "x"}, 100, 10), {"refuse": "REGISTRY_UNREADABLE"})
        self.assertEqual(OG.decide({"verdict": "MATCHED", "filed_at": 0}, 100, 10), {"refuse": "REGISTRY_UNREADABLE"})
        self.assertEqual(OG.decide({"verdict": "MATCHED", "filed_at": 90, "block_time": 90}, 100, 10), {"ok": True})
        self.assertEqual(OG.decide({"verdict": "MATCHED", "filed_at": 89, "block_time": 95}, 100, 10), {"refuse": "STALE_VERDICT"})
        self.assertEqual(OG.decide({"verdict": "MATCHED", "filed_at": 95, "block_time": 89}, 100, 10), {"refuse": "STALE_BLOCK"})
        self.assertEqual(OG.decide({"verdict": "MATCHED", "filed_at": 95}, 100, 10), {"refuse": "REGISTRY_UNREADABLE"})
        self.assertEqual(OG.decide({"verdict": "MATCHED", "filed_at": 95, "block_time": 0}, 100, 10), {"refuse": "STALE_BLOCK"})

    def test_gate_reads_only_its_registry(self):
        other_w, other_cc, _ = self.w, self.w.deploy("CarbonCheck", "CANONICAL", 5, 3600), None
        self.w.call(other_cc, "file_check", BATCHES, 1000, BLOCK, sender=FILER)
        self.gate_refused("NO_VERDICT")

    def test_registry_unreadable(self):
        g = self.w.deploy("OffsetGate", F.addr(4242), 3600)
        with self.assertRaises(world.Reverted) as cm:
            self.w.call(g, "claim_offset", 1000, "n", sender=USER)
        self.assertEqual(cm.exception.msg, "REFUSED: REGISTRY_UNREADABLE")


# ------------------------------------------------------------------ real data

class TestRealRulings(unittest.TestCase):
    """The contract's own decision functions over every real batch read in
    the research (test/feasibility/deep.json) give the rulings documented in
    FEASIBILITY.md."""

    @classmethod
    def setUpClass(cls):
        import subprocess
        import sys
        out = subprocess.run([sys.executable, str(Path(__file__).parent / "feasibility" / "deep_report.py")],
                             capture_output=True, text=True, check=True).stdout
        cls.summary = out.split("\n\n")[0]
        cls.rows = {int(l.split()[0]): (l.split()[1], l.split()[2]) for l in out.split("\n\n")[1].splitlines() if l.strip()}

    def test_counts(self):
        for line in ("MATCHED       ALL_FIELDS_MATCH           802", "MISMATCH      SERIAL_PROJECT_MISMATCH    2",
                     "UNVERIFIABLE  VERRA_NOT_FOUND            5", "UNVERIFIABLE  SERIAL_UNPARSABLE          16",
                     "UNVERIFIABLE  BATCH_NOT_FRACTIONALIZED   6", "UNVERIFIABLE  TCO2_NOT_FOUND             4"):
            self.assertIn(line, self.summary)

    def test_project_mismatches(self):
        self.assertEqual(self.rows[68], ("MISMATCH", "SERIAL_PROJECT_MISMATCH"))
        self.assertEqual(self.rows[180], ("MISMATCH", "SERIAL_PROJECT_MISMATCH"))

    def test_not_found(self):
        for b in (39, 594, 686, 874, 1213):
            self.assertEqual(self.rows[b], ("UNVERIFIABLE", "VERRA_NOT_FOUND"))

    def test_not_fractionalized(self):
        for b in (3, 138, 446, 798, 833, 1001):
            self.assertEqual(self.rows[b], ("UNVERIFIABLE", "BATCH_NOT_FRACTIONALIZED"))

    def test_no_double_claim_among_confirmed_within_a_project(self):
        deep = json.loads((Path(__file__).parent / "feasibility" / "deep.json").read_text())
        rs = []
        for b in deep["batches"].values():
            if b["status"] == 2:
                p = CC.parse_serial(b["serial"])
                if p:
                    rs.append((p["project"], p["start"], p["end"], b["id"]))
        rs.sort()
        hits = []
        for i, a in enumerate(rs):
            for b in rs[i + 1:]:
                if b[0] != a[0] or b[1] > a[2]:
                    break
                hits.append((a[3], b[3]))
        self.assertEqual(hits, [])
        self.assertGreater(len(rs), 800)


# ------------------------------------------------------------------ source

class TestSource(unittest.TestCase):
    def src(self, name):
        return (ROOT / "contracts" / (name + ".py")).read_text()

    def test_header(self):
        for n in ("CarbonCheck", "OffsetGate"):
            lines = self.src(n).splitlines()
            self.assertEqual(lines[0], "# v0.3.0")
            self.assertEqual(lines[1], '# { "Depends": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng" }')

    def test_no_model_calls(self):
        for n in ("CarbonCheck", "OffsetGate"):
            self.assertNotIn("exec_prompt", self.src(n))
            self.assertNotIn("eq_principle", self.src(n))

    def test_ascii_only(self):
        for n in ("CarbonCheck", "OffsetGate"):
            self.assertTrue(all(ord(c) < 128 for c in self.src(n)), n)

    def test_no_undefined_names(self):
        for n in ("CarbonCheck", "OffsetGate"):
            self.assertEqual(stub.undefined_names(ROOT / "contracts" / (n + ".py")), [], n)

    def test_no_setters(self):
        s = self.src("CarbonCheck")
        for bad in ("def set_", "owner: Address", "emit_transfer", "payable"):
            self.assertNotIn(bad, s)

    def test_frozen_addresses_are_toucans(self):
        self.assertEqual(CC.TOUCAN_BATCHES, "0x8a4d7458dde3023a3b24225d62087701a88b09dd")
        self.assertEqual(CC.TOUCAN_TCO2_FACTORY, "0x2359677e513bc83106268514c5b2de3c29c849ea")

    def test_rpcs_distinct_operators(self):
        self.assertEqual(len({u.split("/")[2].split(".")[-2] for u in CC.RPCS}), 2)

    def test_selectors(self):
        self.assertEqual((CC.SEL_NFT_LIST, CC.SEL_OWNER_OF, CC.SEL_PV_TO_ERC20, CC.SEL_ATTRIBUTES),
                         ("0x75bea166", "0x6352211e", "0x5e813d3c", "0x152583de"))


if __name__ == "__main__":
    unittest.main()
