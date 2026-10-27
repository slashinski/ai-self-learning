#!/usr/bin/env python3
"""Grade one output against a tests file.

The output is either a file you already have (--output) or the bare prompt sent
once to the model (--bare). It is graded two ways:

1. Deterministic checks, from the '## Deterministic Checks' section of the tests file.
2. An LLM judge, once per test case, on that test case's expected and failure criteria.

A test case passes when all of its judged criteria pass. The run passes at 95% or more
of all criteria met, deterministic and judged together. Every model call is recorded
with its model, tokens, and cost.

Files written to results/ next to the tests file:
  <artifact>.md          the output (--bare runs only)
  <artifact>-results.md  the report: summary first, then every check and verdict

Usage:
  python3 scripts/eval.py <tests.md> --bare <prompt.txt> --artifact bare-prd
  python3 scripts/eval.py <tests.md> --output <file.md> --artifact bare-prd [--model sonnet|haiku]
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

PASS_THRESHOLD = 95.0  # percent of criteria met across all test cases
APPROVED_MODELS = ("sonnet", "haiku")
USAGE = []  # one record per Claude CLI call in this run


def fail(message):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def bullets(block):
    return [line[2:].strip() for line in block.splitlines() if line.startswith("- ")]


def parse_tests(path):
    """Read '## Test Case N: name' sections, in the schemas/test-case.md format."""
    tests = []
    for block in re.split(r"^## Test Case ", path.read_text(), flags=re.MULTILINE)[1:]:
        heading, _, body = block.partition("\n")
        given = re.search(r"\*\*Input:\*\*\s*(.*?)\n\s*\n", body, flags=re.DOTALL)
        expected = re.search(r"\*\*Expected Output Criteria:\*\*\s*(.*?)(?=\*\*Failure Criteria|\Z)",
                             body, flags=re.DOTALL)
        failures = re.search(r"\*\*Failure Criteria.*?:\*\*\s*(.*?)(?=\n---|\Z)", body, flags=re.DOTALL)
        tests.append({
            "name": heading.split(":", 1)[-1].strip(),
            "input": given.group(1).strip() if given else "",
            "expected": bullets(expected.group(1)) if expected else [],
            "failures": bullets(failures.group(1)) if failures else [],
        })
    if not tests:
        fail(f"No '## Test Case N:' sections found in {path}")
    return tests


def parse_range(text):
    """'5+' -> (5, None), '3' -> (3, 3)."""
    if text.endswith("+"):
        return int(text[:-1]), None
    return int(text), int(text)


def in_range(n, bounds):
    low, high = bounds
    return n >= low and (high is None or n <= high)


def make_check(kind, args):
    """Turn one '- type: args' line into (name, function(text) -> (passed, detail)).

    Arguments are separated by ' | ' so that regexes can contain '|'.
    """
    parts = [p.strip() for p in args.split(" | ")]
    flags = re.IGNORECASE | re.MULTILINE

    if kind == "starts-with":
        pattern = parts[0]

        def run(text):
            first = text.lstrip().splitlines()[0] if text.strip() else ""
            return bool(re.match(pattern, first)), f"first line: {first[:60]!r}"
        return f"starts-with: {parts[1] if len(parts) > 1 else pattern}", run

    if kind == "count":
        pattern, bounds, label = parts[0], parse_range(parts[1]), parts[2]

        def run(text):
            n = len(re.findall(pattern, text, flags))
            return in_range(n, bounds), f"{n} found (need {parts[1]})"
        return f"count: {label}", run

    if kind == "headings":
        wanted = [w.strip() for w in args.split(",")]

        def run(text):
            titles = [l.lstrip("# ").lower() for l in text.splitlines() if l.startswith("#")]
            missing = [w for w in wanted if not any(w.lower() in t for t in titles)]
            return not missing, f"missing: {', '.join(missing)}" if missing else "all present"
        return f"headings: {', '.join(wanted)}", run

    if kind == "changelog":
        def run(text):
            version = re.search(r"^\*\*Version:\*\*\s*(\S+)", text, re.MULTILINE)
            date = re.search(r"^\*\*Date:\*\*\s*(\S+)", text, re.MULTILINE)
            if not (version and date):
                return False, "missing the **Version:** or **Date:** line"
            rows = [[c.strip() for c in line.strip().strip("|").split("|")]
                    for line in text.splitlines() if re.match(r"^\|\s*\d+\.\d+\s*\|", line)]
            if not rows:
                return False, "changelog has no data rows"
            top = rows[0]
            if len(top) < 4:
                return False, f"topmost row has {len(top)} of 4 fields"
            problems = []
            if top[0] != version.group(1):
                problems.append(f"version {version.group(1)} does not match row {top[0]}")
            if top[1] != date.group(1):
                problems.append(f"date {date.group(1)} does not match row {top[1]}")
            if not all(top[:4]):
                problems.append("an empty field in the topmost row")
            return not problems, "; ".join(problems) or "matches topmost row, all fields filled"
        return f"changelog: {args}", run

    if kind == "no-unmeasured":
        words = [w.strip() for w in args.split(",")]

        def run(text):
            hits = [w for w in words if re.search(rf"\b{re.escape(w)}\b", text, re.IGNORECASE)]
            return not hits, f"found: {', '.join(hits)}" if hits else "none found"
        return f"no-unmeasured: {', '.join(words)}", run

    fail(f"Unknown deterministic check type: '{kind}'")


def parse_checks(path):
    """Read the '## Deterministic Checks' section: one '- type: args' line per check."""
    section = re.search(r"^## Deterministic Checks\s*\n(.*?)(?=^## |\Z)",
                        path.read_text(), flags=re.MULTILINE | re.DOTALL)
    if not section:
        return []
    return [make_check(*(part.strip() for part in line.split(":", 1)))
            for line in bullets(section.group(1))]


def run_claude(prompt, model):
    """Call the Claude CLI with the prompt on stdin and return the reply text.

    The call runs from an empty folder outside the project, so the project's CLAUDE.md
    is never loaded. Tools are off, and the system prompt is replaced: with the CLI
    default, the model wrote tool calls as text. The JSON reply carries the usage
    ("usage" and "modelUsage") and the cost ("total_cost_usd"); verified on CLI 2.1.310.
    """
    cmd = ["claude", "-p", "--model", model, "--output-format", "json",
           "--tools", "", "--system-prompt", "You are a helpful assistant."]
    cwd = tempfile.mkdtemp(prefix="eval-call-")
    result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        fail(f"Claude CLI failed ({result.returncode}): {result.stderr.strip()}")
    try:
        data = json.loads(result.stdout)
    except ValueError:
        fail(f"Claude CLI did not return JSON: {result.stdout[:200]}")
    text = (data.get("result") or "").strip()
    if data.get("is_error") or not text:
        fail(f"Claude CLI returned an error or empty reply: {data.get('result')}")
    usage = data.get("usage", {})
    USAGE.append({
        "model": ", ".join(data.get("modelUsage", {})) or model,
        "input_tokens": usage.get("input_tokens", 0),
        "cache_write_tokens": usage.get("cache_creation_input_tokens", 0),
        "cache_read_tokens": usage.get("cache_read_input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "cost_usd": data.get("total_cost_usd", 0.0),
    })
    return text


def usage_line():
    """Totals over every recorded call. Input is uncached plus cache-write plus cache-read."""
    if not USAGE:
        return "no model calls"
    models = ", ".join(dict.fromkeys(u["model"] for u in USAGE))
    total = {k: sum(u[k] for u in USAGE) for k in
             ("input_tokens", "cache_write_tokens", "cache_read_tokens", "output_tokens", "cost_usd")}
    input_all = total["input_tokens"] + total["cache_write_tokens"] + total["cache_read_tokens"]
    return (f"{models}; {len(USAGE)} call(s); input {input_all} (uncached {total['input_tokens']}, "
            f"cache write {total['cache_write_tokens']}, cache read {total['cache_read_tokens']}), "
            f"output {total['output_tokens']}; cost ${total['cost_usd']:.4f}")


def judge(output, test, model):
    """Ask the model for a verdict on each of one test case's criteria."""
    criteria = [("C%d" % (i + 1), "Must be true", c) for i, c in enumerate(test["expected"])]
    criteria += [("F%d" % (i + 1), "Must NOT occur", c) for i, c in enumerate(test["failures"])]
    listing = "\n".join(f"{cid} ({kind}): {text}" for cid, kind, text in criteria)
    prompt = f"""You are grading the output of an AI skill against evaluation criteria.
Grade only the criteria listed. Do not add criteria of your own.

Test case: {test['name']}
Input: {test['input']}

Criteria:
{listing}

For a "Must be true" criterion, passed is true when the output satisfies it.
For a "Must NOT occur" criterion, passed is true when the output avoids it.
Score each criterion from 1 (clearly not met) to 5 (clearly met).

Return ONLY valid JSON in this shape, with one entry per criterion. Never use
double quotes inside the reasoning text; use single quotes if you must quote.
{{"criteria": [{{"id": "C1", "passed": true, "score": 5, "reasoning": "one or two sentences citing the output"}}]}}

=== OUTPUT TO GRADE ===
{output}
=== END OUTPUT ==="""
    verdicts = None
    for _ in range(2):  # models occasionally return invalid JSON; retry once
        raw = run_claude(prompt, model)
        try:
            verdicts = json.loads(raw[raw.find("{"):raw.rfind("}") + 1])["criteria"]
            break
        except (ValueError, KeyError):
            continue
    if verdicts is None:
        fail(f"Judge did not return valid JSON for '{test['name']}':\n{raw}")
    by_id = {v["id"]: v for v in verdicts}
    return [{"id": cid, "criterion": text, **by_id.get(
        cid, {"passed": False, "score": 0, "reasoning": "Judge returned no verdict."})}
        for cid, _, text in criteria]


