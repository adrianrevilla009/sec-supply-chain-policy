# kyverno

A Kyverno ClusterPolicy, two sample Pods and a Kyverno CLI test file that expects one to pass and one to fail.

## Goal

Write the no-`latest` admission rule as plain YAML, without a new policy language, and test it offline with the Kyverno CLI.

## Run it

```
pip install pyyaml==6.0.3
python3 kyverno/check.py
kyverno test kyverno
```
Expected from the first command: `ok`. With Kyverno CLI v1.13, `kyverno test` should report the `good` pod as pass and the `bad` pod as fail.

Not run end to end: the Kyverno CLI was not installed, so the policy was never evaluated. `check.py` only cross-checks that the test file names rules and resources that exist.

## What it proves

- `policy.yaml` is an enforcing ClusterPolicy with one rule, `no-latest-tag`, using the pattern `!*:latest` on Pod container images.
- `resources.yaml` has the `good` pod (`orders:1.0`) and the `bad` pod (`orders:latest`).
- `kyverno-test.yaml` expects `pass` for `good` and `fail` for `bad`; `check.py` fails if it references a missing rule or resource, or covers only one outcome.

## Trade-offs

- YAML patterns are easy to read but limited for complex logic.
- The policy is named `require-signed-pinned-images` but only blocks the `latest` tag; image signature verification (`verifyImages`) needs a registry and keys and is not included.
- An image with no tag at all is not matched by the pattern.

## When not to use it

- When you need cross-resource logic that fits Rego better.
- On clusters where another admission controller is not acceptable.
