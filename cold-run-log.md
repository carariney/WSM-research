# Cold-Run Log

**Run date:** October 15, 2026, 09:37 EDT  
**Fresh directory:** `/private/tmp/wsm-cold-run.ZqJuDm`  
**Interpreter:** system Python 3.9.6, invoked with a cleared environment except the system executable path.  
**Files copied into fresh directory:** `wsm_proforma.py`, `validate_wsm_model.py`, and `lab08_wsm_pe_comps.py`. No repository virtual environment, cached bytecode, or third-party package was used.

## First run - failure preserved

The initial clean run at 09:37:04 EDT failed before validation because system Python 3.9 rejected an f-string expression containing a backslash in the sensitivity-table header:

```text
SyntaxError: f-string expression part cannot include a backslash
```

**Resolution:** The model now assigns `"WACC \\ Terminal Growth"` to a normal string variable before formatting. This preserves the same visible header while supporting Python 3.9.

## Rerun - pass

At 09:37:21 EDT, the clean run completed:

```text
PASS: known-answer DCF, base-year reconciliation, pro-forma articulation,
FCFF/FCFE reconciliation, enterprise-to-equity bridge, and DCF directionality.
PASS: integrated base FCFF value per share = $138.88 as of August 31, 2026.
FCFF value per share: $138.88
Market-implied terminal growth: 6.28% to match $228.25
Minimum EV/EBIT implied value: $140.65 per share
Maximum EV/EBIT implied value: $169.66 per share
```

Python emitted a macOS `confstr()` temporary-directory warning in the cleared environment but continued normally. It did not affect calculations or output. The first failure and fix remain part of this record.
