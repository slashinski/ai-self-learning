# Exercise 3: Promptfoo Setup and Baseline

*Estimated time: 105 minutes*
*Prerequisites: Exercises 1 and 2 completed and committed*

---

## Goal

Install Promptfoo, convert your manual test cases to Promptfoo format, and run your first automated evaluation against `create-scope` — on **two models simultaneously**. By the end of this exercise you will have a baseline score for both a capable model (Sonnet or GPT-4o) and a lower-cost model (Haiku or GPT-4o mini). The gap between them is your Model Ladder starting point.

---

## Why Promptfoo

Manual testing against written criteria works, but it does not scale. As you build more commands and iterate on them, you need a way to run all your test cases automatically and get a consistent score. Promptfoo is the EDD measurement tool for this program.

More importantly: Promptfoo with `llm-rubric` assertions lets you test criteria that cannot be expressed as simple string matches. "Does this scope document surface timer drift as an explicit non-functional requirement with a measurable definition?" is a criterion that a human can evaluate and that an `llm-rubric` assertion can evaluate. This is how you close the gap between what you care about and what you can measure.

---

## Why Two Models From the Start

Every Promptfoo configuration in this program runs against two providers: a capable model and a lower-cost model. This is not a cost-optimization exercise bolted on at the end — it is an integral part of EDD.

When you run against only Sonnet, you cannot tell whether your instructions are clear or whether Sonnet is inferring what you meant. The lower-cost model is a diagnostic instrument: it is less forgiving of ambiguity, so when it fails an assertion that Sonnet passes, it is telling you something specific about where your prompt is underspecified.

The gap you measure today is your Model Ladder baseline. You will use it in Exercise 4.

---

## Use CLI Providers Instead of API Keys

