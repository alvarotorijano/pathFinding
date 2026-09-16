# Student Setup Guide

Welcome to the Maze Search Algorithms framework! This guide will get you started in 5 minutes.

---

## Step 1: Clone the Repository

```bash
git clone <repo-url>
cd labyrinth
```

---

## Step 2: Create a Virtual Environment

Keep your system clean by using a Python virtual environment:

```bash
# Create venv
python -m venv venv

# Activate it
source venv/bin/activate        # macOS/Linux
# OR
venv\Scripts\activate           # Windows (cmd)
# OR
venv\Scripts\Activate.ps1       # Windows (PowerShell)
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Install the WASM Solver (Optional)

The framework works without the solver, but installing it gives you optimal metrics for comparison:

```bash
pip install vendor/wheels/labyrinth_solver_wasm-*.whl
```

**Verify it works:**
```bash
python -c "import labyrinth_solver_wasm; print('✅ Solver ready')"
```

---

## Step 5: Run a Quick Test

```bash
# Generate a simple maze
python -m labyrinth generate --width 10 --height 10 --type perfect --seed 42 --output test.maze

# Solve it with the example BFS agent
python -m labyrinth run --maze test.maze --agent bfs_agent
```

You should see output like:
```
==================================================
Agent: BFSAgent
Solved: YES
Steps: 47
Path Cost: 46.0
Optimal Cost: 18.0
Optimality: 39.1%
...
```

---

## What's Next?

- **[Your First Agent](./YOUR_FIRST_AGENT.md)** - Step-by-step guide to write your own search algorithm
- **[API Reference](./api_reference.md)** - Complete API documentation
- **[Student Guide](./student_guide.md)** - More detailed walkthrough

---

## Project Structure

```
labyrinth/
├── agents/              ← Put your agents here
│   ├── bfs_agent/       ← Example: BFS implementation
│   └── dfs_agent/       ← Example: DFS implementation
├── utils/maze_core/     ← Framework (don't modify)
├── tests/               ← Test suite
├── mazes/               ← Maze files
├── docs/                ← Documentation
├── vendor/wheels/       ← Pre-compiled solver (optional)
├── requirements.txt     ← Python dependencies
└── README.md
```

---

## Common Commands

```bash
# Generate a maze
python -m labyrinth generate --width 20 --height 20 --type perfect --seed 123 --output my_maze.maze

# Run an agent on a maze
python -m labyrinth run --maze my_maze.maze --agent bfs_agent --visualize

# Run all tests
pytest tests/ -v

# List available agents
python -m labyrinth list --agents

# List available mazes
python -m labyrinth list --mazes
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module named labyrinth" | Make sure you're in the `labyrinth/` directory and venv is activated |
| "ModuleNotFoundError: No module named pytest" | Run `pip install -r requirements.txt` |
| "ModuleNotFoundError: labyrinth_solver_wasm" | Optional - only install if you want optimal metrics. Run step 4 above. |
| Maze generation fails | Make sure `--width` and `--height` are both > 2 |

---

## Getting Help

- Check the **[docs/](./docs/)** folder for detailed guides
- Look at the example agents in **[agents/](./agents/)** for inspiration
- Read the **[API Reference](./docs/api_reference.md)** for method signatures

---

**Ready to implement your first agent?** → See [Your First Agent](./docs/YOUR_FIRST_AGENT.md)
