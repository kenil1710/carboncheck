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

| Contract | Address | Mode | Constructor |
|---|---|---|---|
| CarbonCheck | [`0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413`](https://explorer-studio-dev.genlayer.com/address/0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413) | CANONICAL | `["CANONICAL",5,3600]` |
| CarbonCheckDemo | [`0x019B01259A30467de7bdbFD2125e3d3CE00B08a1`](https://explorer-studio-dev.genlayer.com/address/0x019B01259A30467de7bdbFD2125e3d3CE00B08a1) | DEMO | `["DEMO",3,600]` |
| OffsetGate | [`0x7BF9f7b62f65214f9B65647799507FC9A452409B`](https://explorer-studio-dev.genlayer.com/address/0x7BF9f7b62f65214f9B65647799507FC9A452409B) | CANONICAL | `["0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413",2592000]` |
| OffsetGateDemo | [`0x98eF81498Dc820fAb2Db56F112573a6256688348`](https://explorer-studio-dev.genlayer.com/address/0x98eF81498Dc820fAb2Db56F112573a6256688348) | DEMO | `["0x019B01259A30467de7bdbFD2125e3d3CE00B08a1",600]` |

All four from commit `93c92dbc03` on GenLayer Studio Dev (chain 61997, https://studio-dev.genlayer.com/api). Frozen inside CarbonCheck: Toucan CarbonOffsetBatches `0x8A4d7458dDe3023A3B24225D62087701A88b09DD` and ToucanCarbonOffsetsFactory `0x2359677E513Bc83106268514c5B2De3C29C849ea` on Polygon (chain 137).

## Seeds

Every real batch from [docs/FEASIBILITY.md](docs/FEASIBILITY.md) and every real non-MATCHED case found among Confirmed batches, filed on the canonical CarbonCheck at one finalized Polygon block, each final. Details, Polygonscan and Verra links: [docs/SEEDS.md](docs/SEEDS.md).

| Seed | Batch | Verdict | Reason (decided by code) | Check / tx |
|---|---|---|---|---|
| S01 | [2](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/2) | **MATCHED** | 1 units, VCS-1418, 2020 | [#1](https://explorer-studio-dev.genlayer.com/tx/0xc46c754e0584ac06a2641268f66993bb7d407c5b5c23850ecc90fa32072934e7) |
| S02 | [9](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/9) | **MATCHED** | 2340 units, VCS-535, 2014 | [#2](https://explorer-studio-dev.genlayer.com/tx/0x7e83b06e21baa1ce2f608d7cd897733e95122d450f740e733495fea1839fdcf7) |
| S03 | [10](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/10) | **MATCHED** | 12 units, VCS-905, 2013 | [#3](https://explorer-studio-dev.genlayer.com/tx/0xb3425c98caf8e37735c3d9b7349e41170b33365a455223ae8035583e98fd8009) |
| S04 | [23](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/23) | **MATCHED** | 27569 units, VCS-535, 2014 | [#4](https://explorer-studio-dev.genlayer.com/tx/0x9e9e9ba5caa3b80bcd05d5f5409bb6c4fa20ed77f9375ed234989629299f9d65) |
| S05 | [100](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/100) | **MATCHED** | 3367 units, VCS-836, 2012 | [#5](https://explorer-studio-dev.genlayer.com/tx/0x56360e548a9ebf7658bde65aa975fc43e0a13f5b9ec582f2b22dd1230e43ad06) |
| S06 | [256](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/256) | **MATCHED** | 23064 units, VCS-2097, 2015 | [#6](https://explorer-studio-dev.genlayer.com/tx/0x4d0a562625e00502b054e31977fb622e5380897e5953182fafba3a84b2df424f) |
| S07 | [259](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/259) | **MATCHED** | 77600 units, VCS-917, 2014 | [#7](https://explorer-studio-dev.genlayer.com/tx/0x6b84916db67c899bbcb564667463090be667f3be3343327a83b7c8b73e823ebe) |
| S08 | [313](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/313) | **MATCHED** | 3155 units, VCS-1190, 2018 | [#8](https://explorer-studio-dev.genlayer.com/tx/0xf8033a96b7d6cf586b43c7726d418aae43b82b6b67dbd297af07076275760587) |
| S09 | [889](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/889) | **MATCHED** | 4000 units, VCS-476, 2008 | [#9](https://explorer-studio-dev.genlayer.com/tx/0x586a80ecca05a9ed929278b3679580db2a41dbc9c011e804c5576346c0f3761c) |
| S10 | [1000](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1000) | **MATCHED** | 5000 units, VCS-191, 2009 | [#10](https://explorer-studio-dev.genlayer.com/tx/0x950aa53daba2169045957879a193e084691201a104c74dda2d84f5b9c10d93f7) |
| S11 | [68](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/68) | **MISMATCH** | SERIAL_PROJECT_MISMATCH: the serial names project VCS-1477, the TCO2 says VCS-981 | [#11](https://explorer-studio-dev.genlayer.com/tx/0x8abe725e1b000c91ddd0d866c274c8bec88536c2cf3489cccc060e652664ec0f) |
| S12 | [180](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/180) | **MISMATCH** | SERIAL_PROJECT_MISMATCH: the serial names project VCS-10, the TCO2 says VCS-699 | [#12](https://explorer-studio-dev.genlayer.com/tx/0x7037af8d6f4f16b6c4f3771872b72d990bae31a724116e1c835f3f962cc25ef6) |
| S13 | [39](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/39) | **UNVERIFIABLE** | VERRA_NOT_FOUND: the Verra registry lists no retired or active units with this exact serial | [#13](https://explorer-studio-dev.genlayer.com/tx/0xf7e375a08f762cb0c20d9815cf937e2bfca0fdcee5350f49255a1832d34d85d5) |
| S14 | [594](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/594) | **UNVERIFIABLE** | VERRA_NOT_FOUND: the Verra registry lists no retired or active units with this exact serial | [#14](https://explorer-studio-dev.genlayer.com/tx/0x9ab43affc514cf9d2dae4127317ac946e77ff967bc9634a070030e18a9393cab) |
| S15 | [686](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/686) | **UNVERIFIABLE** | VERRA_NOT_FOUND: the Verra registry lists no retired or active units with this exact serial | [#15](https://explorer-studio-dev.genlayer.com/tx/0x575ca43cbdfb03e0ec1697ad261cca77cc51967e7e92bcd17e94a833cd2c79cc) |
| S16 | [874](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/874) | **UNVERIFIABLE** | VERRA_NOT_FOUND: the Verra registry lists no retired or active units with this exact serial | [#16](https://explorer-studio-dev.genlayer.com/tx/0xa1f5c512af49de5f90fade77b9c3c905515f3f064e0c531142c417192305ddf1) |
| S17 | [1213](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1213) | **UNVERIFIABLE** | VERRA_NOT_FOUND: the Verra registry lists no retired or active units with this exact serial | [#17](https://explorer-studio-dev.genlayer.com/tx/0xc7a7b0b617440c0f51c408b954a6ff89f757a7680f1230b6b0a7b12d2211c487) |
| S18 | [3](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/3) | **UNVERIFIABLE** | BATCH_NOT_FRACTIONALIZED: the batch is held by 0x25bdff8db8d80971935a7f38a0cf31dec62f7696, not by its TCO2 | [#18](https://explorer-studio-dev.genlayer.com/tx/0xf37391826471fbafebf7fd32452232033522b56460d582008f529576348ad1ed) |
| S19 | [138](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/138) | **UNVERIFIABLE** | BATCH_NOT_FRACTIONALIZED: the batch is held by 0x25bdff8db8d80971935a7f38a0cf31dec62f7696, not by its TCO2 | [#19](https://explorer-studio-dev.genlayer.com/tx/0x41ec3e8c179f4135ae66943390b9e10ea8fba930f52dcff16b81bc502081083a) |
| S20 | [446](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/446) | **UNVERIFIABLE** | BATCH_NOT_FRACTIONALIZED: the batch is held by 0xdb97aa9b0c07254ef9e017641f5da271e5c31f35, not by its TCO2 | [#20](https://explorer-studio-dev.genlayer.com/tx/0x7866c3adf29bf0acbdfa0e616dfdf2c81e3e8eee064b8670e10c9720407ca5ab) |
| S21 | [798](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/798) | **UNVERIFIABLE** | BATCH_NOT_FRACTIONALIZED: the batch is held by 0xe2da2b0691fc74c3bbbe8305581308b0dc61ee30, not by its TCO2 | [#21](https://explorer-studio-dev.genlayer.com/tx/0x03923a22b60addaf7ff285f9db62d77d8a5a12a346b1022376d3e15657364119) |
| S22 | [833](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/833) | **UNVERIFIABLE** | BATCH_NOT_FRACTIONALIZED: the batch is held by 0x63a32f1595a68e811496d820680b74a5cca303c5, not by its TCO2 | [#22](https://explorer-studio-dev.genlayer.com/tx/0x28f524f03a6ace45207c45d645ea4b136fcda66aeef5c5a79b6356cd5b1b440c) |
| S23 | [1001](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1001) | **UNVERIFIABLE** | BATCH_NOT_FRACTIONALIZED: the batch is held by 0x10080bb62dafe52753af9d6bdd0bd14ac313bf43, not by its TCO2 | [#23](https://explorer-studio-dev.genlayer.com/tx/0x1c05e4a5b8c6d84f96c222ca6b6b295d93c00a1bec83f295ef0baa8f6f34e798) |
| S24 | [217](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/217) | **UNVERIFIABLE** | TCO2_NOT_FOUND: the official factory maps this batch's vintage to no TCO2 | [#24](https://explorer-studio-dev.genlayer.com/tx/0x43980ded10ebe8c4f2fdac626483ace0b8122f13c548b271ae07e76f21aeba91) |
| S25 | [1713](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1713) | **UNVERIFIABLE** | TCO2_NOT_FOUND: the official factory maps this batch's vintage to no TCO2 | [#25](https://explorer-studio-dev.genlayer.com/tx/0xc7624c2627745ebc0df66f960e25d0d1cdf0903890dd99adb40c6d9aaec804fd) |
| S26 | [1715](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1715) | **UNVERIFIABLE** | TCO2_NOT_FOUND: the official factory maps this batch's vintage to no TCO2 | [#26](https://explorer-studio-dev.genlayer.com/tx/0x4236ad032cfb04ec99e726f3cb78c13cebdae00a04ad8bf76c6f91b6d5bf68a5) |
| S27 | [1717](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1717) | **UNVERIFIABLE** | TCO2_NOT_FOUND: the official factory maps this batch's vintage to no TCO2 | [#27](https://explorer-studio-dev.genlayer.com/tx/0xa4dafe8b429dbb789f90d0a67e170014064b03ee9089df182741c10dd7cff8b6) |
| S28 | [7](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/7) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#28](https://explorer-studio-dev.genlayer.com/tx/0xaa2b2ca2c8ea1694a31a5254238d53415606d63380a7b7116c46cae54441774d) |
| S29 | [140](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/140) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#29](https://explorer-studio-dev.genlayer.com/tx/0x67b66217cb4c7ff8c4a8a9c7f8e4f464f8d6ab8d4dfa35341a9a1bd579a005d6) |
| S30 | [564](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/564) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#30](https://explorer-studio-dev.genlayer.com/tx/0x290a9e2625da9a5e9c6ef0e92f91f09e1ad24a1a2847e1f1485dda30004f5421) |
| S31 | [576](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/576) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#31](https://explorer-studio-dev.genlayer.com/tx/0x67b0efa7894215386aba1557649211cdf7f7fca776a71a155271e5e2f701f079) |
| S32 | [698](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/698) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#32](https://explorer-studio-dev.genlayer.com/tx/0x6c26ffe0976e9a2f763ea641315e1639f574e1d126d6158829a54ff3f05276fc) |
| S33 | [711](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/711) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#33](https://explorer-studio-dev.genlayer.com/tx/0x49eb82581a0640508fb752740b9c74e6fd398fa65bd9b6ba7a1bcf033bce2e6f) |
| S34 | [712](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/712) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#34](https://explorer-studio-dev.genlayer.com/tx/0x82ceaf3658f83cdfa2bfdada66c2b3f109530705d003f5c8f4ff28a602d1323a) |
| S35 | [718](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/718) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#35](https://explorer-studio-dev.genlayer.com/tx/0x9da1bb95893fc678cc7341eb747760ad7f75cdec657445f0177d47fdb1569d12) |
| S36 | [719](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/719) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#36](https://explorer-studio-dev.genlayer.com/tx/0xc3e7ba4fe79b8d80157f7bbc95d94ff9d4907b63a361be172b0809e676308c86) |
| S37 | [890](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/890) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#37](https://explorer-studio-dev.genlayer.com/tx/0x39a456989a4cb2ddbc4fcde84b3a5f4bb511db6c61c53ed0684b4507eb2dec36) |
| S38 | [898](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/898) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#38](https://explorer-studio-dev.genlayer.com/tx/0x1cf9b825d5cd2a654a6a8f5cc15f6bbb40691a7214c7624069adca1d5fb0d88d) |
| S39 | [910](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/910) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#39](https://explorer-studio-dev.genlayer.com/tx/0x4f430536b3fa3b89203e13163888dab1b65de64a8a1fcff5498a006db6c150d7) |
| S40 | [934](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/934) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#40](https://explorer-studio-dev.genlayer.com/tx/0x8f7d7c06413272f4524f1b7a7d053b01f041d03356240ebe8b5a7b568d5b61c2) |
| S41 | [965](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/965) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#41](https://explorer-studio-dev.genlayer.com/tx/0x8876433f39f92681ffe69cbe10004fbd94e91f62d79e6a6aeeb353a6783b2e17) |
| S42 | [977](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/977) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#42](https://explorer-studio-dev.genlayer.com/tx/0xa52a9d0350a74b721c15e085ce32b4edd1397ab78eea0956bc83b6f50edf16ce) |
| S43 | [1163](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1163) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#43](https://explorer-studio-dev.genlayer.com/tx/0xbb40b89880a5798ecff908a02befb9549204747824f98c308e862fa762cced94) |
| S44 | [199](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/199) | **UNVERIFIABLE** | SERIAL_UNPARSABLE: the batch serial is not a well-formed Verra VCU serial | [#44](https://explorer-studio-dev.genlayer.com/tx/0xae817158c3ff665a1d545c491c989a6519c202131a245d95ff36394b49ed4696) |
| S45 | [1](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1) | **UNVERIFIABLE** | BATCH_NOT_CONFIRMED: the batch is Pending, not Confirmed | [#45](https://explorer-studio-dev.genlayer.com/tx/0xd7847001e381eb788c7191cd2f28e29a99983b75cce91558fe266b265ed01a7f) |
| S46 | [1350](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1350) | **UNVERIFIABLE** | BATCH_NOT_CONFIRMED: the batch is Pending, not Confirmed | [#46](https://explorer-studio-dev.genlayer.com/tx/0x8ed9f4f7135f96bf7c5299cbad7697e07aa789e433de777cc3cc04b8ed0a09e6) |
| S47 | [244](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/244) | **UNVERIFIABLE** | BATCH_NOT_CONFIRMED: the batch is Rejected, not Confirmed | [#47](https://explorer-studio-dev.genlayer.com/tx/0x648bca62206a9e20de712b77ca7422767a658b3793465f39c5e866f6bd3ef29e) |
| S48 | [1716](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1716) | **UNVERIFIABLE** | BATCH_NOT_CONFIRMED: the batch is DetokenizationFinalized, not Confirmed | [#48](https://explorer-studio-dev.genlayer.com/tx/0x7ee87ef0505a625bc33d8f241150420a23141a70a46634ffe17850a911180116) |
| S49 | [1714](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1714) | **UNVERIFIABLE** | BATCH_NOT_CONFIRMED: the batch is RetirementFinalized, not Confirmed | [#49](https://explorer-studio-dev.genlayer.com/tx/0x2ee5f3def8ab5f8c805eda1de5084f1a9445c4f5a3f92a8b2a256649a6419beb) |
| S50 | [2000](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/2000) | **UNVERIFIABLE** | BATCH_NOT_FOUND: the batch contract has no such token at this block | [#50](https://explorer-studio-dev.genlayer.com/tx/0x5b8b13e8afe6672a547100bcc0ac130265b9e96a86b947d0c7c6f813facde311) |

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
