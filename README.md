# FortiGate Config Compliance Checker 🔒

A lightweight, self-contained **Fortinet FortiGate configuration compliance checker**.
It scans a FortiGate text backup (e.g., `show full-configuration` or `execute backup config flash`) and reports
alignment with opinionated best practices (logging, password policy, TLS minimums, lockout thresholds, etc.).

> ✅ No credentials or live devices required. Works offline against config files in this repo.

---

## Features
- Parse FortiGate CLI config backups (`.conf`/`.cfg`)
- 12+ opinionated checks (TLS min version, FAZ/syslog logging, admin lockout, password policy, etc.)
- JSON and Markdown reports with pass/warn/fail status
- Simple rule engine via `rules.yaml` (easy to extend)
- Tested with `pytest`

## Quickstart
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/fortigate_compliance_checker.py samples/fortigate_sample.conf --md report.md --json report.json
```

## Example Output (Markdown)
```markdown
# FortiGate Compliance Report
Target: samples/fortigate_sample.conf

| Check | Status | Details |
|------|--------|---------|
| ssl-min-proto-version >= TLS1.2 | PASS | Found: TLS1-2 |
| FortiAnalyzer logging enabled | WARN | Section present but status not enabled |
| Syslog logging enabled | FAIL | Not found |
```

## Repo Structure
```
src/                    # code
  fortigate_compliance_checker.py
rules.yaml              # opinionated checks (regex-based)
samples/
  fortigate_sample.conf # demo config (anonymized)
tests/
  test_checker.py
```

## Extending Rules
Update `rules.yaml` to add/edit checks. Each rule supports:
- `name`: human-friendly label
- `pattern`: regex searched across the config
- `must_include`: (optional) additional regex that must match inside the found block
- `severity`: PASS/WARN/FAIL default outcome if not found
- `advice`: remediation tip shown when FAIL/WARN

See file comments for examples.

## Caveats
- This is a **static** linter for text backups. It doesn't guarantee device state.
- FortiOS syntax evolves; rules here are conservative and generic but may require tuning per version.
- The sample config is synthetic for demo purposes.
