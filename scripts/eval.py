#!/usr/bin/env python3
"""Evaluate the output of a skill against a manually written test file.

Two run modes, as in eval.js:
  --baseline  the bare prompt, no skill. Re-running it resets the results
              folder for this skill and starts a fresh log (Run 001).
  --skill     the skill applied. Each run is the next iteration and is logged.

Two kinds of checks run, in this order:

1. Deterministic checks. Declared in the tests file under a
   '## Deterministic Checks' heading and run as plain Python. No model call:
   fast, free, and the same answer every time.
2. LLM judge. For each test case in the tests file, the output plus the test's
   Expected Output Criteria and Failure Criteria are sent to a model, which
   returns JSON with pass/fail, a score, and reasoning per criterion.

Scoring: the score is the percent of criteria met across all test cases, deterministic
and judged together. A run passes at 95% or more (PASS_THRESHOLD). Judged criteria that
were skipped count as not met. Every Claude CLI call is logged with model, tokens, and
cost. Each log entry records the hypothesis, the one change, the baseline, previous, and
resulting scores, and a reasoning line (--reasoning, or --reasoning-last afterwards).

The judge is skipped when a deterministic check fails (use --judge-anyway to
force it), because there is no point paying for a judgment on broken output.

Usage:
  python3 scripts/eval.py <skill> <tests.md> --check-ec
  python3 scripts/eval.py <skill> <tests.md> --reasoning-last "one line after seeing the result"
  python3 scripts/eval.py <skill> <tests.md> --baseline (--bare <prompt file or skill> | --output file)
  python3 scripts/eval.py <skill> <tests.md> --skill --hypothesis "..." --change "..."
                          [--reasoning "..."] [--output file]
                          [--per-input] [--args text] [--artifact name]
                          [--model sonnet|haiku] [--judge-anyway] [--no-judge]
                          [--out dir]

Where the output comes from:
  --baseline: --bare <prompt file or skill> sends that prompt to the model unchanged (no
              skill), or --output file grades a response you already have
  --skill:    --output file grades a file written by running /<skill> <path>
              in Claude Code, or with no --output the script runs the skill
              through the Claude CLI (passing the previous PRD so it is
              updated in place) and grades the reply

Files written to results/ next to the tests file (default):
  <skill>-<artifact>.md          the latest PRD from a --skill run
  <skill>-baseline-<artifact>.md the baseline output
  <skill>-results.md / .json     the latest report (summary first) and raw verdicts
  <skill>-run.log.md             the iteration log, one entry per run
  .<skill>-previous.md           the last PRD, so the next run can check its changelog
  .<skill>-input.snapshot        the tests and skill text used for the last run
"""

import argparse
import difflib
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPROVED_MODELS = ("sonnet", "haiku")
PASS_THRESHOLD = 95.0  # percent of criteria met across all test cases
USAGE = []  # one record per Claude CLI call in this run: model, tokens, cost


def fail(message):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def strip_frontmatter(text):
    """Drop the YAML block between the leading --- lines."""
    return re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL).strip()


def parse_tests(path):
    """Read tests written in the schemas/test-case.md format."""
    text = path.read_text()
    tests = []
    for block in re.split(r"^## Test Case ", text, flags=re.MULTILINE)[1:]:
        heading, _, body = block.partition("\n")
        name = heading.split(":", 1)[-1].strip()
        given = re.search(r"\*\*Input:\*\*\s*(.*?)\n\s*\n", body, flags=re.DOTALL)
        expected = re.search(
            r"\*\*Expected Output Criteria:\*\*\s*(.*?)(?=\*\*Failure Criteria|\Z)",
            body, flags=re.DOTALL)
        failures = re.search(r"\*\*Failure Criteria.*?:\*\*\s*(.*?)(?=\n---|\Z)",
                             body, flags=re.DOTALL)
        tests.append({
            "name": name,
            "input": given.group(1).strip() if given else "",
            "expected": bullets(expected.group(1)) if expected else [],
            "failures": bullets(failures.group(1)) if failures else [],
        })
    if not tests:
        fail(f"No '## Test Case N:' sections found in {path}")
    return tests


