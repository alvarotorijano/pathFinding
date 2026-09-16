# Quick Start for Instructors

**Get the WASM solver running in 10 minutes.**

---

## 1️⃣ Prerequisites (One-Time)

Check you have:

```bash
rustc --version       # ✅ Rust compiler installed (https://rustup.rs/)
python --version      # ✅ Python 3.8 or newer
git clone --version   # ✅ Git installed
pip --version         # ✅ pip installed
```

If any fail, install missing tools first.

---

## 2️⃣ Clone Private Repo

```bash
git clone <private-repo-url> labyrinth-solver-wasm
cd labyrinth-solver-wasm
```

(You should have access. If not, contact admin.)

---

## 3️⃣ Build WASM Wheel

**macOS/Linux:**
```bash
pip install maturin
./build.sh
```

**Windows (PowerShell):**
```bash
pip install maturin
.\build.ps1
```

**Timing:** ~90 seconds for first build.

---

## 4️⃣ Install Wheel

```bash
pip install target/wheels/labyrinth_solver_wasm-*.whl
```

**Verify:**
```bash
python -c "import labyrinth_solver_wasm; print('✅ Solver ready')"
```

---

## 5️⃣ Test Integration

```bash
cd ../labyrinth
pytest tests/ -v
```

**Look for:**
```
optimal_solved: True
optimal_cost: <value>
```

If you see these → ✅ **Ready to evaluate!**

---

## 6️⃣ Evaluate Student Agents

```bash
# Run a student agent
python -m labyrinth run \
    --maze generated \
    --width 20 \
    --height 20 \
    --agent student_bfs \
    --visualize
```

**Output includes:**
- Agent metrics (steps, cost, time)
- **Optimal metrics** (optimal cost, optimality ratio) ← WASM

---

## What If...

| Issue | Solution |
|-------|----------|
| "command not found: maturin" | `pip install maturin` |
| Build fails | Check [labyrinth-solver-wasm/BUILDING.md](../labyrinth-solver-wasm/BUILDING.md) |
| Import fails | Reinstall wheel: `pip install --force-reinstall target/wheels/*.whl` |
| Can't access repo | Contact admin for private repo access |

---

## Deployment Options

### Option 1: Local Only (Simplest)
- Build WASM locally
- Use for evaluation on your machine
- **Best for:** Individual instructors

### Option 2: Pre-Install Lab Machines
- Build WASM once
- Include in lab setup script
- Students see no solver infrastructure
- **Best for:** Shared lab environment

### Option 3: Docker Container
- Build WASM
- Include in Dockerfile
- Students run: `docker pull && docker run`
- **Best for:** Online courses, consistency

### Option 4: Private PyPI
- Build and upload wheel
- Students install via pip
- Binary never exposed as source
- **Best for:** Enterprise, security-conscious

**See [Instructor Setup Guide](./INSTRUCTOR_SETUP.md) for details on each.**

---

## Next Steps

1. ✅ Build WASM (10 min)
2. ✅ Test locally (2 min)
3. ⏭️ **Choose deployment** → Pick from options above
4. ⏭️ **Deploy to environment** → See Instructor Setup Guide

---

## Documentation

- **[WASM_SETUP.md](./WASM_SETUP.md)** — Reference guide
- **[Instructor Setup Guide](./INSTRUCTOR_SETUP.md)** — Detailed setup + deployment
- **[Architecture Overview](./ARCHITECTURE_OVERVIEW.md)** — How it all works
- **[Status Report](./SOLVER_INFRASTRUCTURE_STATUS.md)** — What's included

---

**That's it!** You now have optimal metrics for evaluating student agents.

Need help? Check the docs or see [labyrinth-solver-wasm/BUILDING.md](../labyrinth-solver-wasm/BUILDING.md) in the solver repo.
