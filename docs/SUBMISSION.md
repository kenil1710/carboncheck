# Submission

Plain ASCII. Character counts are measured by `tools/submission.mjs`.

## Title (86 / 100 characters)

```
CarbonCheck: does a tokenized carbon credit batch match real retired credits on Verra?
```

## Description (809 / 1000 characters)

```
CarbonCheck checks one Toucan carbon credit batch on Polygon against the public Verra registry. Code reads the batch on Polygon and the public Verra record, compares them field by field and decides; no model decides anything. Two RPCs must agree at one finalized block on the batch's serial, quantity and status and on its TCO2's project and vintage. Code parses the serial and requires a Verra record with that exact serial that is RETIRED with the same unit count, project and vintage. Verdicts: MATCHED, MISMATCH, DOUBLE_CLAIMED (units overlap a range already matched for another batch of the same project) or UNVERIFIABLE. Each verdict is final and as of its fetch time and block. Seeds: 51 real batches, 10 MATCHED, 2 MISMATCH, 39 UNVERIFIABLE. OffsetGate accepts an offset claim only on a fresh MATCHED.
```

## Links

- Repository: https://github.com/kenil1710/carboncheck
- CarbonCheck (canonical): 0x959Fe7E8Fb95Ae349895B1557AeF7916E3eCf413
- CarbonCheckDemo: 0x019B01259A30467de7bdbFD2125e3d3CE00B08a1
- OffsetGate: 0x7BF9f7b62f65214f9B65647799507FC9A452409B
- OffsetGateDemo: 0x98eF81498Dc820fAb2Db56F112573a6256688348
- Network: GenLayer Studio Dev, chain id 61997, https://studio-dev.genlayer.com/api
- Offline tests: 373
- Seeds: https://github.com/kenil1710/carboncheck/blob/main/docs/SEEDS.md
- Demo run: https://github.com/kenil1710/carboncheck/blob/main/docs/demo-run.log
