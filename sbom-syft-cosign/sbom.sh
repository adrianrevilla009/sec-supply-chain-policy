#!/usr/bin/env bash
# Generate an SBOM for an image, sign it, and verify the signature (keyless needs CI OIDC; local uses a key pair).
set -euo pipefail
IMAGE="${1:?usage: sbom.sh <image> }"
syft "$IMAGE" -o cyclonedx-json=sbom.cdx.json
COSIGN_PASSWORD="" cosign generate-key-pair      # demo key, empty password (no prompt); writes cosign.key / cosign.pub (git-ignored)
COSIGN_PASSWORD="" cosign sign-blob --key cosign.key --yes sbom.cdx.json --output-signature sbom.sig
cosign verify-blob --key cosign.pub --signature sbom.sig sbom.cdx.json
