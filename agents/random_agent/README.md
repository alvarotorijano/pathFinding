# Random Agent

**Classification:** Baseline / Uninformed Search  
**Algorithm:** Random Walk  
**Expected Performance:** Poor (baseline only)

## Description

The Random Agent is a baseline agent that simply picks a random valid direction at each step. It will eventually find the goal (if reachable) through pure random exploration, but it's extremely inefficient.

## How It Works

1. Look at all valid neighbors (directions where `neighbors[direction] == True`)
2. Pick one at random
3. Move in that direction
4. Repeat until goal or timeout

## When to Use

Use this as a **baseline** to compare your search algorithms against:
- If your algorithm performs worse than Random, something is wrong
- If your algorithm performs 10x better than Random, you have a working algorithm
- If your algorithm performs 100x better than Random, you have an optimized algorithm

## Example Output

```
Agent: RandomAgent
Solved: YES
Steps: 587
Path Cost: 586.0
Optimal Cost: 18.0
Optimality: 3.1%
Nodes Explored: 234
Time: 8.42ms
Invalid Moves: 0
```

**Notice:** Random finds the goal but takes 587 steps for what should be 18 cost! This is why we need smarter algorithms.

## Usage

```bash
# Generate a maze
python -m labyrinth generate --width 10 --height 10 --type perfect --seed 42 --output maze.maze

# Run the Random Agent
python -m labyrinth run --maze maze.maze --agent random_agent

# With visualization
python -m labyrinth run --maze maze.maze --agent random_agent --visualize --speed 5
```

## Algorithm Complexity

| Metric | Value |
|--------|-------|
| Time Complexity | O(?) - Random, could be infinite |
| Space Complexity | O(1) - Only stores current position |
| Optimal | ✗ - Never optimal |
| Complete | ✓ - Will eventually find goal |

## See Also

- [Your First Agent](../../docs/YOUR_FIRST_AGENT.md) - Tutorial on writing agents
- [API Reference](../../docs/api_reference.md) - Framework API
- [BFS Agent](../bfs_agent/) - Example of a better algorithm
- [DFS Agent](../dfs_agent/) - Another search algorithm
