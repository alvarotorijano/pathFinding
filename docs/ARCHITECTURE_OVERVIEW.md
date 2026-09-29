# Architecture Overview - Two-Repository System

**Purpose:** Explain the architecture of the Maze Search Algorithms framework to instructors.

---

## Executive Summary

The labyrinth framework is split into **two repositories**:

1. **labyrinth** (PUBLIC) - Student-facing
   - Maze generation, agent interface, CLI, examples
   - Students clone and modify this
   - ~1200 lines of core code, 54 tests
   - NO solver implementation

2. **labyrinth-solver-wasm** (PRIVATE) - Instructor infrastructure
   - Rust A* reference solver
   - Compiled to Python wheel via maturin
   - Only instructors can access and build
   - ~200 lines of Rust code

---

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────┐
│                STUDENT ENVIRONMENT                   │
├──────────────────────────────────────────────────────┤
│                                                      │
│  git clone labyrinth  ← Public repository           │
│  cd labyrinth                                        │
│  pip install -r requirements.txt                     │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  Agent Implementation (student writes)     │    │
│  └─────────────┬────────────────────────────┘     │
│                │                                    │
│                ▼                                    │
│  ┌────────────────────────────────────────────┐    │
│  │  Simulator                                 │    │
│  │  ├─ step() agent on maze                   │    │
│  │  ├─ record metrics (steps, cost, time)     │    │
│  │  └─ try to call wasm_solver (optional)     │    │
│  └─────────────┬────────────────────────────┘     │
│                │                                    │
│         ┌──────▼───────────────────┐              │
│         │ WASM Available?           │              │
│         ├──────┬───────────────────┤              │
│         │ YES  │ NO (expected)      │              │
│         └──┬───┴───────────┬────────┘              │
│            ▼               ▼                        │
│      ┌──────────┐    ┌──────────────────┐         │
│      │ Call     │    │ Skip optimal     │         │
│      │ WASM     │    │ metrics, report  │         │
│      │ solver   │    │ only agent stats │         │
│      └────┬─────┘    └──────────────────┘         │
│           ▼                                        │
│      ┌───────────────────────────────────┐        │
│      │  MazeResult                        │        │
│      │  ├─ solved: bool                   │        │
│      │  ├─ steps: int                     │        │
│      │  ├─ path_cost: float               │        │
│      │  ├─ optimal_cost: float (0 if N/A) │        │
│      │  ├─ optimality_ratio: float (N/A)  │        │
│      │  └─ ...                            │        │
│      └──────────────────────────────────┘        │
│                                                      │
└──────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────┐
│         INSTRUCTOR ENVIRONMENT (Build-Time)          │
├──────────────────────────────────────────────────────┤
│                                                      │
│  git clone labyrinth-solver-wasm (PRIVATE)         │
│  cd labyrinth-solver-wasm                           │
│  pip install maturin                                │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  Rust Source Code                          │    │
│  │  ├─ src/lib.rs (A* algorithm)             │    │
│  │  ├─ Position, Node, SolveResult structs   │    │
│  │  └─ PyO3 bindings                         │    │
│  └─────────────┬────────────────────────────┘     │
│                │                                    │
│                ▼                                    │
│  ┌────────────────────────────────────────────┐    │
│  │  Maturin Build System                      │    │
│  │  ├─ pyproject.toml: build config           │    │
│  │  ├─ build.sh/build.ps1: helper scripts     │    │
│  │  └─ Cargo.toml: Rust dependencies          │    │
│  └─────────────┬────────────────────────────┘     │
│                │                                    │
│                ▼                                    │
│  ┌────────────────────────────────────────────┐    │
│  │  Compiled Output                            │    │
│  │  └─ target/wheels/*.whl  (Python wheel)    │    │
│  │     ├─ labyrinth_solver_wasm-*.whl (Win)   │    │
│  │     ├─ labyrinth_solver_wasm-*.whl (Mac)   │    │
│  │     └─ labyrinth_solver_wasm-*.whl (Linux) │    │
│  └─────────────┬────────────────────────────┘     │
│                │                                    │
│                ▼                                    │
│  ┌────────────────────────────────────────────┐    │
│  │  Distribution Options                       │    │
│  │  ├─ Direct file: pip install /path/*.whl   │    │
│  │  ├─ PyPI: private package server            │    │
│  │  ├─ Pre-install: include in lab setup       │    │
│  │  └─ Docker: embed in container image        │    │
│  └─────────────┬────────────────────────────┘     │
│                │                                    │
│                └─→ Deployed to student machines/labs
│                   (optionally; works without it)
│
└──────────────────────────────────────────────────────┘
```

---

## Component Details

### labyrinth Repository (Public)

**Purpose:** Teaching framework for search algorithms.

**What's Inside:**
```
labyrinth/
├── agents/
│   ├── dfs_agent/
│   ├── random_agent/
│   └── ... (student agents)
├── utils/maze_core/
│   ├── models.py         (Cell, Maze, Observation, etc.)
│   ├── generator.py      (Maze generation)
│   ├── simulator.py      (Agent execution, metrics)
│   ├── wasm_solver.py    (Wrapper for WASM - tries to import, handles gracefully)
│   └── agent.py          (Base Agent class)
├── labyrinth/cli/
│   ├── runner.py         (CLI for generate, run, list)
│   └── ... (commands)
├── mazes/                (Sample .maze files)
├── tests/
│   ├── test_models.py
│   ├── test_generator.py
│   └── test_integration.py
├── docs/
│   ├── reference_solver.md  (Student-facing: explains optimal solution)
│   ├── INSTRUCTOR_SETUP.md  (Instructor-only: setup guide)
│   ├── ARCHITECTURE_OVERVIEW.md
│   └── ...
├── requirements.txt
└── README.md
```

**Key Code: wasm_solver.py**
```python
# This is the BRIDGE between student code and instructor infrastructure

try:
    import labyrinth_solver_wasm
    WASM_AVAILABLE = True
except ImportError:
    WASM_AVAILABLE = False
    labyrinth_solver_wasm = None

def solve_maze(...) -> Tuple[bool, List, float, int]:
    """Solve using WASM. If not available, raises error."""
    if not WASM_AVAILABLE:
        raise RuntimeError("WASM solver not available. "
                         "Install labyrinth-solver-wasm from private repo.")
    
    result = labyrinth_solver_wasm.solve_maze(...)
    return (result.solved, result.path, result.cost, result.nodes_expanded)
```

**Key Code: simulator.py**
```python
# When agent solves the maze, optionally call WASM to get optimal solution

if position == self.maze.goal:
    try:
        walls = [cell.walls for cell in maze.cells]
        costs = [cell.cost for cell in maze.cells]
        optimal_solved, optimal_path, optimal_cost, _ = wasm_solve_maze(...)
    except Exception:  # WASM not available
        optimal_solved = False
        optimal_cost = 0.0
    
    return MazeResult(
        solved=True,
        steps=steps,
        path_cost=path_cost,
        optimal_cost=optimal_cost,  # 0.0 if WASM unavailable
        ...
    )
```

---

### labyrinth-solver-wasm Repository (Private)

**Purpose:** Reference solver for calculating optimal solutions.

**What's Inside:**
```
labyrinth-solver-wasm/
├── src/
│   └── lib.rs            (Rust A* algorithm)
│       ├── Position struct (with Manhattan distance heuristic)
│       ├── Node struct (for BinaryHeap frontier)
│       ├── solve_maze() function (A* search)
│       ├── reconstruct_path() helper
│       └── SolveResult struct (solved, cost, path, nodes_expanded)
│           with #[pyclass] and #[pyfunction] attributes
├── tests/
│   └── integration_tests.rs
├── Cargo.toml             (Rust dependencies: pyo3, wasm-bindgen)
├── pyproject.toml         (Maturin build config)
├── build.sh, build.ps1    (Helper scripts)
├── .gitignore
├── README.md              (Marked PRIVATE)
├── BUILDING.md            (Build instructions - instructors only)
├── DISTRIBUTION.md        (Distribution strategies)
└── .github/
    └── workflows/         (Optional: CI/CD to build on all platforms)
```

**Algorithm: A* Search**
```
solve_maze(width, height, start, goal, walls, costs):
    
    g_score = {start: 0}
    h_score = manhattan_distance(start, goal)
    f_score = {start: h_score}
    frontier = priority_queue([start])
    closed = set()
    
    while frontier not empty:
        current = frontier.pop_best()  // lowest f_score
        
        if current == goal:
            return reconstruct_path(current)
        
        if current in closed:
            continue
        closed.add(current)
        
        for neighbor in neighbors(current):
            if neighbor in closed:
                continue
            
            tentative_g = g_score[current] + cost(neighbor)
            
            if tentative_g < g_score.get(neighbor, inf):
                g_score[neighbor] = tentative_g
                h = manhattan_distance(neighbor, goal)
                f_score[neighbor] = tentative_g + h
                frontier.push(neighbor)
    
    return not_found()
```

**PyO3 Bindings:**
```rust
#[pyclass]                           // Python class
pub struct SolveResult {
    #[pyo3(get)]                     // Python readable attribute
    pub solved: bool,
    #[pyo3(get)]
    pub cost: f64,
    #[pyo3(get)]
    pub path: Vec<(i32, i32)>,
    #[pyo3(get)]
    pub nodes_expanded: u32,
}

#[pyfunction]                        // Python function
pub fn solve_maze(
    width: i32, height: i32,
    start_x: i32, start_y: i32,
    goal_x: i32, goal_y: i32,
    walls: Vec<u8>,
    costs: Vec<f64>,
) -> SolveResult { ... }

#[pymodule]                          // Python module definition
fn labyrinth_solver_wasm(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(solve_maze, m)?)?;
    m.add_class::<SolveResult>()?;
    Ok(())
}
```

---

## Build & Deployment Workflow

### Step 1: Build (Instructor, One-Time)

```bash
cd labyrinth-solver-wasm

# Check prerequisites
rustc --version  # Rust compiler
python --version  # Python 3.8+
pip install maturin

# Compile Rust to Python wheel
./build.sh  # or .\build.ps1 on Windows

# Output: target/wheels/labyrinth_solver_wasm-1.0.0-cp313-*.whl
```

**Time:** ~90 seconds (first build), ~10-30 seconds (incremental)

### Step 2: Install (Instructor)

```bash
# Option A: Local development
pip install target/wheels/labyrinth_solver_wasm-*.whl

# Option B: Instructor environment
pip install --target /shared/lab/site-packages target/wheels/*.whl

# Option C: Upload to private PyPI
twine upload --repository private-pypi target/wheels/*
```

### Step 3: Verify (Instructor)

```bash
# Check import
python -c "import labyrinth_solver_wasm; print('✅ Solver ready')"

# Run full test suite
cd labyrinth
pytest tests/ -v

# Look for: optimal_solved: True, optimal_cost: <value>
```

### Step 4: Deploy to Students (Optional)

**Option 1: Pre-Installed Lab Machines**
- Wheel installed by IT during lab setup
- Students see no solver infrastructure
- Transparent to students

**Option 2: Private Package Server**
- Upload wheel to private PyPI/Artifactory
- Create combined `labyrinth-complete` package
- Students install via pip (no source visible)

**Option 3: Containerized (Docker)**
- Include wheel in Docker image
- Students run: `docker pull instructor/labyrinth && docker run -it`
- No local Python setup needed

**Option 4: Not Distributed (Recommended)**
- Only instructors have WASM solver
- Students run tests WITHOUT it (still pass)
- Instructors evaluate using WASM (see optimal metrics)
- Educational value: students don't trivially access reference implementation

---

## Educational Design Rationale

### Why Two Repositories?

1. **Separation of Concerns**
   - Students implement search algorithms
   - Reference solver is black-box infrastructure
   - No temptation to copy or reverse-engineer

2. **Security Through Compartmentalization**
   - Student repo: MIT/Apache licensed, public
   - Solver repo: private, instructor-only
   - Clear boundaries, no accidental exposure

3. **Scalability**
   - One public framework serves all courses
   - Each instructor manages their own solver deployment
   - Easy to update solver independently

4. **Testing & Evaluation**
   - Students test against their own solutions
   - Instructors evaluate using optimal reference
   - Fair comparison: same algorithm, different implementations

### Why WASM (Compiled)?

1. **Performance**
   - Rust is ~2-5x faster than Python A*
   - Relevant for larger mazes (100x100+)

2. **Obfuscation**
   - Compiled binary is harder to reverse-engineer
   - "Security through obscurity" is not cryptographic protection, but raises the bar

3. **Portability**
   - Python wheel works on Windows/macOS/Linux
   - No native code compilation on student machines
   - Consistent behavior across platforms

4. **Isolation**
   - Rust memory safety prevents buffer overflows
   - WASM sandboxing (future-proofing)
   - Can't corrupt student process even if buggy

### Why Optional (Graceful Degradation)?

1. **Learning**
   - Students can run full framework without WASM
   - Tests pass whether or not solver is installed
   - Solver dependency is instructor infrastructure, not student requirement

2. **Flexibility**
   - Instructors without build capability can still teach
   - Pre-compiled wheels can be distributed separately
   - No installation burden on students

3. **Resilience**
   - System doesn't break if solver unavailable
   - Optimal metrics simply skipped
   - Agent execution and testing unaffected

---

## File Organization

### Student Visibility

```
labyrinth/  ← Students see this
├── agents/  ← Where students write code
├── mazes/
├── utils/maze_core/
│   ├── models.py
│   ├── generator.py
│   ├── simulator.py
│   ├── wasm_solver.py    ← Wrapper only, not implementation
│   └── agent.py
├── tests/
├── docs/
│   └── reference_solver.md  ← "A reference solver is used to calculate optimal path"
├── README.md
└── requirements.txt        ← Does NOT list labyrinth-solver-wasm
```

### Instructor Visibility

```
labyrinth/  ← Students see this
└── docs/
    └── INSTRUCTOR_SETUP.md  ← "How to build and deploy WASM"
    └── ARCHITECTURE_OVERVIEW.md

labyrinth-solver-wasm/  ← PRIVATE, only instructors
├── src/lib.rs           ← A* algorithm source
├── Cargo.toml           ← Build config
├── BUILDING.md          ← "How to compile"
├── DISTRIBUTION.md      ← "How to deploy"
└── README.md            ← "PRIVATE REPOSITORY"
```

---

## Integration Points

### 1. Data Format: Maze Representation

**Cells:**
```python
# Each cell has:
walls: int  # 4-bit encoding: N=8, E=4, S=2, W=1
            # 1 = passage open, 0 = wall
cost: float  # Movement cost into this cell
```

**Maze:**
```python
width: int
height: int
start: Position
goal: Position
cells: List[List[Cell]]  # 2D grid
```

**Serialization:**
```
SIZE 20 20
SEED 12345
START 0 0
GOAL 19 19

TOPOLOGY
1010 0110 1100 ... (one 4-bit value per cell)

COSTS
1.0 1.0 1.5 ... (one float per cell)
```

### 2. API: Solver Input/Output

**Input:**
```python
solve_maze(
    width: int,
    height: int,
    start_x: int, start_y: int,
    goal_x: int, goal_y: int,
    walls: List[int],          # 4-bit values per cell
    costs: List[float],        # floats per cell
) -> SolveResult
```

**Output:**
```python
class SolveResult:
    solved: bool               # true if goal reachable
    cost: float                # optimal path cost
    path: List[(int, int)]     # coordinates from start to goal
    nodes_expanded: int        # A* frontier size
```

### 3. Integration Point: Simulator

**When Agent Solves Maze:**
```python
if position == maze.goal:
    # Extract maze data
    walls = [...all cell walls...]
    costs = [...all cell costs...]
    
    # Call WASM solver (if available)
    try:
        optimal_solved, optimal_path, optimal_cost, nodes = wasm_solve_maze(
            maze.width, maze.height,
            maze.start.x, maze.start.y,
            maze.goal.x, maze.goal.y,
            walls, costs
        )
    except ImportError:
        # WASM not installed
        optimal_solved = False
        optimal_cost = 0.0
    
    # Return result with optional optimal metrics
    return MazeResult(
        solved=True,
        path_cost=agent_cost,
        optimal_cost=optimal_cost,
        ...
    )
```

---

## Deployment Scenarios

### Scenario 1: Local Development (Instructor)

```bash
# Step 1: Build WASM
cd labyrinth-solver-wasm
./build.sh
pip install target/wheels/*.whl

# Step 2: Develop & test
cd labyrinth
pytest tests/  # WASM metrics included

# Step 3: Evaluate agents
python labyrinth/cli/runner.py run --agent student_agent
# Shows: optimal_cost, optimality ratio
```

### Scenario 2: Lab Environment (Pre-Install)

```bash
# IT Setup (once)
cd labyrinth-solver-wasm
./build.sh
pip install target/wheels/*.whl

# Student Workflow
git clone labyrinth
cd labyrinth
pip install -r requirements.txt
# WASM already installed, works transparently
pytest tests/  # Runs without WASM if not needed
```

### Scenario 3: Online Course (Docker)

```dockerfile
FROM python:3.11
COPY labyrinth-solver-wasm-*.whl /tmp/
RUN pip install /tmp/*.whl
RUN git clone labyrinth
WORKDIR labyrinth
RUN pytest tests/
```

Students: `docker run -it instructor/labyrinth bash`

### Scenario 4: No Solver (Students Only)

```bash
git clone labyrinth
cd labyrinth
pip install -r requirements.txt
pytest tests/

# Tests run fine, just skip optimal metrics
# Agent evaluation still works
```

---

## Security & Privacy

### What's Protected

- **Solver source code** - Only in private repo
- **Solver binary** - Compiled wheel, not distributed to students
- **Build documentation** - BUILDING.md, DISTRIBUTION.md in private repo

### What's Transparent

- **Maze format** - Well-documented, students can read/write .maze files
- **Algorithm results** - Optimal cost shown (students see it was calculated)
- **Integration points** - Code shows WASM is called (they can see `wasm_solver.py`)

### Security Model

- **Not cryptographic** - WASM is low-level bytecode, could theoretically be decompiled
- **Practical obscurity** - Discourages casual attempts to see source
- **Separation** - No compiled solver in student repository

**This is appropriate for education.** Students may eventually see the solver (good), but don't trivially copy it (also good).

---

## Maintenance & Updates

### Adding New Features

1. **Student-facing feature** → Update `labyrinth/` repo
2. **Solver bug fix** → Update `labyrinth-solver-wasm/`, rebuild
3. **New algorithm** → Add to `labyrinth-solver-wasm/`, maintain compatibility

### Version Management

**labyrinth-solver-wasm/Cargo.toml:**
```toml
[package]
version = "1.1.0"  # Increment on changes
```

**labyrinth/docs/SOLVER_VERSION.md:**
```
Requires: labyrinth-solver-wasm >= 1.0.0
Current installed: 1.1.0 (built 2024-01-15)
```

### Backward Compatibility

- WASM API is stable (solve_maze signature doesn't change)
- Framework handles both old and new solver versions
- New solver works with old framework (graceful upgrade)

---

## FAQ

**Q: Can students access the solver source?**
A: Not via this repo. Source is in private repository. They could eventually reverse-engineer the compiled binary (it's not cryptographically protected), but that's high effort and defeats the learning goal.

**Q: Do I have to use WASM?**
A: No. Framework works without it. WASM is optional instructor infrastructure for evaluation.

**Q: Can I modify the solver?**
A: Yes, in your copy of private repo. Rebuild the wheel and redeploy. Changes don't affect framework code (clean separation).

**Q: How do I test students haven't cheated using the solver?**
A: Check their code/git history. Framework shows optimality ratio (if they claim 0.95, you know 0.95 ≤ optimal). Suspicious claims can be investigated.

**Q: Is WASM faster than Python?**
A: Yes, ~2-5x faster on large mazes. But for 20x20 mazes, the difference is ~1ms, unnoticeable.

**Q: What if WASM has a bug?**
A: Framework still works (skips optimal metrics). Your agent tests still run. You can rollback to previous solver version by rebuilding old Cargo.toml.

---

## References

- [INSTRUCTOR_SETUP.md](./INSTRUCTOR_SETUP.md) - Step-by-step setup guide
- [WASM_SETUP.md](./WASM_SETUP.md) - Quick reference for instructors
- [reference_solver.md](./reference_solver.md) - Student-facing explanation
- [labyrinth-solver-wasm/BUILDING.md](../labyrinth-solver-wasm/BUILDING.md) - Build details
- [labyrinth-solver-wasm/DISTRIBUTION.md](../labyrinth-solver-wasm/DISTRIBUTION.md) - Deployment strategies

---

**Last Updated:** 2024-01-15
**Status:** Production Ready
**Access:** This document is public to students; detailed setup docs are instructor-only.
