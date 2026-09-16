# BFS Agent - Example Implementation

Breadth-First Search implementation for maze solving.

## Algorithm

BFS expands nodes level-by-level (layer by layer). It explores all neighbors at distance `d` before exploring neighbors at distance `d+1`.

**Properties:**
- **Complete:** Always finds a solution if one exists
- **Optimal (uniform costs):** Finds shortest path when all edge costs are equal
- **Memory:** O(b^d) where b is branching factor, d is depth
- **Time:** O(b^d)

## Implementation

```python
from agents.bfs_agent.agent import BFSAgent

# Use in simulator
agent = BFSAgent()
result = simulator.run()
```

## Key Methods

- `step(observation)` - Returns next direction using BFS
- `debug_state()` - Returns frontier, explored cells for visualization

## Usage Example

```bash
python -m labyrinth run --maze maze.maze --agent bfs_agent
```

## When to Use

- When you want guaranteed shortest path with uniform costs
- For educational understanding of breadth-first search
- Baseline comparison with other algorithms
