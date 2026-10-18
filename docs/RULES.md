# CarbonCheck rules

These are the rules `contracts/CarbonCheck.py` applies, in the order it applies them. Code decides every step. No model is called anywhere (`get_rules()` answers `"model": "none"`).

A filing is `file_check(batch_contract, token_id, block)`: a Toucan batch NFT and one finalized Polygon block. `recheck(check_id, block)` files the same batch again at another block. Each filing ends with one of four verdicts, and every verdict is final as soon as it is ruled:

| Verdict | Meaning |
|---|---|
| `MATCHED` | The batch on Polygon and the serial's record in the public Verra registry agree on every field the rules compare. |
| `MISMATCH` | Code found a field that differs (listed in `why`). |
| `DOUBLE_CLAIMED` | Everything matched, but the batch's units overlap units of the same Verra project that an earlier filing already MATCHED for a different batch. |
| `UNVERIFIABLE` | Something could not be established: a source did not answer or disagreed, the batch is not in the required state, the serial cannot be parsed, or Verra has no record with this exact serial. |

## Rule 0: the door (refusals store nothing)

A refused filing reverts with `REFUSED: <reason>`. Nothing is stored and no counter moves.

| Refusal | When |
|---|---|
| `NOT_TOUCAN_BATCH_CONTRACT` | `batch_contract` is not Toucan's CarbonOffsetBatches `0x8A4d7458dDe3023A3B24225D62087701A88b09DD` (case and surrounding spaces are ignored; nothing else is). |
| `BAD_TOKEN_ID` | Not an integer (a Python int or a string of ASCII digits) from 1 to 10^9. Floats, hex strings and booleans are refused. |
| `BAD_BLOCK` | Not an integer from 19,000,000 (before the batch contract existed) to 10^10. |
| `DUPLICATE_OF_<id>` | The same batch at the same block was already filed (by anyone), whatever its verdict. |
| `RATE_LIMITED_UNTIL_<epoch>` | The sender used its filings for the window: canonical 5 per hour, demo 3 per 10 minutes. Refused filings do not count. |
| `NO_SUCH_CHECK` | `recheck` names a check that does not exist. |
| `NO_CLOCK` | The transaction carries no readable datetime. |
| `DEMO_ONLY` | `demo_claim_range` on the canonical deployment. |

## Rule 1: the official batch contract, Confirmed and fractionalized

Frozen in the contract (no setter exists), from Toucan's deployment records at `github.com/ToucanProtocol/contracts/deployments/production/matic/` (see FEASIBILITY.md):

- CarbonOffsetBatches `0x8A4d7458dDe3023A3B24225D62087701A88b09DD`
- ToucanCarbonOffsetsFactory `0x2359677E513Bc83106268514c5B2De3C29C849ea` (Verra TCO2s)

Code reads `nftList(token_id)` and `ownerOf(token_id)` from the batch contract, maps the batch's project-vintage id to its TCO2 with the factory's `pvIdtoERC20`, and reads the TCO2's `getAttributes()`. It never reads any other address.

| Code | Verdict | When |
|---|---|---|
| `BATCH_NOT_FOUND` | UNVERIFIABLE | `ownerOf` reverts (no such token at the block) or `nftList` is unreadable. |
| `BATCH_NOT_CONFIRMED` | UNVERIFIABLE | The status is not `Confirmed` (2). Pending, Rejected, DetokenizationRequested, DetokenizationFinalized, RetirementRequested and RetirementFinalized batches are named in `why`. |
| `TCO2_NOT_FOUND` | UNVERIFIABLE | The factory maps the batch's vintage to no TCO2 (zero address). |
| `BATCH_NOT_FRACTIONALIZED` | UNVERIFIABLE | The batch NFT is not held by that TCO2. A Confirmed batch is fractionalized when Toucan's TCO2 holds it and minted the tokens; a batch held by a wallet backs no TCO2. |
| `TCO2_UNREADABLE` | UNVERIFIABLE | `getAttributes()` reverts or cannot be decoded. |
| `NOT_A_VERRA_CREDIT` | UNVERIFIABLE | The TCO2's project id does not start with `VCS-`. |

## Rule 2: one pinned, finalized Polygon block, two RPCs that agree exactly

Every call names the filed block. Two RPCs run by different operators are read: `https://polygon.drpc.org` (dRPC) and `https://gateway.tenderly.co/public/polygon` (Tenderly). Both serve archive state to GenVM (FEASIBILITY.md).

From each RPC: `eth_chainId` must be 137; the RPC's `finalized` block must be at or above the filed block; then the block hash and time, and the raw hex results of `nftList`, `ownerOf`, `pvIdtoERC20` and `getAttributes`. The two RPCs' raw answers must be identical, byte for byte.

