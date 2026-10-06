# gitleaks

A gitleaks config with a custom rule, a pre-commit hook config and a pull request workflow that scans the full history.

## Goal

Block secrets before they land: run gitleaks locally as a pre-commit hook and in CI over all commits, with a custom rule for an internal token format.

## Run it

```
pip install pyyaml==6.0.3
python3 gitleaks/check.py
pre-commit install && pre-commit run --all-files
```
Expected from the first command: `ok`. The second needs `pre-commit` and network access to fetch the hook.

Not run end to end: gitleaks and pre-commit were not available, so neither the hook nor the CI job was executed. `check.py` only tests the custom regex in Python. No sample secrets are stored; it builds a fake token in memory.

## What it proves

- `.gitleaks.toml` extends the default rules and adds `orders-internal-token`, which matches `ordtok_` followed by 24 alphanumerics; `check.py` confirms it matches such a token and ignores `ordtok_short`.
- `.pre-commit-config.yaml` and `gitleaks.yml` both use gitleaks v8.21.2.
- The CI job checks out with `fetch-depth: 0` so it scans history, and redacts findings in its output.

## Trade-offs

- Regex rules give false positives and miss unstructured secrets.
- The allowlist skips every `.md` file, which is a deliberate blind spot.
- A leaked secret still has to be rotated; detection does not undo it.
- The workflow downloads the gitleaks binary without checking a checksum.

## When not to use it

- When the hosting platform's push protection already blocks secrets.
- For repositories holding only generated artifacts.
