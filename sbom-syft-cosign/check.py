#!/usr/bin/env python3
"""Offline structural check: no scanner binaries needed. Exit 1 on failure."""
import json, pathlib, sys
import yaml
H = pathlib.Path(__file__).parent
def load(n): return yaml.safe_load((H / n).read_text())
bad = []
def need(cond, msg):
    if not cond: bad.append(msg)

s = (H / "sbom.sh").read_text(); p = load("verify-policy.yaml")
need("set -euo pipefail" in s, "strict shell")
need("syft" in s and "cosign verify-blob" in s, "script must generate and verify")
need(p["require"]["sbom_format"] in s, "format in policy matches script")
need(all(v.startswith("v") for v in p["tools"].values()), "tool versions pinned")
need("cosign.key" in (H / ".gitignore").read_text(), "private key ignored")

print("FAIL: " + "; ".join(bad) if bad else "ok")
sys.exit(1 if bad else 0)
