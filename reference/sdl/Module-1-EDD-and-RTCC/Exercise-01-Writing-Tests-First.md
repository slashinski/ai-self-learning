# Exercise 1: Writing Tests First

*Estimated time: 90 minutes*
*Prerequisites: None — this is the starting point*

---

## Goal

Write a manual test file for a `create-scope` prompt that does not exist yet. The prompt will generate a scope document for a Pomodoro timer application. You will write the test file before building any prompt, so that your test cases capture what you actually need — not what the model produces by default.

---

## Background: Why This Comes First

The most common failure in prompt engineering is building first and testing second. When you build the prompt first, the output shapes your idea of what "good" looks like. By the time you write the test, you have already been anchored by what the model produces — and your criteria drift toward "what the model does" rather than "what I actually need."

Writing the test first forces you to commit to a specific definition of success. This is uncomfortable, because you have to define success before you have seen an example of it. That discomfort is the point. If you can't describe what a good scope document looks like without seeing one first, you do not yet understand what you need.

---

## The Task

You are going to write a manual test file for this bare prompt:

> `"Write a scope document for a Pomodoro timer application with 25-minute work intervals, 5-minute break intervals, session tracking, and a weekly productivity heat map."`

This prompt will become the `create-scope` command you build in Exercise 2. For now, you are only writing the tests — not the prompt.

---

## Step 1: Understand the Domain (15 minutes)

Before you can write good test criteria for a scope document, you need a clear picture of what a developer-ready scope document actually contains. Think through these questions — write your answers down, even briefly:

1. What sections would a skilled Product Manager always include in a scope document that a developer needs before beginning implementation? Think beyond the feature list: non-functional requirements, success criteria, explicit out-of-scope items, and open questions.

2. What implied technical requirements exist in this product description that are not stated explicitly? The description says "25-minute work intervals" — but `setInterval` in JavaScript drifts over time. Does a 25-minute timer that ends at 25:03 meet the product requirement? Who decides?

3. What does "weekly productivity heat map" mean specifically enough to implement? Is this client-side only? Does it survive a browser restart? What data gets stored, and where?

4. What does a developer need to know about browser API dependencies that this description implies but does not name? (Hint: audio notifications at break transitions, visual notifications, potential background tab behavior.)

5. What would a developer ask about during sprint planning that the bare product description leaves unanswered?

Do not move on until you have answered all five. These answers feed directly into your test criteria — and the quality of your answers here determines whether your tests will catch real gaps or only obvious ones.

---

## Step 2: Write the Test File (60 minutes)

Create a file called `create-scope-tests.md` in your repository. Write 5 test cases. Do this entirely by hand — no AI assistance, no looking at AI output first.

**Each test case must include:**

**Input** — the specific product description variant or focus area for this test. You can use the full Pomodoro description or targeted variants (e.g., "Pomodoro timer — focus on notification requirements only", "Pomodoro timer — focus on data persistence"). Do not use the same input twice.

**Expected Output Criteria** — describe what the scope document must contain to pass. This is not the exact text of the response — it is the *criteria* the response must meet. Be specific enough that two different people reading the criterion would grade an output the same way.

**At Least One Explicit Failure Criterion** — something the scope document must NOT contain or do.

---

**The difference between bad and good criteria:**

Bad: "A good scope document." (Untestable.)

Bad: "The scope document has requirements." (Trivially met by any output.)

Good: "The scope document contains a Non-Functional Requirements section that addresses timing accuracy with a specific, measurable definition (e.g., timer drift must not exceed ±1 second per 25-minute interval). A scope document that uses the word 'accurate' without a measurable definition fails this criterion."

Good: "The scope document explicitly declares what is out of scope for V1. The out-of-scope section must name at least three items that a developer might reasonably assume were in scope based on the product description."

The test for whether your criterion is specific enough: could two different developers grade an AI-generated scope document against it and arrive at the same pass/fail verdict? If not, the criterion needs more specificity.

---

**Template for each test case:**

```
## Test Case [N]: [Short name]

**Input:** [The specific product description or variant]

**Expected Output Criteria:**
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]
- (add more as needed)

**Failure Criteria (must NOT occur):**
- [Failure criterion 1]
- [Failure criterion 2]
```

---

**Guidance on which criteria to include:**

At minimum, your 5 test cases should collectively cover:
- **Required sections** — what must be present in every scope document regardless of domain
- **Implied non-functional requirements** — at least one test should check whether the scope document surfaces the drift correction requirement (or another non-stated technical constraint)
- **Scope boundaries** — the scope document must explicitly declare what is out of scope, not just omit features
- **Specificity** — the scope document must not use vague language like "responsive," "fast," or "easy to use" without measurable definitions
- **Open questions** — the scope document should surface what is genuinely unknown and must be decided before implementation begins

---

## Step 3: Run the Bare Prompt Against Your Test Cases (15 minutes)

Take the bare prompt — `"Write a scope document for a Pomodoro timer application with 25-minute work intervals, 5-minute break intervals, session tracking, and a weekly productivity heat map."` — and run it through your AI tool.

Grade the output against each of your 5 test cases. Record pass/fail for each criterion in your test file.

Pay particular attention: did the bare prompt's scope document mention timer drift or `setInterval` accuracy? Did it specify how the heat map data persists across browser sessions? Did it surface browser API dependencies (notifications, audio, local storage)? These are the implied requirements your test criteria should have been designed to catch.

You should see failures. If all 5 test cases pass against the bare prompt, your criteria are too permissive. Strengthen them and re-run before continuing.

---

## Step 4: Commit (required before moving on)

Commit `create-scope-tests.md` to your repository **before you write a single word of the prompt**. The commit timestamp is proof that your tests came first.

If you find yourself wanting to adjust the test criteria after seeing the bare-prompt output, stop. Note the impulse. Then ask: are you adjusting the criteria because they were wrong, or because the model output is changing your idea of what good looks like? The first is legitimate. The second is the failure mode this exercise is designed to surface.

---

## Self-Check

Before moving to Exercise 2, verify:

- [ ] `create-scope-tests.md` is committed to your repository
- [ ] The file contains 5 test cases with distinct inputs or focus areas
- [ ] Each test case has specific, testable criteria (not "a good scope document")
- [ ] Each test case has at least one explicit failure criterion
- [ ] At least 2 of the 5 test cases fail against the bare prompt
- [ ] At least one test case covers an implied non-functional requirement (timer accuracy, persistence, or browser API behavior)
- [ ] The commit of the test file predates any prompt file commit

If fewer than 2 test cases fail against the bare prompt, your criteria are too loose. Strengthen them before proceeding.
