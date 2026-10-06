# sec-supply-chain-policy

Eight small, separate examples of supply-chain and policy controls (vulnerability scanning, SBOMs and signing, static analysis, secret detection, admission policies and build provenance), each with a check you can run to see the configuration is consistent.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`trivy-grype`](./trivy-grype) | Image scan gate with Trivy and Grype, pinned non-root Dockerfile, expiring ignore list | `python3 trivy-grype/check.py` |
| [`dependency-check`](./dependency-check) | OWASP Dependency-Check in Maven, failing at CVSS 7, with a deliberately vulnerable log4j-core | `python3 dependency-check/check.py` |
| [`sbom-syft-cosign`](./sbom-syft-cosign) | CycloneDX SBOM with Syft, signed and verified with Cosign | `python3 sbom-syft-cosign/check.py` |
| [`codeql-semgrep`](./codeql-semgrep) | CodeQL workflow plus two custom Semgrep rules and a fixture that must trigger them | `python3 codeql-semgrep/check.py` |
| [`gitleaks`](./gitleaks) | gitleaks as pre-commit hook and CI job, with a custom token rule | `python3 gitleaks/check.py` |
| [`opa-gatekeeper`](./opa-gatekeeper) | Rego admission rules with unit tests, and a Gatekeeper template and constraint | `python3 opa-gatekeeper/check.py` |
| [`kyverno`](./kyverno) | The no-`latest` rule as a Kyverno ClusterPolicy with CLI test fixtures | `python3 kyverno/check.py` |
| [`slsa-provenance`](./slsa-provenance) | SLSA level 3 provenance workflow and consumer-side verification | `python3 slsa-provenance/check.py` |

The examples use a small Orders domain (an `orders` image, an `orders:1.0` pod).

## Prerequisites

- Python 3 with `pyyaml==6.0.3` (`pip install pyyaml==6.0.3`) for every `check.py`.
- The scanners themselves are optional and only needed for the full commands in each folder: Docker, Trivy, Grype, Maven with Java 21, Syft v1.14.0, Cosign v2.4.1, Semgrep, pre-commit and gitleaks v8.21.2, OPA 0.70+, Kyverno CLI v1.13, slsa-verifier.

## How to read it

Start with `opa-gatekeeper` and `kyverno`, which express the same rule two ways, then pick any other folder. The `check.py` scripts run offline and only check the files in the folder; none of the scanner or policy tools was run end to end, and each folder README says which commands need which tool.
