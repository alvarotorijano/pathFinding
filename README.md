# Maze Search Algorithms - Learning Framework

A comprehensive Python framework for teaching **uninformed and informed search algorithms** through practical maze-solving exercises.

Students implement search agents (BFS, DFS, Dijkstra, Greedy, A*, etc.) to navigate procedurally generated mazes, with real-time visualization and detailed performance metrics.

---

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/alvarotorijano/pathFinding
cd pathFinding

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate a Maze

```bash
python -m labyrinth generate \
    --width 20 \
    --height 20 \
    --type perfect \
    --seed 42 \
    --output maze.maze
```

### 3. Run an Example Agent

```bash
python -m labyrinth run \
    --maze maze.maze \
    --agent dfs_agent \
    --visualize \
    --speed 10
```

### 4. Implement Your First Agent

See [Your First Agent](./docs/YOUR_FIRST_AGENT.md) for step-by-step instructions.

---

## 📚 Documentation

### For Students

**Just starting?** Read these in order:
1. **[Student Setup](./docs/STUDENT_SETUP.md)** — Installation and first steps (5 minutes)
2. **[Your First Agent](./docs/YOUR_FIRST_AGENT.md)** — Write Random, DFS, and BFS agents (tutorial)
3. **[Student Guide](./docs/student_guide.md)** — Detailed walkthrough
4. **[API Reference](./docs/api_reference.md)** — Framework API documentation

### For Instructors

**Setup and evaluation:**
1. **[Quick Start (Instructors)](./docs/QUICK_START_INSTRUCTOR.md)** — 10-minute setup checklist
2. **[WASM Solver Setup](./docs/WASM_SETUP.md)** — Reference solver setup
3. **[Instructor Setup Guide](./docs/INSTRUCTOR_SETUP.md)** — Comprehensive guide with deployment options
4. **[Architecture Overview](./docs/ARCHITECTURE_OVERVIEW.md)** — System design and security

### Reference

- **[Delivery Summary](./docs/DELIVERY_SUMMARY.md)** — What's been built
- **[Solver Infrastructure Status](./docs/SOLVER_INFRASTRUCTURE_STATUS.md)** — Current status
- **[Maze Format](./docs/maze_format.md)** — `.maze` file specification
- **[Reference Solver](./docs/reference_solver.md)** — How the optimal solution works
- **[CLI Reference](./docs/cli_reference.md)** — Command-line reference

---

## Key Features

✅ **Maze Generation** — Multiple topology types with configurable parameters  
✅ **Persistent Agent State** — Maintain search state between steps  
✅ **Real-time Visualization** — Terminal-based ASCII display  
✅ **Comprehensive Metrics** — Path cost, optimality, nodes explored, execution time  
✅ **Multiple Visibility Modes** — Full map, radius-based, local perception  
✅ **Benchmarking** — Compare multiple agents on multiple mazes  
✅ **Reproducible Results** — Seed-based maze generation  
✅ **Cross-platform** — Windows, macOS, Linux  
✅ **Reference Solver** — Private WASM-based optimal path calculator  

---

## For Instructors: WASM Solver Setup

The framework includes an **optional private reference solver** compiled to WebAssembly for calculating optimal solutions:

- **Public Repository** (this one) — Student-facing framework
- **Private Repository** (`labyrinth-solver-wasm`) — Instructor-only A* solver

**Quick Start:**
```bash
git clone <private-repo-url> labyrinth-solver-wasm
cd labyrinth-solver-wasm
./build.sh              # macOS/Linux, or .\build.ps1 on Windows
pip install target/wheels/labyrinth_solver_wasm-*.whl
```

For detailed setup and deployment:
- **[WASM_SETUP.md](./docs/WASM_SETUP.md)** — Quick reference
- **[Instructor Setup Guide](./docs/INSTRUCTOR_SETUP.md)** — Step-by-step with deployment options
- **[Architecture Overview](./docs/ARCHITECTURE_OVERVIEW.md)** — System design and security model
- **[Status Report](./docs/SOLVER_INFRASTRUCTURE_STATUS.md)** — What's included and how to use it

**Note:** The framework works perfectly fine without the solver (all tests pass). The WASM solver is instructor infrastructure for calculating optimal metrics during evaluation.

---

## Project Structure

