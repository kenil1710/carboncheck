# Final check

Run 2026-10-18T08:41:37.851Z by `tools/final_check.mjs` against commit `e204bd4135` and Studio Dev. **10/11 PASS.**

## PASS: Source match: gen_getContractCode byte-identical to contracts/ at HEAD for every deployment, all from one commit, contracts/ unchanged since

```
HEAD e204bd4135982d95486189674c678264a001664c
CarbonCheck          0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413  chain sha256 25e652965e1fc4c9940d06f29d1c56bfbd6d632ad66efcd29065015159936996  identical to HEAD  matches deployments.json  deploy commit 93c92dbc03  contracts/ unchanged since
CarbonCheckDemo      0x019B01259A30467de7bdbFD2125e3d3CE00B08a1  chain sha256 25e652965e1fc4c9940d06f29d1c56bfbd6d632ad66efcd29065015159936996  identical to HEAD  matches deployments.json  deploy commit 93c92dbc03  contracts/ unchanged since
OffsetGate           0x7BF9f7b62f65214f9B65647799507FC9A452409B  chain sha256 26923fbc428e4a6939c07fbd57a0ec22b5c15bc271b8cd4c28894ede6025303c  identical to HEAD  matches deployments.json  deploy commit 93c92dbc03  contracts/ unchanged since
OffsetGateDemo       0x98eF81498Dc820fAb2Db56F112573a6256688348  chain sha256 26923fbc428e4a6939c07fbd57a0ec22b5c15bc271b8cd4c28894ede6025303c  identical to HEAD  matches deployments.json  deploy commit 93c92dbc03  contracts/ unchanged since
all deployments from one commit: 93c92dbc03666bf5fbbb1e5825c73b3f1d835a79
```

## PASS: Seeds: every seed filed on the canonical contract at one Polygon block, final (tx FINALIZED), verdict matching docs/seeds.onchain.json