| Code | Verdict | When |
|---|---|---|
| `RPC_UNAVAILABLE` | UNVERIFIABLE | An RPC did not answer after 3 tries (transport error, HTTP 429 or 5xx), answered another chain, or answered an error that is not a revert. |
| `BLOCK_NOT_FINALIZED` | UNVERIFIABLE | Either RPC's finalized block is below the filed block. |
| `RPC_DISAGREE` | UNVERIFIABLE | Any raw answer or the block hash differs between the two RPCs. `why` names the fields. |

## Rule 3: the serial, parsed by code, against the TCO2 and the batch quantity

A Verra VCU serial reads `<issuance>-<first unit>-<last unit>-...VCU...-<project id>-<DDMMYYYY>-<DDMMYYYY>-<0|1>`. Real examples from the chain:

```
12078-382273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0
7236-378945246-378945248-VCU-034-APX-IN-1-1190-01012018-31052018-0
793-36303349-36306753-VCU-001-TZ1-CN-11-439-18072008-19042009-0
```

`parse_serial` accepts only upper-case ASCII letters, ASCII digits and single hyphens, 30 to 120 characters, 9 to 16 parts; the issuance and both unit numbers have no leading zero; `1 <= first <= last < 10^15`; the last part is `0` or `1`; the two dates are real calendar dates with the start on or before the end; the project id is a positive number with no leading zero; `VCU` is one of the middle parts. Anything else is `SERIAL_UNPARSABLE` (UNVERIFIABLE). That includes the 16 real Confirmed batches whose serial field holds several serials joined by commas: code does not pick one.

Then, in this order:

| Code | Verdict | When |
|---|---|---|
| `SERIAL_UNPARSABLE` | UNVERIFIABLE | As above. |
| `SERIAL_PROJECT_MISMATCH` | MISMATCH | The TCO2's project id is not exactly `VCS-` + the serial's project id. |
| `SERIAL_VINTAGE_MISMATCH` | MISMATCH | The TCO2's vintage `startTime` / `endTime` do not fall on the serial's start / end dates (compared by UTC calendar day; Toucan stores midnight). |
| `QUANTITY_MISMATCH` | MISMATCH | The serial's unit count `last - first + 1` is not the batch's on-chain `quantity`. |

## Rule 4: the Verra record, field by field

Code asks the registry's own JSON endpoints (the ones registry.verra.org's Retirements and Holdings reports call) for records whose `serialNo` **equals** the serial:

1. `POST https://prod-us.api.platts.com/ci-raas-prod/raas-report-api/es/public/retirements/publicReportPageSearch`
2. only if (1) has no such record: `.../holdings/publicReportPageSearch` (units still active), so a serial that was never retired is a status MISMATCH rather than "not found".

Only records whose `serialNo` equals the serial character for character count. Validators must get the identical normalized record: `source`, `serial`, `status` (`stateCode`), `quantity` (`holdingQuantity`, whole numbers only), `project` (`vcsProjectId`), `vintage`, `retired_on`, `remark` (`publicRetirementReasonDetails`, first 240 characters), `beneficiary` (first 100 characters).

**MATCHED requires all of:**

- status is exactly `RETIRED`;
- Verra's unit count equals the serial's `last - first + 1` (which rule 3 already tied to the on-chain quantity);
- Verra's project id equals the serial's;
- Verra's vintage equals the serial's vintage written the way Verra writes it: the year (`"2009"`), or `"<start year> - <end year>"` when the vintage spans two calendar years (`"2008 - 2009"`).

**Why `RETIRED` and nothing else.** Toucan bridged a credit by retiring it on Verra with a remark naming the Polygon transaction and the batch (`TOUCAN-1.0-137-<tx hash>-<batch id>`); the tokenized credit exists because the Verra credit can no longer be used. Verra has no separate status for these: every one of the 802 matching Toucan batches reads `stateCode` `RETIRED` (FEASIBILITY.md, section d). `ACTIVE` (listed in Holdings), `CANCELLED` or any other value, including a differently-cased `Retired`, means the credit is not retired on Verra as the bridge requires, and is a MISMATCH.

**The remark is evidence, never a rule.** It is stored on the check (`verra.remark`, `verra.beneficiary`) so anyone can read which Polygon transaction the registry names. It never changes a verdict: a missing or different remark does not make a match fail, and a remark naming the batch does not make a mismatch pass.

| Code | Verdict | When |
|---|---|---|
| `ALL_FIELDS_MATCH` | MATCHED | Every field above agrees. |
| `VERRA_STATUS_MISMATCH` | MISMATCH | Status is not `RETIRED`. |
| `VERRA_QUANTITY_MISMATCH` | MISMATCH | Unit count differs (or is not a whole number). |
| `VERRA_PROJECT_MISMATCH` | MISMATCH | Project id differs. |
| `VERRA_VINTAGE_MISMATCH` | MISMATCH | Vintage differs. |
| `VERRA_NOT_FOUND` | UNVERIFIABLE | Neither report lists a record with exactly this serial. |
| `VERRA_AMBIGUOUS` | UNVERIFIABLE | More than one record with exactly this serial. |
| `VERRA_UNAVAILABLE` | UNVERIFIABLE | The registry did not answer after 3 tries or answered an HTTP error. |
| `VERRA_UNREADABLE` | UNVERIFIABLE | The answer is not JSON or has no `entities` list. |

