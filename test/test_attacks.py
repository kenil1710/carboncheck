"""The internal attack round (docs/ATTACK_REPORT.md). Each test is one attack;
the assertion is the defence holding.

    cd test && python3 -m unittest -q test_attacks
"""
import json
import re
import unittest
from pathlib import Path

import fixtures as F
import stub
import world
from fixtures import CC, OG, BATCHES, BLOCK, FILER, FILER2, USER, S1000, DAY

ROOT = Path(__file__).resolve().parent.parent


class Base(unittest.TestCase):
    demo = False

    def setUp(self):
        self.w, self.cc, self.gate = F.deploy(demo=self.demo)
        F.real_batch()

    def file(self, token_id=1000, block=BLOCK, contract=BATCHES, sender=FILER):
        return self.w.call(self.cc, "file_check", contract, token_id, block, sender=sender)

    def refused(self, code, **k):
        with self.assertRaises(world.Reverted) as cm:
            self.file(**k)
        self.assertTrue(cm.exception.msg.startswith("REFUSED: " + code), cm.exception.msg)


# ---------------------------------------------------------------- A1 fake batch contracts

class A1FakeBatchContract(Base):
    def test_lookalike_one_nibble_off(self):
        self.refused("NOT_TOUCAN_BATCH_CONTRACT", contract=BATCHES[:-1] + "c")

    def test_zero_address(self):
        self.refused("NOT_TOUCAN_BATCH_CONTRACT", contract="0x" + "0" * 40)

    def test_official_with_null_byte(self):
        self.refused("NOT_TOUCAN_BATCH_CONTRACT", contract=BATCHES + "\x00")

    def test_official_with_cyrillic_a(self):
        self.refused("NOT_TOUCAN_BATCH_CONTRACT", contract=BATCHES.replace("a", "а", 1))

    def test_official_with_fullwidth_digit(self):
        self.refused("NOT_TOUCAN_BATCH_CONTRACT", contract=BATCHES.replace("8", "８", 1))

    def test_official_with_0X_prefix_is_the_same_address(self):
        self.assertEqual(self.file(contract="0X" + BATCHES[2:].upper())["verdict"], "MATCHED")

    def test_list_argument(self):
        self.refused("NOT_TOUCAN_BATCH_CONTRACT", contract=[BATCHES])

    def test_reads_only_frozen_addresses(self):
        """Whatever the filer passes, the RPC calls go to the frozen batch
        contract and the frozen factory, then to the TCO2 the factory names."""
        self.file()
        tos = set()
        for url in CC.RPCS:
            for m, p in stub.WEB.chains[url].log:
                if m == "eth_call":
                    tos.add(json.loads(p)[0]["to"])
        info_tco2 = F.tco2_of(2000).lower()
        self.assertEqual(tos, {BATCHES, F.FACTORY, info_tco2})

    def test_tco2_not_from_factory_ignored(self):
        """A batch held by some contract that answers getAttributes() does not
        count: the TCO2 must be the one the official factory maps the vintage to."""
        rogue = F.addr(666)
        F.set_batch(50, S1000, 5000, owner=rogue)
        for u in CC.RPCS:
            stub.WEB.chains[u].calls[(rogue, CC.SEL_ATTRIBUTES)] = F.enc_attributes("VCS-191", "2009", F.ep(2009, 1, 1), F.ep(2009, 12, 31))
        self.assertEqual(self.file(token_id=50)["code"], "BATCH_NOT_FRACTIONALIZED")


# ---------------------------------------------------------------- A2 serial-format tricks

