# codeql-semgrep

A GitHub Actions CodeQL workflow, two custom Semgrep rules for Java and a `Bad.java` fixture that both rules should flag.

## Goal

Combine CodeQL (deep dataflow analysis, per pull request and weekly) with Semgrep (fast custom rules), and keep a fixture proving the custom rules fire.

## Run it

```
pip install pyyaml==6.0.3
python3 codeql-semgrep/check.py
semgrep --config codeql-semgrep/semgrep-rules.yml --error codeql-semgrep/Bad.java
```
Expected from the first command: `ok`. Semgrep is expected to report two findings and exit non-zero.

Not run end to end: Semgrep was not installed, and CodeQL only runs on GitHub Actions. `check.py` only searches `Bad.java` for the text each rule targets; it does not run Semgrep.

## What it proves

- `codeql.yml` runs on pull requests and Mondays at 06:00 UTC, uses the `security-extended` query suite and a read-only `contents` token (plus `security-events: write`); every action is pinned to a major version.
- `semgrep-rules.yml` defines `orders-sql-string-concat` and `orders-hardcoded-password`.
- `Bad.java` contains a hardcoded `password` literal and a SQL string built with `+ id`, one trigger per rule.

## Trade-offs

- CodeQL is slow and needs a build; Semgrep is quick but pattern-based and misses flows across functions.
- Two tools mean two queues of findings to triage.
- Actions are pinned to major tags, not commit SHAs.

## When not to use it

- On tiny repositories where a dependency bot and code review are enough.
- For languages neither tool supports well.
