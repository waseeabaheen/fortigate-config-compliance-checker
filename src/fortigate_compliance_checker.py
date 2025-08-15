#!/usr/bin/env python3
import re, argparse, json, pathlib, sys, yaml
from datetime import datetime

def load_rules(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def read_config_text(path: str) -> str:
    with open(path, "r", errors="ignore") as f:
        return f.read()

def evaluate_rules(cfg_text: str, rules):
    results = []
    for rule in rules:
        name = rule["name"]
        pattern = re.compile(rule["pattern"], re.IGNORECASE | re.MULTILINE)
        severity = rule.get("severity", "FAIL")
        advice = rule.get("advice", "")
        must_include = rule.get("must_include")
        m = pattern.search(cfg_text)
        status = "FAIL"
        details = "Not found"
        if m:
            if must_include:
                inner = re.compile(must_include, re.IGNORECASE | re.MULTILINE | re.DOTALL)
                if inner.search(m.group(0)):
                    status = "PASS"
                    details = "Pattern and required settings present"
                else:
                    status = "WARN"
                    details = "Block found but required settings missing"
            else:
                status = "PASS"
                details = "Pattern present"
        else:
            status = "WARN" if severity.upper() == "WARN" else "FAIL"
            details = "Pattern not present"
        results.append({
            "check": name,
            "status": status,
            "details": details,
            "advice": advice if status != "PASS" else ""
        })
    return results

def to_markdown(results, target):
    lines = [f"# FortiGate Compliance Report", f"Target: `{target}`", ""]
    lines += ["| Check | Status | Details |", "|------|--------|---------|"]
    for r in results:
        lines.append(f"| {r['check']} | {r['status']} | {r['details']} |")
    lines.append("")
    lines.append("## Remediation Advice")
    for r in results:
        if r["status"] != "PASS" and r["advice"]:
            lines.append(f"- **{r['check']}**: {r['advice']}")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser(description="FortiGate Config Compliance Checker")
    ap.add_argument("config", help="Path to FortiGate text config (e.g., .conf)")
    ap.add_argument("--rules", default=str(pathlib.Path(__file__).resolve().parent.parent / "rules.yaml"))
    ap.add_argument("--json", help="Path to write JSON report")
    ap.add_argument("--md", help="Path to write Markdown report")
    args = ap.parse_args()

    cfg_text = read_config_text(args.config)
    rules = load_rules(args.rules)
    results = evaluate_rules(cfg_text, rules)

    summary = {
        "target": args.config,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "results": results,
        "score": round(sum(1 for r in results if r["status"] == "PASS") / len(results) * 100, 1)
    }

    print(json.dumps(summary, indent=2))

    if args.json:
        with open(args.json, "w") as f:
            json.dump(summary, f, indent=2)

    if args.md:
        md = to_markdown(results, args.config)
        with open(args.md, "w") as f:
            f.write(md)

if __name__ == "__main__":
    main()