When several fields differ, `code` names the first in the order above and `why` lists all of them.

## Rule 5: DOUBLE_CLAIMED, by interval overlap within one Verra project

The contract keeps an index of every range it has MATCHED: `(project id, first unit, last unit, batch, check)` (`list_claimed`). A filing that would be MATCHED is `DOUBLE_CLAIMED` / `RANGE_ALREADY_CLAIMED` instead when its range overlaps an indexed range of the **same project** that belongs to a **different batch**:

```
overlap  iff  same project  and  first_a <= last_b  and  first_b <= last_a
```

- Touching ranges (`last_a + 1 == first_b`) do not overlap.
- A recheck of the same batch never conflicts with its own earlier MATCHED range.
- Only MATCHED filings enter the index. A DOUBLE_CLAIMED, MISMATCH or UNVERIFIABLE filing does not, so it cannot block a later honest filing.
- The first MATCHED batch keeps the range. A later batch cannot displace it.
- **Why the project scopes the ranges.** Verra reuses unit numbers across projects: real Confirmed Toucan batches 9 (project 535) and 889 (project 476) both contain unit 48565711, and they are different credits. Comparing numbers across projects would call honest batches DOUBLE_CLAIMED. Within one project, the real data has zero overlaps between Confirmed batches (FEASIBILITY.md, section d).

`demo_claim_range(project, first, last, label)` exists only on the demo deployment (`REFUSED: DEMO_ONLY` on the canonical one). It enters a labelled range so the DOUBLE_CLAIMED path can be shown on chain with a real batch; such a range carries batch 0 and its label appears in `why`.

## Rule 6: every verdict is "as of" its fetch

Verra is a live registry and a batch's on-chain state can change. Each check stores `filed_at` / `as_of` (the transaction's time, which is when every validator fetched Verra) and the Polygon `block`, `block_hash` and `block_time` it read. A verdict says what the two sources said at that moment, and nothing about later. `recheck(check_id, block)` files a fresh check of the same batch at another block and is subject to the same door rules.

`latest_verdict(batch)` returns the filing that read the **newest Polygon block** for the batch (one filing per batch and block, so there are no ties). A filing pinned to an older block can never mask a newer one, whatever order they were filed in. A filing that read no block (a transport code, see rule 7, including `BLOCK_NOT_FINALIZED`) is skipped as long as any filing of the batch did read its block, so nobody can mask a verdict by filing at a block that does not exist yet or while a source is down. `is_matched(batch)` is `latest_verdict(batch).verdict == "MATCHED"`.

## Rule 7: no funds, free filing, every filing ends

- The contract holds no funds, has no owner and no setter. Filing is free apart from network fees.
- Counters (`get_stats`) and the rate-limit count change only after all checks pass, in the same transaction that stores the verdict.
- Every accepted filing ends in a stored verdict. Each network read is retried 3 times; a read that still fails ends UNVERIFIABLE with a transport code (`RPC_UNAVAILABLE`, `RPC_DISAGREE`, `BLOCK_NOT_FINALIZED`, `VERRA_UNAVAILABLE`, `VERRA_UNREADABLE`, `INTERNAL`). Validators accept a leader's UNVERIFIABLE with one of these codes without reproducing it, so it asserts nothing: the contract stores no chain or registry data from it (`block_time` 0), it indexes no range, opens no gate and never becomes the latest verdict over a filing that read its block. Every other result is recomputed by each validator in full and must be identical.
- Views: `get_check(id)`, `list_checks(start, count)`, `latest_verdict(batch)`, `is_matched(batch)`, `list_claimed(start, count)`, `get_stats()`, `get_rules()`, `rate_status(sender)`.

## OffsetGate

`claim_offset(batch_id, note)` accepts an offset claim only if `CarbonCheck.latest_verdict(batch_id)`:

- is `MATCHED` (else `REFUSED: NO_VERDICT` or `REFUSED: NOT_MATCHED_<verdict>`),
- was ruled at most `max_age` seconds ago (else `REFUSED: STALE_VERDICT`), and
- read a Polygon block at most `max_age` seconds old (else `REFUSED: STALE_BLOCK`).

Each batch backs at most one accepted claim (`REFUSED: ALREADY_CLAIMED_IN_<id>`). The note is printable ASCII, at most 140 characters. The CarbonCheck address and `max_age` are frozen at deploy (canonical 30 days, demo 10 minutes). A refusal stores nothing. `check_offset(batch)` answers what `claim_offset` would do now, without storing anything.