Before configuring Promptfoo, copy the provider wrapper scripts from **[github.com/improving/promptfoo](https://github.com/improving/promptfoo)** into your project directory alongside your Promptfoo YAML files.

The repository provides JavaScript wrapper scripts — `claude.js`, `gh_copilot.js`, `devin.js`, `gemini.js` — that route Promptfoo evaluations through your installed AI CLI tools rather than calling a model API directly. Each script auto-detects whether it is being called as a **provider** (evaluating your prompt) or as a **grader** (scoring an `llm-rubric` assertion) and handles both cases through the CLI.

**Why this matters:**

**No API key required.** The wrappers use the same authentication your CLI tools already have. If you have Claude Code installed and authenticated, `claude.js` handles both provider calls and rubric grading — no separate API key or environment variable needed.

**Closes the tool gap.** When Promptfoo calls a model via the API directly, the model runs without the tool environment your CLI provides — no file access, no bash, none of the built-in tools from Claude Code, GitHub Copilot, or other AI CLI environments. If your prompts depend on those tools, or if you want evaluations to reflect how the model actually behaves in your workflow, the CLI wrapper is the accurate path. Evaluations against the raw API are testing a different configuration than the one your team actually uses.

Copy `claude.js` (or whichever wrapper matches your CLI tooling) from the repository into the same directory as your Promptfoo configuration files. The provider and grader configuration in Step 2 uses these scripts.

---

## Step 1: Install Promptfoo (15 minutes)

If you have not already installed Promptfoo:

```bash
npm install -g promptfoo
```

Verify installation:

```bash
promptfoo --version
```

Verify your Claude Code CLI is installed and authenticated:

```bash
claude --version
```

The `claude.js` wrapper from the previous section uses this CLI for both provider calls and `llm-rubric` grading — no separate API key is required.

---

## Step 2: Understand the Promptfoo Configuration Format (10 minutes)

A Promptfoo configuration is a YAML file that specifies the prompt to test, the test inputs, and the assertions each output must satisfy.

Here is the basic structure with **two providers**:

```yaml
prompts:
  - id: create-scope
    raw: |
      [your RTCC prompt text goes here]

      Product Description:
      {{product_description}}

# Route llm-rubric grading through the Claude Code CLI — no API key needed
defaultTest:
  options:
    provider: 'exec: node ./claude.js'

providers:
  - id: 'exec: node ./claude.js'
    label: sonnet
    config:
      model: sonnet
  - id: 'exec: node ./claude.js'
    label: haiku
    config:
      model: haiku

tests:
  - vars:
      product_description: |
        Pomodoro timer with 25-minute work intervals, 5-minute break intervals,
        audio notifications at each transition, session tracking per day, and a
        weekly productivity heat map showing sessions completed per day.
    assert:
      - type: llm-rubric
        value: "The scope document contains a Non-Functional Requirements section that addresses timing accuracy with a specific, measurable definition — not just the word 'accurate'."
      - type: llm-rubric
        value: "The scope document explicitly declares what is out of scope for V1, naming at least three items a developer might reasonably assume were in scope."
      - type: llm-rubric
        value: "The scope document surfaces at least one browser API dependency (such as the Notifications API, AudioContext, or localStorage) with a note about required user permission or browser support."
```

The two assertion types you will use most:

**`contains`** — checks that the output contains a specific string. Fast and cheap. Use for format requirements (e.g., must include a specific section heading).

**`llm-rubric`** — passes the output and the rubric text to an LLM and asks whether the criterion is met. Handles qualitative criteria. The rubric text should be the same language you used in your manual test file.

The `label` field on each provider is optional but makes your results table readable — you will see "sonnet" and "haiku" as column headers instead of full model IDs.

---

---

### Session Break Point

If you are completing this exercise across two sessions, this is the natural stopping point. Steps 1–2 installed Promptfoo and explained the configuration format. Steps 3–7 convert your tests, run evaluations, and record baselines. Pick up from here in your next session.

---

## Step 3: Convert Your Test Cases (30 minutes)

Create a file called `create-scope-promptfoo.yaml` in your repository. Convert at least 3 of your 5 manual test cases to Promptfoo format.

For each test case:
1. The `vars.product_description` (or equivalent variable name) should match your manual test case input
2. Each Expected Output Criterion from your manual test file should become an `llm-rubric` assertion
3. Each Failure Criterion from your manual test file should become an `llm-rubric` assertion phrased as what should NOT be true

**Important:** Your `llm-rubric` assertions should be specific enough to fail. An assertion that always passes regardless of output is not testing anything useful. If you find that an assertion always passes, the rubric text is not specific enough — rewrite it so that bad output would fail it.

Example of a too-permissive rubric: "The output includes requirements."

Example of a useful rubric: "The scope document includes a measurable definition of timer accuracy — a specific tolerance (e.g., ±1 second per 25-minute interval) or equivalent — not just a statement that the timer should be accurate."

---

## Step 4: Run Promptfoo and Record Both Baselines (25 minutes)

Run Promptfoo against your configuration:

```bash
promptfoo eval -c create-scope-promptfoo.yaml --no-cache
```

Always use `--no-cache` with CLI-backed providers. Promptfoo's cache keys are based on provider string and prompt text only — they do not detect changes to the wrapper scripts themselves, so stale results can silently appear if the flag is omitted.

Promptfoo will print a results table showing pass/fail per assertion per test case, broken out by provider. You will see separate results for Sonnet and Haiku.

**Record both baseline scores in your test file:**

```
## Promptfoo Baseline Run — [date]
Sonnet score: X/Y assertions passing
Haiku score:  X/Y assertions passing
Model Ladder delta: [Sonnet score] - [Haiku score] = [N] assertions
Config: create-scope-promptfoo.yaml
```

The delta is not a problem to solve right now. It is a measurement. You will analyze it in Exercise 4.

---

## Step 5: Read the Delta (15 minutes)

Look at which assertions Haiku fails that Sonnet passes. For each one, write a brief hypothesis in this form:

> "The assertion [describe it] fails on Haiku but passes on Sonnet. My hypothesis: Sonnet is inferring [specific thing] from the product description without being told. Haiku is not. If I add [specific instruction] to the [Context / Constraints] section, I predict Haiku will pass this assertion."

You do not need to act on these hypotheses yet. Write them down and commit them with your test file. You will use them in Exercise 4.

If Haiku and Sonnet have identical scores: either your assertions are not specific enough to distinguish model performance (in which case, strengthen the rubric text), or your prompt is already very well-specified (unlikely at this stage — examine your rubrics).

---

## Step 6: Identify the Weakest Assertion Across Both Models (5 minutes)

Which assertion failed most consistently — across both models and across multiple test cases? Write a specific hypothesis for why it is failing. This is your first iteration target for Exercise 4.

---

## Step 7: Commit Everything

Commit `create-scope-promptfoo.yaml` and your updated test file (with both baseline scores and your delta hypotheses). The Promptfoo configuration should be committed alongside the command it tests.

---

## Self-Check

Before moving to Exercise 4, verify:

- [ ] Promptfoo is installed and runs without errors
- [ ] `claude.js` (or equivalent wrapper from [improving/promptfoo](https://github.com/improving/promptfoo)) committed alongside your Promptfoo configuration
- [ ] `create-scope-promptfoo.yaml` is committed with at least 3 test cases and two providers
- [ ] Each test case has at least 2 assertions
- [ ] At least one `llm-rubric` assertion is failing on at least one model (if all pass on both, the rubrics are too permissive)
- [ ] Both Sonnet and Haiku baseline scores are recorded in your test file
- [ ] Your Model Ladder delta hypotheses are written and committed
- [ ] The Promptfoo config is committed alongside the command file, not separately
