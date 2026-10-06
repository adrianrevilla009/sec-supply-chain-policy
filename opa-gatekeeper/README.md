# opa-gatekeeper

Plain Rego admission rules with unit tests, and a Gatekeeper ConstraintTemplate and Constraint for the same idea.

## Goal

Express admission rules (no `:latest` tag, run as non-root) in Rego, test them with `opa test`, and ship the tag rule as Gatekeeper objects.

## Run it

```
pip install pyyaml==6.0.3
python3 opa-gatekeeper/check.py
opa test opa-gatekeeper/policy.rego opa-gatekeeper/policy_test.rego -v
```
Expected from the first command: `ok`. With OPA 0.70 or later, `opa test` should list `test_good_allowed` and `test_bad_denied` as passing.

Not run end to end: OPA was not installed and no cluster was used, so the Rego tests and the Gatekeeper objects were never executed. `check.py` only compares the YAML files.

## What it proves

- `policy.rego` has two `deny` rules; `policy_test.rego` expects none for a pod with `orders:1.0` and `runAsNonRoot`, and two for a pod with `orders:latest` and no security context.
- `template.yaml` defines kind `OrdersK8sPolicy` with a `violation` rule for the `latest` tag, and `constraint.yaml` uses that kind with `enforcementAction: deny` on Pods.
- The Gatekeeper template only enforces the tag rule; the non-root rule exists only in `policy.rego`.

## Trade-offs

- Rego has a learning curve, and Gatekeeper's Rego dialect differs slightly from plain OPA (no `rego.v1` here).
- Admission policies add latency and a failure mode to the API server.
- The two files duplicate the tag rule, so they can drift apart.

## When not to use it

- When Kyverno YAML policies are enough (see `kyverno`).
- For checks outside the cluster, where conftest in CI is simpler.
