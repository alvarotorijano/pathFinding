# Your First Agent - Step by Step

In this guide, you'll implement **three search agents** from scratch:
1. **Random** - Baseline agent (moves randomly)
2. **Depth-First Search (DFS)** - Uninformed search
3. **Breadth-First Search (BFS)** - Uninformed search (already done as example)

---

## Part 1: Understanding the Agent Interface

Every agent must inherit from `Agent` and implement one method:

```python
from utils.maze_core.agent import Agent
from utils.maze_core.models import Direction, Observation

class MyAgent(Agent):
    """My custom search agent."""
    
    def step(self, observation: Observation) -> Direction:
        """
        Decide the next move.
        
        Parameters:
            observation: Current maze state, position, neighbors
        
        Returns:
            Direction: The direction to move (NORTH, SOUTH, EAST, WEST)
        """
        # Your logic here
        return Direction.NORTH
```

---

## What is `Observation`?

The `step()` method receives an `Observation` object with:

```python
class Observation:
    position: Position              # Current (x, y)
    goal: Position                  # Target (x, y)
    neighbors: Dict[Direction, bool] # Which directions are passable
    maze: Maze                       # Full maze (for your algorithm)
```

### Example:
```python
# Current position
print(observation.current)  # Position(x=5, y=3)

# Where to go
print(observation.goal)     # Position(x=19, y=19)

# Can I move? (returns list of valid directions)
valid_directions = observation.maze.get_neighbors(observation.current)
print(valid_directions)  # [Direction.NORTH, Direction.EAST, ...]

# Full maze
print(observation.maze)  # Maze(50x50, seed=123)
print(observation.maze.cells)  # 2D grid of all cells
```

---

## Part 2: Random Agent (Baseline)

Let's start with the simplest agent - moves randomly:

### Create the file

Create: `agents/random_agent/agent.py`

```python
import random
from utils.maze_core.agent import Agent
from utils.maze_core.models import Direction, Observation


class RandomAgent(Agent):
    """Baseline agent: moves randomly."""
    
    def step(self, observation: Observation) -> Direction:
        """
        Choose a random valid direction.
        
        Parameters:
            observation: Current state with neighbors dict
        
        Returns:
            Direction: A random valid direction
        """
        # Get all valid moves (directions where neighbors[direction] == True)
        valid_moves = [
            direction 
            for direction, is_passable in observation.neighbors.items()
            if is_passable
        ]
        
        # If stuck, return any direction (will be rejected by simulator)
        if not valid_moves:
            return Direction.NORTH
        
        # Return random valid move
        return random.choice(valid_moves)
```

### Create the README

Create: `agents/random_agent/README.md`

```markdown
# Random Agent

**Type:** Baseline / Uninformed  
**Algorithm:** Random walk  
**Expected Performance:** Poor (baseline comparison)

## How It Works

1. Look at all valid neighbors
2. Pick one at random
3. Repeat until goal or timeout

## When to Use

Use this as a **baseline** to compare your algorithms against. If your agent is worse than Random, something is wrong!

## Command

```bash
python -m labyrinth run --maze maze.maze --agent random_agent
```
```

---

## Part 3: Depth-First Search (DFS)

Now let's implement a real search algorithm. DFS uses a **stack** (LIFO):

### Create the file

Create: `agents/my_dfs_agent/agent.py`

```python
from utils.maze_core.agent import Agent
from utils.maze_core.models import Direction, Observation, Position


class MyDFSAgent(Agent):
    """Depth-First Search agent."""
    
    def __init__(self):
        """Initialize the agent with empty state."""
        super().__init__()
        self.stack = []           # DFS frontier (LIFO - Last In, First Out)
        self.visited = set()      # Cells we've already explored
        self.came_from = {}       # For reconstructing path
        self.parent_direction = {} # Direction we took to reach each cell
    
    def step(self, observation: Observation) -> Direction:
        """
        Execute one DFS step.
        
        Parameters:
            observation: Current maze state
        
        Returns:
            Direction: Next move toward goal or unvisited cell
        """
        current = observation.position
        goal = observation.goal
        
        # Initialize on first step
        if not self.stack:
            self.stack.append(current)
            self.visited.add(current)
        
        # If at goal, we're done!
        if current == goal:
            return Direction.NORTH  # Dummy move (already at goal)
        
        # Get valid neighbors
        valid_directions = observation.maze.get_neighbors(current)
        unvisited_neighbors = []
        
        for direction in valid_directions:
            next_pos = current.move(direction)
            if next_pos not in self.visited:
                unvisited_neighbors.append((direction, next_pos))
        
        # If we have unvisited neighbors, explore one (DFS: pick first)
        if unvisited_neighbors:
            direction, next_pos = unvisited_neighbors[0]
            self.visited.add(next_pos)
            self.stack.append(next_pos)
            return direction
        
        # Backtrack if stuck (all neighbors visited)
        # In a real DFS, we'd backtrack. Here we just pick any valid move.
        valid_moves = observation.maze.get_neighbors(current)
        if valid_moves:
            return valid_moves[0]
        
        return Direction.NORTH
```

### How This Works

1. **Initialize:** First step adds start position to stack, mark as visited
2. **Explore:** Find unvisited neighbors, pick one, add to stack
3. **Backtrack:** If no unvisited neighbors, backtrack (in simple version, just pick any valid)
4. **Repeat:** Until goal reached

### Test It

```bash
python -m labyrinth run --maze maze.maze --agent my_dfs_agent
```

---

## Part 4: Understanding State Persistence

**Key insight:** Your agent's state persists between steps!

