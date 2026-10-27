# Intermediate Katas

*Five katas. Run each kata at least once using the kata feedback loop from Exercise 17. If Run 1 produces a pipeline failure you address via EDD, run a second time to validate the improvement.*

Intermediate katas introduce genuine algorithmic complexity, mathematical correctness requirements, and multi-mode UIs. They expose how well your pipeline handles problems where the right answer is knowable — and where a wrong deliverable is detectably wrong, not just aesthetically weaker.

What intermediate katas will expose in your pipeline:
- How well your Architecture command handles problems with a known-correct algorithmic approach
- Whether your scope document captures mathematical correctness as a requirement (not just "the output should be correct" but specifically what correct means)
- How well your Workstreams and Deliverables handle multi-mode UIs where each mode has different acceptance criteria

---

## Kata I1: Sorting Algorithm Visualizer

**Difficulty:** Intermediate
**Primary challenge areas:** Algorithm (high), Visualization (high), State (medium), UI (medium)

### Challenge

Create a visual comparison tool that animates at least four sorting algorithms simultaneously, side-by-side: bubble sort, insertion sort, merge sort, and quicksort. Each algorithm runs on the same randomly generated array of 50 elements. Include controls for animation speed and array size. Display a step counter for each algorithm showing comparisons made and swaps performed, updating in real time as the animation plays.

### Key Technical Challenges

- Correct implementation of all four algorithms with accessible intermediate state (each algorithm must be able to pause and resume at any comparison or swap, which requires a different structure than a simple recursive implementation)
- Synchronized animation timing across all four algorithms (they finish at different times — the visualization should handle this gracefully)
- State management across multiple simultaneous visualizations
- Step counter accuracy (comparisons and swaps must be counted at the right granularity)

### Stretch Goals

- Sound effects where pitch corresponds to the value of the element being compared or swapped
- Big-O notation display with real-time tracking of actual comparisons against the theoretical bound (O(n²) for bubble and insertion, O(n log n) for merge and quicksort)
- Additional algorithms: heap sort, radix sort, shell sort, timsort
- Race mode with a finish-line animation highlighting the first algorithm to complete

### Pipeline Focus for This Kata

The generator pattern (or equivalent step-by-step execution model) is the key architectural decision here — standard recursive sorting algorithms cannot be easily paused mid-execution to update the UI. Watch whether your Architecture command identifies this requirement and proposes an approach. A generic "implement sorting algorithms and display them" architecture that does not address how to pause and resume execution mid-sort is missing the most important technical decision for this kata.

---

## Kata I2: Blackjack with Strategy Coach

**Difficulty:** Intermediate
**Primary challenge areas:** Math (high), Algorithm (medium), State (medium), UI (medium)

### Challenge

Create a blackjack game against a dealer following standard casino rules: dealer hits on soft 16, stands on soft 17, blackjack pays 3:2, insurance available when dealer shows an ace. For every player decision point, display the mathematically optimal play (hit, stand, double down, or split) based on basic strategy charts. After each hand, track and display the player's decision accuracy — the percentage of decisions that matched the optimal strategy — across the session.

### Key Technical Challenges

- Basic strategy lookup table (a complete basic strategy chart covers all hard hands, soft hands, and pair splits against all dealer up-cards — this is a 2D lookup, not a simple rule set)
- Multi-hand split logic (when a player splits, they may be playing up to four simultaneous hands)
- Soft hand vs. hard hand distinction (an Ace can count as 1 or 11, and this affects which strategy row to look up)
- Running statistics across multiple hands in a session

### Stretch Goals

- Card counting simulation using the Hi-Lo system: display the running count and true count (running count divided by decks remaining) as the game progresses
- Configurable house rules: number of decks, whether dealer hits or stands on soft 17, whether surrender is allowed
- Expected value display showing the EV of each possible decision (hit, stand, double, split) in units of the original bet
- Training mode that replays hands where the player deviated from optimal strategy

### Pipeline Focus for This Kata

The basic strategy lookup table is the most important structural element of this kata. It is not an algorithm you derive — it is a table you implement correctly. Watch whether your Architecture and Plan Deliverable commands recognize this distinction: the work here is correctly encoding a known reference table, not discovering an algorithmic approach. A plan that says "implement a strategy function that calculates the optimal play" misses the point. The calculation is the table lookup.

---

## Kata I3: Wordle Clone with Analysis

**Difficulty:** Intermediate
**Primary challenge areas:** UI (high), State (medium), Algorithm (medium), Math (medium)

### Challenge

Build a Wordle clone with a dictionary of 5-letter words. After each guess, the game shows which letters are correct and in the right position (green), correct but in the wrong position (yellow), and not in the word (gray) — following standard Wordle coloring rules. Additionally, after each guess, display the number of words from the dictionary that are still possible based on all revealed constraints. Include a solver mode that suggests the optimal next guess from the remaining possible words based on letter frequency analysis.

### Key Technical Challenges

