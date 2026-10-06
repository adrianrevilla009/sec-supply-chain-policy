#!/usr/bin/env python3
"""Offline structural check: no scanner binaries needed. Exit 1 on failure."""
import json, pathlib, sys
import yaml
H = pathlib.Path(__file__).parent
def load(n): return yaml.safe_load((H / n).read_text())
bad = []
def need(cond, msg):
    if not cond: bad.append(msg)

p = load("policy.yaml"); t = load("kyverno-test.yaml")
need(p["spec"]["validationFailureAction"] == "Enforce", "enforcing")
names = {r["name"] for r in p["spec"]["rules"]}
need(all(r["rule"] in names for r in t["results"]), "tests reference real rules")
docs = list(yaml.safe_load_all((H / "resources.yaml").read_text()))
have = {d["metadata"]["name"] for d in docs}
need(all(n in have for r in t["results"] for n in r["resources"]), "tests reference real resources")
need({r["result"] for r in t["results"]} == {"pass", "fail"}, "both outcomes covered")

print("FAIL: " + "; ".join(bad) if bad else "ok")
sys.exit(1 if bad else 0)