```
S01 batch 2 check #1 MATCHED/ALL_FIELDS_MATCH at block 95735897 (research: MATCHED/ALL_FIELDS_MATCH) tx 0xc46c754e05 FINALIZED ok
S02 batch 9 check #2 MATCHED/ALL_FIELDS_MATCH at block 95735897 (research: MATCHED/ALL_FIELDS_MATCH) tx 0x7e83b06e21 FINALIZED ok
S03 batch 10 check #3 MATCHED/ALL_FIELDS_MATCH at block 95735897 (research: MATCHED/ALL_FIELDS_MATCH) tx 0xb3425c98ca FINALIZED ok
S04 batch 23 check #4 MATCHED/ALL_FIELDS_MATCH at block 95735897 (research: MATCHED/ALL_FIELDS_MATCH) tx 0x9e9e9ba5ca FINALIZED ok
S05 batch 100 check #5 MATCHED/ALL_FIELDS_MATCH at block 95735897 (research: MATCHED/ALL_FIELDS_MATCH) tx 0x56360e548a FINALIZED ok
S06 batch 256 check #6 MATCHED/ALL_FIELDS_MATCH at block 95735897 (research: MATCHED/ALL_FIELDS_MATCH) tx 0x4d0a562625 FINALIZED ok
S07 batch 259 check #7 MATCHED/ALL_FIELDS_MATCH at block 95735897 (research: MATCHED/ALL_FIELDS_MATCH) tx 0x6b84916db6 FINALIZED ok
S08 batch 313 check #8 MATCHED/ALL_FIELDS_MATCH at block 95735897 (research: MATCHED/ALL_FIELDS_MATCH) tx 0xf8033a96b7 FINALIZED ok
S09 batch 889 check #9 MATCHED/ALL_FIELDS_MATCH at block 95735897 (research: MATCHED/ALL_FIELDS_MATCH) tx 0x586a80ecca FINALIZED ok
S10 batch 1000 check #10 MATCHED/ALL_FIELDS_MATCH at block 95735897 (research: MATCHED/ALL_FIELDS_MATCH) tx 0x950aa53dab FINALIZED ok
S11 batch 68 check #11 MISMATCH/SERIAL_PROJECT_MISMATCH at block 95735897 (research: MISMATCH/SERIAL_PROJECT_MISMATCH) tx 0x8abe725e1b FINALIZED ok
S12 batch 180 check #12 MISMATCH/SERIAL_PROJECT_MISMATCH at block 95735897 (research: MISMATCH/SERIAL_PROJECT_MISMATCH) tx 0x7037af8d6f FINALIZED ok
S13 batch 39 check #13 UNVERIFIABLE/VERRA_NOT_FOUND at block 95735897 (research: UNVERIFIABLE/VERRA_NOT_FOUND) tx 0xf7e375a08f FINALIZED ok
S14 batch 594 check #14 UNVERIFIABLE/VERRA_NOT_FOUND at block 95735897 (research: UNVERIFIABLE/VERRA_NOT_FOUND) tx 0x9ab43affc5 FINALIZED ok
S15 batch 686 check #15 UNVERIFIABLE/VERRA_NOT_FOUND at block 95735897 (research: UNVERIFIABLE/VERRA_NOT_FOUND) tx 0x575ca43cbd FINALIZED ok
S16 batch 874 check #16 UNVERIFIABLE/VERRA_NOT_FOUND at block 95735897 (research: UNVERIFIABLE/VERRA_NOT_FOUND) tx 0xa1f5c512af FINALIZED ok
S17 batch 1213 check #17 UNVERIFIABLE/VERRA_NOT_FOUND at block 95735897 (research: UNVERIFIABLE/VERRA_NOT_FOUND) tx 0xc7a7b0b617 FINALIZED ok
S18 batch 3 check #18 UNVERIFIABLE/BATCH_NOT_FRACTIONALIZED at block 95735897 (research: UNVERIFIABLE/BATCH_NOT_FRACTIONALIZED) tx 0xf373918264 FINALIZED ok
S19 batch 138 check #19 UNVERIFIABLE/BATCH_NOT_FRACTIONALIZED at block 95735897 (research: UNVERIFIABLE/BATCH_NOT_FRACTIONALIZED) tx 0x41ec3e8c17 FINALIZED ok
S20 batch 446 check #20 UNVERIFIABLE/BATCH_NOT_FRACTIONALIZED at block 95735897 (research: UNVERIFIABLE/BATCH_NOT_FRACTIONALIZED) tx 0x7866c3adf2 FINALIZED ok
S21 batch 798 check #21 UNVERIFIABLE/BATCH_NOT_FRACTIONALIZED at block 95735897 (research: UNVERIFIABLE/BATCH_NOT_FRACTIONALIZED) tx 0x03923a22b6 FINALIZED ok
S22 batch 833 check #22 UNVERIFIABLE/BATCH_NOT_FRACTIONALIZED at block 95735897 (research: UNVERIFIABLE/BATCH_NOT_FRACTIONALIZED) tx 0x28f524f03a FINALIZED ok
S23 batch 1001 check #23 UNVERIFIABLE/BATCH_NOT_FRACTIONALIZED at block 95735897 (research: UNVERIFIABLE/BATCH_NOT_FRACTIONALIZED) tx 0x1c05e4a5b8 FINALIZED ok
S24 batch 217 check #24 UNVERIFIABLE/TCO2_NOT_FOUND at block 95735897 (research: UNVERIFIABLE/TCO2_NOT_FOUND) tx 0x43980ded10 FINALIZED ok
S25 batch 1713 check #25 UNVERIFIABLE/TCO2_NOT_FOUND at block 95735897 (research: UNVERIFIABLE/TCO2_NOT_FOUND) tx 0xc7624c2627 FINALIZED ok
S26 batch 1715 check #26 UNVERIFIABLE/TCO2_NOT_FOUND at block 95735897 (research: UNVERIFIABLE/TCO2_NOT_FOUND) tx 0x4236ad032c FINALIZED ok
S27 batch 1717 check #27 UNVERIFIABLE/TCO2_NOT_FOUND at block 95735897 (research: UNVERIFIABLE/TCO2_NOT_FOUND) tx 0xa4dafe8b42 FINALIZED ok
S28 batch 7 check #28 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0xaa2b2ca2c8 FINALIZED ok
S29 batch 140 check #29 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0x67b66217cb FINALIZED ok
S30 batch 564 check #30 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0x290a9e2625 FINALIZED ok
S31 batch 576 check #31 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0x67b0efa789 FINALIZED ok
S32 batch 698 check #32 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0x6c26ffe097 FINALIZED ok
S33 batch 711 check #33 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0x49eb82581a FINALIZED ok
S34 batch 712 check #34 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0x82ceaf3658 FINALIZED ok
S35 batch 718 check #35 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0x9da1bb9589 FINALIZED ok
S36 batch 719 check #36 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0xc3e7ba4fe7 FINALIZED ok
S37 batch 890 check #37 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0x39a456989a FINALIZED ok
S38 batch 898 check #38 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0x1cf9b825d5 FINALIZED ok
S39 batch 910 check #39 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0x4f430536b3 FINALIZED ok
S40 batch 934 check #40 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0x8f7d7c0641 FINALIZED ok
S41 batch 965 check #41 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0x8876433f39 FINALIZED ok
S42 batch 977 check #42 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0xa52a9d0350 FINALIZED ok
S43 batch 1163 check #43 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0xbb40b89880 FINALIZED ok
S44 batch 199 check #44 UNVERIFIABLE/SERIAL_UNPARSABLE at block 95735897 (research: UNVERIFIABLE/SERIAL_UNPARSABLE) tx 0xae817158c3 FINALIZED ok
S45 batch 1 check #45 UNVERIFIABLE/BATCH_NOT_CONFIRMED at block 95735897 (research: UNVERIFIABLE/BATCH_NOT_CONFIRMED) tx 0xd7847001e3 FINALIZED ok
S46 batch 1350 check #46 UNVERIFIABLE/BATCH_NOT_CONFIRMED at block 95735897 (research: UNVERIFIABLE/BATCH_NOT_CONFIRMED) tx 0x8ed9f4f713 FINALIZED ok
S47 batch 244 check #47 UNVERIFIABLE/BATCH_NOT_CONFIRMED at block 95735897 (research: UNVERIFIABLE/BATCH_NOT_CONFIRMED) tx 0x648bca6220 FINALIZED ok
S48 batch 1716 check #48 UNVERIFIABLE/BATCH_NOT_CONFIRMED at block 95735897 (research: UNVERIFIABLE/BATCH_NOT_CONFIRMED) tx 0x7ee87ef050 FINALIZED ok
S49 batch 1714 check #49 UNVERIFIABLE/BATCH_NOT_CONFIRMED at block 95735897 (research: UNVERIFIABLE/BATCH_NOT_CONFIRMED) tx 0x2ee5f3def8 FINALIZED ok
S50 batch 2000 check #50 UNVERIFIABLE/BATCH_NOT_FOUND at block 95735897 (research: UNVERIFIABLE/BATCH_NOT_FOUND) tx 0x5b8b13e8af FINALIZED ok
S51 batch 1200 check #51 UNVERIFIABLE/BATCH_NOT_CONFIRMED at block 95735897 (research: UNVERIFIABLE/BATCH_NOT_CONFIRMED) tx 0xf520c5e35c FINALIZED ok
```