def cell(text):
    return str(text).replace("|", "/").replace("\n", " ")


def write_report(path, title, model, prompt, deterministic, judged, pct):
    det_met = sum(r["passed"] for r in deterministic)
    verdicts = [v for t in judged for v in t["verdicts"]]
    judge_met = sum(v["passed"] for v in verdicts)
    overall = "PASS" if pct >= PASS_THRESHOLD else "FAIL"
    lines = [f"# {title}", "", f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
             f"- Judge model: {model}", f"- Usage: {usage_line()}",
             "- Context note: every call also carries the account email and the organization instructions. "
             "The system prompt is replaced, but these are added by the harness and cannot be removed from the CLI call.",
             ""]
    if prompt:
        lines += ["## Prompt", "", f"> {prompt}", ""]
    lines += ["## Summary", "",
              f"**Overall: {overall}** ({pct:.1f}% of criteria met; threshold {PASS_THRESHOLD:.0f}%)", "",
              "| Stage | Result | Detail |", "|---|---|---|",
              f"| Deterministic checks | {'PASS' if det_met == len(deterministic) else 'FAIL'} | "
              f"{det_met} of {len(deterministic)} passed |",
              f"| LLM judge | {'PASS' if judge_met == len(verdicts) else 'FAIL'} | "
              f"{judge_met} of {len(verdicts)} criteria passed |", "",
              "| Test case | Result | Criteria passed | Average score | Failed criteria |",
              "|---|---|---|---|---|"]
    for t in judged:
        vs = t["verdicts"]
        failed = ", ".join(v["id"] for v in vs if not v["passed"]) or "none"
        result = "PASS" if all(v["passed"] for v in vs) else "FAIL"
        lines.append(f"| {cell(t['name'])} | {result} | {sum(v['passed'] for v in vs)} of {len(vs)} | "
                     f"{sum(v['score'] for v in vs) / len(vs):.1f} | {failed} |")
    lines += ["", "## Deterministic checks", "", "| Check | Result | Detail |", "|---|---|---|"]
    for r in deterministic:
        lines.append(f"| {cell(r['name'])} | {'PASS' if r['passed'] else 'FAIL'} | {cell(r['detail'])} |")
    lines += ["", "## LLM judge", "",
              "Scores run from 1 (clearly not met) to 5 (clearly met) and are the judge's own rating.", ""]
    for t in judged:
        lines += [f"### {t['name']}", "", "| ID | Criterion | Result | Score | Reasoning |",
                  "|---|---|---|---|---|"]
        for v in t["verdicts"]:
            lines.append(f"| {v['id']} | {cell(v['criterion'])} | {'PASS' if v['passed'] else 'FAIL'} | "
                         f"{v['score']} | {cell(v['reasoning'])} |")
        lines.append("")
    path.write_text("\n".join(lines) + "\n")
    return overall


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("tests", type=Path)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--bare", type=Path, help="prompt file, sent to the model once, unchanged")
    source.add_argument("--output", type=Path, help="grade this file instead of calling the model")
    parser.add_argument("--artifact", default="output", help="name for the saved files")
    parser.add_argument("--model", default="sonnet", choices=APPROVED_MODELS)
    args = parser.parse_args()

    tests_path = args.tests.resolve()
    tests = parse_tests(tests_path)
    checks = parse_checks(tests_path)
    results_dir = tests_path.parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    prompt = None
    if args.bare:
        prompt = args.bare.read_text().strip()
        output = run_claude(prompt, args.model)
        (results_dir / f"{args.artifact}.md").write_text(output + "\n")
    else:
        output = args.output.read_text()

    deterministic = []
    for name, function in checks:
        passed, detail = function(output)
        deterministic.append({"name": name, "passed": passed, "detail": detail})
    judged = [{"name": t["name"], "verdicts": judge(output, t, args.model)} for t in tests]

    met = sum(r["passed"] for r in deterministic) + sum(v["passed"] for t in judged for v in t["verdicts"])
    total = len(deterministic) + sum(len(t["verdicts"]) for t in judged)
    pct = 100.0 * met / total if total else 0.0
    report = results_dir / f"{args.artifact}-results.md"
    overall = write_report(report, f"{args.artifact} - Evaluation Results", args.model, prompt,
                           deterministic, judged, pct)
    print(f"{overall}: {pct:.1f}% of criteria met ({met} of {total}).")
    print(f"Report: {report}")
    print(f"Usage: {usage_line()}")


if __name__ == "__main__":
    main()
