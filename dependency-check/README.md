# dependency-check

A minimal Maven `pom.xml` with an old log4j-core, the OWASP Dependency-Check plugin configured with a CVSS gate, and an empty suppression file.

## Goal

Fail a Maven build when a dependency has a known CVE with CVSS 7 or higher, with suppressions that need a reason and an end date.

## Run it

```
pip install pyyaml==6.0.3
python3 dependency-check/check.py
mvn -f dependency-check/pom.xml org.owasp:dependency-check-maven:10.0.4:check
```
Expected from the first command: `ok`. The Maven scan is expected to fail the build on log4j-core 2.14.1.

Not run end to end: the scan downloads the NVD database and was not executed here, so the failure is the expected result, not an observed one. Set an NVD API key through the environment, never in git.

## What it proves

- `pom.xml` pins `log4j-core` 2.14.1 (affected by CVE-2021-44228) and `dependency-check-maven` 10.0.4.
- `failBuildOnCVSS` is 7 and `suppressions.xml` is wired in; the only suppression is a commented example with an `until` date.
- `check.py` parses both XML files and fails on an unpinned plugin or dependency version, or a gate above 7.

## Trade-offs

- The first run is slow because of the NVD download.
- Matching is by CPE and produces false positives, which is why suppressions exist.
- It only sees dependencies in the Maven tree, not the final image.

## When not to use it

- When Trivy or Grype on the built artifact already covers Java dependencies.
- In offline builds without a mirrored NVD.