class A2SerialTricks(Base):
    def via_chain(self, serial, qty=5000):
        F.set_batch(60, serial, qty)
        F.retire(serial, qty, 191, 2009)
        return self.file(token_id=60)

    def test_leading_zero_alias_of_matched_range(self):
        r = self.via_chain("12078-0382273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0")
        self.assertEqual(r["code"], "SERIAL_UNPARSABLE")

    def test_fullwidth_digits(self):
        r = self.via_chain("12078-３８２273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0")
        self.assertEqual(r["code"], "SERIAL_UNPARSABLE")

    def test_escaped_unicode_text_seen_on_chain(self):
        r = self.via_chain("\\u00311015-267732157-267732168-VCS-VCU-279-VER-TR-1-905-01012013-31122013-0", 12)
        self.assertEqual(r["code"], "SERIAL_UNPARSABLE")

    def test_two_serials_joined(self):
        r = self.via_chain(S1000 + "," + S1000)
        self.assertEqual(r["code"], "SERIAL_UNPARSABLE")

    def test_lowercase_letters(self):
        r = self.via_chain(S1000.lower())
        self.assertEqual(r["code"], "SERIAL_UNPARSABLE")

    def test_trailing_space(self):
        r = self.via_chain(S1000 + " ")
        self.assertEqual(r["code"], "SERIAL_UNPARSABLE")

    def test_project_swapped_in_serial(self):
        """Claiming another project's numbers by editing the serial's project
        field fails against the TCO2."""
        r = self.via_chain(S1000.replace("-191-", "-192-"))
        self.assertEqual(r["code"], "SERIAL_PROJECT_MISMATCH")

    def test_verra_record_for_near_serial_does_not_count(self):
        s = F.serial_for(5, 9)
        F.set_batch(61, s, 5)
        F.verra().retired[s] = [F.entity(s.replace("-0", "-1"), 5, 191, 2009)]
        self.assertEqual(self.file(token_id=61)["code"], "VERRA_NOT_FOUND")

    def test_verra_contains_search_superset_ignored(self):
        s = F.serial_for(5, 9)
        F.set_batch(62, s, 5)
        F.verra().retired[s] = [F.entity("1" + s, 5, 191, 2009), F.entity(s + "9", 5, 191, 2009)]
        self.assertEqual(self.file(token_id=62)["code"], "VERRA_NOT_FOUND")


# ---------------------------------------------------------------- A3 overlap evasion

class A3OverlapEvasion(Base):
    def setUp(self):
        super().setUp()
        self.assertEqual(self.file()["verdict"], "MATCHED")

    def test_split_into_many_small_batches(self):
        for i, start in enumerate(range(382273659, 382278658, 1000)):
            s = F.serial_for(start, start + 9)
            F.set_batch(100 + i, s, 10)
            F.retire(s, 10, 191, 2009)
            self.assertEqual(self.file(token_id=100 + i, sender=F.addr(5000 + i))["verdict"], "DOUBLE_CLAIMED")

    def test_other_issuance_id_same_units(self):
        s = F.serial_for(382273659, 382273700, issuance=99999)
        F.set_batch(120, s, 42)
        F.retire(s, 42, 191, 2009)
        self.assertEqual(self.file(token_id=120)["verdict"], "DOUBLE_CLAIMED")

    def test_other_vintage_same_project_same_units(self):
        s = F.serial_for(382273659, 382273700, year=2010)
        F.set_batch(121, s, 42, vintage=(F.ep(2010, 1, 1), F.ep(2010, 12, 31)))
        F.retire(s, 42, 191, 2010)
        self.assertEqual(self.file(token_id=121)["verdict"], "DOUBLE_CLAIMED")

    def test_extend_one_unit_past_end(self):
        s = F.serial_for(382278658, 382278658)
        F.set_batch(122, s, 1)
        F.retire(s, 1, 191, 2009)
        self.assertEqual(self.file(token_id=122)["verdict"], "DOUBLE_CLAIMED")

    def test_first_filer_cannot_be_displaced(self):
        F.set_batch(123, S1000, 5000)
        self.assertEqual(self.file(token_id=123)["verdict"], "DOUBLE_CLAIMED")
        self.assertTrue(self.w.view(self.cc, "is_matched", 1000))

    def test_double_claimed_cannot_index_itself(self):
        F.set_batch(124, S1000, 5000)
        self.file(token_id=124)
        F.set_batch(125, F.serial_for(382273659, 382273659), 1)
        F.retire(F.serial_for(382273659, 382273659), 1, 191, 2009)
        r = self.file(token_id=125)
        self.assertEqual(self.w.view(self.cc, "get_check", r["check_id"])["conflict_batch"], 1000)


# ---------------------------------------------------------------- A4 stale verdicts

