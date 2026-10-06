#!/usr/bin/env python3
"""Offline structural check: no scanner binaries needed. Exit 1 on failure."""
import json, pathlib, sys
import yaml
H = pathlib.Path(__file__).parent
def load(n): return yaml.safe_load((H / n).read_text())
bad = []
def need(cond, msg):
    if not cond: bad.append(msg)

import xml.etree.ElementTree as ET
ns = {"m": "http://maven.apache.org/POM/4.0.0"}
pom = ET.parse(H / "pom.xml").getroot(); ET.parse(H / "suppressions.xml")
pl = pom.find(".//m:plugin[m:artifactId='dependency-check-maven']", ns)
need(pl is not None, "plugin missing")
if pl is not None:
    need(pl.findtext("m:version", namespaces=ns) not in (None, "", "LATEST", "RELEASE"), "plugin version pinned")
    need(int(pl.findtext(".//m:failBuildOnCVSS", namespaces=ns)) <= 7, "CVSS gate must be <= 7")
for v in pom.findall(".//m:dependency/m:version", ns):
    need(not v.text.startswith(("LATEST", "RELEASE", "[")), "dependency versions pinned")

print("FAIL: " + "; ".join(bad) if bad else "ok")
sys.exit(1 if bad else 0)