- Word filtering logic (after each guess, correctly eliminating words that violate any constraint — including the non-obvious case where a letter appears multiple times)
- Keyboard state tracking (the on-screen keyboard should reflect the best-known status of each letter)
- Optimal guess heuristics (letter frequency analysis across remaining candidates is a reasonable heuristic; implementing it correctly without excessive computation is the challenge)
- Dictionary management (the dictionary must be large enough to be a real game but curated enough that the target words are reasonable)

### Stretch Goals

- Information theory scoring: measure each guess's value in bits gained (how much it narrows the possibility space, quantified)
- Hard mode enforcement: in hard mode, the player must use any revealed green letters in the correct position and any revealed yellow letters somewhere in subsequent guesses
- Adversarial mode: instead of picking a fixed target word at the start, the system changes the target word after each guess to maximize the number of guesses required (while remaining consistent with all revealed constraints)
- Variable word lengths: support 4-letter through 7-letter word modes

### Pipeline Focus for This Kata

The multi-letter constraint is the tricky part of the filtering logic — if a word has two E's and the player guesses a word with one E that comes back yellow, what does that tell you about the target word? This constraint is non-obvious and easy to get wrong. Watch whether your Workstreams and Deliverables include a deliverable specifically for multi-letter constraint handling, with acceptance criteria specific enough to test this case. If the deliverables treat word filtering as a single, uniform deliverable, the acceptance criteria will not be specific enough to catch the multi-letter edge case.

---

## Kata I4: Color Palette Generator

**Difficulty:** Intermediate
**Primary challenge areas:** UI (high), Algorithm (medium), Math (medium), Visualization (medium)

### Challenge

Generate harmonious color palettes using different color theory rules: complementary (colors opposite on the color wheel), triadic (three colors equidistant on the color wheel), analogous (adjacent colors on the wheel), and split-complementary (a base color plus the two colors adjacent to its complement). Given a user-selected base color, display the generated palette with hex and RGB values for each color, WCAG contrast ratios for text-on-background accessibility, and a live preview component that shows the palette applied to a sample UI.

### Key Technical Challenges

- HSL color space manipulation (color theory harmonies are defined in terms of hue angles, which requires working in HSL, then converting to hex/RGB for display)
- WCAG contrast ratio calculation (relative luminance formula applied to each color pair)
- Color harmony algorithms (each harmony type requires a specific geometric relationship on the color wheel)
- Live preview component (applying an arbitrary palette to a UI mockup without hardcoded colors)

### Stretch Goals

- Dominant color extraction from an uploaded image to seed the palette (requires color quantization)
- Color blindness simulation: show how the palette appears to someone with protanopia, deuteranopia, or tritanopia
- CSS custom properties export (generate a `--primary`, `--secondary`, etc. variable block) or Tailwind config export
- Palette locking: allow the user to lock individual palette colors while regenerating the rest

### Pipeline Focus for This Kata

The WCAG contrast ratio calculation is a specific mathematical formula that must be implemented correctly to be useful. Watch whether your Plan Deliverable command provides the formula (relative luminance = 0.2126R + 0.7152G + 0.0722B, where R, G, B are linearized) or whether it says "calculate contrast ratio using the WCAG formula" and leaves the implementation underspecified. The latter is not a useful plan. This kata is a good signal for how technically specific your deliverable plans are for mathematically defined requirements.

---

## Kata I5: Password Generator with Entropy Meter

**Difficulty:** Intermediate
**Primary challenge areas:** Math (high), Algorithm (medium), UI (medium), Visualization (medium)

### Challenge

Build a password generator with controls for: total length, inclusion of uppercase letters, lowercase letters, digits, and symbols. After generating a password, calculate and visualize its entropy in bits (based on the character set size and password length) and display an estimated crack time against three attack scenarios: online attack (1,000 guesses/second), offline slow hash (100,000 guesses/second), and offline fast hash (10 billion guesses/second). Include a pronounceable mode that generates passwords using alternating consonant-vowel patterns while maintaining reasonable entropy.

### Key Technical Challenges

- Cryptographic randomness (use `crypto.getRandomValues()` or equivalent — not `Math.random()`, which is not cryptographically secure)
- Entropy calculation (entropy in bits = log₂(character_set_size ^ password_length) = password_length × log₂(character_set_size))
- Crack time estimation (convert entropy to expected guesses to 50% probability, then divide by attack rate)
- Pronounceable generation algorithm (a consonant-vowel alternating pattern that produces something human-readable while still being random)

### Stretch Goals

- Passphrase generation using a diceware-style word list (random words from a curated list, with entropy calculated from list size and word count)
- Memorable password generation using a word + number + symbol pattern with calculated entropy
- Integration with the Have I Been Pwned API to check whether a generated password has appeared in known data breaches (k-anonymity model: send only the first 5 characters of the SHA-1 hash)

### Pipeline Focus for This Kata

The `Math.random()` vs. `crypto.getRandomValues()` distinction is a security requirement, not a functional one. Functionally, both generate passwords. But one is cryptographically secure and one is not. Watch whether your scope document or Constraints section surfaces this as an explicit requirement, or whether it is left implicit. This is a good signal for how your scope document handles security requirements that are not stated in the feature description but are implied by the domain.