class A4Stale(Base):
    def test_old_block_cannot_mask_newer(self):
        n = F.new_block(F.NOW)
        F.set_batch(1000, S1000, 5000, status=4, block=n)
        self.assertEqual(self.file(block=n)["verdict"], "UNVERIFIABLE")
        self.assertEqual(self.file(block=BLOCK)["verdict"], "MATCHED")
        self.assertEqual(self.w.view(self.cc, "latest_verdict", 1000)["verdict"], "UNVERIFIABLE")

    def test_gate_refuses_old_block_filed_fresh(self):
        self.w.advance(31 * DAY)
        self.file()
        with self.assertRaises(world.Reverted) as cm:
            self.w.call(self.gate, "claim_offset", 1000, "x", sender=USER)
        self.assertEqual(cm.exception.msg, "REFUSED: STALE_BLOCK")

    def test_gate_refuses_old_verdict(self):
        self.file()
        self.w.advance(30 * DAY + 1)
        with self.assertRaises(world.Reverted) as cm:
            self.w.call(self.gate, "claim_offset", 1000, "x", sender=USER)
        self.assertEqual(cm.exception.msg, "REFUSED: STALE_VERDICT")

    def test_verdict_text_says_as_of(self):
        r = self.file()
        c = self.w.view(self.cc, "get_check", r["check_id"])
        self.assertEqual((c["as_of"], c["block"]), (F.NOW_ISO, BLOCK))


# ---------------------------------------------------------------- A5 gate bypass

class A5GateBypass(Base):
    def test_gate_bound_to_its_registry(self):
        rogue = self.w.deploy("CarbonCheck", "DEMO", 5, 3600)
        self.w.call(rogue, "file_check", BATCHES, 1000, BLOCK, sender=FILER)
        with self.assertRaises(world.Reverted) as cm:
            self.w.call(self.gate, "claim_offset", 1000, "x", sender=USER)
        self.assertEqual(cm.exception.msg, "REFUSED: NO_VERDICT")

    def test_demo_range_cannot_touch_canonical(self):
        with self.assertRaises(world.Reverted):
            self.w.call(self.cc, "demo_claim_range", 191, 1, 2, "abc", sender=FILER)

    def test_registry_lying_shape(self):
        for lv in ({"verdict": "MATCHED"}, {"verdict": "MATCHED", "filed_at": -1, "block_time": 5},
                   {"verdict": "matched", "filed_at": 5, "block_time": 5}, [], "MATCHED"):
            self.assertIn("refuse", OG.decide(lv, 10, 100))

    def test_second_claimant_refused(self):
        self.file()
        self.w.call(self.gate, "claim_offset", 1000, "a", sender=USER)
        with self.assertRaises(world.Reverted):
            self.w.call(self.gate, "claim_offset", 1000, "b", sender=FILER2)

    def test_gate_no_setter(self):
        src = (ROOT / "contracts" / "OffsetGate.py").read_text()
        self.assertNotIn("def set_", src)
        self.assertEqual(len(re.findall(r"@gl\.public\.write", src)), 1)


# ---------------------------------------------------------------- A6 unicode and input sizes

class A6Inputs(Base):
    def test_note_unicode_refused(self):
        self.file()
        for note in ("‮evil", "a​b", "\u0000"):
            with self.assertRaises(world.Reverted):
                self.w.call(self.gate, "claim_offset", 1000, note, sender=USER)

    def test_huge_serial_from_chain_bounded(self):
        F.set_batch(70, "1" * 4000, 1)
        r = self.file(token_id=70)
        self.assertEqual(r["code"], "SERIAL_UNPARSABLE")
        self.assertLessEqual(len(self.w.view(self.cc, "get_check", r["check_id"])["serial"]), CC.MAX_SERIAL + 8)

    def test_huge_verra_strings_bounded(self):
        s = F.serial_for(1, 3)
        F.set_batch(71, s, 3)
        F.retire(s, 3, 191, 2009, remark="R" * 100000)
        F.verra().retired[s][0]["publicBeneficialOwner"] = "B" * 100000
        r = self.file(token_id=71)
        v = self.w.view(self.cc, "get_check", r["check_id"])["verra"]
        self.assertEqual((len(v["remark"]), len(v["beneficiary"])), (240, 100))

    def test_quantity_bool_from_verra(self):
        s = F.serial_for(1, 3)
        F.set_batch(72, s, 3)
        F.retire(s, 3, 191, 2009)
        F.verra().retired[s][0]["holdingQuantity"] = True
        self.assertEqual(self.file(token_id=72)["code"], "VERRA_QUANTITY_MISMATCH")

    def test_quantity_nan_from_verra(self):
        s = F.serial_for(1, 3)
        F.set_batch(73, s, 3)
        F.retire(s, 3, 191, 2009)
        F.verra().raw["retirements"] = json.dumps({"entities": [dict(F.entity(s, 3, 191, 2009), holdingQuantity=None)]})
        self.assertEqual(self.file(token_id=73)["code"], "VERRA_QUANTITY_MISMATCH")


