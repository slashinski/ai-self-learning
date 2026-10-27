# Advanced Katas

*Three katas. Run each kata at least once using the kata feedback loop from Exercise 17. If Run 1 produces a pipeline failure you address via EDD, run a second time to validate the improvement.*

Advanced katas have multiple interacting systems, complex algorithm visualization requirements, and multi-layer state management. They expose how well your pipeline handles problems where the architecture must account for several independent subsystems that need to coordinate.

What advanced katas will expose in your pipeline:
- Whether your Architecture correctly identifies subsystem boundaries and their interactions
- How well your Workstreams and Deliverables handle multiple independent but coordinated features
- Whether your Deliverable Plans address the coordination and sequencing of complex operations, not just the individual algorithms

---

## Kata A1: Pathfinding Grid Explorer

**Difficulty:** Advanced
**Primary challenge areas:** Algorithm (high), UI (high), State (medium), Visualization (high)

### Challenge

Build an interactive grid where users can place start and end points and draw walls by clicking or dragging. Implement both A* and Dijkstra's algorithms. When the user triggers the search, animate the algorithm's execution step-by-step: show the frontier expansion (cells currently being evaluated), visited nodes (cells already evaluated and set aside), and the final path when found. Display the path length (number of steps) and total nodes explored for each algorithm side-by-side, allowing comparison.

### Key Technical Challenges

- Priority queue implementation for A* (a correct min-heap is necessary for performance — a naive sorted array becomes unacceptably slow on larger grids)
- Heuristic functions for A* (the Manhattan distance heuristic for grid-based movement without diagonals, the Euclidean distance for diagonal movement)
- Click-and-drag wall drawing without missing cells (the mouse can move faster than mousemove fires, requiring interpolation between events)
- Animation pacing that allows the user to see individual steps without the animation being either too slow or too fast to follow

### Stretch Goals

- Weighted terrain with different traversal costs: swamp (cost 5), road (cost 1), walls (impassable) — requires updating the grid state model and the algorithm's cost function
- Bidirectional search: run A* from both the start and the end simultaneously, visualizing both frontiers and the meeting point
- Maze generation algorithms to create interesting test grids: recursive backtracking (depth-first), Prim's, and Kruskal's
- Diagonal movement with correct cost calculation (diagonal steps cost √2 ≈ 1.414, not 1)

### Pipeline Focus for This Kata

The A* heuristic function is the difference between A* and Dijkstra's — without an admissible heuristic, A* degrades to Dijkstra's. Watch whether your Architecture and Plan Deliverable commands correctly identify and distinguish the two algorithms at the implementation level, or whether they describe both as "pathfinding algorithms" without addressing what makes them different to implement. A plan that says "implement A* using the heuristic function" without specifying what the heuristic is for a grid is not complete.

---

## Kata A2: Binary Search Tree Visualizer

**Difficulty:** Advanced
**Primary challenge areas:** Algorithm (high), State (high), Visualization (high), UI (medium)

### Challenge

Build an interactive binary search tree where users can insert values, delete values, and search for values. Animate each operation to show the traversal process: for insertion, show the comparisons at each node as the algorithm descends to find the insertion point. For deletion, show the three cases (leaf deletion, one-child deletion, two-child deletion with in-order successor) explicitly. Support in-order, pre-order, and post-order traversal animations that highlight each visited node in sequence. Display the tree height and balance factor for each node, updating after every operation.

### Key Technical Challenges

- Tree layout algorithm (positioning nodes on a 2D canvas such that the tree is readable for arbitrary insertion sequences — including degenerate cases like sorted input producing a linked list)
- Operation animation sequencing (insert, delete, and traversal each require different animation logic that must not interfere with each other)
- Balanced rendering of unbalanced trees (a degenerate BST with 20 nodes may have 20 levels; the layout must remain usable)
- Balance factor calculation for each node (height of left subtree minus height of right subtree, requiring correct height tracking after every mutation)

### Stretch Goals

- AVL tree extension with self-balancing: show the rotation operations (left rotation, right rotation, left-right, right-left) with animation
- Bulk insert with tree evolution visualization: insert a set of values one-by-one, with the ability to step forward and backward through the evolution
- Pathological case demonstration: show sorted input degenerating the BST to a linked list, and explain visually why this happens
- Expression tree support: allow the user to input a mathematical expression, parse it into a tree, and animate its evaluation

### Pipeline Focus for This Kata

The tree layout algorithm is a classic problem in graph visualization, and it is the hardest part of this kata to get right for degenerate cases. Watch whether your Architecture command identifies the layout algorithm as a distinct subsystem with its own design requirements, or whether it treats "display the tree" as a trivial rendering concern. A plan that says "render each node at its appropriate position" without addressing how positions are calculated for an arbitrary tree shape is not actionable. This is a good signal for how your Architecture handles visualization subsystems.

---

## Kata A3: Sudoku Generator and Solver

**Difficulty:** Advanced
**Primary challenge areas:** Algorithm (high), UI (high), State (medium), Visualization (medium)

### Challenge

Create a Sudoku game that generates valid puzzles at three difficulty levels (easy, medium, hard) with unique solutions. Include a hint button that reveals the value of one cell using the solver's logic (not random). Include a solve button that animates the backtracking algorithm's execution: show cells being filled in, show the backtracking when a contradiction is reached, and highlight the final solution. Validate user input in real-time, highlighting conflicting cells immediately.

### Key Technical Challenges

- Puzzle generation with a unique solution (a Sudoku puzzle must have exactly one solution — generating a valid board is different from generating a puzzle, which requires removing cells while verifying uniqueness through the solver)
- Difficulty estimation (easy, medium, and hard correspond to roughly which solving techniques are required — naked singles only, hidden singles, or more advanced techniques — not just the number of given cells)
- Efficient solving visualization (the backtracking algorithm may make thousands of recursive calls; showing every step would be too fast to follow and too slow to run; the animation must throttle intelligently)
- Real-time conflict highlighting (when a user places a value, all conflicts — same row, same column, same box — must be highlighted immediately)

### Stretch Goals

- Pencil marks (candidate values) with automatic constraint elimination: when a value is placed, eliminate it from all candidates in the same row, column, and box
- Advanced technique visualization: show naked pairs, hidden singles, and X-wing patterns being applied, with explanatory text
- "Rate my puzzle" mode: analyze a user-provided puzzle and report which techniques are required to solve it
- Variant sudoku support: killer sudoku (caged cells with sum constraints), thermometer sudoku (cells must increase along a line), diagonal sudoku (both main diagonals must contain 1–9)

### Pipeline Focus for This Kata

Puzzle generation and puzzle solving are different algorithms that both require correct implementation — but generation depends on solving (you need the solver to verify uniqueness after each cell removal during generation). Watch whether your Architecture correctly identifies this dependency and describes the two subsystems in the right order, or whether it treats "generate a Sudoku" as a single operation. A deliverable for "puzzle generation" that does not reference the solver as a dependency is missing the relationship between the two subsystems. This is a good signal for how your Workstreams and Deliverables handles dependency management between deliverables.
