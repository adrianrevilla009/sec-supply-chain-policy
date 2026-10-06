#!/usr/bin/env python3
"""Offline structural check: no scanner binaries needed. Exit 1 on failure."""
import json, pathlib, sys
import yaml
H = pathlib.Path(__file__).parent
def load(n): return yaml.safe_load((H / n).read_text())
bad = []
def need(cond, msg):
    if not cond: bad.append(msg)

c = load("codeql.yml"); r = load("semgrep-rules.yml")
need(c["permissions"]["contents"] == "read", "least privilege token")
need(all("@v" in s.get("uses", "@v") for s in c["jobs"]["analyze"]["steps"]), "actions versioned")
ids = {x["id"] for x in r["rules"]}
need(len(ids) == 2, "two rules expected")
fixture = (H / "Bad.java").read_text()
need('executeQuery("' in fixture and '+ id' in fixture and 'password = "' in fixture, "fixture must trigger both rules")

print("FAIL: " + "; ".join(bad) if bad else "ok")
sys.exit(1 if bad else 0)