## PASS: Seeds cover every batch in FEASIBILITY.md and every real non-MATCHED Confirmed batch the research found

```
FEASIBILITY batches: 26, missing: none
non-MATCHED Confirmed batches in deep_report.txt: 33, missing: none
```

## PASS: Seed verdicts equal the research ruling at block 95733573 (or the difference is explained in SEEDS.md)

```
51/51 identical; mix {"MATCHED":10,"MISMATCH":2,"UNVERIFIABLE":39}
```

## PASS: Canonical counters equal the filed checks (checks = matched + mismatch + double_claimed + unverifiable)

```
{"checks":51,"claimed_ranges":10,"double_claimed":0,"matched":10,"mismatch":2,"mode":"CANONICAL","rate_max":5,"rate_window":3600,"unverifiable":39,"version":"1.0.0"}
```

## PASS: Demo: every path on chain (each verdict incl. DOUBLE_CLAIMED via overlap, each refusal, gate allow + refuse + stale), all expectations met

```
28 PASS, 0 FAIL in the last run of docs/demo-run.log; paths missing: none
```

## PASS: Addresses consistent everywhere (deployments.json = README = SEEDS = SUBMISSION = demo log; frozen Toucan addresses; every other address is a seed's owner/TCO2/filer, a test account or a probe)

```
deployments: CarbonCheck 0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413, CarbonCheckDemo 0x019B01259A30467de7bdbFD2125e3d3CE00B08a1, OffsetGate 0x7BF9f7b62f65214f9B65647799507FC9A452409B, OffsetGateDemo 0x98eF81498Dc820fAb2Db56F112573a6256688348
missing: none
unknown addresses: none
```

## PASS: Every link in README and docs answers HTTP 200, or is marked POST-only / browser-only

```
176 links answered GET; failing: none
marked POST-only (RPC / registry API endpoints, not pages): https://studio-dev.genlayer.com/api, https://polygon.drpc.org, https://gateway.tenderly.co/public/polygon, https://prod-us.api.platts.com/ci-raas-prod/raas-report-api/es/public/retirements/publicReportPageSearch, https://prod-us.api.platts.com/ci-raas-prod/raas-report-api/es/public/holdings/publicReportPageSearch
```

## PASS: All offline tests pass (200+)

```
Ran 373 tests in 0.289s  OK
```

## PASS: Docs: README sections (Scope, Rules, Addresses, How to verify), no hygiene-list word in README or docs/, SUBMISSION plain ASCII, title <= 100 and description <= 1000 with true counts, says code decides and no model does

```
missing: none; files with a listed word: none (8 files); SUBMISSION ASCII: true; counts: Title 86/100, Description 809/1000; plain statement: true
```

## FAIL: Git: keys never committed, no assistant attribution or assistant name in history or files

```
commits touching test/.accounts.json: none; in messages: none; in files: docs/FINAL_CHECK.md
```