```
labyrinth/
├── labyrinth/              # Main package
│   ├── __init__.py
│   ├── __main__.py         # CLI entry point
│   └── cli/                # Command implementations
├── utils/                  # Framework utilities
│   ├── maze_core/          # Core data models & algorithms
│   ├── maze_generator/     # Maze generation CLI
│   ├── maze_runner/        # Agent execution CLI
│   ├── maze_visualizer/    # Visualization tools
│   └── ...
├── agents/                 # Student agent implementations
│   ├── bfs_agent/          # Example: BFS
│   ├── dfs_agent/          # Example: DFS
│   └── ...
├── mazes/                  # Maze files
│   ├── examples/           # Example mazes
│   └── generated/          # Generated mazes
├── tests/                  # Test suite
├── docs/                   # Documentation
│   ├── CLAUDE.md           # Project constraints
│   ├── api_reference.md    # API documentation
│   ├── student_guide.md    # Student walkthrough
│   ├── maze_format.md      # `.maze` file format
│   └── ...
├── CLAUDE.md               # Project rules (root level)
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── config.json             # Configuration
└── .gitignore
```

---

## Usage

### Generate Mazes

```bash
# Perfect maze (one solution, many dead ends)
maze generate --width 50 --height 50 --type perfect --seed 123 --output perfect.maze

# Multiple solutions
maze generate --width 30 --height 30 --type multiple --seed 456 --output multiple.maze

# Unsolvable (no path from start to goal)
maze generate --width 20 --height 20 --type unsolvable --seed 789 --output unsolvable.maze

# With random costs
maze generate --width 30 --height 30 --type perfect --cost-map random --cost-range 1:10 --seed 999 --output costs.maze
```

### Run Agents

```bash
# Full map, realtime visualization
maze run --maze perfect.maze --agent bfs_agent --visualize

# With specific parameters
maze run --maze costs.maze --agent dijkstra_agent --visualize --speed 5 --max-steps 5000

# Partial observability
maze run --maze perfect.maze --agent my_agent --visibility radius --radius 3 --visualize

# Generate inline, run, output trace
maze run --width 25 --height 25 --type perfect --agent a_star_agent --output-trace result.json
```

### Benchmark Agents

```bash
# Compare BFS and DFS on all mazes in directory
maze benchmark \
    --maze-dir ./mazes/examples \
    --agents bfs_agent,dfs_agent \
    --output results.csv
```

### Replay Results

```bash
# Replay previous execution from trace
maze replay result.json --visualize --speed 10
```

### List Available

```bash
# List agents
maze list --agents

# List mazes
maze list --mazes
```

---

## CLI Reference

See [CLI Documentation](./docs/cli_reference.md) for complete command reference.

---

## Complete Documentation Index

See the **[Documentation](./docs/)** section above for the full list of guides organized by audience (students/instructors) and topic.

---

## Example Agents

### BFS (Breadth-First Search)

```bash
maze run --maze maze.maze --agent bfs_agent --visualize
```

Explores level-by-level. Good for finding shortest path with uniform costs.

### DFS (Depth-First Search)

```bash
maze run --maze maze.maze --agent dfs_agent --visualize
```

Explores depth-first. Uses less memory but may find longer paths.

---

## Implementing Your Own Agent

1. Create a folder: `agents/my_agent/`
2. Implement the `Agent` interface:

```python
from utils.maze_core.agent import Agent
from utils.maze_core.models import Direction, Observation

class MyAgent(Agent):
    
    def __init__(self):
        """Initialize persistent state."""
        self.visited = set()
        self.frontier = []
    
    def step(self, observation: Observation) -> Direction:
        """
        Decide next move based on observation.
        
        Parameters:
            observation: Current maze state, position, goal
        
        Returns:
            Direction to move (NORTH, SOUTH, EAST, WEST)
        """
        # Your algorithm here
        return Direction.NORTH
    
    def debug_state(self):
        """Optional: return visualization data."""
        return {
            "visited": self.visited,
            "frontier": self.frontier
        }
```

3. Run your agent:

```bash
maze run --maze maze.maze --agent my_agent --visualize
```

See [Your First Agent](./docs/YOUR_FIRST_AGENT.md) for a detailed tutorial, or [Student Guide](./docs/student_guide.md) for a comprehensive walkthrough.

---

## Testing

Run the full test suite:

```bash
python tests/run_tests.py
```

Or with pytest directly:

```bash
pytest tests/ -v --cov
```

---

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`
- Virtual environment recommended

---

## License

[Specify license if applicable]

---

## Support

- **Questions?** See [Student Guide](./docs/student_guide.md)
- **Bug reports?** Check [Issues](./docs/troubleshooting.md)
- **Contributing?** Follow [CLAUDE.md](./CLAUDE.md) standards

---

**Last updated:** 2026-09-07  
**Status:** V1 Implementation in Progress