def bullets(block):
    return [line.lstrip("- ").strip() for line in block.splitlines() if line.startswith("- ")]


def run_claude(prompt, model, clean=False):
    """Call the locally authenticated Claude CLI. The prompt goes in on stdin.

    --output-format json returns the reply in "result" and the usage in "usage",
    "modelUsage", and "total_cost_usd" (fields verified against CLI 2.1.310).
    Every call is recorded in USAGE so the run log can report tokens and cost.
    clean=True runs from an empty folder outside the project, so the project's
    CLAUDE.md is not loaded into a baseline. It does not remove user-level config
    or the default system prompt.
    """
    cwd = tempfile.mkdtemp(prefix="eval-baseline-") if clean else None
    result = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json"],
                            input=prompt, capture_output=True, text=True, cwd=cwd)
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


def usage_totals():
    """Sum the recorded calls. Input is uncached plus cache-write plus cache-read tokens."""
    total = {k: sum(u[k] for u in USAGE) for k in
             ("input_tokens", "cache_write_tokens", "cache_read_tokens", "output_tokens", "cost_usd")}
    total["calls"] = len(USAGE)
    total["models"] = ", ".join(dict.fromkeys(u["model"] for u in USAGE)) or "-"
    total["input_all"] = total["input_tokens"] + total["cache_write_tokens"] + total["cache_read_tokens"]
    return total


def usage_line(total):
    if not total["calls"]:
        return "none (graded an existing file, no model call)"
    return (f"{total['models']}; {total['calls']} call(s); input {total['input_all']} "
            f"(uncached {total['input_tokens']}, cache write {total['cache_write_tokens']}, "
            f"cache read {total['cache_read_tokens']}), output {total['output_tokens']}; "
            f"cost ${total['cost_usd']:.4f}")


def generate(skill_body, arguments, model, previous=None, input_changes=None):
    prompt = skill_body
    if arguments:
        prompt += f"\n\nInput for this run:\n{arguments}"
    if previous:
        prompt += ("\n\nA previous PRD exists. Treat it as the existing PRD at the output path and update "
                   "it in place as the File Contract's versioning rules describe.\n\n"
                   f"What changed in the inputs since it was written:\n{input_changes}\n\n"
                   f"===BEGIN_PREVIOUS_PRD===\n{previous}\n===END_PREVIOUS_PRD===")
    # Without this, the model tends to describe the document instead of returning it.
    prompt += ("\n\n---\nRun this skill now. Reply with the complete finished document in "
               "Markdown. Do not summarize it, write files, or add commentary before or after it.")
    return run_claude(prompt, model)


def parse_range(text):
    """'5-8' -> (5, 8), '5+' -> (5, None), '3' -> (3, 3)."""
    text = text.strip()
    if text.endswith("+"):
        return int(text[:-1]), None
    low, _, high = text.partition("-")
    return int(low), int(high or low)


def in_range(n, bounds):
    low, high = bounds
    return n >= low and (high is None or n <= high)


def describe(bounds):
    low, high = bounds
    return f"{low}+" if high is None else f"{low}-{high}" if high != low else str(low)


CONTEXT = {"previous": None}  # the last PRD from a --skill run, set by main() for the changelog check
VERSION = re.compile(r"\*\*Version:\*\*\s*(\d+)\.(\d+)")


def changelog_rows(text):
    rows = []
    for line in text.splitlines():
        m = re.match(r"^\|\s*(\d+\.\d+)\s*\|", line)
        if m:
            cells = [c.strip() for c in line.split("|")[1:-1]]
            rows.append({"version": m.group(1), "changes": "|".join(cells[3:]), "line": line.strip()})
    return rows


