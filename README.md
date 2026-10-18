# CarbonCheck

A GenLayer intelligent contract that checks whether **one** tokenized carbon credit batch (a Toucan batch NFT on Polygon) matches real credits retired in the public **Verra** registry, and that no Verra unit range is claimed by two batches. It answers **MATCHED**, **MISMATCH**, **DOUBLE_CLAIMED** or **UNVERIFIABLE**.

Code reads the batch on Polygon and the serial's public Verra record, compares them field by field and decides. No model is called anywhere.

```
filer: (Toucan batch contract, batch token id, finalized Polygon block)
  -> door: official contract only, ids, duplicate, rate limit      refused: nothing stored
  -> Polygon, two RPCs, byte-identical at the block:
       nftList (serial, quantity, status), ownerOf, factory pvIdtoERC20 -> TCO2, TCO2 getAttributes
     Confirmed and held by its own TCO2, else UNVERIFIABLE
  -> code parses the serial: units first..last, project id, vintage dates
     serial vs TCO2 project / vintage, units vs quantity            else MISMATCH
  -> Verra registry JSON (Retirements, then Holdings), exact serial:
     RETIRED, same unit count, project, vintage                     else MISMATCH / UNVERIFIABLE
  -> code: overlap with a range already MATCHED for another batch of the same project -> DOUBLE_CLAIMED
  -> stored, final, "as of" this fetch and this block
```

Contract only, no frontend. GenLayer Studio Dev (chain 61997), GenVM v0.6 format (`# v0.3.0`, `py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng`). Version 1.0.0.

## Why

A tokenized carbon credit is only as good as the registry entry behind it. Toucan bridged Verra credits to Polygon by retiring them on Verra and minting a batch NFT plus TCO2 tokens. Whether a given batch really corresponds to retired Verra credits of the same project, vintage and size is public information in two places that nobody compares automatically. CarbonCheck compares them and leaves an on-chain verdict anyone can read and any contract can consume. The real data has cases worth catching: batches whose serial names a different project than their TCO2, batches whose exact serial Verra does not list, Confirmed batches never fractionalized (FEASIBILITY.md).

## Rules

The full rules are in [docs/RULES.md](docs/RULES.md). In short:

1. **Official batches only.** The batch contract must be Toucan's CarbonOffsetBatches `0x8A4d7458dDe3023A3B24225D62087701A88b09DD` (frozen, from Toucan's own deployment records). The batch must be `Confirmed` and held by the TCO2 that Toucan's factory `0x2359677E513Bc83106268514c5B2De3C29C849ea` maps its vintage to (fractionalized). Otherwise UNVERIFIABLE.
2. **One pinned, finalized Polygon block, two RPCs.** dRPC and Tenderly must both have finalized the block and return byte-identical answers. Any error or difference is UNVERIFIABLE.
3. **Code parses the serial.** Unit range, project id and vintage dates come from the serial (strict ASCII format; several serials in one field, leading zeros or odd characters are UNVERIFIABLE). The serial's project and vintage must equal the TCO2's, and `last - first + 1` must equal the batch quantity, else MISMATCH.
4. **Verra, field by field.** The record with exactly this serial (Retirements report, then Holdings) must be `RETIRED` with the same unit count, project and vintage, else MISMATCH; no record is UNVERIFIABLE. The retirement remark is stored as evidence and never decides.
5. **DOUBLE_CLAIMED.** A range that overlaps (closed intervals; touching is not overlapping) a range of the same Verra project already MATCHED for a different batch.
6. **As of.** Every verdict records its fetch time and Polygon block; `recheck(id, block)` files anew. See Scope.
7. **No funds.** Filing is free and rate-limited per sender (canonical 5 per hour). Duplicates of (batch, block) are refused. Counters change only after all checks pass. Every accepted filing reaches a final verdict; a source that does not answer ends UNVERIFIABLE.

Reads: `get_check(id)`, `list_checks(start, count)`, `latest_verdict(batch)`, `is_matched(batch)`, plus `list_claimed`, `get_stats`, `get_rules`, `rate_status`.

**OffsetGate** consumes CarbonCheck. `claim_offset(batch, note)` accepts an offset claim only if the batch's latest verdict (the one that read the newest Polygon block) is MATCHED, was ruled at most `max_age` ago and read a block at most `max_age` old; otherwise it refuses (`NO_VERDICT`, `NOT_MATCHED_<verdict>`, `STALE_VERDICT`, `STALE_BLOCK`). Each batch backs one accepted claim.

## Scope

- **Verdicts are "as of".** Verra is a live registry and a batch can change on chain. A verdict states what Verra answered when the filing's transaction ran (`as_of`) and what Polygon held at the filed block (`block`, `block_time`). It says nothing about later. `recheck(check_id, block)` files a fresh check; `latest_verdict` follows the newest block; OffsetGate refuses verdicts older than its `max_age`.
- **Toucan's Verra bridge only.** One batch contract and one TCO2 factory, frozen. Puro batches and any other bridge or registry are UNVERIFIABLE.
- **Exact serials.** A batch matches only the Verra record that carries its exact serial. When Verra has since re-labelled a serial (a CORSIA flag `0` -> `1`, an `APX` serial re-issued as `VER`) or split its units into other records, the verdict is UNVERIFIABLE (`VERRA_NOT_FOUND`), not MATCHED and not MISMATCH. Code does not reassemble ranges.
- **DOUBLE_CLAIMED is within this registry.** It compares a batch with ranges this contract has MATCHED, within one Verra project (Verra reuses unit numbers across projects). Ranges are not inferred from batches nobody filed. The real data has no DOUBLE_CLAIMED case; the demo deployment shows the path with a labelled demo range.
- **A source that does not answer ends UNVERIFIABLE.** The leader's UNVERIFIABLE for a transport failure is accepted without being reproduced; it asserts nothing and the batch can be refiled at another block.
- **What a match means.** MATCHED says the batch and its Verra record agree on status, unit count, project and vintage. It does not judge the credits' environmental quality.

## Addresses

ADDRESSES_TABLE

## Seeds

Every real batch from [docs/FEASIBILITY.md](docs/FEASIBILITY.md) and every real non-MATCHED case found among Confirmed batches, filed on the canonical CarbonCheck at one finalized Polygon block, each final. Details, Polygonscan and Verra links: [docs/SEEDS.md](docs/SEEDS.md).

SEEDS_TABLE

## How to verify

```
cd test && npm install
node ../tools/verify_source.mjs          # gen_getContractCode == contracts/ at HEAD, byte for byte, all from one commit
python3 -m unittest test_carboncheck test_attacks     # offline suite
node tx.mjs --set=final --c=CarbonCheck --view=get_check --args='[1]'
node ../tools/final_check.mjs            # writes docs/FINAL_CHECK.md
```

To recompute a verdict by hand: open the check's `batch_url` (Polygonscan) and read `nftList` / `ownerOf` on the batch contract at its `block`; take the serial to the Verra registry's Retirements report (https://registry.verra.org/verra/public/program/VCS) and compare status, quantity, project and vintage.

- Rules: [docs/RULES.md](docs/RULES.md)
- Feasibility research: [docs/FEASIBILITY.md](docs/FEASIBILITY.md)
- Attack round: [docs/ATTACK_REPORT.md](docs/ATTACK_REPORT.md)
- Seeds: [docs/SEEDS.md](docs/SEEDS.md)
- Demo run (every path on chain): [docs/demo-run.log](docs/demo-run.log)
- Final check: [docs/FINAL_CHECK.md](docs/FINAL_CHECK.md)
- Submission text: [docs/SUBMISSION.md](docs/SUBMISSION.md)