# ---------------------------------------------------------------- A7 lying sources

class A7LyingSources(Base):
    def test_one_rpc_lies_about_quantity(self):
        F.set_batch(1000, S1000, 5001, urls=[F.RPC_A])
        self.assertEqual(self.file()["code"], "RPC_DISAGREE")

    def test_one_rpc_lies_about_status(self):
        F.set_batch(1000, S1000, 5000, status=1, urls=[F.RPC_B])
        self.assertEqual(self.file()["code"], "RPC_DISAGREE")

    def test_rpc_claims_finality_it_lacks(self):
        stub.WEB.chains[F.RPC_A].finalized = BLOCK - 1
        stub.WEB.chains[F.RPC_A].set_block(BLOCK - 1, F.NOW)
        self.assertEqual(self.file()["code"], "BLOCK_NOT_FINALIZED")

    def test_leader_reports_matched_for_mismatch(self):
        F.set_batch(80, S1000, 4000)
        stub.FORGE["mutate"] = lambda r: dict(r, verdict="MATCHED", code="ALL_FIELDS_MATCH")
        with self.assertRaises(world.Reverted):
            self.file(token_id=80)

    def test_leader_claims_transport_failure_is_harmless(self):
        """A leader may always say UNVERIFIABLE on a transport code; that
        asserts nothing, gives no gate access and indexes no range."""
        stub.FORGE["payload"] = CC.unv("chain", "RPC_UNAVAILABLE", "x")
        r = self.file()
        self.assertEqual(r["verdict"], "UNVERIFIABLE")
        self.assertEqual(self.w.view(self.cc, "list_claimed", 1, 5)["total"], 0)
        self.assertFalse(self.w.view(self.cc, "is_matched", 1000))


# ---------------------------------------------------------------- A8 docs truth

class A8DocsTruth(unittest.TestCase):
    def read(self, f):
        p = ROOT / f
        return p.read_text() if p.exists() else ""

    def test_rules_doc_names_frozen_addresses(self):
        t = self.read("docs/RULES.md")
        self.assertIn("0x8A4d7458dDe3023A3B24225D62087701A88b09DD", t)
        self.assertIn("0x2359677E513Bc83106268514c5B2De3C29C849ea", t)

    def test_rules_doc_names_rpcs(self):
        t = self.read("docs/RULES.md")
        for u in CC.RPCS:
            self.assertIn(u, t)

    def test_rules_doc_names_retired_status(self):
        self.assertIn("`RETIRED`", self.read("docs/RULES.md"))

    def test_readme_scope_section(self):
        t = self.read("README.md")
        self.assertIn("## Scope", t)
        self.assertIn("as of", t)

    def test_feasibility_mentions_every_rpc_and_probe(self):
        t = self.read("docs/FEASIBILITY.md")
        for u in CC.RPCS:
            self.assertIn(u.split("/")[2], t)
        self.assertIn("GenVM", t)

    def test_every_reason_code_documented(self):
        t = self.read("docs/RULES.md")
        codes = [v for k, v in vars(CC).items() if re.match(r"^(C|M|U)_[A-Z0-9_]+$", k) and isinstance(v, str)]
        missing = [c for c in codes if "`" + c + "`" not in t]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
