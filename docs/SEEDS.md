# Seeds

Every real batch from [FEASIBILITY.md](FEASIBILITY.md) and every real non-MATCHED case found among Confirmed Toucan batches, plus one batch of each non-Confirmed status and one id that does not exist, filed on the canonical CarbonCheck [`0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413`](https://explorer-studio-dev.genlayer.com/address/0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413), all at Polygon block [95735897](https://polygonscan.com/block/95735897). Every verdict is final. Mix: 10 MATCHED, 2 MISMATCH, 38 UNVERIFIABLE. The real data has no DOUBLE_CLAIMED case (FEASIBILITY.md, section d); the demo deployment shows that path ([demo-run.log](demo-run.log)).

Each verdict is "as of" its fetch time and block. The raw records (`get_check` output) are in [seeds.onchain.json](seeds.onchain.json).

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

## S01: batch 2, MATCHED

- Why chosen: Confirmed, fractionalized, retired on Verra (FEASIBILITY a)
- Batch: [Polygonscan NFT 2](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/2), status Confirmed, quantity 1, held by `0x23ad766052ab79644eb850490d1666488094ccc2`
- TCO2: [`0x23ad766052ab79644eb850490d1666488094ccc2`](https://polygonscan.com/address/0x23ad766052ab79644eb850490d1666488094ccc2), VCS-1418, vintage 2020-01-01..2020-02-29
- Serial: `8367-10851650-10851650-VCS-VCU-1423-VER-IN-1-1418-01012020-29022020-0` (units 10851650..10851650, 1, project 1418)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): retirements: RETIRED, 1 units, project 1418, vintage 2020, retired 2021-10-11, remark `TOUCAN-1.0-137-0x01cbf2c3aede792f052e6e9e53a0aa575e6be4a2086335fcdfe455e3a81d59c4-2`
- Verdict: **MATCHED** / `ALL_FIELDS_MATCH`: Retired on Verra; 1 units, project VCS-1418, vintage 2020-01-01..2020-02-29 match the batch and its TCO2
- As of: 2026-10-18T07:40:09Z (fetch) and block 95735897
- Research (block 95733573): MATCHED / `ALL_FIELDS_MATCH` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #1, tx [`0xc46c754e0584ac06a2641268f66993bb7d407c5b5c23850ecc90fa32072934e7`](https://explorer-studio-dev.genlayer.com/tx/0xc46c754e0584ac06a2641268f66993bb7d407c5b5c23850ecc90fa32072934e7), filed by `0x15a54fa8b0b9e37795f959b0e5bc44db26466b4d`

## S02: batch 9, MATCHED

- Why chosen: Confirmed, fractionalized, retired on Verra (FEASIBILITY a)
- Batch: [Polygonscan NFT 9](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/9), status Confirmed, quantity 2340, held by `0x0c29deaa1383c88712af1083ab8328a1e3661b17`
- TCO2: [`0x0c29deaa1383c88712af1083ab8328a1e3661b17`](https://polygonscan.com/address/0x0c29deaa1383c88712af1083ab8328a1e3661b17), VCS-535, vintage 2014-01-01..2014-12-31
- Serial: `8842-48565492-48567831-VCS-VCU-279-VER-TR-1-535-01012014-31122014-0` (units 48565492..48567831, 2340, project 535)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): retirements: RETIRED, 2340 units, project 535, vintage 2014, retired 2021-10-13, remark `TOUCAN-1.0-137-0x86ae2923bfa830b401d8e5f6250ec869763530d6a048cd06bbb81c73371d3108-9`
- Verdict: **MATCHED** / `ALL_FIELDS_MATCH`: Retired on Verra; 2340 units, project VCS-535, vintage 2014-01-01..2014-12-31 match the batch and its TCO2
- As of: 2026-10-18T07:40:31Z (fetch) and block 95735897
- Research (block 95733573): MATCHED / `ALL_FIELDS_MATCH` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #2, tx [`0x7e83b06e21baa1ce2f608d7cd897733e95122d450f740e733495fea1839fdcf7`](https://explorer-studio-dev.genlayer.com/tx/0x7e83b06e21baa1ce2f608d7cd897733e95122d450f740e733495fea1839fdcf7), filed by `0x15a54fa8b0b9e37795f959b0e5bc44db26466b4d`

## S03: batch 10, MATCHED

- Why chosen: Confirmed, fractionalized, retired on Verra (FEASIBILITY a)
- Batch: [Polygonscan NFT 10](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/10), status Confirmed, quantity 12, held by `0xbd55baab51cae4e9e30387c447650eef38419fba`
- TCO2: [`0xbd55baab51cae4e9e30387c447650eef38419fba`](https://polygonscan.com/address/0xbd55baab51cae4e9e30387c447650eef38419fba), VCS-905, vintage 2013-01-01..2013-12-31
- Serial: `11015-267732157-267732168-VCS-VCU-279-VER-TR-1-905-01012013-31122013-0` (units 267732157..267732168, 12, project 905)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): retirements: RETIRED, 12 units, project 905, vintage 2013, retired 2021-10-13, remark `TOUCAN-1.0-137-0xfdeeb63eeeea158a95dde665a9e0e04af96103dd1494d31b3c76fa13fb85338e-10`
- Verdict: **MATCHED** / `ALL_FIELDS_MATCH`: Retired on Verra; 12 units, project VCS-905, vintage 2013-01-01..2013-12-31 match the batch and its TCO2
- As of: 2026-10-18T07:41:00Z (fetch) and block 95735897
- Research (block 95733573): MATCHED / `ALL_FIELDS_MATCH` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #3, tx [`0xb3425c98caf8e37735c3d9b7349e41170b33365a455223ae8035583e98fd8009`](https://explorer-studio-dev.genlayer.com/tx/0xb3425c98caf8e37735c3d9b7349e41170b33365a455223ae8035583e98fd8009), filed by `0x15a54fa8b0b9e37795f959b0e5bc44db26466b4d`

## S04: batch 23, MATCHED

- Why chosen: Confirmed, fractionalized, retired on Verra (FEASIBILITY a)
- Batch: [Polygonscan NFT 23](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/23), status Confirmed, quantity 27569, held by `0x0c29deaa1383c88712af1083ab8328a1e3661b17`
- TCO2: [`0x0c29deaa1383c88712af1083ab8328a1e3661b17`](https://polygonscan.com/address/0x0c29deaa1383c88712af1083ab8328a1e3661b17), VCS-535, vintage 2014-01-01..2014-12-31
- Serial: `8842-48567832-48595400-VCS-VCU-279-VER-TR-1-535-01012014-31122014-0` (units 48567832..48595400, 27569, project 535)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): retirements: RETIRED, 27569 units, project 535, vintage 2014, retired 2021-10-13, remark `TOUCAN-1.0-137-0xa64d4420c25d71cc6249e9929f5896c20c43c635c7b1d676ff701268253a6ebd-23`
- Verdict: **MATCHED** / `ALL_FIELDS_MATCH`: Retired on Verra; 27569 units, project VCS-535, vintage 2014-01-01..2014-12-31 match the batch and its TCO2
- As of: 2026-10-18T07:41:20Z (fetch) and block 95735897
- Research (block 95733573): MATCHED / `ALL_FIELDS_MATCH` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #4, tx [`0x9e9e9ba5caa3b80bcd05d5f5409bb6c4fa20ed77f9375ed234989629299f9d65`](https://explorer-studio-dev.genlayer.com/tx/0x9e9e9ba5caa3b80bcd05d5f5409bb6c4fa20ed77f9375ed234989629299f9d65), filed by `0x15a54fa8b0b9e37795f959b0e5bc44db26466b4d`

## S05: batch 100, MATCHED

- Why chosen: Confirmed, fractionalized, retired on Verra (FEASIBILITY a)
- Batch: [Polygonscan NFT 100](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/100), status Confirmed, quantity 3367, held by `0x1006b2cf2872ebf1bb075642c16bc35816ec18d5`
- TCO2: [`0x1006b2cf2872ebf1bb075642c16bc35816ec18d5`](https://polygonscan.com/address/0x1006b2cf2872ebf1bb075642c16bc35816ec18d5), VCS-836, vintage 2012-03-01..2012-12-31
- Serial: `10851-251565784-251569150-VCS-VCU-291-VER-VN-1-836-01032012-31122012-0` (units 251565784..251569150, 3367, project 836)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): retirements: RETIRED, 3367 units, project 836, vintage 2012, retired 2021-10-15, remark `TOUCAN-1.0-137-0x9fd0f3f52e7ad0db0e994f266eaab655b62dcca6cbd8659f72629fedf0f6aad3-100`
- Verdict: **MATCHED** / `ALL_FIELDS_MATCH`: Retired on Verra; 3367 units, project VCS-836, vintage 2012-03-01..2012-12-31 match the batch and its TCO2
- As of: 2026-10-18T07:41:46Z (fetch) and block 95735897
- Research (block 95733573): MATCHED / `ALL_FIELDS_MATCH` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #5, tx [`0x56360e548a9ebf7658bde65aa975fc43e0a13f5b9ec582f2b22dd1230e43ad06`](https://explorer-studio-dev.genlayer.com/tx/0x56360e548a9ebf7658bde65aa975fc43e0a13f5b9ec582f2b22dd1230e43ad06), filed by `0x15a54fa8b0b9e37795f959b0e5bc44db26466b4d`

## S06: batch 256, MATCHED

- Why chosen: Confirmed, fractionalized, retired on Verra (FEASIBILITY a)
- Batch: [Polygonscan NFT 256](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/256), status Confirmed, quantity 23064, held by `0x26c76a9848c24b4a7d17f69ec6b8c989f7c66c1d`
- TCO2: [`0x26c76a9848c24b4a7d17f69ec6b8c989f7c66c1d`](https://polygonscan.com/address/0x26c76a9848c24b4a7d17f69ec6b8c989f7c66c1d), VCS-2097, vintage 2015-08-13..2015-12-31
- Serial: `10972-262954541-262977604-VCS-VCU-1317-VER-TR-1-2097-13082015-31122015-0` (units 262954541..262977604, 23064, project 2097)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): retirements: RETIRED, 23064 units, project 2097, vintage 2015, retired 2021-10-18, remark `TOUCAN-1.0-137-0x814ded9896245bb09ba4f8e68f9546da3b506f5eb62280e061fbdb9e79be63eb-256`
- Verdict: **MATCHED** / `ALL_FIELDS_MATCH`: Retired on Verra; 23064 units, project VCS-2097, vintage 2015-08-13..2015-12-31 match the batch and its TCO2
- As of: 2026-10-18T07:42:05Z (fetch) and block 95735897
- Research (block 95733573): MATCHED / `ALL_FIELDS_MATCH` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #6, tx [`0x4d0a562625e00502b054e31977fb622e5380897e5953182fafba3a84b2df424f`](https://explorer-studio-dev.genlayer.com/tx/0x4d0a562625e00502b054e31977fb622e5380897e5953182fafba3a84b2df424f), filed by `0xd173c78cfed46e67bf8c37330458d92a800343e5`

## S07: batch 259, MATCHED

- Why chosen: Confirmed, fractionalized, retired on Verra (FEASIBILITY a)
- Batch: [Polygonscan NFT 259](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/259), status Confirmed, quantity 77600, held by `0x87d0558de28926b4ad8fcc19f039b72a76ea2f95`
- TCO2: [`0x87d0558de28926b4ad8fcc19f039b72a76ea2f95`](https://polygonscan.com/address/0x87d0558de28926b4ad8fcc19f039b72a76ea2f95), VCS-917, vintage 2014-03-08..2014-12-31
- Serial: `10996-264559150-264636749-VCS-VCU-290-VER-TR-1-917-08032014-31122014-0` (units 264559150..264636749, 77600, project 917)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): retirements: RETIRED, 77600 units, project 917, vintage 2014, retired 2021-10-18, remark `TOUCAN-1.0-137-0x6fe091364f1fd9513c62b9717f23647404f598fbc2ceaf90defb02de895e0da1-259`
- Verdict: **MATCHED** / `ALL_FIELDS_MATCH`: Retired on Verra; 77600 units, project VCS-917, vintage 2014-03-08..2014-12-31 match the batch and its TCO2
- As of: 2026-10-18T07:42:27Z (fetch) and block 95735897
- Research (block 95733573): MATCHED / `ALL_FIELDS_MATCH` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #7, tx [`0x6b84916db67c899bbcb564667463090be667f3be3343327a83b7c8b73e823ebe`](https://explorer-studio-dev.genlayer.com/tx/0x6b84916db67c899bbcb564667463090be667f3be3343327a83b7c8b73e823ebe), filed by `0xd173c78cfed46e67bf8c37330458d92a800343e5`

## S08: batch 313, MATCHED

- Why chosen: Confirmed, fractionalized, retired on Verra (FEASIBILITY a)
- Batch: [Polygonscan NFT 313](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/313), status Confirmed, quantity 3155, held by `0x64de5c0a430b2b15c6a3a7566c3930e1cf9b22df`
- TCO2: [`0x64de5c0a430b2b15c6a3a7566c3930e1cf9b22df`](https://polygonscan.com/address/0x64de5c0a430b2b15c6a3a7566c3930e1cf9b22df), VCS-1190, vintage 2018-01-01..2018-05-31
- Serial: `7236-378945249-378948403-VCU-034-APX-IN-1-1190-01012018-31052018-0` (units 378945249..378948403, 3155, project 1190)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): retirements: RETIRED, 3155 units, project 1190, vintage 2018, retired 2021-10-19, remark `TOUCAN-1.0-137-0xed1c54bf9982d83dbd5e308393f46b890f5b5dbbc9e41871ba0f3611ea20618e-313`
- Verdict: **MATCHED** / `ALL_FIELDS_MATCH`: Retired on Verra; 3155 units, project VCS-1190, vintage 2018-01-01..2018-05-31 match the batch and its TCO2
- As of: 2026-10-18T07:42:46Z (fetch) and block 95735897
- Research (block 95733573): MATCHED / `ALL_FIELDS_MATCH` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #8, tx [`0xf8033a96b7d6cf586b43c7726d418aae43b82b6b67dbd297af07076275760587`](https://explorer-studio-dev.genlayer.com/tx/0xf8033a96b7d6cf586b43c7726d418aae43b82b6b67dbd297af07076275760587), filed by `0xd173c78cfed46e67bf8c37330458d92a800343e5`

## S09: batch 889, MATCHED

- Why chosen: Confirmed, fractionalized, retired on Verra (FEASIBILITY a)
- Batch: [Polygonscan NFT 889](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/889), status Confirmed, quantity 4000, held by `0xc49c0eafd92753a552cc5f90ccce0dc27ada8c73`
- TCO2: [`0xc49c0eafd92753a552cc5f90ccce0dc27ada8c73`](https://polygonscan.com/address/0xc49c0eafd92753a552cc5f90ccce0dc27ada8c73), VCS-476, vintage 2008-02-01..2009-02-17
- Serial: `1104-48565711-48569710-VCU-010-APX-CN-1-476-01022008-17022009-0` (units 48565711..48569710, 4000, project 476)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): retirements: RETIRED, 4000 units, project 476, vintage 2008 - 2009, retired 2021-12-22, remark `TOUCAN-1.0-137-0xc966ccad54bc0bdee9b8ed461cb46abd4db02dbf6b78d8bfdfcd7f2094fcc74c-889`
- Verdict: **MATCHED** / `ALL_FIELDS_MATCH`: Retired on Verra; 4000 units, project VCS-476, vintage 2008-02-01..2009-02-17 match the batch and its TCO2
- As of: 2026-10-18T07:43:06Z (fetch) and block 95735897
- Research (block 95733573): MATCHED / `ALL_FIELDS_MATCH` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #9, tx [`0x586a80ecca05a9ed929278b3679580db2a41dbc9c011e804c5576346c0f3761c`](https://explorer-studio-dev.genlayer.com/tx/0x586a80ecca05a9ed929278b3679580db2a41dbc9c011e804c5576346c0f3761c), filed by `0xd173c78cfed46e67bf8c37330458d92a800343e5`

## S10: batch 1000, MATCHED

- Why chosen: Confirmed, fractionalized, retired on Verra (FEASIBILITY a)
- Batch: [Polygonscan NFT 1000](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1000), status Confirmed, quantity 5000, held by `0xccacc6099debd9654c6814fcb800431ef7549b10`
- TCO2: [`0xccacc6099debd9654c6814fcb800431ef7549b10`](https://polygonscan.com/address/0xccacc6099debd9654c6814fcb800431ef7549b10), VCS-191, vintage 2009-01-01..2009-12-31
- Serial: `12078-382273659-382278658-VCS-VCU-304-VER-CN-1-191-01012009-31122009-0` (units 382273659..382278658, 5000, project 191)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): retirements: RETIRED, 5000 units, project 191, vintage 2009, retired 2022-01-25, remark `TOUCAN-1.0-137-0x435e7bbf0ef3944251ade91232370ff464b099ed22984c7cb03235e1c7636a21-1000`
- Verdict: **MATCHED** / `ALL_FIELDS_MATCH`: Retired on Verra; 5000 units, project VCS-191, vintage 2009-01-01..2009-12-31 match the batch and its TCO2
- As of: 2026-10-18T07:43:26Z (fetch) and block 95735897
- Research (block 95733573): MATCHED / `ALL_FIELDS_MATCH` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #10, tx [`0x950aa53daba2169045957879a193e084691201a104c74dda2d84f5b9c10d93f7`](https://explorer-studio-dev.genlayer.com/tx/0x950aa53daba2169045957879a193e084691201a104c74dda2d84f5b9c10d93f7), filed by `0xd173c78cfed46e67bf8c37330458d92a800343e5`

## S11: batch 68, MISMATCH

- Why chosen: real non-MATCHED case: serial project differs from its TCO2
- Batch: [Polygonscan NFT 68](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/68), status Confirmed, quantity 1, held by `0x1bdf022e0cf838eb3c777e3e502db9e4029962c8`
- TCO2: [`0x1bdf022e0cf838eb3c777e3e502db9e4029962c8`](https://polygonscan.com/address/0x1bdf022e0cf838eb3c777e3e502db9e4029962c8), VCS-981, vintage 2016-01-01..2016-12-31
- Serial: `6359-303397758-303397758-VCU-016-APX-ID-14-1477-01012017-31122017-1` (units 303397758..303397758, 1, project 1477)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **MISMATCH** / `SERIAL_PROJECT_MISMATCH`: the serial names project VCS-1477, the TCO2 says VCS-981
- As of: 2026-10-18T07:43:57Z (fetch) and block 95735897
- Research (block 95733573): MISMATCH / `SERIAL_PROJECT_MISMATCH` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #11, tx [`0x8abe725e1b000c91ddd0d866c274c8bec88536c2cf3489cccc060e652664ec0f`](https://explorer-studio-dev.genlayer.com/tx/0x8abe725e1b000c91ddd0d866c274c8bec88536c2cf3489cccc060e652664ec0f), filed by `0x6b3c853083e989a71bbcfd35c0bb0631f57d42ab`

## S12: batch 180, MISMATCH

- Why chosen: real non-MATCHED case: serial project differs from its TCO2
- Batch: [Polygonscan NFT 180](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/180), status Confirmed, quantity 99943, held by `0x206276a00b570e36d4a0ee1023a00754f30dbfb8`
- TCO2: [`0x206276a00b570e36d4a0ee1023a00754f30dbfb8`](https://polygonscan.com/address/0x206276a00b570e36d4a0ee1023a00754f30dbfb8), VCS-699, vintage 2009-01-01..2009-05-09
- Serial: `10448-217035889-217135831-VCS-VCU-1491-VER-BR-1-10-01012013-31122013-0` (units 217035889..217135831, 99943, project 10)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **MISMATCH** / `SERIAL_PROJECT_MISMATCH`: the serial names project VCS-10, the TCO2 says VCS-699
- As of: 2026-10-18T07:44:16Z (fetch) and block 95735897
- Research (block 95733573): MISMATCH / `SERIAL_PROJECT_MISMATCH` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #12, tx [`0x7037af8d6f4f16b6c4f3771872b72d990bae31a724116e1c835f3f962cc25ef6`](https://explorer-studio-dev.genlayer.com/tx/0x7037af8d6f4f16b6c4f3771872b72d990bae31a724116e1c835f3f962cc25ef6), filed by `0x6b3c853083e989a71bbcfd35c0bb0631f57d42ab`

## S13: batch 39, UNVERIFIABLE

- Why chosen: real non-MATCHED case: exact serial not on Verra
- Batch: [Polygonscan NFT 39](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/39), status Confirmed, quantity 45000, held by `0x3b28baae3987502b436f6f37d1bcd7b87b517b27`
- TCO2: [`0x3b28baae3987502b436f6f37d1bcd7b87b517b27`](https://polygonscan.com/address/0x3b28baae3987502b436f6f37d1bcd7b87b517b27), VCS-1566, vintage 2019-01-01..2019-12-31
- Serial: `11377-323597077-323642076-VCS-VCU-394-VER-CO-14-1566-01012019-31122019-0` (units 323597077..323642076, 45000, project 1566)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): no record with this exact serial
- Verdict: **UNVERIFIABLE** / `VERRA_NOT_FOUND`: the Verra registry lists no retired or active units with this exact serial
- As of: 2026-10-18T07:44:36Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `VERRA_NOT_FOUND` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #13, tx [`0xf7e375a08f762cb0c20d9815cf937e2bfca0fdcee5350f49255a1832d34d85d5`](https://explorer-studio-dev.genlayer.com/tx/0xf7e375a08f762cb0c20d9815cf937e2bfca0fdcee5350f49255a1832d34d85d5), filed by `0x6b3c853083e989a71bbcfd35c0bb0631f57d42ab`

## S14: batch 594, UNVERIFIABLE

- Why chosen: real non-MATCHED case: exact serial not on Verra
- Batch: [Polygonscan NFT 594](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/594), status Confirmed, quantity 100, held by `0x1ed9a5565e4192ebc076a0d309a62c1c73b7f61b`
- TCO2: [`0x1ed9a5565e4192ebc076a0d309a62c1c73b7f61b`](https://polygonscan.com/address/0x1ed9a5565e4192ebc076a0d309a62c1c73b7f61b), VCS-1883, vintage 2018-01-01..2018-12-31
- Serial: `7139-373861979-373862078-VCU-048-APX-EC-13-1883-01012018-31122018-0` (units 373861979..373862078, 100, project 1883)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): no record with this exact serial
- Verdict: **UNVERIFIABLE** / `VERRA_NOT_FOUND`: the Verra registry lists no retired or active units with this exact serial
- As of: 2026-10-18T07:44:55Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `VERRA_NOT_FOUND` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #14, tx [`0x9ab43affc514cf9d2dae4127317ac946e77ff967bc9634a070030e18a9393cab`](https://explorer-studio-dev.genlayer.com/tx/0x9ab43affc514cf9d2dae4127317ac946e77ff967bc9634a070030e18a9393cab), filed by `0x6b3c853083e989a71bbcfd35c0bb0631f57d42ab`

## S15: batch 686, UNVERIFIABLE

- Why chosen: real non-MATCHED case: exact serial not on Verra
- Batch: [Polygonscan NFT 686](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/686), status Confirmed, quantity 50, held by `0x1ed9a5565e4192ebc076a0d309a62c1c73b7f61b`
- TCO2: [`0x1ed9a5565e4192ebc076a0d309a62c1c73b7f61b`](https://polygonscan.com/address/0x1ed9a5565e4192ebc076a0d309a62c1c73b7f61b), VCS-1883, vintage 2018-01-01..2018-12-31
- Serial: `7139-373856717-373856766-VCU-048-APX-EC-13-1883-01012018-31122018-0` (units 373856717..373856766, 50, project 1883)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): no record with this exact serial
- Verdict: **UNVERIFIABLE** / `VERRA_NOT_FOUND`: the Verra registry lists no retired or active units with this exact serial
- As of: 2026-10-18T07:45:15Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `VERRA_NOT_FOUND` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #15, tx [`0x575ca43cbdfb03e0ec1697ad261cca77cc51967e7e92bcd17e94a833cd2c79cc`](https://explorer-studio-dev.genlayer.com/tx/0x575ca43cbdfb03e0ec1697ad261cca77cc51967e7e92bcd17e94a833cd2c79cc), filed by `0x6b3c853083e989a71bbcfd35c0bb0631f57d42ab`

## S16: batch 874, UNVERIFIABLE

- Why chosen: real non-MATCHED case: exact serial not on Verra
- Batch: [Polygonscan NFT 874](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/874), status Confirmed, quantity 300, held by `0xf29aac9817fa56fc321d50a0940bd06df6e98791`
- TCO2: [`0xf29aac9817fa56fc321d50a0940bd06df6e98791`](https://polygonscan.com/address/0xf29aac9817fa56fc321d50a0940bd06df6e98791), VCS-1935, vintage 2017-01-01..2017-12-31
- Serial: `9918-159433015-159433314-VCS-VCU-324-VER-CN-14-1935-01012017-31122017-0` (units 159433015..159433314, 300, project 1935)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): no record with this exact serial
- Verdict: **UNVERIFIABLE** / `VERRA_NOT_FOUND`: the Verra registry lists no retired or active units with this exact serial
- As of: 2026-10-18T07:45:34Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `VERRA_NOT_FOUND` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #16, tx [`0xa1f5c512af49de5f90fade77b9c3c905515f3f064e0c531142c417192305ddf1`](https://explorer-studio-dev.genlayer.com/tx/0xa1f5c512af49de5f90fade77b9c3c905515f3f064e0c531142c417192305ddf1), filed by `0xd21c1986ed66353ea389182f86b1f22be4e433a4`

## S17: batch 1213, UNVERIFIABLE

- Why chosen: real non-MATCHED case: exact serial not on Verra
- Batch: [Polygonscan NFT 1213](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1213), status Confirmed, quantity 5000, held by `0xc42cb8538e0dea6459c5965876131120ba96122e`
- TCO2: [`0xc42cb8538e0dea6459c5965876131120ba96122e`](https://polygonscan.com/address/0xc42cb8538e0dea6459c5965876131120ba96122e), VCS-1715, vintage 2013-01-01..2013-12-31
- Serial: `12286-398946449-398951448-VCS-VCU-323-VER-CN-14-1715-01012013-31122013-0` (units 398946449..398951448, 5000, project 1715)
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): no record with this exact serial
- Verdict: **UNVERIFIABLE** / `VERRA_NOT_FOUND`: the Verra registry lists no retired or active units with this exact serial
- As of: 2026-10-18T07:46:00Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `VERRA_NOT_FOUND` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #17, tx [`0xc7a7b0b617440c0f51c408b954a6ff89f757a7680f1230b6b0a7b12d2211c487`](https://explorer-studio-dev.genlayer.com/tx/0xc7a7b0b617440c0f51c408b954a6ff89f757a7680f1230b6b0a7b12d2211c487), filed by `0xd21c1986ed66353ea389182f86b1f22be4e433a4`

## S18: batch 3, UNVERIFIABLE

- Why chosen: real non-MATCHED case: Confirmed but held by a wallet
- Batch: [Polygonscan NFT 3](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/3), status Confirmed, quantity 3, held by `0x25bdff8db8d80971935a7f38a0cf31dec62f7696`
- TCO2: [`0x64de5c0a430b2b15c6a3a7566c3930e1cf9b22df`](https://polygonscan.com/address/0x64de5c0a430b2b15c6a3a7566c3930e1cf9b22df), , vintage ..
- Serial: `7236-378945246-378945248-VCU-034-APX-IN-1-1190-01012018-31052018-0`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `BATCH_NOT_FRACTIONALIZED`: the batch is held by 0x25bdff8db8d80971935a7f38a0cf31dec62f7696, not by its TCO2
- As of: 2026-10-18T07:46:26Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `BATCH_NOT_FRACTIONALIZED` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #18, tx [`0xf37391826471fbafebf7fd32452232033522b56460d582008f529576348ad1ed`](https://explorer-studio-dev.genlayer.com/tx/0xf37391826471fbafebf7fd32452232033522b56460d582008f529576348ad1ed), filed by `0xd21c1986ed66353ea389182f86b1f22be4e433a4`

## S19: batch 138, UNVERIFIABLE

- Why chosen: real non-MATCHED case: Confirmed but held by a wallet
- Batch: [Polygonscan NFT 138](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/138), status Confirmed, quantity 1, held by `0x25bdff8db8d80971935a7f38a0cf31dec62f7696`
- TCO2: [`0xdbcb00bde2a7f1094688f59bf257374947911f5a`](https://polygonscan.com/address/0xdbcb00bde2a7f1094688f59bf257374947911f5a), , vintage ..
- Serial: `10749-246307571-246307571-VCS-VCU-352-VER-BZ-14-812-01012009-31122009-0`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `BATCH_NOT_FRACTIONALIZED`: the batch is held by 0x25bdff8db8d80971935a7f38a0cf31dec62f7696, not by its TCO2
- As of: 2026-10-18T07:46:47Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `BATCH_NOT_FRACTIONALIZED` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #19, tx [`0x41ec3e8c179f4135ae66943390b9e10ea8fba930f52dcff16b81bc502081083a`](https://explorer-studio-dev.genlayer.com/tx/0x41ec3e8c179f4135ae66943390b9e10ea8fba930f52dcff16b81bc502081083a), filed by `0xd21c1986ed66353ea389182f86b1f22be4e433a4`

## S20: batch 446, UNVERIFIABLE

- Why chosen: real non-MATCHED case: Confirmed but held by a wallet
- Batch: [Polygonscan NFT 446](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/446), status Confirmed, quantity 10000, held by `0xdb97aa9b0c07254ef9e017641f5da271e5c31f35`
- TCO2: [`0x354e2edcfbcd2f3b5fdce8cad3730408c052804e`](https://polygonscan.com/address/0x354e2edcfbcd2f3b5fdce8cad3730408c052804e), , vintage ..
- Serial: `5876-264591927-264599176-VCU-013-APX-CN-14-1542-01012013-31122013-0,5876-264599177-264601926-VCU-013-APX-CN-14-1542-01012013-311`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `BATCH_NOT_FRACTIONALIZED`: the batch is held by 0xdb97aa9b0c07254ef9e017641f5da271e5c31f35, not by its TCO2
- As of: 2026-10-18T07:47:07Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `BATCH_NOT_FRACTIONALIZED` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #20, tx [`0x7866c3adf29bf0acbdfa0e616dfdf2c81e3e8eee064b8670e10c9720407ca5ab`](https://explorer-studio-dev.genlayer.com/tx/0x7866c3adf29bf0acbdfa0e616dfdf2c81e3e8eee064b8670e10c9720407ca5ab), filed by `0xd21c1986ed66353ea389182f86b1f22be4e433a4`

## S21: batch 798, UNVERIFIABLE

- Why chosen: real non-MATCHED case: Confirmed but held by a wallet
- Batch: [Polygonscan NFT 798](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/798), status Confirmed, quantity 1, held by `0xe2da2b0691fc74c3bbbe8305581308b0dc61ee30`
- TCO2: [`0x42f3148d4a93a030978e2f909ccc6626dc8e2aed`](https://polygonscan.com/address/0x42f3148d4a93a030978e2f909ccc6626dc8e2aed), , vintage ..
- Serial: `2973-131635188-131635188-VCU-028-MER-CN-1-1044-20122010-31122010-0`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `BATCH_NOT_FRACTIONALIZED`: the batch is held by 0xe2da2b0691fc74c3bbbe8305581308b0dc61ee30, not by its TCO2
- As of: 2026-10-18T07:47:35Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `BATCH_NOT_FRACTIONALIZED` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #21, tx [`0x03923a22b60addaf7ff285f9db62d77d8a5a12a346b1022376d3e15657364119`](https://explorer-studio-dev.genlayer.com/tx/0x03923a22b60addaf7ff285f9db62d77d8a5a12a346b1022376d3e15657364119), filed by `0x9c023ed7d4ca3b5287944b546fba6aa2a93748bd`

## S22: batch 833, UNVERIFIABLE

- Why chosen: real non-MATCHED case: Confirmed but held by a wallet
- Batch: [Polygonscan NFT 833](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/833), status Confirmed, quantity 1, held by `0x63a32f1595a68e811496d820680b74a5cca303c5`
- TCO2: [`0xe47838cb5874da9b8a40107abbf4edf75a7e7ba0`](https://polygonscan.com/address/0xe47838cb5874da9b8a40107abbf4edf75a7e7ba0), , vintage ..
- Serial: `11419-326998327-326998327-VCS-VCU-261-VER-BR-14-875-01012016-31122016-1`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `BATCH_NOT_FRACTIONALIZED`: the batch is held by 0x63a32f1595a68e811496d820680b74a5cca303c5, not by its TCO2
- As of: 2026-10-18T07:47:55Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `BATCH_NOT_FRACTIONALIZED` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #22, tx [`0x28f524f03a6ace45207c45d645ea4b136fcda66aeef5c5a79b6356cd5b1b440c`](https://explorer-studio-dev.genlayer.com/tx/0x28f524f03a6ace45207c45d645ea4b136fcda66aeef5c5a79b6356cd5b1b440c), filed by `0x9c023ed7d4ca3b5287944b546fba6aa2a93748bd`

## S23: batch 1001, UNVERIFIABLE

- Why chosen: real non-MATCHED case: Confirmed but held by a wallet
- Batch: [Polygonscan NFT 1001](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1001), status Confirmed, quantity 700, held by `0x10080bb62dafe52753af9d6bdd0bd14ac313bf43`
- TCO2: [`0xf29aac9817fa56fc321d50a0940bd06df6e98791`](https://polygonscan.com/address/0xf29aac9817fa56fc321d50a0940bd06df6e98791), , vintage ..
- Serial: `9918-159433315-159434014-VCS-VCU-324-VER-CN-14-1935-01012017-31122017-0`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `BATCH_NOT_FRACTIONALIZED`: the batch is held by 0x10080bb62dafe52753af9d6bdd0bd14ac313bf43, not by its TCO2
- As of: 2026-10-18T07:48:22Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `BATCH_NOT_FRACTIONALIZED` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #23, tx [`0x1c05e4a5b8c6d84f96c222ca6b6b295d93c00a1bec83f295ef0baa8f6f34e798`](https://explorer-studio-dev.genlayer.com/tx/0x1c05e4a5b8c6d84f96c222ca6b6b295d93c00a1bec83f295ef0baa8f6f34e798), filed by `0x9c023ed7d4ca3b5287944b546fba6aa2a93748bd`

## S24: batch 217, UNVERIFIABLE

- Why chosen: real non-MATCHED case: no TCO2 from the Verra factory
- Batch: [Polygonscan NFT 217](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/217), status Confirmed, quantity 16326, held by `0xb208e3dcc8e2b091fa4b9aa65d528fdfdc8bfa93`
- TCO2: (none)
- Serial: `10763-246981648-246997973-VCS-VCU-259-VER-IN-1-132-01012012-31122012-0`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `TCO2_NOT_FOUND`: the official factory maps this batch's vintage to no TCO2
- As of: 2026-10-18T07:48:42Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `TCO2_NOT_FOUND` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #24, tx [`0x43980ded10ebe8c4f2fdac626483ace0b8122f13c548b271ae07e76f21aeba91`](https://explorer-studio-dev.genlayer.com/tx/0x43980ded10ebe8c4f2fdac626483ace0b8122f13c548b271ae07e76f21aeba91), filed by `0x9c023ed7d4ca3b5287944b546fba6aa2a93748bd`

## S25: batch 1713, UNVERIFIABLE

- Why chosen: real non-MATCHED case: no TCO2 from the Verra factory
- Batch: [Polygonscan NFT 1713](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1713), status Confirmed, quantity 5, held by `0x6960ce1d21f63c4971324b5b611c4de29acf980c`
- TCO2: (none)
- Serial: `643002406801000010000000192331-643002406801000010000000192335`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `TCO2_NOT_FOUND`: the official factory maps this batch's vintage to no TCO2
- As of: 2026-10-18T07:49:09Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `TCO2_NOT_FOUND` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #25, tx [`0xc7624c2627745ebc0df66f960e25d0d1cdf0903890dd99adb40c6d9aaec804fd`](https://explorer-studio-dev.genlayer.com/tx/0xc7624c2627745ebc0df66f960e25d0d1cdf0903890dd99adb40c6d9aaec804fd), filed by `0x9c023ed7d4ca3b5287944b546fba6aa2a93748bd`

## S26: batch 1715, UNVERIFIABLE

- Why chosen: real non-MATCHED case: no TCO2 from the Verra factory
- Batch: [Polygonscan NFT 1715](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1715), status Confirmed, quantity 5, held by `0x42f37cd772e3dd2686a34f7bbbbac710f497920a`
- TCO2: (none)
- Serial: `643002406801000010000000195465-643002406801000010000000195469`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `TCO2_NOT_FOUND`: the official factory maps this batch's vintage to no TCO2
- As of: 2026-10-18T07:49:29Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `TCO2_NOT_FOUND` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #26, tx [`0x4236ad032cfb04ec99e726f3cb78c13cebdae00a04ad8bf76c6f91b6d5bf68a5`](https://explorer-studio-dev.genlayer.com/tx/0x4236ad032cfb04ec99e726f3cb78c13cebdae00a04ad8bf76c6f91b6d5bf68a5), filed by `0x55db82a5d8cb62802c6ef41cd637e88ae04320f7`

## S27: batch 1717, UNVERIFIABLE

- Why chosen: real non-MATCHED case: no TCO2 from the Verra factory
- Batch: [Polygonscan NFT 1717](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1717), status Confirmed, quantity 1, held by `0x9bbc1563fa8a2267ee0c846c591208160afb0b34`
- TCO2: (none)
- Serial: `926aeaf2-5603-4388-a6fe-53af6108c34a_643002406801000010000000213789-643002406801000010000000213789`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `TCO2_NOT_FOUND`: the official factory maps this batch's vintage to no TCO2
- As of: 2026-10-18T07:49:56Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `TCO2_NOT_FOUND` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #27, tx [`0xa4dafe8b429dbb789f90d0a67e170014064b03ee9089df182741c10dd7cff8b6`](https://explorer-studio-dev.genlayer.com/tx/0xa4dafe8b429dbb789f90d0a67e170014064b03ee9089df182741c10dd7cff8b6), filed by `0x55db82a5d8cb62802c6ef41cd637e88ae04320f7`

## S28: batch 7, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 7](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/7), status Confirmed, quantity 128900, held by `0x62896f42cf1371b268db56e50d67c34f3eb1ad7a`
- TCO2: [`0x62896f42cf1371b268db56e50d67c34f3eb1ad7a`](https://polygonscan.com/address/0x62896f42cf1371b268db56e50d67c34f3eb1ad7a), VCS-674, vintage 2014-07-01..2014-12-31
- Serial: `9380-92545283-92645182-VCS-VCU-263-VER-ID-14-674-01072014-31122014-1,7627-414200938-414229937-VCU-016-MER-ID-14-674-01072014-311`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:50:17Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #28, tx [`0xaa2b2ca2c8ea1694a31a5254238d53415606d63380a7b7116c46cae54441774d`](https://explorer-studio-dev.genlayer.com/tx/0xaa2b2ca2c8ea1694a31a5254238d53415606d63380a7b7116c46cae54441774d), filed by `0x55db82a5d8cb62802c6ef41cd637e88ae04320f7`

## S29: batch 140, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 140](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/140), status Confirmed, quantity 2, held by `0x77c47b081527c999b4603556a8f225d503b6f44a`
- TCO2: [`0x77c47b081527c999b4603556a8f225d503b6f44a`](https://polygonscan.com/address/0x77c47b081527c999b4603556a8f225d503b6f44a), VCS-499, vintage 2009-07-01..2009-12-31
- Serial: `10478-220818842-220818842-VCS-VCU-337-VER-IN-1-499-01072009-31122009-0,10486-221038471-221038471-VCS-VCU-337-VER-IN-1-499-010720`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:50:53Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #29, tx [`0x67b66217cb4c7ff8c4a8a9c7f8e4f464f8d6ab8d4dfa35341a9a1bd579a005d6`](https://explorer-studio-dev.genlayer.com/tx/0x67b66217cb4c7ff8c4a8a9c7f8e4f464f8d6ab8d4dfa35341a9a1bd579a005d6), filed by `0x55db82a5d8cb62802c6ef41cd637e88ae04320f7`

## S30: batch 564, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 564](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/564), status Confirmed, quantity 2821, held by `0xf60ea4c1890cb80ddc60ea49a09580d7f1e1a1d8`
- TCO2: [`0xf60ea4c1890cb80ddc60ea49a09580d7f1e1a1d8`](https://polygonscan.com/address/0xf60ea4c1890cb80ddc60ea49a09580d7f1e1a1d8), VCS-870, vintage 2009-03-30..2009-12-31
- Serial: `2625-114776544-114779362-VCU-010-MER-IN-1-870-30032009-31122009-0,2625-114776542-114776543-VCU-010-MER-IN-1-870-30032009-3112200`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:51:21Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #30, tx [`0x290a9e2625da9a5e9c6ef0e92f91f09e1ad24a1a2847e1f1485dda30004f5421`](https://explorer-studio-dev.genlayer.com/tx/0x290a9e2625da9a5e9c6ef0e92f91f09e1ad24a1a2847e1f1485dda30004f5421), filed by `0x55db82a5d8cb62802c6ef41cd637e88ae04320f7`

## S31: batch 576, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 576](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/576), status Confirmed, quantity 1000, held by `0x6ff91030fbe98af0047934962231eb0c47a64892`
- TCO2: [`0x6ff91030fbe98af0047934962231eb0c47a64892`](https://polygonscan.com/address/0x6ff91030fbe98af0047934962231eb0c47a64892), VCS-486, vintage 2011-01-01..2011-12-31
- Serial: `11813-359885711-359885779-VCS-VCU-842-VER-ID-1-486-01012011-31122011-1,3401-151906516-151907446-VCU-044-MER-ID-1-486-01012011-31`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:51:42Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #31, tx [`0x67b0efa7894215386aba1557649211cdf7f7fca776a71a155271e5e2f701f079`](https://explorer-studio-dev.genlayer.com/tx/0x67b0efa7894215386aba1557649211cdf7f7fca776a71a155271e5e2f701f079), filed by `0x5ca5172a8cf615c92f4936d6fcbe3a27f62bd3df`

## S32: batch 698, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 698](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/698), status Confirmed, quantity 50000, held by `0xeb9dea5c277b3d2eb42a54e3db9e0899d8dfdf96`
- TCO2: [`0xeb9dea5c277b3d2eb42a54e3db9e0899d8dfdf96`](https://polygonscan.com/address/0xeb9dea5c277b3d2eb42a54e3db9e0899d8dfdf96), VCS-1205, vintage 2015-01-01..2015-12-31
- Serial: `11696-351385660-351433474-VCS-VCU-262-VER-TR-1-1205-01012015-31122015-0,11696-351333475-351335659-VCS-VCU-262-VER-TR-1-1205-0101`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:52:03Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #32, tx [`0x6c26ffe0976e9a2f763ea641315e1639f574e1d126d6158829a54ff3f05276fc`](https://explorer-studio-dev.genlayer.com/tx/0x6c26ffe0976e9a2f763ea641315e1639f574e1d126d6158829a54ff3f05276fc), filed by `0x5ca5172a8cf615c92f4936d6fcbe3a27f62bd3df`

## S33: batch 711, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 711](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/711), status Confirmed, quantity 29466, held by `0xb51913749ff2babc2d152023b74c0af50ecf8a10`
- TCO2: [`0xb51913749ff2babc2d152023b74c0af50ecf8a10`](https://polygonscan.com/address/0xb51913749ff2babc2d152023b74c0af50ecf8a10), VCS-929, vintage 2013-11-01..2013-12-31
- Serial: `10861-253225978-253240977-VCS-VCU-208-VER-CA-3-929-01112013-31122013-0,11759-355580695-355595160-VCS-VCU-208-VER-CA-3-929-011120`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:52:24Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #33, tx [`0x49eb82581a0640508fb752740b9c74e6fd398fa65bd9b6ba7a1bcf033bce2e6f`](https://explorer-studio-dev.genlayer.com/tx/0x49eb82581a0640508fb752740b9c74e6fd398fa65bd9b6ba7a1bcf033bce2e6f), filed by `0x5ca5172a8cf615c92f4936d6fcbe3a27f62bd3df`

## S34: batch 712, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 712](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/712), status Confirmed, quantity 134752, held by `0xbe0cd710eaadf41dd5c591c3655f4bd0d50ffbd4`
- TCO2: [`0xbe0cd710eaadf41dd5c591c3655f4bd0d50ffbd4`](https://polygonscan.com/address/0xbe0cd710eaadf41dd5c591c3655f4bd0d50ffbd4), VCS-929, vintage 2014-01-01..2014-12-31
- Serial: `5356-227767822-227768221-VCU-015-APX-CA-3-929-01012014-31122014-0,11761-355630943-355765294-VCS-VCU-208-VER-CA-3-929-01012014-31`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:52:45Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #34, tx [`0x82ceaf3658f83cdfa2bfdada66c2b3f109530705d003f5c8f4ff28a602d1323a`](https://explorer-studio-dev.genlayer.com/tx/0x82ceaf3658f83cdfa2bfdada66c2b3f109530705d003f5c8f4ff28a602d1323a), filed by `0x5ca5172a8cf615c92f4936d6fcbe3a27f62bd3df`

## S35: batch 718, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 718](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/718), status Confirmed, quantity 54189, held by `0xfffce8e66fd470e401fadf3d47ca9ad28e82013a`
- TCO2: [`0xfffce8e66fd470e401fadf3d47ca9ad28e82013a`](https://polygonscan.com/address/0xfffce8e66fd470e401fadf3d47ca9ad28e82013a), VCS-414, vintage 2013-01-01..2013-12-25
- Serial: `10999-265085766-265108839-VCS-VCU-279-VER-CN-1-414-01012013-25122013-0,10999-265108840-265113028-VCS-VCU-279-VER-CN-1-414-010120`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:53:06Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #35, tx [`0x9da1bb95893fc678cc7341eb747760ad7f75cdec657445f0177d47fdb1569d12`](https://explorer-studio-dev.genlayer.com/tx/0x9da1bb95893fc678cc7341eb747760ad7f75cdec657445f0177d47fdb1569d12), filed by `0x5ca5172a8cf615c92f4936d6fcbe3a27f62bd3df`

## S36: batch 719, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 719](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/719), status Confirmed, quantity 48300, held by `0xd1960efc6c907d01ef618e29fe9a31910cfbec66`
- TCO2: [`0xd1960efc6c907d01ef618e29fe9a31910cfbec66`](https://polygonscan.com/address/0xd1960efc6c907d01ef618e29fe9a31910cfbec66), VCS-513, vintage 2014-01-01..2014-12-31
- Serial: `10180-193046847-193091926-VCS-VCU-279-VER-BR-1-513-01012014-31122014-0,7750-426631800-426635019-VCU-005-MER-BR-1-513-01012014-31`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:53:27Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #36, tx [`0xc3e7ba4fe79b8d80157f7bbc95d94ff9d4907b63a361be172b0809e676308c86`](https://explorer-studio-dev.genlayer.com/tx/0xc3e7ba4fe79b8d80157f7bbc95d94ff9d4907b63a361be172b0809e676308c86), filed by `0xb348425c819f7eccd9227812eb3db840e931ca23`

## S37: batch 890, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 890](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/890), status Confirmed, quantity 70000, held by `0x351501415569e372fa36eb115b309dea50289fdc`
- TCO2: [`0x351501415569e372fa36eb115b309dea50289fdc`](https://polygonscan.com/address/0x351501415569e372fa36eb115b309dea50289fdc), VCS-1505, vintage 2011-12-01..2012-10-31
- Serial: `4183-177715521-177735520-VCU-010-APX-UG-1-1505-01122011-31102012-0,4183-177695521-177715520-VCU-010-APX-UG-1-1505-01122011-31102`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:53:50Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #37, tx [`0x39a456989a4cb2ddbc4fcde84b3a5f4bb511db6c61c53ed0684b4507eb2dec36`](https://explorer-studio-dev.genlayer.com/tx/0x39a456989a4cb2ddbc4fcde84b3a5f4bb511db6c61c53ed0684b4507eb2dec36), filed by `0xb348425c819f7eccd9227812eb3db840e931ca23`

## S38: batch 898, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 898](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/898), status Confirmed, quantity 100000, held by `0x0cf0b2c0d780520571c6e4be838b274739c07519`
- TCO2: [`0x0cf0b2c0d780520571c6e4be838b274739c07519`](https://polygonscan.com/address/0x0cf0b2c0d780520571c6e4be838b274739c07519), VCS-1205, vintage 2016-01-01..2016-12-31
- Serial: `11695-351185660-351235659-VCS-VCU-262-VER-TR-1-1205-01012016-31122016-0,11695-351235660-351285659-VCS-VCU-262-VER-TR-1-1205-0101`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:54:18Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #38, tx [`0x1cf9b825d5cd2a654a6a8f5cc15f6bbb40691a7214c7624069adca1d5fb0d88d`](https://explorer-studio-dev.genlayer.com/tx/0x1cf9b825d5cd2a654a6a8f5cc15f6bbb40691a7214c7624069adca1d5fb0d88d), filed by `0xb348425c819f7eccd9227812eb3db840e931ca23`

## S39: batch 910, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 910](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/910), status Confirmed, quantity 30992, held by `0x53697c351d326e9bc50d9947eea1c5a9a92b9c83`
- TCO2: [`0x53697c351d326e9bc50d9947eea1c5a9a92b9c83`](https://polygonscan.com/address/0x53697c351d326e9bc50d9947eea1c5a9a92b9c83), VCS-148, vintage 2012-07-01..2012-12-31
- Serial: `12034-376487681-376498672-VCS-VCU-259-VER-CN-1-148-01072012-31122012-0,12034-376467681-376487680-VCS-VCU-259-VER-CN-1-148-010720`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:54:39Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #39, tx [`0x4f430536b3fa3b89203e13163888dab1b65de64a8a1fcff5498a006db6c150d7`](https://explorer-studio-dev.genlayer.com/tx/0x4f430536b3fa3b89203e13163888dab1b65de64a8a1fcff5498a006db6c150d7), filed by `0xb348425c819f7eccd9227812eb3db840e931ca23`

## S40: batch 934, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 934](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/934), status Confirmed, quantity 25000, held by `0xc7cfca393c969865c70056d0324ee1d7d0dc98ba`
- TCO2: [`0xc7cfca393c969865c70056d0324ee1d7d0dc98ba`](https://polygonscan.com/address/0xc7cfca393c969865c70056d0324ee1d7d0dc98ba), VCS-10, vintage 2013-01-01..2013-12-31
- Serial: `10448-217135832-217140896-VCS-VCU-1491-VER-BR-1-10-01012013-31122013-0,10448-216890897-216905766-VCS-VCU-1491-VER-BR-1-10-010120`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:55:03Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #40, tx [`0x8f7d7c06413272f4524f1b7a7d053b01f041d03356240ebe8b5a7b568d5b61c2`](https://explorer-studio-dev.genlayer.com/tx/0x8f7d7c06413272f4524f1b7a7d053b01f041d03356240ebe8b5a7b568d5b61c2), filed by `0xb348425c819f7eccd9227812eb3db840e931ca23`

## S41: batch 965, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 965](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/965), status Confirmed, quantity 100000, held by `0x48174098315b1b390abda702b5fbc1572714a3ad`
- TCO2: [`0x48174098315b1b390abda702b5fbc1572714a3ad`](https://polygonscan.com/address/0x48174098315b1b390abda702b5fbc1572714a3ad), VCS-1291, vintage 2014-01-01..2018-08-17
- Serial: `11034-271709011-271779010-VCS-VCU-508-VER-IN-1-1291-01012014-17082018-0,11034-271866295-271896294-VCS-VCU-508-VER-IN-1-1291-0101`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:55:27Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #41, tx [`0x8876433f39f92681ffe69cbe10004fbd94e91f62d79e6a6aeeb353a6783b2e17`](https://explorer-studio-dev.genlayer.com/tx/0x8876433f39f92681ffe69cbe10004fbd94e91f62d79e6a6aeeb353a6783b2e17), filed by `0x47e7267ebbd2439d94535cd9f7613fad8f880646`

## S42: batch 977, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 977](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/977), status Confirmed, quantity 100000, held by `0x701f5f7a70a17b141fc2de45ef45e86eeed642fc`
- TCO2: [`0x701f5f7a70a17b141fc2de45ef45e86eeed642fc`](https://polygonscan.com/address/0x701f5f7a70a17b141fc2de45ef45e86eeed642fc), VCS-494, vintage 2009-01-01..2009-09-10
- Serial: `11832-361525338-361575337-VCS-VCU-259-VER-CN-1-494-01012009-10092009-0,11780-356784787-356834786-VCS-VCU-259-VER-CN-1-494-010120`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T07:55:50Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #42, tx [`0xa52a9d0350a74b721c15e085ce32b4edd1397ab78eea0956bc83b6f50edf16ce`](https://explorer-studio-dev.genlayer.com/tx/0xa52a9d0350a74b721c15e085ce32b4edd1397ab78eea0956bc83b6f50edf16ce), filed by `0x47e7267ebbd2439d94535cd9f7613fad8f880646`

## S43: batch 1163, UNVERIFIABLE

- Why chosen: real non-MATCHED case: serial field holds several serials
- Batch: [Polygonscan NFT 1163](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1163), status Confirmed, quantity 3845, held by `0xfbc5d9620b6bb729be2f72fca157054bd3da3d1a`
- TCO2: [`0xfbc5d9620b6bb729be2f72fca157054bd3da3d1a`](https://polygonscan.com/address/0xfbc5d9620b6bb729be2f72fca157054bd3da3d1a), VCS-1764, vintage 2020-06-15..2021-06-14
- Serial: `12100-386868267-386871645-VCS-VCU-262-VER-MM-14-1764-15062020-14062021-0,12100-386855404-386855869-VCS-VCU-262-VER-MM-14-1764-15`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T08:02:29Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #43, tx [`0xbb40b89880a5798ecff908a02befb9549204747824f98c308e862fa762cced94`](https://explorer-studio-dev.genlayer.com/tx/0xbb40b89880a5798ecff908a02befb9549204747824f98c308e862fa762cced94), filed by `0x47e7267ebbd2439d94535cd9f7613fad8f880646`

## S44: batch 199, UNVERIFIABLE

- Why chosen: real non-MATCHED case: Confirmed with an empty serial
- Batch: [Polygonscan NFT 199](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/199), status Confirmed, quantity 0, held by `0x04fdf735f31326d05e0ad8078f10b4f4c30885b2`
- TCO2: [`0x04fdf735f31326d05e0ad8078f10b4f4c30885b2`](https://polygonscan.com/address/0x04fdf735f31326d05e0ad8078f10b4f4c30885b2), VCS-722, vintage 2008-10-01..2008-12-31
- Serial: `(empty)`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `SERIAL_UNPARSABLE`: the batch serial is not a well-formed Verra VCU serial
- As of: 2026-10-18T08:15:23Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `SERIAL_UNPARSABLE` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #44, tx [`0xae817158c3ff665a1d545c491c989a6519c202131a245d95ff36394b49ed4696`](https://explorer-studio-dev.genlayer.com/tx/0xae817158c3ff665a1d545c491c989a6519c202131a245d95ff36394b49ed4696), filed by `0x47e7267ebbd2439d94535cd9f7613fad8f880646`

## S45: batch 1, UNVERIFIABLE

- Why chosen: real non-MATCHED case: Pending, empty serial
- Batch: [Polygonscan NFT 1](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1), status Pending, quantity 0, held by `0x7262a4e14ced289795097deaf32c845cabad2403`
- TCO2: (none)
- Serial: `(empty)`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `BATCH_NOT_CONFIRMED`: the batch is Pending, not Confirmed
- As of: 2026-10-18T08:18:52Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `BATCH_NOT_CONFIRMED` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #45, tx [`0xd7847001e381eb788c7191cd2f28e29a99983b75cce91558fe266b265ed01a7f`](https://explorer-studio-dev.genlayer.com/tx/0xd7847001e381eb788c7191cd2f28e29a99983b75cce91558fe266b265ed01a7f), filed by `0x47e7267ebbd2439d94535cd9f7613fad8f880646`

## S46: batch 1350, UNVERIFIABLE

- Why chosen: real non-MATCHED case: Pending, serial starts with the text \u0031
- Batch: [Polygonscan NFT 1350](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1350), status Pending, quantity 0, held by `0x8a303833908bfdafa68c4da9cb5c80501d628799`
- TCO2: (none)
- Serial: `\u00311015-267732157-267732168-VCS-VCU-279-VER-TR-1-905-01012013-31122013-0`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `BATCH_NOT_CONFIRMED`: the batch is Pending, not Confirmed
- As of: 2026-10-18T08:19:14Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `BATCH_NOT_CONFIRMED` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #46, tx [`0x8ed9f4f7135f96bf7c5299cbad7697e07aa789e433de777cc3cc04b8ed0a09e6`](https://explorer-studio-dev.genlayer.com/tx/0x8ed9f4f7135f96bf7c5299cbad7697e07aa789e433de777cc3cc04b8ed0a09e6), filed by `0x6d15df503988c08c67dc5f0c9e635ac98cf5a761`

## S47: batch 244, UNVERIFIABLE

- Why chosen: real non-MATCHED case: Rejected, quantity 5e18
- Batch: [Polygonscan NFT 244](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/244), status Rejected, quantity 5000000000000000000, held by `0x99988890f2de1d59e1eb76d2f34cde371044b8c8`
- TCO2: (none)
- Serial: `10972-262954541-262977604-VCS-VCU-1317-VER-TR-1-2097-13082015-31122016-0`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `BATCH_NOT_CONFIRMED`: the batch is Rejected, not Confirmed
- As of: 2026-10-18T08:19:36Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `BATCH_NOT_CONFIRMED` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #47, tx [`0x648bca62206a9e20de712b77ca7422767a658b3793465f39c5e866f6bd3ef29e`](https://explorer-studio-dev.genlayer.com/tx/0x648bca62206a9e20de712b77ca7422767a658b3793465f39c5e866f6bd3ef29e), filed by `0x6d15df503988c08c67dc5f0c9e635ac98cf5a761`

## S48: batch 1716, UNVERIFIABLE

- Why chosen: real non-MATCHED case: DetokenizationFinalized (Puro)
- Batch: [Polygonscan NFT 1716](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1716), status DetokenizationFinalized, quantity 5, held by `0x9bbc1563fa8a2267ee0c846c591208160afb0b34`
- TCO2: (none)
- Serial: `643002406801000010000000213752-643002406801000010000000213756`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `BATCH_NOT_CONFIRMED`: the batch is DetokenizationFinalized, not Confirmed
- As of: 2026-10-18T08:19:58Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `BATCH_NOT_CONFIRMED` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #48, tx [`0x7ee87ef0505a625bc33d8f241150420a23141a70a46634ffe17850a911180116`](https://explorer-studio-dev.genlayer.com/tx/0x7ee87ef0505a625bc33d8f241150420a23141a70a46634ffe17850a911180116), filed by `0x6d15df503988c08c67dc5f0c9e635ac98cf5a761`

## S49: batch 1714, UNVERIFIABLE

- Why chosen: real non-MATCHED case: RetirementFinalized (Puro)
- Batch: [Polygonscan NFT 1714](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/1714), status RetirementFinalized, quantity 143, held by `0x42f37cd772e3dd2686a34f7bbbbac710f497920a`
- TCO2: (none)
- Serial: `643002406801000010000000200721-643002406801000010000000200863`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `BATCH_NOT_CONFIRMED`: the batch is RetirementFinalized, not Confirmed
- As of: 2026-10-18T08:20:22Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `BATCH_NOT_CONFIRMED` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #49, tx [`0x2ee5f3def8ab5f8c805eda1de5084f1a9445c4f5a3f92a8b2a256649a6419beb`](https://explorer-studio-dev.genlayer.com/tx/0x2ee5f3def8ab5f8c805eda1de5084f1a9445c4f5a3f92a8b2a256649a6419beb), filed by `0x6d15df503988c08c67dc5f0c9e635ac98cf5a761`

## S50: batch 2000, UNVERIFIABLE

- Why chosen: token id above batchTokenCounter (1719)
- Batch: [Polygonscan NFT 2000](https://polygonscan.com/nft/0x8A4d7458dDe3023A3B24225D62087701A88b09DD/2000), status (not read), quantity -, held by `-`
- TCO2: (none)
- Serial: `(empty)`
- Polygon block: [95735897](https://polygonscan.com/block/95735897), hash `0x0d8e1cdc13340c565909a87e438de12a928800b4d678113a361e245e5ff4eb2a`, time 2026-10-18T07:39:53.000Z
- Verra (exact serial, https://registry.verra.org/verra/public/program/VCS, Retirements report): not looked up (the check ended before the Verra stage)
- Verdict: **UNVERIFIABLE** / `BATCH_NOT_FOUND`: the batch contract has no such token at this block
- As of: 2026-10-18T08:21:15Z (fetch) and block 95735897
- Research (block 95733573): UNVERIFIABLE / `BATCH_NOT_FOUND` (same)
- On chain: CarbonCheck `0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413` check #50, tx [`0x5b8b13e8afe6672a547100bcc0ac130265b9e96a86b947d0c7c6f813facde311`](https://explorer-studio-dev.genlayer.com/tx/0x5b8b13e8afe6672a547100bcc0ac130265b9e96a86b947d0c7c6f813facde311), filed by `0x6d15df503988c08c67dc5f0c9e635ac98cf5a761`