def check_changelog(text, previous):
    """Version and changelog rules: 1.0 for a new PRD; unchanged or one minor bump when updating."""
    current = VERSION.search(text)
    if not current:
        return False, "no **Version:** line"
    version = f"{current.group(1)}.{current.group(2)}"
    rows = changelog_rows(text)
    before = VERSION.search(previous) if previous else None
    if not before:
        ok = version == "1.0" and len(rows) == 1
        return ok, f"new PRD: version {version}, {len(rows)} changelog row(s) (need 1.0 and exactly 1)"
    old_version = f"{before.group(1)}.{before.group(2)}"
    old_rows = changelog_rows(previous)
    if version == old_version:
        ok = rows == old_rows
        return ok, f"version unchanged at {version}" + ("" if ok else ", but the changelog was altered")
    if version != f"{before.group(1)}.{int(before.group(2)) + 1}":
        return False, f"version {version} is neither {old_version} nor the next minor version"
    if not rows or rows[0]["version"] != version:
        return False, f"changelog has no newest-first entry for {version}"
    if "reason:" not in rows[0]["changes"].lower():
        return False, f"entry for {version} does not state a reason"
    if len(rows[0]["changes"]) > 250:
        return False, f"entry for {version} is {len(rows[0]['changes'])} characters (max 200)"
    lost = [r["version"] for r in old_rows if r["line"] not in {x["line"] for x in rows}]
    if lost:
        return False, f"earlier changelog rows altered or removed: {', '.join(lost)}"
    return True, f"{old_version} to {version}, new row first, earlier rows preserved"


def make_check(kind, args):
    """Turn one '- type: args' line into (name, function(text) -> (passed, detail)).

    Arguments are separated by ' | ' (with spaces) so regexes can use |.
    """
    parts = [p.strip() for p in args.split(" | ")]
    flags = re.IGNORECASE | re.MULTILINE

    if kind == "headings":
        wanted = [w.strip() for w in args.split(",")]

        def run(text):
            titles = [l.lstrip("# ").lower() for l in text.splitlines() if l.startswith("#")]
            missing = [w for w in wanted if not any(w.lower() in t for t in titles)]
            return not missing, f"missing: {', '.join(missing)}" if missing else "all present"
        return f"headings: {', '.join(wanted)}", run

    if kind == "count":
        pattern, bounds, label = parts[0], parse_range(parts[1]), parts[2]

        def run(text):
            n = len(re.findall(pattern, text, flags))
            return in_range(n, bounds), f"{n} found (need {describe(bounds)})"
        return f"count: {label}", run

    if kind == "each-matches":
        start, pattern, bounds, label = parts[0], parts[1], parse_range(parts[2]), parts[3]

        def run(text):
            # Items begin at each line matching `start`; text before the first is ignored.
            starts = [m.start() for m in re.finditer(start, text, flags)]
            if not starts:
                return False, "no items found"
            chunks = [text[i:j] for i, j in zip(starts, starts[1:] + [len(text)])]
            counts = [len(re.findall(pattern, c, flags)) for c in chunks]
            bad = [f"item {i + 1} has {n}" for i, n in enumerate(counts) if not in_range(n, bounds)]
            detail = f"{len(chunks)} items, all within {describe(bounds)}"
            return not bad, f"{'; '.join(bad[:3])} (need {describe(bounds)})" if bad else detail
        return f"each-matches: {label}", run

    if kind == "starts-with":
        pattern = parts[0]

        def run(text):
            first = text.lstrip().splitlines()[0] if text.strip() else ""
            return bool(re.match(pattern, first)), f"first line: {first[:60]!r}"
        return f"starts-with: {parts[1] if len(parts) > 1 else pattern}", run

    if kind == "changelog":
        return f"changelog: {args}", lambda text: check_changelog(text, CONTEXT["previous"])

    if kind == "no-unmeasured":
        words = [w.strip() for w in args.split(",")]

        def run(text):
            bad = [l.strip()[:60] for l in text.splitlines()
                   if any(re.search(rf"\b{w}\b", l, re.IGNORECASE) for w in words)
                   and not re.search(r"\d", l)]
            return not bad, f"{len(bad)} line(s) without a number: {bad[:2]}" if bad else "none found"
        return f"no-unmeasured: {', '.join(words)}", run

    fail(f"Unknown deterministic check type: '{kind}'")


