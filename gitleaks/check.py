#!/usr/bin/env python3
"""Offline structural check: no scanner binaries needed. Exit 1 on failure."""
import json, pathlib, sys
import yaml
H = pathlib.Path(__file__).parent
def load(n): return yaml.safe_load((H / n).read_text())
bad = []
def need(cond, msg):
    if not cond: bad.append(msg)

import re
toml = (H / ".gitleaks.toml").read_text()
need("useDefault = true" in toml, "extends defaults")
rx = re.compile(re.search(r"regex = \x27\x27\x27(.+?)\x27\x27\x27", toml).group(1))
need(rx.search("ordtok_" + "a" * 24), "custom rule matches a sample token")
need(not rx.search("ordtok_short"), "custom rule ignores short strings")
hook = load(".pre-commit-config.yaml")["repos"][0]
need(hook["rev"].startswith("v8."), "hook pinned")
need("v8.21.2" in (H / "gitleaks.yml").read_text(), "CI and pre-commit use same version")
load("gitleaks.yml")

print("FAIL: " + "; ".join(bad) if bad else "ok")
sys.exit(1 if bad else 0)
