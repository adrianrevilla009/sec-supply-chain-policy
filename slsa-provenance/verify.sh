#!/usr/bin/env bash
# Consumer side: verify the artifact against its provenance before use.
set -euo pipefail
slsa-verifier verify-artifact "${1:?artifact}" \
  --provenance-path "${2:?provenance.intoto.jsonl}" \
  --source-uri "github.com/${3:?adrianrevilla009/REPO}" \
  --source-tag "${4:?v1.0.0}"