def parse_checks(path):
    """Read the '## Deterministic Checks' section of the tests file."""
    section = re.search(r"^## Deterministic Checks\s*\n(.*?)(?=^## |^---|\Z)",
                        path.read_text(), flags=re.MULTILINE | re.DOTALL)
    if not section:
        print("Note: no '## Deterministic Checks' section in the tests file; none run.")
        return []
    checks = []
    for line in bullets(section.group(1)):
        kind, _, args = line.partition(":")
        checks.append(make_check(kind.strip(), args.strip()))
    return checks


def run_deterministic(checks, output):
    results = []
    for name, function in checks:
        passed, detail = function(output)
        results.append({"name": name, "passed": passed, "detail": detail})
    return results


def judge(output, test, model):
    """Ask a model to grade the output against one test case's criteria."""
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
    for attempt in range(2):  # models occasionally emit invalid JSON; retry once
        raw = run_claude(prompt, model)
        start, end = raw.find("{"), raw.rfind("}")
        try:
            verdicts = json.loads(raw[start:end + 1])["criteria"]
            break
        except (ValueError, KeyError):
            continue
    if verdicts is None:
        fail(f"Judge did not return valid JSON for '{test['name']}':\n{raw}")
    by_id = {v["id"]: v for v in verdicts}
    return [{"id": cid, "kind": kind, "criterion": text, **by_id.get(
        cid, {"passed": False, "score": 0, "reasoning": "Judge returned no verdict."})}
        for cid, kind, text in criteria]


def cell(text):
    return str(text).replace("|", "/").replace("\n", " ")


def compute_score(deterministic, judged, tests, skipped_judge):
    """Percent of criteria met across all test cases, deterministic and judged together.

    Judged criteria that never ran because a deterministic check failed count as
    not met, so a skipped judge cannot inflate the score. With --no-judge the score
    covers deterministic checks only and the run can never be a PASS.
    """
    met = sum(r["passed"] for r in deterministic) + sum(
        v["passed"] for t in judged for v in t["verdicts"])
    total = len(deterministic) + sum(len(t["verdicts"]) for t in judged)
    if skipped_judge:
        total += sum(len(t["expected"]) + len(t["failures"]) for t in tests)
    pct = 100.0 * met / total if total else 0.0
    if not judged and not skipped_judge:
        overall = "NOT JUDGED"
    else:
        overall = "PASS" if pct >= PASS_THRESHOLD else "FAIL"
    return {"met": met, "total": total, "pct": pct, "overall": overall}


def summarize(deterministic, judged, skipped_judge, score):
    """High-level numbers for the report: stage results and one row per test case."""
    det_pass = sum(r["passed"] for r in deterministic)
    verdicts = [v for t in judged for v in t["verdicts"]]
    judge_pass = sum(v["passed"] for v in verdicts)
    det_ok = det_pass == len(deterministic)
    judge_ok = bool(judged) and judge_pass == len(verdicts)
    overall = score["overall"]
    lines = [f"**Overall: {overall}** ({score['pct']:.1f}% of criteria met, "
             f"{score['met']} of {score['total']}; threshold {PASS_THRESHOLD:.0f}%)",
             "", "| Stage | Result | Detail |", "|---|---|---|",
             f"| Deterministic checks | {'PASS' if det_ok else 'FAIL'} | {det_pass} of {len(deterministic)} passed |"]
    if judged:
        avg = sum(v["score"] for v in verdicts) / len(verdicts)
        lines.append(f"| LLM judge | {'PASS' if judge_ok else 'FAIL'} | {judge_pass} of {len(verdicts)} criteria passed, average score {avg:.1f} of 5 |")
        lines += ["", "| Test case | Passed | Average score | Failed criteria |", "|---|---|---|---|"]
        for t in judged:
            vs = t["verdicts"]
            failed = ", ".join(v["id"] for v in vs if not v["passed"]) or "none"
            lines.append(f"| {cell(t['name'])} | {sum(v['passed'] for v in vs)} of {len(vs)} | "
                         f"{sum(v['score'] for v in vs) / len(vs):.1f} | {failed} |")
    else:
        reason = "skipped because a deterministic check failed" if skipped_judge else "not run"
        lines.append(f"| LLM judge | - | {reason} |")
    return overall, lines


