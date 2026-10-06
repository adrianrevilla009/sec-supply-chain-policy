# slsa-provenance

A release workflow that builds a JAR and calls the SLSA generic generator, plus a script that verifies the artifact on the consumer side.

## Goal

Generate SLSA level 3 build provenance for a release JAR with the official generator, and verify it with `slsa-verifier` before use.

## Run it

```
pip install pyyaml==6.0.3
python3 slsa-provenance/check.py
slsa-provenance/verify.sh app.jar provenance.intoto.jsonl <owner>/<repo> v1.0.0
```
Expected from the first command: `ok`. The second needs `slsa-verifier` and a real release with its provenance file.

Not run end to end: the workflow only runs on GitHub Actions for a `v*` tag, and `verify.sh` needs a real release, so neither was executed. The workflow also runs `mvn -B -q package` and expects a Maven project at the repository root, which this folder does not contain.

## What it proves

- `provenance.yml` triggers on `v*` tags with a read-only default token; the `build` job packages the JAR and outputs base64 SHA-256 hashes.
- The `provenance` job calls `generator_generic_slsa3.yml@v2.0.0` with `id-token: write`; it is referenced by release tag, as the generator's documentation requires.
- `verify.sh` runs `slsa-verifier verify-artifact` with `--source-uri` and `--source-tag`, so the repository and tag are pinned.

## Trade-offs

- It needs GitHub-hosted runners and the public Sigstore services.
- Provenance shows how an artifact was built, not that the source is free of bugs.
- `actions/checkout` and `upload-artifact` are pinned to major tags, not commit SHAs.

## When not to use it

- For private builds without access to Sigstore.
- When no consumer will verify the provenance.
