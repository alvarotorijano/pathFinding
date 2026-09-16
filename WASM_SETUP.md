# WASM Solver Setup - Instructors Only

**⚠️ CONFIDENTIAL** - This document is for instructors who have access to the private `labyrinth-solver-wasm` repository.

**Students should NOT follow these steps** - the WASM solver will be pre-built and distributed to your environment.

---

## Quick Start (5 minutes)

### Prerequisites
- Rust toolchain (https://rustup.rs/)
- Python 3.8+
- Access to private `labyrinth-solver-wasm` repository

### Build & Install

```bash
# 1. Clone private repo
git clone <private-repo-url> labyrinth-solver-wasm
cd labyrinth-solver-wasm

# 2. Install build tools
pip install maturin

# 3. Build (2-3 minutes)
./build.sh          # macOS/Linux
# or
.\build.ps1         # Windows PowerShell

# 4. Install wheel
pip install target/wheels/labyrinth_solver_wasm-*.whl

# 5. Verify
python -c "import labyrinth_solver_wasm; print('✅ Solver ready')"
```

Done! The framework now calculates optimal metrics.

---

## Comprehensive Setup Guide

**For detailed setup instructions**, see: [`docs/INSTRUCTOR_SETUP.md`](docs/INSTRUCTOR_SETUP.md)

That document covers:
- Step-by-step build process
- Multiple deployment scenarios (local, lab, cloud, Docker)
- Building for multiple platforms (Windows/macOS/Linux)
- Distribution methods (pre-install, package server, containerized)
- Troubleshooting and best practices
- FAQ

---

## Architecture

The WASM solver is compiled once and distributed as a Python wheel:

```
labyrinth-solver-wasm (private repo)
    ├── src/lib.rs          (Rust A* implementation)
    └── Cargo.toml, pyproject.toml (Build config)
    
    ./build.sh (maturin build --release)
    ↓
    target/wheels/labyrinth_solver_wasm-*.whl
    
    pip install *.whl
    ↓
    import labyrinth_solver_wasm   (Python module)
    ↓
    utils/maze_core/wasm_solver.py (wrapper)
    ↓
    Framework calculates optimal solutions
```

---

## How It Works

### With WASM Installed (Normal Operation)

1. `wasm_solver.py` imports `labyrinth_solver_wasm` successfully
2. `WASM_AVAILABLE = True`
3. When an agent solves a maze, simulator calls `solve_maze()`
4. Optimal cost and path are calculated
5. Optimality metrics displayed in results

**Test Output:**
```
optimal_solved: True
optimal_cost: 45.3
optimality_ratio: 0.95
```

### Without WASM (Graceful Fallback)

1. `wasm_solver.py` fails to import (ImportError caught)
2. `WASM_AVAILABLE = False`
3. Framework runs normally
4. Optimal metrics are skipped (cost = 0.0, solved = False)
5. Tests still pass

**Test Output:**
```
optimal_solved: False
optimal_cost: 0.0
optimality_ratio: (skipped)
```

---

## Key Points

1. **Framework works without WASM** - Tests pass, agents run normally
2. **WASM is instructor infrastructure only** - Students never see source code or binary
3. **Wheel is platform-specific** - Must build for Windows/macOS/Linux separately
4. **No external dependencies** - Everything runs locally after `pip install`
5. **Security through separation** - Private repo not accessible to students

---

## What Students Experience

**Without WASM (Student Environment):**
```
Agent: bfs_agent
Solved: YES ✓
Steps: 45
Path Cost: 67.3
Nodes Explored: 127
Execution Time: 1.23ms
```

**With WASM (Instructor Environment):**
```
Agent: bfs_agent
Solved: YES ✓
Steps: 45
Path Cost: 67.3
Nodes Explored: 127
Execution Time: 1.23ms
─────────────────────────────────
Optimal Cost: 63.0      ← Only visible to instructors
Optimality: 94.8%       ← Only visible to instructors
```

---

## Workflow

1. **Access the private repository**
   - You should have git access to `labyrinth-solver-wasm`

2. **Build the wheel** (once per platform)
   ```bash
   cd labyrinth-solver-wasm
   ./build.sh
   ```

3. **Install locally** or distribute to environment
   ```bash
   pip install target/wheels/labyrinth_solver_wasm-*.whl
   ```

4. **Test the integration**
   ```bash
   cd labyrinth
   pytest tests/ -v
   ```
   Results should show `optimal_solved: True`

5. **Deploy to your teaching environment**
   - See `docs/INSTRUCTOR_SETUP.md` for distribution strategies

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `command not found: maturin` | `pip install maturin` |
| Build fails on your platform | Check `labyrinth-solver-wasm/BUILDING.md` |
| `ModuleNotFoundError: labyrinth_solver_wasm` | Install the wheel: `pip install target/wheels/*.whl` |
| Can't access private repo | Contact your course administrator |
| `optimal_solved: False` in tests | Verify solver installed: `python -c "import labyrinth_solver_wasm"` |

---

## Next Steps

1. Clone the private `labyrinth-solver-wasm` repository
2. Follow the Quick Start above to build and install
3. Refer to [`docs/INSTRUCTOR_SETUP.md`](docs/INSTRUCTOR_SETUP.md) for deployment options
4. Test locally before deploying to your environment

---

**Important:** Keep the private repository and all build documentation confidential. Students should only see the public `labyrinth` repository.