def stats(data):
    """Counts used in the log and for comparing with the baseline."""
    verdicts = [v for t in data["judge"] for v in t["verdicts"]]
    return {
        "det_pass": sum(r["passed"] for r in data["deterministic"]),
        "det_total": len(data["deterministic"]),
        "judge_pass": sum(v["passed"] for v in verdicts),
        "judge_total": len(verdicts),
        "avg": sum(v["score"] for v in verdicts) / len(verdicts) if verdicts else None,
    }


def write_report(paths, skill, model, deterministic, judged, skipped_judge, meta, score, tests):
    overall, summary = summarize(deterministic, judged, skipped_judge, score)
    lines = [f"# {skill} - Evaluation Results", "", f"- Iteration: {meta['iteration']}",
             f"- Timestamp: {meta['stamp']}", f"- Mode: {meta['mode']}", f"- Judge model: {model}",
             f"- Hypothesis: {meta['hypothesis']}", f"- Change: {meta['change']}",
             f"- Usage: {usage_line(usage_totals())}"]
    if meta["version"]:
        lines.append(f"- PRD version: {meta['version']}")
    lines += ["", "## Summary", ""] + summary
    if meta["vs_baseline"]:
        lines += ["", f"- {meta['vs_baseline']}"]
    lines += ["",
              "Scores run from 1 (clearly not met) to 5 (clearly met) and are the judge's own rating. Pass or fail is the judge's verdict on whether the criterion is satisfied.",
              "", "## Deterministic checks", "", "| Check | Result | Detail |", "|---|---|---|"]
    for r in deterministic:
        lines.append(f"| {cell(r['name'])} | {'PASS' if r['passed'] else 'FAIL'} | {cell(r['detail'])} |")
    if not deterministic:
        lines.append("| (none defined) | - | - |")
    lines += ["", "## LLM judge", ""]
    if skipped_judge:
        lines.append("Skipped: a deterministic check failed.")
    for test in judged:
        lines += [f"### {test['name']}", "", "| ID | Criterion | Result | Score | Reasoning |",
                  "|---|---|---|---|---|"]
        for v in test["verdicts"]:
            lines.append(f"| {v['id']} | {cell(v['criterion'])} | "
                         f"{'PASS' if v['passed'] else 'FAIL'} | {v['score']} | {cell(v['reasoning'])} |")
        lines.append("")
    paths["results"].write_text("\n".join(lines) + "\n")
    paths["json"].write_text(json.dumps(
        {"skill": skill, "run": meta["stamp"], "mode": meta["mode"], "iteration": meta["iteration"],
         "model": model, "hypothesis": meta["hypothesis"], "change": meta["change"],
         "score": score, "threshold": PASS_THRESHOLD, "usage": usage_totals(), "calls": USAGE,
         "deterministic": deterministic, "judge": judged,
         "judge_skipped": skipped_judge}, indent=2) + "\n")


def next_run_number(log_path):
    if not log_path.exists():
        return 1
    return len(re.findall(r"^## Run \d+", log_path.read_text(), flags=re.MULTILINE)) + 1


def logged_scores(log_path):
    """Every score in the iteration log, oldest first. The first is the baseline."""
    if not log_path.exists():
        return []
    return [float(s) for s in re.findall(r"^- Score: ([\d.]+)%", log_path.read_text(), flags=re.MULTILINE)]


def add_reasoning(log_path, text):
    """Fill the newest log entry's pending reasoning line (written after seeing the result)."""
    if not log_path.exists():
        fail(f"No log at {log_path}")
    log = log_path.read_text()
    index = log.rfind("- Reasoning: (pending)")
    if index == -1:
        fail("The newest log entry has no pending reasoning line.")
    log = log[:index] + f"- Reasoning: {text}" + log[index + len("- Reasoning: (pending)"):]
    log_path.write_text(log)


