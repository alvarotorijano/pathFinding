# Reference Solver Integration

## Overview

The framework uses a reference solver to evaluate agent performance objectively. This document explains the integration from a user perspective (not implementation).

## How It Works

### Step 1: Student Agent Solves Maze

```bash
python -m labyrinth run --agent my_agent --maze-file maze.maze
```

Your agent runs step-by-step through the maze:
- Makes decisions based on observations
- Records each move, cost, and state
- Either reaches goal or times out

### Step 2: Reference Solver Evaluates (Automatically)

After your agent finishes, the framework **independently** runs the reference solver:

```python
# Framework internal logic (you don't see this)
student_result = simulator.run(my_agent, maze)   # Your agent

# Solver is called to find optimal solution
optimal_result = ReferenceSolver.solve(maze)      # Private solver

# Comparison is made
student_result.optimal_cost = optimal_result.cost
student_result.optimality_ratio = optimal_result.cost / student_result.path_cost
```

### Step 3: Metrics Are Displayed

You see the comparison:

```
Agent: my_agent
Solved: YES
Steps: 45
Path Cost: 67.3
Optimal Cost: 63.0          ← From reference solver
Optimality: 94.8%           ← 63.0 / 67.3
Nodes Explored: 127
Time: 1.23ms
```

## What You Can See

✅ The **results** of what the reference solver calculated:
- Optimal cost
- Optimal path length
- Your performance vs. optimal

## What You Cannot See

❌ The **implementation**:
- How it calculates optimal paths
- The search algorithm used
- Its internal data structures
- Its source code

## The Purpose

The reference solver serves as **neutral arbiter**:

1. **Fair evaluation** - All agents compared to same reference
2. **Objective metrics** - Your optimality is measured against truth
3. **Learning feedback** - See how close you are to perfect
4. **Prevention of cheating** - Can't copy the solver

## How to Use This Information

Your goal: **Get as close to optimal as possible**

- Study the optimality percentage
- Compare against other agents
- Improve your algorithm
- Measure progress

Example progression:

```
Attempt 1: Optimality 75%  (basic DFS)
Attempt 2: Optimality 88%  (improved DFS with heuristic)
Attempt 3: Optimality 95%  (BFS with cost awareness)
Attempt 4: Optimality 99%  (A* implementation)
```

## Integration Points

The reference solver is called in these scenarios:

1. **`maze run` command** - After each agent execution
2. **`maze benchmark` command** - For each agent-maze pair
3. **Tournament mode** - For final rankings

## Private Repository

The actual solver code lives in a separate private repository:
- **URL:** [labyrinth-solver-wasm](../labyrinth-solver-wasm) (PRIVATE)
- **Language:** Rust compiled to WebAssembly
- **Access:** Instructors only

This separation ensures:
- Students focus on **their own algorithm implementation**
- Evaluation is **objective and fair**
- Source code is **protected**

## Summary

```
┌──────────────────┐
│  You implement   │
│  YOUR algorithm  │
│    (BFS, DFS,   │
│     A*, etc.)   │
└────────┬─────────┘
         │
         ▼
    ┌─────────┐
    │ Results │ (steps, cost, time)
    └────┬────┘
         │
         ▼
    ┌─────────────────────┐
    │ Reference Solver    │
    │ (Private, Hidden)   │
    │    (A*)             │
    └────┬────────────────┘
         │
         ▼
    ┌─────────────────────┐
    │ Comparison Metrics  │
    │ - Optimality %      │
    │ - vs. Optimal Cost  │
    │ - vs. Optimal Steps │
    └─────────────────────┘
```

---

**Bottom line:** The reference solver is **infrastructure you can't access**, but you can **see its results** to measure your performance.
