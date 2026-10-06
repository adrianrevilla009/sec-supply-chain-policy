#!/usr/bin/env python3
"""Offline structural check: no scanner binaries needed. Exit 1 on failure."""
import json, pathlib, sys
import yaml
H = pathlib.Path(__file__).parent
def load(n): return yaml.safe_load((H / n).read_text())
bad = []
def need(cond, msg):
    if not cond: bad.append(msg)

t = load("trivy.yaml"); g = load("grype.yaml")
need(t["exit-code"] == 1, "trivy must exit non-zero on findings")
need(set(t["severity"]) == {"HIGH", "CRITICAL"}, "trivy severity gate")
need(g["fail-on-severity"] in ("high", "critical"), "grype gate")
df = (H / "Dockerfile").read_text()
need("FROM alpine:3." in df and ":latest" not in df, "base image must be pinned")
need("USER " in df, "image must not run as root")
load("ci.yml.example")

print("FAIL: " + "; ".join(bad) if bad else "ok")
sys.exit(1 if bad else 0)
