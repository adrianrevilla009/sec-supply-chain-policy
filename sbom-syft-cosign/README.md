# sbom-syft-cosign

A shell script that generates an SBOM, signs it and verifies the signature, plus a consumer policy file listing what must be checked.

## Goal

Produce a CycloneDX SBOM for an image with Syft, sign it with Cosign and verify the signature, so a consumer can check what an artifact contains.

## Run it

```
pip install pyyaml==6.0.3
python3 sbom-syft-cosign/check.py
cd sbom-syft-cosign && ./sbom.sh alpine:3.20.3
```
Expected from the first command: `ok`. The script writes `sbom.cdx.json`, `cosign.key`, `cosign.pub` and `sbom.sig`, then `cosign verify-blob` reports the blob as verified.

Not run end to end: Syft v1.14.0, Cosign v2.4.1 and Docker were not available, so `sbom.sh` was only checked for its contents, never executed.

## What it proves

- `sbom.sh` runs with `set -euo pipefail`, so any failing step stops it, and it generates, signs (`sign-blob`) and verifies (`verify-blob`) in that order.
- `verify-policy.yaml` pins both tool versions and requires `cyclonedx-json`, the same format the script writes.
- `.gitignore` excludes `cosign.key`, `cosign.pub`, the SBOM and the signature, so the demo key cannot be committed.

## Trade-offs

- A local key pair with an empty password proves the mechanism but not who signed; real use needs keyless signing tied to a CI identity (the script says this in a comment; it is not implemented here).
- SBOM completeness depends on what Syft can detect in the image.

## When not to use it

- When every build already publishes SLSA provenance (see `slsa-provenance`).
- For artifacts that nobody consumes downstream.
