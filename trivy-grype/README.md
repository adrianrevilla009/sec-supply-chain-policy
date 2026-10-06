# trivy-grype

A Trivy config, a Grype config, a pinned non-root Dockerfile, an ignore file and an example CI caller, plus a script that checks the gate settings.

## Goal

Gate an image build on two independent vulnerability scanners, Trivy and Grype, with one documented place to accept risk.

## Run it

```
pip install pyyaml==6.0.3
python3 trivy-grype/check.py
docker build -t orders:scan trivy-grype
trivy image --config trivy-grype/trivy.yaml orders:scan
grype orders:scan -c trivy-grype/grype.yaml
```
Expected from the first command: `ok`. The last three need Docker, Trivy and Grype.

Not run end to end: Trivy, Grype and Docker were not available, so the scans were never executed. Only `check.py` was run, and it reads the config files without scanning anything.

## What it proves

- `trivy.yaml` exits with code 1 on HIGH or CRITICAL findings and also scans for secrets and misconfigurations; `grype.yaml` fails on `high`.
- `Dockerfile` uses `alpine:3.20.3` (not `latest`) and switches to the non-root user `app`.
- `.trivyignore` is the only ignore file and its example entry (commented out) carries an expiry date; `check.py` fails if the gate values or the Dockerfile pinning drift.

## Trade-offs

- Two scanners produce more noise but cover each other's database gaps.
- `ignore-unfixed: true` (Trivy) and `only-fixed: true` (Grype) hide vulnerabilities that have no patch yet, which may not be acceptable in regulated work.
- `ci.yml.example` calls a reusable workflow from a separate repository, so it cannot run on its own.

## When not to use it

- When the image is distroless or scratch and the policy is SBOM-only.
- When a registry-side scanner already blocks pushes.
