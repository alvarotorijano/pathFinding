# Student Guide - Implement Your First Agent

This guide walks you through implementing your own search algorithm agent.

## Step 1: Create Your Agent Folder

Create a new folder in `agents/` with your algorithm name:

```bash
mkdir agents/my_agent
```

## Step 2: Implement the Agent Class

Create `agents/my_agent/agent.py`:

```python
from utils.maze_core.agent import Agent
from utils.maze_core.models import Direction, Observation, AgentDebugState, Position
from typing import Optional, Set, List

class MyAgent(Agent):
    """My awesome search algorithm."""
    
    def __init__(self):
        """Initialize persistent state."""
        self.visited = set()
        self.frontier = []
    
    def step(self, observation: Observation) -> Direction:
        """
        Decide next move.
        
        Parameters:
            observation: Contains maze, position, goal, metrics
        
        Returns:
            Direction.NORTH, SOUTH, EAST, or WEST
        """
        # Your algorithm here
        # Example: random valid move
        neighbors = observation.maze.get_neighbors(observation.current)
        if neighbors:
            return neighbors[0]
        return Direction.NORTH
    
    def debug_state(self) -> Optional[AgentDebugState]:
        """Optional: return visualization data."""
        return AgentDebugState(
            frontier=set(self.frontier),
            explored=self.visited,
        )
```

## Step 3: Test Your Agent

```bash
# Generate a maze
python -m labyrinth generate --width 10 --height 10 --seed 42 --output my_maze.maze

# Run your agent
python -m labyrinth run --agent my_agent --maze-file my_maze.maze
```

## Step 4: Try Different Mazes

```bash
# Perfect maze (one solution)
python -m labyrinth run --agent my_agent --width 20 --height 20 --type perfect

# Multiple solutions
python -m labyrinth run --agent my_agent --width 20 --height 20 --type multiple

# With varied costs
python -m labyrinth run --agent my_agent --width 15 --height 15 --cost-map random --cost-range 1:10
```

## Understanding the Observation

Each `step()` receives an `Observation` with:

```python
observation.maze      # The maze (all walls and passages)
observation.current   # Your current position (x, y)
observation.goal      # Goal position (x, y)
observation.step_count # Number of moves made so far
observation.path_cost  # Total cost accumulated
```

## Understanding the Maze

```python
# Check possible neighbors from current position
neighbors = observation.maze.get_neighbors(observation.current)
# Returns: [Direction.NORTH, Direction.EAST, ...]

# Move to neighbor
next_pos = observation.current.move(Direction.NORTH)

# Check distance to goal
distance = observation.current.distance_to(observation.goal)

# Get cell details
cell = observation.maze.get_cell(observation.current)
print(cell.cost)  # Cost to enter this cell
```

## Example Algorithms

### Random Walk

```python
import random

def step(self, observation: Observation) -> Direction:
    neighbors = observation.maze.get_neighbors(observation.current)
    return random.choice(neighbors) if neighbors else Direction.NORTH
```

### Greedy (Always move toward goal)

```python
def step(self, observation: Observation) -> Direction:
    neighbors = observation.maze.get_neighbors(observation.current)
    best = None
    best_dist = float('inf')
    
    for direction in neighbors:
        next_pos = observation.current.move(direction)
        dist = next_pos.distance_to(observation.goal)
        if dist < best_dist:
            best_dist = dist
            best = direction
    
    return best or neighbors[0]
```

### BFS (see `agents/dfs_agent/` for a full, working search-agent example)

```python
from collections import deque

def step(self, observation: Observation) -> Direction:
    # On first call, initialize
    if not hasattr(self, 'initialized'):
        self.frontier = deque([observation.current])
        self.visited = {observation.current}
        self.parent = {}
        self.initialized = True
    
    # Expand frontier
    while self.frontier:
        current = self.frontier.popleft()
        if current == observation.goal:
            # Reconstruct and follow path
            ...
        
        for direction in observation.maze.get_neighbors(current):
            neighbor = current.move(direction)
            if neighbor not in self.visited:
                self.visited.add(neighbor)
                self.parent[neighbor] = current
                self.frontier.append(neighbor)
    
    # Return next move toward goal
    ...
```

## Debugging

Print debug information (goes to stderr):

```python
import sys

def step(self, observation: Observation) -> Direction:
    print(f"Position: {observation.current}", file=sys.stderr)
    print(f"Goal: {observation.goal}", file=sys.stderr)
    print(f"Neighbors: {observation.maze.get_neighbors(observation.current)}",
          file=sys.stderr)
    
    # Your logic...
    return Direction.NORTH
```

## Metrics You'll See

After running:

```
Agent: my_agent
Solved: YES
Steps: 45
Path Cost: 67.3
Optimal Cost: 63.0
Optimality: 94.8%
Nodes Explored: 127
Time: 1.23ms
Invalid Moves: 0
```

- **Solved**: Did you reach the goal?
- **Steps**: How many moves?
- **Path Cost**: Total cost (sum of cell costs traversed)
- **Optimal Cost**: Best possible (calculated by reference solver)
- **Optimality**: Your cost vs optimal (higher is better)
- **Nodes Explored**: Cells you visited
- **Time**: Execution time

## Hints

1. Maintain persistent state between `step()` calls
2. The maze is known - you have full information
3. Always return a valid Direction
4. Be efficient - don't recompute on every step
5. Implement `debug_state()` for visualization help

## Next Steps

1. Implement BFS or DFS from example agents
2. Try Dijkstra's algorithm (like BFS but with costs)
3. Implement A* with Manhattan distance heuristic
4. Optimize for speed/memory
5. Compete in tournaments!

## Files to Reference

- `utils/maze_core/models.py` - Data structures (Direction, Position, Maze, etc.)
- `agents/dfs_agent/agent.py` - Full DFS example
- `agents/random_agent/agent.py` - Full baseline example
