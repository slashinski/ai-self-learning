#!/usr/bin/env python3
"""Grade a PRD against a manually written test file and write a plain results report.

A simpler alternative to eval.py: no deterministic checks, no skill runs, no
iteration log. One model call per test case grades every criterion, and the
script writes one Markdown report: a summary table, then a pass/partial/fail
table per test case with any failure criteria that were triggered.

Usage:
  python3 scripts/grade.py <prd.md> <tests.md> [--model sonnet|haiku]
                           [--title text] [--out file]

The report goes next to the tests file as initial-test-results.md unless --out
is given. A relative --out is resolved from the modules/ directory (for example
--out module-1/exercise-1/results.md); an absolute --out is used as written. A test case passes only when every expected criterion is met and no
failure criterion is triggered; a partial counts as not met.
"""

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ROOT / "modules"
APPROVED_MODELS = ("sonnet", "haiku")
MARKS = {"pass": "✅ Met", "partial": "⚠️ Partial", "fail": "❌ Not met"}


def fail(message):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def bullets(block):
    return [line[2:].strip() for line in block.splitlines() if line.startswith("- ")]


def parse_tests(text):
    """Read '## Test Case N: Name' sections: Input, Expected Output Criteria, Failure Criteria."""
    tests = []
    for block in re.split(r"^## Test Case ", text, flags=re.MULTILINE)[1:]:
        heading, _, body = block.partition("\n")
        body = re.split(r"^---\s*$", body, flags=re.MULTILINE)[0]
        number, _, name = heading.partition(":")
        given = re.search(r"\*\*Input:\*\*[ \t]*(.*)", body)
        expected = re.search(r"\*\*Expected Output Criteria:\*\*(.*?)(?=\*\*Failure Criteria|\Z)",
                             body, flags=re.DOTALL)
        failures = re.search(r"\*\*Failure Criteria[^*]*\*\*(.*)", body, flags=re.DOTALL)
        tests.append({
            "number": number.strip(),
            "name": name.strip(),
            "input": given.group(1).strip() if given else "",
            "expected": bullets(expected.group(1)) if expected else [],
            "failures": bullets(failures.group(1)) if failures else [],
        })
    if not tests:
        fail("No '## Test Case N:' sections found in the tests file.")
    return tests


def run_claude(prompt, model):
    """Call the locally authenticated Claude CLI. The prompt goes in on stdin."""
    result = subprocess.run(["claude", "-p", "--model", model], input=prompt,
                            capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        fail(f"Claude CLI failed ({result.returncode}): {result.stderr.strip()}")
    return result.stdout.strip()


def grade(prd, test, model):
    """Ask the model to grade the PRD against one test case. Returns (criteria, failures)."""
    listing = [f"C{i}: {c}" for i, c in enumerate(test["expected"], 1)]
    listing += [f"F{i}: {c}" for i, c in enumerate(test["failures"], 1)]
    prompt = f"""You are grading a product requirements document against one test case.
Grade only the items listed. Do not add items of your own.

Test case: {test['name']}
Input: {test['input']}

Items:
C items are expected criteria. Result is "pass" if the PRD clearly meets it, "partial" if it
touches the point without meeting it, "fail" if it is missing or silent.
F items are failure criteria. Triggered is true if the PRD does what the item says must not occur.
{chr(10).join(listing)}

Return ONLY valid JSON in this shape, one entry per item, each note under 15 words citing the PRD.
Never use double quotes inside a note; use single quotes if you must quote.
{{"criteria": [{{"id": "C1", "result": "pass", "note": "..."}}],
 "failures": [{{"id": "F1", "triggered": false, "note": "..."}}]}}

=== PRD ===
{prd}
=== END PRD ==="""
    for attempt in range(2):  # models occasionally emit invalid JSON; retry once
        raw = run_claude(prompt, model)
        try:
            data = json.loads(raw[raw.find("{"):raw.rfind("}") + 1])
            criteria = {c["id"]: c for c in data.get("criteria", [])}
            failures = {f["id"]: f for f in data.get("failures", [])}
            return criteria, failures
        except (ValueError, KeyError):
            continue
    fail(f"Judge did not return valid JSON for '{test['name']}':\n{raw}")


def cell(text):
    return str(text).replace("|", "/").replace("\n", " ")


def passed(test, criteria, failures):
    met = all(criteria.get(f"C{i}", {}).get("result") == "pass" for i in range(1, len(test["expected"]) + 1))
    clean = not any(f.get("triggered") for f in failures.values())
    return met and clean


def render(title, prd_name, tests_name, tests, graded):
    results = [passed(t, c, f) for t, (c, f) in zip(tests, graded)]
    lines = [f"# {title}: {prd_name}", "", f"Graded against each test case in `{tests_name}`.", "",
             "## Summary", "",
             "| Test Case | Result |", "|---|---|"]
    for t, ok in zip(tests, results):
        lines.append(f"| {t['number']} - {cell(t['name'])} | {'✅ PASS' if ok else '❌ FAIL'} |")
    lines += ["", f"**Overall: {sum(results)} / {len(results)} passed.**", "", "---"]
    for t, (criteria, failures), ok in zip(tests, graded, results):
        lines += ["", f"## Test Case {t['number']}: {t['name']} - {'✅ PASS' if ok else '❌ FAIL'}", "",
                  "| Criterion | Result |", "|---|---|"]
        for i, text in enumerate(t["expected"], 1):
            c = criteria.get(f"C{i}", {})
            mark = MARKS.get(c.get("result"), MARKS["fail"])
            note = c.get("note", "Judge returned no verdict.")
            lines.append(f"| {cell(text)} | {mark} - {cell(note)} |")
        triggered = [f"{text} ({cell(failures[f'F{i}'].get('note', ''))})"
                     for i, text in enumerate(t["failures"], 1)
                     if failures.get(f"F{i}", {}).get("triggered")]
        lines += ["", "**Failure criteria triggered:** " + ("; ".join(triggered) if triggered else "none"),
                  "", f"**Verdict: {'PASS' if ok else 'FAIL'}**", "", "---"]
    return "\n".join(lines[:-1]).rstrip() + "\n"


def under_modules(value):
    """Resolve a command-line path from the modules/ directory (an absolute path stays as written)."""
    return MODULES / value


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("prd", type=under_modules, help="PRD path, relative to modules/")
    parser.add_argument("tests", type=under_modules, help="tests path, relative to modules/")
    parser.add_argument("--model", default="sonnet", choices=APPROVED_MODELS)
    parser.add_argument("--title", default="Initial Test Results")
    parser.add_argument("--out", type=under_modules, help="report path, relative to modules/ (default: initial-test-results.md next to the tests file)")
    args = parser.parse_args()

    for path in (args.prd, args.tests):
        if not path.exists():
            fail(f"File not found: {path}")
    prd = args.prd.read_text()
    tests = parse_tests(args.tests.read_text())

    with ThreadPoolExecutor(max_workers=len(tests)) as pool:
        graded = list(pool.map(lambda t: grade(prd, t, args.model), tests))

    report = render(args.title, args.prd.name, args.tests.name, tests, graded)
    out = args.out or args.tests.parent / "initial-test-results.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report)
    print(report.split("## Test Case")[0].split("## Summary")[1].strip())
    print(f"\nReport: {out}")


if __name__ == "__main__":
    main()
