# Feasibility (Step 0)

Done before any contract code. Every number below was measured on 2026-10-18 and is reproducible with the scripts in `test/feasibility/`. Raw data: `test/feasibility/onchain.json` (two-RPC reads), `scan.json` (every batch NFT), `deep.json` (owner, TCO2, attributes and Verra record for every batch with a serial), `deep_report.txt` (what the contract's own code rules for each).

**Result: feasible.** Toucan batches can be read from two independent Polygon RPCs that agree byte for byte, and the public Verra registry can be read from inside GenVM. Real non-MATCHED cases exist (section d).

## a) Toucan batch NFTs on Polygon

### Official addresses

From Toucan's own deployment records, `github.com/ToucanProtocol/contracts`, `deployments/production/matic/*.json` (the docs at docs.toucan.earth point to this repository for contract addresses; commit `9afe1809bd`, 2025-12-17):

| Contract | Address |
|---|---|
| CarbonOffsetBatches (batch NFTs) | [`0x8A4d7458dDe3023A3B24225D62087701A88b09DD`](https://polygonscan.com/address/0x8A4d7458dDe3023A3B24225D62087701A88b09DD) |
| ToucanCarbonOffsetsFactory (Verra TCO2s) | [`0x2359677E513Bc83106268514c5B2De3C29C849ea`](https://polygonscan.com/address/0x2359677E513Bc83106268514c5B2De3C29C849ea) |
| ToucanContractRegistry | [`0x263fA1c180889b3a3f46330F32a4a23287E99FC9`](https://polygonscan.com/address/0x263fA1c180889b3a3f46330F32a4a23287E99FC9) |

Calls used (selectors computed with viem): `nftList(uint256)` `0x75bea166` -> (projectVintageTokenId, serialNumber, quantity, status, uri); `ownerOf(uint256)` `0x6352211e`; factory `pvIdtoERC20(uint256)` `0x5e813d3c` -> TCO2; TCO2 `getAttributes()` `0x152583de` -> (ProjectData{projectId, ...}, VintageData{name, startTime, endTime, ...}). Status values come from Toucan's `CarbonOffsetBatchesTypes.sol`: 0 Pending, 1 Rejected, 2 Confirmed, 3 DetokenizationRequested, 4 DetokenizationFinalized, 5 RetirementRequested, 6 RetirementFinalized. A Confirmed batch that was fractionalized is held by its own TCO2 contract (`ownerOf(batch) == TCO2`).

### Two independent RPCs, one pinned finalized block

Block **95733573** (hash `0x484850823110fecf1c4ac8bbc9b5f6b49f1ca8878c88aec442414c88933ebb5e`), the finalized head at the time. Every `eth_call` result and the block hash were compared as raw hex across the two RPCs; all agreed (`node test/feasibility/onchain.mjs --block=95733573 --ids=...`). `batchTokenCounter()` was 1719.

RPC choice was itself measured. `polygon-bor-rpc.publicnode.com` answered at first, then refused every historical `eth_call` ("Archive requests require a personal token"), so it cannot serve a pinned block. polygon-rpc.com, Ankr, nodies, BlockPI, Blast, Tatum and 1rpc need keys or refuse historical state. Four keyless RPCs answered archive `eth_call` at blocks 100, 5,000 and 200,000 behind the head: **dRPC** (`https://polygon.drpc.org`), **Tenderly** (`https://gateway.tenderly.co/public/polygon`), QuikNode's public endpoint and Pocket. The contract uses dRPC and Tenderly (different operators).

| Batch | Status | Fractionalized | Serial | Qty | TCO2 project / vintage | Verra (exact serial) |
|---|---|---|---|---|---|---|
| [2](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/2) | Confirmed | yes | `8367-10851650-10851650-VCS-VCU-1423-VER-IN-1-1418-01012020-29022020-0` | 1 | VCS-1418 / 2020-01-01..2020-02-29 | retirements RETIRED, 1 units, VCS-1418, vintage 2020, remark `TOUCAN-1.0-137-0x01cbf2c3aede792f0` |
| [9](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/9) | Confirmed | yes | `8842-48565492-48567831-VCS-VCU-279-VER-TR-1-535-01012014-31122014-0` | 2340 | VCS-535 / 2014-01-01..2014-12-31 | retirements RETIRED, 2340 units, VCS-535, vintage 2014, remark `TOUCAN-1.0-137-0x86ae2923bfa830b40` |
| [10](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/10) | Confirmed | yes | `11015-267732157-267732168-VCS-VCU-279-VER-TR-1-905-01012013-31122013-0` | 12 | VCS-905 / 2013-01-01..2013-12-31 | retirements RETIRED, 12 units, VCS-905, vintage 2013, remark `TOUCAN-1.0-137-0xfdeeb63eeeea158a9` |
| [23](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/23) | Confirmed | yes | `8842-48567832-48595400-VCS-VCU-279-VER-TR-1-535-01012014-31122014-0` | 27569 | VCS-535 / 2014-01-01..2014-12-31 | retirements RETIRED, 27569 units, VCS-535, vintage 2014, remark `TOUCAN-1.0-137-0xa64d4420c25d71cc6` |
| [100](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/100) | Confirmed | yes | `10851-251565784-251569150-VCS-VCU-291-VER-VN-1-836-01032012-31122012-0` | 3367 | VCS-836 / 2012-03-01..2012-12-31 | retirements RETIRED, 3367 units, VCS-836, vintage 2012, remark `TOUCAN-1.0-137-0x9fd0f3f52e7ad0db0` |
| [256](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/256) | Confirmed | yes | `10972-262954541-262977604-VCS-VCU-1317-VER-TR-1-2097-13082015-31122015-0` | 23064 | VCS-2097 / 2015-08-13..2015-12-31 | retirements RETIRED, 23064 units, VCS-2097, vintage 2015, remark `TOUCAN-1.0-137-0x814ded9896245bb09` |
| [259](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/259) | Confirmed | yes | `10996-264559150-264636749-VCS-VCU-290-VER-TR-1-917-08032014-31122014-0` | 77600 | VCS-917 / 2014-03-08..2014-12-31 | retirements RETIRED, 77600 units, VCS-917, vintage 2014, remark `TOUCAN-1.0-137-0x6fe091364f1fd9513` |
| [313](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/313) | Confirmed | yes | `7236-378945249-378948403-VCU-034-APX-IN-1-1190-01012018-31052018-0` | 3155 | VCS-1190 / 2018-01-01..2018-05-31 | retirements RETIRED, 3155 units, VCS-1190, vintage 2018, remark `TOUCAN-1.0-137-0xed1c54bf9982d83db` |
| [889](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/889) | Confirmed | yes | `1104-48565711-48569710-VCU-010-APX-CN-1-476-01022008-17022009-0` | 4000 | VCS-476 / 2008-02-01..2009-02-17 | retirements RETIRED, 4000 units, VCS-476, vintage 2008 - 2009, remark `TOUCAN-1.0-137-0xc966ccad54bc0bdee` |
| [1000](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/1000) | Confirmed | yes | `12078-382273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0` | 5000 | VCS-191 / 2009-01-01..2009-12-31 | retirements RETIRED, 5000 units, VCS-191, vintage 2009, remark `TOUCAN-1.0-137-0x435e7bbf0ef394425` |
| [1200](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/1200) | Pending | no | `(empty)` | 0 | no TCO2 from the factory | not looked up (not Confirmed) |
| [3](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/3) | Confirmed | no | `7236-378945246-378945248-VCU-034-APX-IN-1-1190-01012018-31052018-0` | 3 | VCS-1190 / 2018-01-01..2018-05-31 | retirements RETIRED, 3 units, VCS-1190, vintage 2018, remark `TOUCAN-1.0-137-0x81ba03e822f23d0bc` |
| [68](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/68) | Confirmed | yes | `6359-303397758-303397758-VCU-016-APX-ID-14-1477-01012017-31122017-1` | 1 | VCS-981 / 2016-01-01..2016-12-31 | retirements RETIRED, 1 units, VCS-1477, vintage 2017, remark `TOUCAN-1.0-137-0xcde435700a139fc36` |
| [180](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/180) | Confirmed | yes | `10448-217035889-217135831-VCS-VCU-1491-VER-BR-1-10-01012013-31122013-0` | 99943 | VCS-699 / 2009-01-01..2009-05-09 | retirements RETIRED, 99943 units, VCS-10, vintage 2013, remark `TOUCAN-1.0-137-0x7fd5315c59d2b7111` |
| [39](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/39) | Confirmed | yes | `11377-323597077-323642076-VCS-VCU-394-VER-CO-14-1566-01012019-31122019-0` | 45000 | VCS-1566 / 2019-01-01..2019-12-31 | not found (retirements and holdings) |
| [594](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/594) | Confirmed | yes | `7139-373861979-373862078-VCU-048-APX-EC-13-1883-01012018-31122018-0` | 100 | VCS-1883 / 2018-01-01..2018-12-31 | not found (retirements and holdings) |
| [1213](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/1213) | Confirmed | yes | `12286-398946449-398951448-VCS-VCU-323-VER-CN-14-1715-01012013-31122013-0` | 5000 | VCS-1715 / 2013-01-01..2013-12-31 | not found (retirements and holdings) |
| [217](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/217) | Confirmed | no | `10763-246981648-246997973-VCS-VCU-259-VER-IN-1-132-01012012-31122012-0` | 16326 | no TCO2 from the factory | retirements RETIRED, 16326 units, VCS-132, vintage 2012, remark `TOUCAN-1.0-137-0xea1911ec4a89faf12` |
| [7](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/7) | Confirmed | yes | `9380-92545283-92645182-VCS-VCU-263-VER-ID-14-674-01072014-31122014-1,7627-41...` | 128900 | VCS-674 / 2014-07-01..2014-12-31 | - |
| [199](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/199) | Confirmed | yes | `(empty)` | 0 | VCS-722 / 2008-10-01..2008-12-31 | - |
| [244](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/244) | Rejected | no | `10972-262954541-262977604-VCS-VCU-1317-VER-TR-1-2097-13082015-31122016-0` | 5000000000000000000 | no TCO2 from the factory | not looked up (not Confirmed) |
| [1350](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/1350) | Pending | no | `\u00311015-267732157-267732168-VCS-VCU-279-VER-TR-1-905-01012013-31122013-0` | 0 | no TCO2 from the factory | not looked up (not Confirmed) |
| [1713](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/1713) | Confirmed | no | `643002406801000010000000192331-643002406801000010000000192335` | 5 | no TCO2 from the factory | not found (retirements and holdings) |
| [1714](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/1714) | RetireFinal | no | `643002406801000010000000200721-643002406801000010000000200863` | 143 | no TCO2 from the factory | not looked up (not Confirmed) |
| [1716](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/1716) | Detokenized | no | `643002406801000010000000213752-643002406801000010000000213756` | 5 | no TCO2 from the factory | not looked up (not Confirmed) |
| [2000](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/2000) | Pending | no | `(empty)` | 0 | no TCO2 from the factory | not looked up (not Confirmed) |

TCO2 vintages are stored as UTC midnight of the first and last day (2009-01-01 = 1230768000), so the serial's DDMMYYYY dates compare to them by calendar day.

## b) The public Verra registry, from the Mac and from GenVM

The Verra registry moved to a new platform. Its website (registry.verra.org, "Retirements" and "Holdings" reports) calls these JSON endpoints, observed in the browser's network log:

- `POST https://prod-us.api.platts.com/ci-raas-prod/raas-report-api/es/public/retirements/publicReportPageSearch`
- `POST https://prod-us.api.platts.com/ci-raas-prod/raas-report-api/es/public/holdings/publicReportPageSearch` (units still active)

with the headers the site ships to every browser in `registry.verra.org/config/environment.config.json` (`appkey`, `registry: VERRA`, `standardId: 150000000000001`, `standardAcronym: VCS`, `application: Markit`, `X-XSRF-TOKEN`). The filter that works is the one the site sends: `{"serialNo": {"columnFilters": [{"filterType": "Text", "type": "equals", "filter": "<serial>"}]}}`. Each record carries `serialNo`, `stateCode` (`RETIRED`, `ACTIVE`), `holdingQuantity` (a JSON number, e.g. `5000.0`), `vcsProjectId`, `vintage`, `retiredDate`, `publicRetirementReasonDetails` (the retirement remark) and `publicBeneficialOwner`.

**From the Mac:** all 856 distinct serials of Confirmed batches were looked up (`test/feasibility/deep.mjs`). Every Toucan-era retirement has status `RETIRED` and a remark of the form `TOUCAN-1.0-137-<Polygon tx hash>-<batch id>`; e.g. batch 1000's record ends `-1000`.

**From inside GenVM:** three throwaway probe contracts (not in the repo; deployed by the `probe` test account on Studio Dev) called the endpoints with `gl.nondet.web.request` and were ACCEPTED:

| Probe | What it read | Result |
|---|---|---|
| `0xc142eAd6d1a9F089e9F43fDeE3844b6B59eBE3DE` | Verra retirements, batch 1000's serial | HTTP 200, 1 record: RETIRED, 5000.0, project 191, vintage 2009, remark `TOUCAN-1.0-137-0x435e...-1000` |
| `0x67A1C346AFD235B727D4213Bf39B86043f4E62D4` | `nftList(1000)` at block 95533573 on dRPC, Tenderly, QuikNode, Pocket | all four HTTP 200, same block hash, same 642-character result |
| `0x5afBb00D49ecB086A9340Bcfbb91821625E05330` | Verra retirements + holdings for an active serial of project 191 | retirements 0 records; holdings 1 record: ACTIVE, 4106.0, vintage 2011 |

## c) Gate

Verra can be read from inside GenVM, so the contract was built.

## d) Real non-MATCHED cases

The contract's own decision functions were run over the raw answers for all 947 batches that carry a serial (`python3 test/feasibility/deep_report.py`, before rule 5):

```
batches with a serial: 947
  MATCHED       ALL_FIELDS_MATCH           802
  UNVERIFIABLE  BATCH_NOT_CONFIRMED        112
  UNVERIFIABLE  SERIAL_UNPARSABLE          16
  UNVERIFIABLE  BATCH_NOT_FRACTIONALIZED   6
  UNVERIFIABLE  VERRA_NOT_FOUND            5
  UNVERIFIABLE  TCO2_NOT_FOUND             4
  MISMATCH      SERIAL_PROJECT_MISMATCH    2
```

Plain findings:

- **Most batches match.** 802 Confirmed, fractionalized batches match their Verra record on status, unit count, project and vintage.
- **Project mismatch (real).** Batch [68](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/68): the serial is project 1477, vintage 2017; the TCO2 it was minted into is VCS-981, vintage 2016. Batch [180](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/180): the serial is project 10; the TCO2 is VCS-699. Both are `MISMATCH` / `SERIAL_PROJECT_MISMATCH`.
- **Serial not on Verra (real).** Batch [1213](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/1213) holds units 398946449..398951448 of project 1715. Verra lists no record with that serial; the same unit numbers appear there split into many smaller retirements from July 2022 onward for other beneficiaries (e.g. "Retired on behalf of Climate Positive", 76 units). Batches 39, 594, 686 and 874: Verra now writes the serial differently (CORSIA flag `-0` became `-1`; 594/686 also `VCU-048-APX` became `VCU-1423-VER`). All five end `UNVERIFIABLE` / `VERRA_NOT_FOUND`: the rule is an exact serial, and code does not guess.
- **Confirmed but not fractionalized (real).** Batches 3, 138, 446, 798, 833, 1001 are Confirmed but held by a wallet, not by their TCO2. Batch 3's Verra record is a Toucan retirement whose beneficiary is that same wallet. `UNVERIFIABLE` / `BATCH_NOT_FRACTIONALIZED`.
- **No TCO2 from the Verra factory (real).** Batch 217 (a Verra serial whose vintage has no TCO2 in the factory) and Puro batches 1713, 1715, 1717. `UNVERIFIABLE` / `TCO2_NOT_FOUND`.
- **Unparsable serials (real).** 16 Confirmed batches hold two or more serials joined by commas (e.g. batch [7](https://polygonscan.com/nft/0x8a4d7458dde3023a3b24225d62087701a88b09dd/7)); batch 199 is Confirmed with an empty serial. `UNVERIFIABLE` / `SERIAL_UNPARSABLE`.
- **Not Confirmed (real).** 830 Pending, 46 Rejected, 2 Detokenized, 2 RetirementFinalized; e.g. Rejected batch 244 (quantity 5000000000000000000) and Pending batch 1350 whose serial starts with the literal text `\u0031`. `UNVERIFIABLE` / `BATCH_NOT_CONFIRMED`.
- **Verra status mismatch: none in real data.** No Confirmed batch's serial is listed as ACTIVE or anything but RETIRED.
- **Quantity / vintage mismatch against Verra: none in real data** once Verra's vintage format is read exactly (it writes `"2008 - 2009"` for a period spanning two years; see RULES.md).
- **One serial range in two batches: none among Confirmed batches.** Toucan's own `serialNumberApproved` check held: every overlap of unit numbers between two Confirmed batches is between *different Verra projects* (e.g. batch 9, project 535, units 48565492..48567831 and batch 889, project 476, units 48565711..48569710). Verra reuses unit numbers across projects (APX-era and VER-era serials), so the contract compares ranges only within one project. With that scope there are zero overlaps between Confirmed batches; the only same-project overlaps involve Rejected or Pending batches (e.g. Rejected 143 vs Confirmed 313, Rejected 260 vs Confirmed 259), which never reach MATCHED. **There is no real DOUBLE_CLAIMED case**; the demo deployment shows the path with a labelled demo range.