```python
class MyAgent(Agent):
    def __init__(self):
        # This is called ONCE at the start
        self.step_count = 0
        self.path_taken = []  # Remember all moves
        self.visited = set()  # Track explored cells
    
    def step(self, observation: Observation) -> Direction:
        # This is called EVERY step
        self.step_count += 1
        self.path_taken.append(observation.position)
        
        # Your state is available across all calls!
        print(f"Step {self.step_count}: at {observation.position}")
        
        return Direction.NORTH
```

This is why your agent can maintain data structures like `stack`, `queue`, `visited` across multiple calls.

---

## Part 5: Testing Your Agent

### Run Against One Maze

```bash
python -m labyrinth generate --width 15 --height 15 --type perfect --seed 42 --output test.maze

python -m labyrinth run --maze test.maze --agent my_dfs_agent
```

Output:
```
==================================================
Agent: MyDFSAgent
Solved: YES
Steps: 142
Path Cost: 141.0
Optimal Cost: 18.0
Optimality: 12.8%
Nodes Explored: 89
Time: 5.23ms
Invalid Moves: 0
==================================================
```

### Run All Tests

```bash
pytest tests/ -v
```

---

## Part 6: Comparison - What Should You Implement?

Here are some popular search algorithms you could implement:

### Uninformed Search (no heuristic)
- **BFS** - Explore level by level (shortest path)
- **DFS** - Explore deeply (memory efficient)
- **Dijkstra** - Uniform cost search (weighted graphs)
- **IDDFS** - Iterative deepening (memory + optimality)

### Informed Search (with heuristic)
- **Greedy** - Follow heuristic only (fast, not optimal)
- **A\*** - Combine cost + heuristic (optimal & efficient)

### Algorithm Comparison

| Algorithm | Optimal | Complete | Time | Space | Notes |
|-----------|---------|----------|------|-------|-------|
| **Random** | ✗ | ✗ | ? | O(1) | Baseline only |
| **DFS** | ✗ | ✓ | O(b^d) | O(d) | Memory efficient |
| **BFS** | ✓ | ✓ | O(b^d) | O(b^d) | Guarantees shortest |
| **Dijkstra** | ✓ | ✓ | O(b^d) | O(b^d) | For weighted graphs |
| **Greedy** | ✗ | ✗ | O(b^d) | O(b^d) | Fast but not optimal |
| **A\*** | ✓ | ✓ | O(b^d) | O(b^d) | Best of both worlds |

*b = branching factor, d = depth*

---

## Part 7: Tips for Success

### ✅ DO:
- Test with small mazes first (5x5)
- Print debug info: `print(f"At {observation.position}, goal {observation.goal}")`
- Use `observation.maze` to understand the maze structure
- Compare your results to BFS/DFS examples

### ❌ DON'T:
- Modify framework code in `utils/maze_core/` (it won't work!)
- Hardcode positions or maze sizes
- Use global variables (each test gets new maze)
- Ignore the `neighbors` dict (it tells you valid moves)

### 🐛 Debugging

If your agent doesn't solve mazes:

```python
def step(self, observation: Observation) -> Direction:
    print(f"At {observation.position}")
    print(f"Goal {observation.goal}")
    print(f"Neighbors: {observation.neighbors}")
    print(f"Visited so far: {len(self.visited)}")
    
    # Then your logic...
```

Then run:
```bash
python -m labyrinth run --maze small.maze --agent my_agent 2>&1 | head -50
```

---

## Part 8: Next Steps

1. **Implement DFS** - Copy the code above, test it
2. **Implement BFS** - Similar to DFS but use `deque` (queue) instead of list (stack)
3. **Implement Dijkstra** - Like BFS but track `cost_to_reach[position]` instead of just visited
4. **Implement A\*** - Add heuristic: `f = g + h` where `h = manhattan_distance(pos, goal)`

---

## Example: BFS (for reference)

Here's how BFS differs from DFS (already in `agents/bfs_agent/`):

```python
from collections import deque  # Queue (FIFO) instead of list (LIFO)

class BFSAgent(Agent):
    def __init__(self):
        self.queue = deque()      # Changed: FIFO instead of LIFO
        self.visited = set()
        self.came_from = {}
    
    def step(self, observation: Observation) -> Direction:
        current = observation.position
        goal = observation.goal
        
        if not self.queue:
            self.queue.append(current)
            self.visited.add(current)
        
        if current == goal:
            return Direction.NORTH
        
        valid_directions = observation.maze.get_neighbors(current)
        unvisited_neighbors = []
        
        for direction in valid_directions:
            next_pos = current.move(direction)
            if next_pos not in self.visited:
                unvisited_neighbors.append((direction, next_pos))
        
        if unvisited_neighbors:
            direction, next_pos = unvisited_neighbors[0]
            self.visited.add(next_pos)
            self.queue.append(next_pos)  # append (front of queue for BFS)
            return direction
        
        valid_moves = observation.maze.get_neighbors(current)
        return valid_moves[0] if valid_moves else Direction.NORTH
```

**Key difference:** `deque` (queue) explores level-by-level, while `list` (stack) explores deeply.

---

## Get Started!

1. Create `agents/random_agent/` and copy the Random Agent code
2. Create `agents/my_dfs_agent/` and copy the DFS code
3. Run them:
   ```bash
   python -m labyrinth run --maze test.maze --agent random_agent
   python -m labyrinth run --maze test.maze --agent my_dfs_agent
   ```
4. Compare results - DFS should be much better than Random!

**Happy coding!** 🚀
