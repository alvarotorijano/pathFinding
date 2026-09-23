# DFS Agent - Example Implementation

Depth-First Search implementation for maze solving.

## Algorithm

DFS explores as far as possible along each branch before backtracking. It uses a stack (LIFO) to manage the frontier.

**Properties:**
- **Complete:** Finds solution if one exists (with memoization)
- **Optimal:** NOT optimal - may find longer paths
- **Memory:** O(bd) where b is branching factor, d is depth
- **Time:** O(b^d)

## Implementation

```python
from agents.dfs_agent.agent import DFSAgent

# Use in simulator
agent = DFSAgent()
result = simulator.run()
```

## Key Methods

- `step(observation)` - Returns next direction using DFS
- `debug_state()` - Returns frontier, explored cells for visualization

## Usage Example

```bash
python -m labyrinth run --maze-file maze.maze --agent dfs_agent
```

## When to Use

- For educational understanding of depth-first search
- When memory is limited (better than BFS)
- To demonstrate non-optimal search
- Comparison with BFS on same mazes
