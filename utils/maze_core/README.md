# Maze Core - Core Data Models

This module provides all fundamental data structures for the maze search framework.

## Data Models

### Direction

Cardinal directions with coordinate deltas:

```python
from utils.maze_core import Direction

# All four directions
north = Direction.NORTH  # (0, -1)
south = Direction.SOUTH  # (0, 1)
east = Direction.EAST    # (1, 0)
west = Direction.WEST    # (-1, 0)

# Get opposite direction
opposite = Direction.NORTH.opposite()  # Direction.SOUTH

# Get coordinate delta
dx, dy = Direction.EAST.delta  # (1, 0)
```

### Position

A coordinate (x, y) in the maze:

```python
from utils.maze_core import Position

pos = Position(5, 10)

# Move in a direction
new_pos = pos.move(Direction.NORTH)  # Position(5, 9)

# Calculate distance
dist = pos.distance_to(Position(10, 10))  # Manhattan distance

# Use in sets/dicts (hashable)
visited = set()
visited.add(pos)

# Convert to tuple
x, y = pos.to_tuple()
```

### Cell

A single maze cell with walls and cost:

```python
from utils.maze_core import Cell, Direction

# 4-bit walls: NESW (North, East, South, West)
# 1 = passage open, 0 = wall
cell = Cell(walls=0b1010, cost=1.0)  # N and S open, E and W blocked

# Check walls
is_blocked = cell.has_wall(Direction.NORTH)  # False
can_go = cell.can_move(Direction.EAST)      # False
```

### Maze

Complete maze with topology and metadata:

```python
from utils.maze_core import Maze, Position, Direction

maze = Maze(
    width=20,
    height=20,
    cells=[[Cell(...), ...], ...],  # 2D grid
    start=Position(0, 0),
    goal=Position(19, 19),
    seed=12345,
    solution_count=1
)

# Query maze
cell = maze.get_cell(Position(5, 5))
is_valid = maze.is_valid(Position(0, 0))

# Movement validation
can_move = maze.can_move_to(Position(5, 5), Direction.NORTH)

# Get all valid neighbors
neighbors = maze.get_neighbors(Position(5, 5))  # [Direction.NORTH, Direction.EAST, ...]
```

### Observation

What the agent receives each step:

```python
from utils.maze_core import Observation, Maze, Position

obs = Observation(
    maze=maze,
    current=Position(5, 5),
    goal=Position(19, 19),
    step_count=10,
    path_cost=12.5
)

# Agent uses this information to decide next move
next_direction = agent.step(obs)
```

### AgentDebugState

Optional visualization data from agents:

```python
from utils.maze_core import AgentDebugState, Position

debug = AgentDebugState(
    frontier={Position(5, 5), Position(6, 5)},
    explored={Position(4, 4), Position(4, 5)},
    discovered={Position(5, 6), Position(6, 6)},
    current_path=[Position(0, 0), Position(1, 0), Position(2, 0)],
    metadata={"algorithm": "BFS", "queue_size": 15}
)

# Visualizer displays this data
```

### MazeResult

Execution results and metrics:

```python
from utils.maze_core import MazeResult

result = MazeResult(
    solved=True,
    steps=87,
    path_cost=142.0,
    optimal_cost=137.0,
    nodes_explored=421,
    execution_time_ms=3.2,
    maze_seed=12345,
    agent_name="a_star_agent"
)

# Calculate metrics
ratio = result.optimality_ratio          # 0.9635
percent = result.optimality_percentage   # 96.35%

# Serialize to JSON
json_str = result.to_json()
dict_repr = result.to_dict()
```

## Usage Example

```python
from utils.maze_core import Maze, Cell, Position, Direction, Observation

# Create a simple 3x3 maze
cells = [
    [Cell(0b1001, 1), Cell(0b1010, 1), Cell(0b0110, 1)],
    [Cell(0b1001, 1), Cell(0b0000, 1), Cell(0b0110, 1)],
    [Cell(0b1000, 1), Cell(0b0100, 1), Cell(0b0100, 1)],
]

maze = Maze(
    width=3,
    height=3,
    cells=cells,
    start=Position(0, 0),
    goal=Position(2, 2),
    seed=42
)

# Check validity
print(maze.can_move_to(Position(0, 0), Direction.EAST))  # True
print(maze.get_neighbors(Position(1, 1)))                # [NORTH, SOUTH, EAST, WEST]

# Create observation for agent
obs = Observation(maze=maze, current=Position(0, 0), goal=Position(2, 2))
```

## API Reference

See [api_reference.md](../../docs/api_reference.md) for complete documentation.
