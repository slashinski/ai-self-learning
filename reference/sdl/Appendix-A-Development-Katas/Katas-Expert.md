# Expert Katas

*Two katas. Run each kata at least once using the kata feedback loop from Exercise 17. If Run 1 produces a pipeline failure you address via EDD, run a second time to validate the improvement.*

Expert katas have a probabilistic or financial engine at their core — domains where correctness is mathematically verifiable and where the gap between a working prototype and a correct deliverable is significant. They expose how well your pipeline handles problems where the most important requirements are mathematical accuracy and computational performance, not just feature completeness.

What expert katas will expose in your pipeline:
- Whether your Architecture correctly separates the computational engine from the UI, and describes both with appropriate specificity
- Whether your scope document captures accuracy and performance as first-class requirements rather than implied concerns
- Whether your Deliverable Plans provide enough mathematical detail to produce a correct implementation without further research

---

## Kata E1: Texas Hold'em Probability Simulator

**Difficulty:** Expert
**Primary challenge areas:** Math (high), State (medium), Algorithm (medium), UI (medium)

### Challenge

Simulate a full 9-handed Texas Hold'em table without betting or folding. Deal a hand to each of the nine players and display each hand in the UI. Show live win probability percentages for each player that update as community cards are revealed through the flop (three cards), turn (one card), and river (one card). Probabilities must be calculated using Monte Carlo simulation — repeatedly simulating the remainder of the hand with random card draws and counting outcomes.

### Key Technical Challenges

- Card deck management (a standard deck, correctly dealing without replacement, tracking which cards are in community, in player hands, and remaining in the deck)
- Monte Carlo simulation (running thousands of simulated completions of the hand for each revealed board state — accuracy improves with more simulations but takes longer; the implementation must balance both)
- Probability calculation from simulation results (win probability for each player is wins divided by total simulations — but ties must be handled correctly as fractional wins)
- Responsive UI updates (re-running the simulation after each card reveal must not block the UI)

### Stretch Goals

- Hand strength classification labels that update in real time: high card, one pair, two pair, three of a kind, straight, flush, full house, four of a kind, straight flush, royal flush — for each player's current holding against the current board
- Equity for all-in scenarios showing exact odds (enumerate all remaining card combinations) vs. Monte Carlo estimates (compare accuracy vs. speed tradeoff)
- "What if" mode: allow the user to set specific cards for any player or for the community, and recalculate
- Outs count and percentage for drawing hands: show how many cards in the remaining deck would complete a player's draw, and the probability of hitting

### Pipeline Focus for This Kata

The Monte Carlo simulation is the core technical requirement of this kata, and it has specific implementation parameters: how many simulations are enough for acceptable accuracy? (10,000 is a reasonable default for real-time display.) How should the simulation be structured to avoid blocking the UI? (Web Workers or a chunked async approach.) How should ties be handled in the win probability calculation? Watch whether your Architecture and Plan Deliverable commands provide this level of specificity, or whether they describe the simulation at a level of abstraction that leaves all these decisions to the implementer. A plan that says "use Monte Carlo simulation to calculate probabilities" without addressing simulation count, threading model, and tie handling is underspecified for this domain.

---

## Kata E2: Loan Amortization Dashboard

**Difficulty:** Expert
**Primary challenge areas:** Math (high), Visualization (high), State (medium), UI (medium)

### Challenge

Build a mortgage and loan calculator that generates a complete amortization schedule from three inputs: principal amount, annual interest rate, and loan term in years. Display the full amortization schedule as a table showing each payment's: payment number, payment date, total payment amount, principal portion, interest portion, and remaining balance. Visualize the payment breakdown over the full loan term as an area chart, with the principal and interest portions as stacked areas. Allow users to add extra payments (one-time or recurring) and show how they reduce the total interest paid and the loan term.

### Key Technical Challenges

- Amortization formula (monthly payment = P × [r(1+r)^n] / [(1+r)^n - 1], where P is principal, r is monthly rate, n is number of payments — and the balance must decrease to exactly zero at the final payment due to rounding)
- Rounding handling (monthly payment amounts must be rounded to cents, which means the final payment may differ slightly from the standard payment — this must be handled explicitly)
- Extra payment scenarios (one-time extra payments reduce the principal immediately and change all subsequent interest calculations; recurring extra payments compound across the life of the loan)
- Chart rendering for large datasets (a 30-year mortgage has 360 data points; the area chart must remain readable and interactive at that scale)

### Stretch Goals

- Multi-scenario comparison: allow the user to compare two scenarios side-by-side — for example, a 15-year vs. 30-year mortgage at different rates — with the difference in total interest paid and monthly payment displayed clearly
- Refinancing analysis: given current loan state (remaining balance, remaining term, current rate), show the break-even point for refinancing at a new rate (the point where accumulated savings exceed refinancing costs)
- Bi-weekly payment option: instead of 12 monthly payments per year, 26 bi-weekly payments — show the accelerated payoff timeline and total interest savings
- Mortgage interest deduction: calculate the after-tax cost of the loan based on a configurable marginal tax rate and the deductibility of mortgage interest

### Pipeline Focus for This Kata

The rounding problem in amortization is easy to miss and produces a visibly wrong result: after 360 payments, the balance does not reach exactly zero. A loan amortization calculator that accumulates rounding errors over 360 payments will show a small negative or positive balance at the end instead of exactly zero. Watch whether your scope document and Architecture capture this as an explicit requirement and describe the correction approach (typically, the final payment is adjusted to bring the balance to exactly zero). This is a strong signal for how your pipeline handles domain-specific precision requirements that are not stated explicitly in the feature description but are implied by the domain.

Also watch the extra payment scenario: a one-time extra payment reduces the principal at a specific point in time, which changes all subsequent interest calculations. This is not a simple subtraction — it requires recalculating the entire amortization schedule from that point forward. A plan that says "reduce the principal by the extra payment amount" without addressing the recalculation is underspecified in a way that will produce incorrect totals.
