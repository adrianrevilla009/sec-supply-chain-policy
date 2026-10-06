#!/usr/bin/env python3
"""Offline structural check: no scanner binaries needed. Exit 1 on failure."""
import json, pathlib, sys
import yaml
H = pathlib.Path(__file__).parent
def load(n): return yaml.safe_load((H / n).read_text())
bad = []
def need(cond, msg):
    if not cond: bad.append(msg)

w = load("provenance.yml")
need(w["permissions"] == {"contents": "read"}, "top-level token read-only")
gen = w["jobs"]["provenance"]
need(gen["uses"].split("@")[1].startswith("v2."), "generator pinned to a release tag")
need(gen["permissions"]["id-token"] == "write", "OIDC needed for signing")
need("slsa-verifier verify-artifact" in (H / "verify.sh").read_text(), "verify step present")
need("--source-uri" in (H / "verify.sh").read_text(), "source identity pinned")

print("FAIL: " + "; ".join(bad) if bad else "ok")
sys.exit(1 if bad else 0)
