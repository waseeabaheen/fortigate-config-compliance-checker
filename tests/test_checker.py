import json, subprocess, sys, os, pathlib

def test_runs_and_scores(tmp_path):
    base = pathlib.Path(__file__).resolve().parents[1]
    cfg = base / "samples" / "fortigate_sample.conf"
    script = base / "src" / "fortigate_compliance_checker.py"
    out_json = tmp_path / "report.json"
    cmd = [sys.executable, str(script), str(cfg), "--json", str(out_json)]
    subprocess.check_call(cmd)
    data = json.loads(out_json.read_text())
    assert "results" in data
    assert isinstance(data["results"], list)
    assert data["score"] >= 0
