# Reference Solver

## What It Is

The reference solver is a **private, internal component** that calculates optimal solutions for maze problems.

## Access Level

🔒 **PRIVATE** - You do NOT have access to:
- ❌ Solver source code
- ❌ Solver binaries
- ❌ Solver implementation details
- ❌ Direct solver API or method calls

## What It Does

The reference solver runs **internally** to provide evaluation metrics:

```
Student Agent Solution          Reference Solver
       ↓                                ↓
    steps = 45                    steps = 40
    cost = 67.3        =====>     cost = 63.0
    explored = 127               explored = 95
       ↓                                ↓
    ┌──────────────────────────────────┘
    │
    ▼
  Metrics Report
  - Optimality: 94.8% (63.0 / 67.3)
  - Efficiency: 92.2% (40 steps / 45 steps)
```

## What You See

After running an agent, you'll see metrics like:

```
Agent: my_agent
Solved: YES
Steps: 45
Path Cost: 67.3
Optimal Cost: 63.0          ← Calculated by reference solver
Optimality: 94.8%           ← Comparison against optimal
Nodes Explored: 127
Time: 1.23ms
```

## Why It's Private

The reference solver is hidden to:
1. **Prevent cheating** - Students implement their own search algorithms
2. **Ensure fair evaluation** - Everyone is evaluated against the same reference
3. **Maintain architecture isolation** - Solver is completely separate from student code
4. **Security** - Implementation details are not exposed

## How It Works (Conceptually)

The reference solver uses **A* search algorithm** to find optimal paths:

- **Admissible heuristic**: Manhattan distance to goal
- **Complete**: Always finds solution if one exists
- **Optimal**: Always finds the shortest/cheapest path
- **Fast**: Compiled to WebAssembly for efficiency

## Integration

The framework calls the reference solver **after** your agent finishes, completely independently:

```python
# Your agent runs
result = simulator.run()

# Framework internally calls reference solver
optimal_solved, optimal_path, optimal_cost, nodes = ReferenceSolver.solve(maze)

# Comparison is made
result.optimal_cost = optimal_cost
result.optimality_ratio = optimal_cost / result.path_cost
```

You never interact with it directly.

## What This Means for You

✅ **You CAN:**
- View the metrics it produces
- Compare your solution to optimal
- See how close you are to perfect performance
- Use the metrics to improve your algorithm

❌ **You CANNOT:**
- Access solver code
- Call the solver directly
- Copy its implementation
- Use it to cheat

## The Point

The reference solver ensures that:
1. **Evaluation is fair** - Everyone's compared to the same reference
2. **Metrics are reliable** - Optimality ratios are calculated correctly
3. **Framework is secure** - Students focus on their own algorithms

---

**Bottom line:** The reference solver is infrastructure, not a teaching tool. Your job is to implement search algorithms and get as close to optimal as possible.
