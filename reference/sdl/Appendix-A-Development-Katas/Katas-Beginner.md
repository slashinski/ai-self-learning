# Beginner Katas

*Four katas. Run each kata at least once using the kata feedback loop from Exercise 17. If Run 1 produces a pipeline failure you address via EDD, run a second time to validate the improvement.*

These katas are "beginner" in the sense that the implementation surface is constrained — the game rules are well-known, the scope is clear, and there are no novel algorithms to discover. That makes them ideal for your first pipeline runs, where you are learning how your delivery skills handle a well-specified problem before you throw ambiguous or algorithmically complex problems at them.

What beginner katas will expose in your pipeline:
- How well your scope document handles requirements that are implicit rather than stated (Conway's rules do not need to be explained, but the implementation requirements around rendering performance do)
- How well your Architecture handles state management in an interactive, real-time UI
- Whether your Workstreams and Deliverables produce deliverables at a granularity that makes sense for a single-session build

---

## Kata B1: Conway's Game of Life Sandbox

**Difficulty:** Beginner
**Primary challenge areas:** State (high), Algorithm (medium), Visualization (medium), UI (medium)

### Challenge

Implement Conway's Game of Life with a resizable grid, play/pause/step controls, adjustable simulation speed, and a pattern library containing at least the following patterns: glider, blinker, pulsar, and glider gun. Include a generation counter and live cell count. Allow users to draw cells by clicking or dragging on the grid, and support save/load of patterns.

### Key Technical Challenges

- Efficient neighbor counting at scale (a 100x100 grid with 10,000 cells updated every frame is a performance problem)
- Boundary conditions (does the grid wrap, or do cells die at the edge?)
- Pattern storage format (how do you represent a pattern in a way that can be loaded and saved reliably?)
- Performant rendering (avoid re-rendering every cell on every tick — only the changed cells)

### Stretch Goals

- Alternative rulesets (HighLife, Day and Night, Seeds) with a visual rule editor
- Pattern detection for stable states or cycles, with a notification when the grid reaches a stable state
- Trail mode showing cell age with a color gradient (younger cells brighter, older cells fading)
- RLE pattern import/export for compatibility with external pattern libraries

### Pipeline Focus for This Kata

Pay attention to how your Architecture command handles the state management question. Conway's Game of Life has a specific, well-known performance pattern: maintaining two boards (current and next generation) and swapping them. If your Architecture command produces a generic "store state in React state" recommendation without addressing double-buffering, that is a failure to note and investigate.

---

## Kata B2: Snake with Replay System

**Difficulty:** Beginner
**Primary challenge areas:** State (high), Algorithm (medium), UI (medium)

### Challenge

Implement the classic Snake game with arrow key controls, increasing speed as the snake grows, and score tracking. Record all game states throughout a session and allow users to replay any completed game at variable speeds (0.5x, 1x, 2x, 4x). Include a ghost snake showing the replay of a prior game while the user is actively playing a new game simultaneously.

### Key Technical Challenges

- Input handling (preventing the snake from reversing direction in a single move, handling rapid key presses correctly)
- Collision detection (snake hitting walls, snake hitting its own body)
- State serialization (recording every game state in a format that can be replayed accurately and efficiently)
- Synchronized playback (ghost snake on the same grid as live game without either interfering with the other)

### Stretch Goals

- AI autopilot using pathfinding (A* or BFS) to navigate toward food while avoiding the snake's body
- Time rewind allowing the player to undo the last N moves during a live game
- Leaderboard with shareable replay links (replays encoded in URL parameters)
- Obstacles and power-ups (speed boost, temporary wall pass-through)

### Pipeline Focus for This Kata

The ghost snake feature is where your pipeline will most likely fall short. It is stated clearly in the challenge description but is easy for a scope document to underspecify (just mentioning "ghost snake" without specifying the interaction model — does it share the same grid? Is it rendered differently? Does it affect the live game in any way?). Watch whether your scope document command produces a spec that a developer could implement without asking follow-up questions.

---

## Kata B3: Tic-Tac-Toe with Unbeatable AI

**Difficulty:** Beginner
**Primary challenge areas:** Algorithm (high), State (medium), UI (medium), Visualization (medium)

### Challenge

Create a Tic-Tac-Toe game with three play modes: Player vs. Player, Easy AI (random legal move selection), and Impossible AI (minimax algorithm — must never lose). When playing against the Impossible AI, visualize its evaluation of each possible move: show the minimax score for each open cell so the player can see why the AI made its choice.

### Key Technical Challenges

- Minimax algorithm implementation with correct terminal state detection (win, loss, draw)
- Alpha-beta pruning to make minimax efficient (not strictly necessary for a 3x3 board, but good practice)
- Move evaluation display (showing scores on the board without cluttering the UI)
- Game state detection (win, draw, ongoing)

### Stretch Goals

- Extension to Ultimate Tic-Tac-Toe (nine 3x3 boards forming a meta-game, where each move constrains which board the opponent must play in)
- 4x4 or 5x5 grid variants requiring 4-in-a-row to win
- Teaching mode that shows the optimal response after any suboptimal move, with an explanation
- Adjustable difficulty with deliberate suboptimal move selection at lower levels

### Pipeline Focus for This Kata

The Impossible AI requires a specific algorithm (minimax). Watch whether your Plan Deliverable command names the algorithm and describes its implementation — or whether it produces a generic "implement game AI" plan. This is a signal about how well your Deliverable Plan command handles deliverables with a known-correct algorithmic approach. A plan that does not name minimax is not a useful plan for this kata.

---

## Kata B4: Pomodoro Timer with Analytics

**Difficulty:** Beginner
**Primary challenge areas:** UI (high), State (high), Visualization (medium)

### Challenge

Create a Pomodoro timer with 25-minute work intervals and 5-minute break intervals, with audio notifications at each transition. Track completed sessions per day and visualize weekly productivity as a heat map (similar to a GitHub contributions chart) where each cell represents one day and the color intensity represents the number of sessions completed. Include customizable interval durations and a distraction log where users can note interruptions during a work session.

### Key Technical Challenges

- Accurate timing (JavaScript's `setInterval` drifts over time — a production timer needs drift correction)
- Browser notification API (requires user permission, needs graceful handling when denied)
- Local storage for persistence (the heat map data must survive page refreshes and browser restarts)
- Heat map visualization (generating a calendar-like grid with color-coded cells)

### Stretch Goals

- Task association: track time spent per named task across sessions
- Long break logic: after every 4 completed pomodoros, offer a 15-minute break instead of 5
- Streak tracking with daily and weekly goals, with visual badges for completed streaks
- Data export as CSV or calendar (ICS) file

### Pipeline Focus for This Kata

The drift correction in the timer is the kind of non-functional requirement that a generic scope document will miss. It is not in the challenge description as stated — it is implied by the requirement that the timer be accurate. Watch whether your scope document command surfaces this implied requirement, or whether it produces a spec that would result in a timer that gradually falls behind over long sessions. If it misses this, that is a signal about how well your scope document handles implicit performance and accuracy requirements.
