#!/usr/bin/env python3
"""Offline structural check: no scanner binaries needed. Exit 1 on failure."""
import json, pathlib, sys
import yaml
H = pathlib.Path(__file__).parent
def load(n): return yaml.safe_load((H / n).read_text())
bad = []
def need(cond, msg):
    if not cond: bad.append(msg)

t = load("template.yaml"); c = load("constraint.yaml")
need(t["spec"]["crd"]["spec"]["names"]["kind"] == c["kind"], "constraint kind matches template")
need(c["spec"]["enforcementAction"] == "deny", "enforcing, not dryrun")
need("violation" in t["spec"]["targets"][0]["rego"], "template defines violation")
need("test_bad_denied" in (H / "policy_test.rego").read_text(), "tests present")

print("FAIL: " + "; ".join(bad) if bad else "ok")
sys.exit(1 if bad else 0)