def append_log(log_path, skill, entry):
    if not log_path.exists():
        log_path.write_text(f"# {skill} - Iteration Log\n")
    with log_path.open("a") as f:
        f.write("\n" + "\n".join(entry) + "\n")


def input_snapshot(tests_path, skill_file, prompt_file):
    parts = [f"# TESTS FILE\n{tests_path.read_text()}"]
    if skill_file:
        parts.append(f"# SKILL FILE\n{skill_file.read_text()}")
    if prompt_file:
        parts.append(f"# PROMPT FILE\n{prompt_file.read_text()}")
    return "\n".join(parts)


def check_ec(tests, checks):
    """Inspect the evaluation criteria themselves. Returns a list of problems."""
    problems = []
    for name, function in checks:
        try:
            function("")  # compiles every regex; a bad pattern raises re.error
        except re.error as error:
            problems.append(f"Deterministic check '{name}' has an invalid regex: {error}")
    for i, t in enumerate(tests, 1):
        label = f"Test case {i} ({t['name']})"
        if not t["input"] or t["input"].startswith("["):
            problems.append(f"{label}: Input is empty or still a placeholder.")
        if not t["expected"]:
            problems.append(f"{label}: no Expected Output Criteria.")
        if not t["failures"]:
            problems.append(f"{label}: no Failure Criteria (each case needs at least one).")
        if any(c.startswith("[") for c in t["expected"] + t["failures"]):
            problems.append(f"{label}: a criterion is still a template placeholder.")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("skill")
    parser.add_argument("tests", type=Path)
    parser.add_argument("--baseline", action="store_true",
                        help="the bare prompt, no skill; resets this skill's results and log")
    parser.add_argument("--skill", dest="use_skill", action="store_true",
                        help="the skill applied; logged as the next iteration")
    parser.add_argument("--output", type=Path, help="grade this file instead of generating one")
    parser.add_argument("--bare", type=Path, help="baseline only: the prompt, sent to the model unchanged (a skill file works; its frontmatter is dropped)")
    parser.add_argument("--per-input", action="store_true",
                        help="run the skill once per test case, using its Input as the skill input")
    parser.add_argument("--artifact", default="output",
                        help="name for the saved output file: <skill>-<artifact>.md (e.g. prd)")
    parser.add_argument("--args", default="", help="input text passed to the skill")
    parser.add_argument("--model", default="sonnet", choices=APPROVED_MODELS)
    parser.add_argument("--judge-anyway", action="store_true")
    parser.add_argument("--no-judge", action="store_true")
    parser.add_argument("--hypothesis", help="what you expect this run to show (required for --skill)")
    parser.add_argument("--change", help="the ONE change made since the previous run (required for --skill)")
    parser.add_argument("--reasoning", help="one line on what the result says about the hypothesis")
    parser.add_argument("--reasoning-last", metavar="TEXT",
                        help="write the reasoning line of the newest log entry and exit; no run")
    parser.add_argument("--check-ec", action="store_true",
                        help="inspect the tests file (criteria and checks) and exit; no skill run, no model call")
    parser.add_argument("--out", type=Path, help="results directory (default: <tests dir>/results)")
    args = parser.parse_args()

    skill_file = ROOT / "skills" / args.skill / "SKILL.md"
    tests_path = args.tests if args.tests.is_absolute() else Path.cwd() / args.tests
    tests = parse_tests(tests_path)
    if args.check_ec:
        checks = parse_checks(tests_path)
        problems = check_ec(tests, checks)
        total = sum(len(t["expected"]) + len(t["failures"]) for t in tests)
        print(f"Evaluation criteria: {len(checks)} deterministic checks, {len(tests)} test cases, "
              f"{total} judged criteria")
        for t in tests:
            print(f"  {t['name']}: {len(t['expected'])} expected, {len(t['failures'])} failure")
        print("Problems:" if problems else "No problems found.")
        for problem in problems:
            print(f"  - {problem}")
        sys.exit(1 if problems else 0)

    if args.reasoning_last:
        results_dir = args.out or tests_path.parent / "results"
        add_reasoning(results_dir / f"{args.skill}-run.log.md", args.reasoning_last)
        print("Reasoning recorded in the newest log entry.")
        sys.exit(0)

    if args.baseline == args.use_skill:
        fail("Choose exactly one of --baseline or --skill.")
    if args.use_skill and not (args.hypothesis and args.change):
        fail("A --skill run needs --hypothesis and --change: one hypothesis, one change per iteration.")
    hypothesis = args.hypothesis or "The bare prompt establishes the Red state."
    change = args.change or "None (bare prompt, no skill)"
    if args.use_skill and not skill_file.exists():
        fail(f"Skill not found: {skill_file.relative_to(ROOT)}")
    if args.output and args.bare:
        fail("Use either --output or --bare, not both.")
    if args.baseline and not (args.bare or args.output):
        fail("A baseline is the bare prompt, with no skill. Give --bare <prompt.txt> "
             "(or --output <file> for a response you already have).")
    if args.use_skill and args.bare:
        fail("--bare is for --baseline. A --skill run applies the skill: use --output or no source.")

    results_dir = args.out or tests_path.parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "prd": results_dir / f"{args.skill}-{args.artifact}.md",
        "baseline": results_dir / f"{args.artifact}.md",
        "results": results_dir / f"{args.skill}-results.md",
        "json": results_dir / f"{args.skill}-results.json",
        "log": results_dir / f"{args.skill}-run.log.md",
        "previous": results_dir / f".{args.skill}-previous.md",
        "snapshot": results_dir / f".{args.skill}-input.snapshot",
    }
    started = datetime.now()
    mode = "baseline" if args.baseline else "skill"
    output_file = args.output.resolve() if args.output else None

    # A baseline resets this skill's results and starts a fresh log. The graded
    # file is read first so a baseline response stored in results/ survives.
    graded = output_file.read_text() if output_file else None
    if args.baseline:
        removed = [p.name for p in paths.values() if p.exists() and p.resolve() != output_file]
        for p in paths.values():
            if p.exists() and p.resolve() != output_file:
                p.unlink()
        if removed:
            print(f"Baseline reset: removed {', '.join(removed)}")

    iteration = f"{next_run_number(paths['log']):03d}"
    previous = paths["previous"].read_text() if paths["previous"].exists() else None
    CONTEXT["previous"] = previous if args.use_skill else None
    body = strip_frontmatter(skill_file.read_text()) if args.use_skill else None
    snapshot = input_snapshot(tests_path, None if args.baseline else skill_file, args.bare)

    # One output shared by every test case, unless --per-input is set.
    if graded is not None:
        outputs = [graded] * len(tests)
    elif args.bare:
        # One bare output, shared by every test case, as the exercise specifies.
        outputs = [run_claude(strip_frontmatter(args.bare.read_text()), args.model, clean=True)] * len(tests)
    elif args.per_input:
        outputs = [generate(body, t["input"], args.model) for t in tests]
    else:
        changes = "(none recorded)"
        if previous and paths["snapshot"].exists():
            old = paths["snapshot"].read_text().splitlines()
            diff = "\n".join(difflib.unified_diff(old, snapshot.splitlines(), "previous", "current", lineterm=""))
            changes = f"Unified diff of the tests and skill:\n{diff}" if diff else "No changes to the tests or skill."
        outputs = [generate(body, args.args, args.model, previous, changes)] * len(tests)
    saved = "\n\n---\n\n".join(dict.fromkeys(outputs)) + "\n"
    target = paths["baseline"] if args.baseline else paths["prd"]
    if output_file is None or output_file != target.resolve():
        target.write_text(saved)

    checks = parse_checks(tests_path)
    deterministic = []
    for test, output in zip(tests, outputs):
        for r in run_deterministic(checks, output):
            if args.per_input:
                r["name"] = f"{test['name']}: {r['name']}"
            if not any(d["name"] == r["name"] for d in deterministic):
                deterministic.append(r)
    deterministic_ok = all(r["passed"] for r in deterministic)

    skip_judge = args.no_judge or (not deterministic_ok and not args.judge_anyway)
    judged = []
    if not skip_judge:
        for test, output in zip(tests, outputs):
            judged.append({"name": test["name"], "verdicts": judge(output, test, args.model)})
    skipped_judge = skip_judge and not args.no_judge

    st = stats({"deterministic": deterministic, "judge": judged})
    score = compute_score(deterministic, judged, tests, skipped_judge)
    version_match = VERSION.search(outputs[0])
    version = f"{version_match.group(1)}.{version_match.group(2)}" if version_match else None
    first_row = next(iter(changelog_rows(outputs[0])), None)
    earlier = logged_scores(paths["log"])
    baseline_pct = earlier[0] if earlier else None
    previous_pct = earlier[-1] if earlier else None
    vs_baseline = ""
    if args.use_skill and baseline_pct is not None:
        vs_baseline = (f"Change vs baseline: {baseline_pct:.1f}% to {score['pct']:.1f}% "
                       f"({score['pct'] - baseline_pct:+.1f} points)")
    meta = {"iteration": iteration, "mode": mode, "stamp": started.strftime("%Y-%m-%d %H:%M:%S"),
            "version": version, "vs_baseline": vs_baseline, "hypothesis": hypothesis, "change": change}
    write_report(paths, args.skill, args.model, deterministic, judged, skipped_judge, meta, score, tests)
    overall, summary = summarize(deterministic, judged, skipped_judge, score)

    old_version = VERSION.search(previous) if previous and args.use_skill else None
    old_version = f"{old_version.group(1)}.{old_version.group(2)}" if old_version else None
    fmt = lambda p: f"{p:.1f}%" if p is not None else "-"
    entry = [f"## Run {iteration}", "", f"- Timestamp: {meta['stamp']}", f"- Mode: {mode}",
             f"- Model: {args.model}",
             f"- Hypothesis: {hypothesis}", f"- Change: {change}",
             f"- Baseline score: {fmt(baseline_pct if baseline_pct is not None else score['pct'])}",
             f"- Previous score: {fmt(previous_pct)}",
             f"- Score: {score['pct']:.1f}% ({score['met']} of {score['total']} criteria; threshold {PASS_THRESHOLD:.0f}%)",
             f"- Reasoning: {args.reasoning or '(pending)'}",
             f"- Usage: {usage_line(usage_totals())}",
             f"- Skill: {args.skill if args.use_skill else '-'}",
             f"- Previous PRD version: {old_version or '-'}",
             f"- Duration: {(datetime.now() - started).total_seconds():.1f}s",
             f"- PRD version: {version or '-'}" + (" (unchanged)" if version and version == old_version else ""),
             f"- PRD changes: {first_row['changes'] if first_row else '-'}",
             f"- Deterministic: {st['det_pass']}/{st['det_total']} passed"]
    if st["judge_total"]:
        entry.append(f"- Judge: {st['judge_pass']}/{st['judge_total']} passed, average score {st['avg']:.1f}")
    else:
        entry.append("- Judge: " + ("skipped, a deterministic check failed" if skipped_judge else "not run"))
    if vs_baseline:
        entry.append(f"- {vs_baseline}")
    entry.append(f"- Overall result: {overall}")
    append_log(paths["log"], args.skill, entry)

    if args.use_skill:
        paths["previous"].write_text(outputs[0])
    paths["snapshot"].write_text(snapshot)

    print("\n".join(summary[:6]))
    if vs_baseline:
        print(vs_baseline)
    print(f"Report: {paths['results']}")
    print(f"Log: {paths['log']}")
    print(f"Usage: {usage_line(usage_totals())}")
    sys.exit(0 if overall == "PASS" else 1)


if __name__ == "__main__":
    main()
