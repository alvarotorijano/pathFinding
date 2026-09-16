# Instructor Setup Guide - WASM Reference Solver

**Confidential** - For authorized instructors only.

This guide explains how to build, install, and deploy the WASM reference solver for use in your Maze Search Algorithms course.

---

## Overview

The labyrinth framework uses a **private WASM reference solver** (stored in a separate repository) to calculate optimal solutions for maze problems. This solver is:

- **Hidden from students** - They cannot see the source code or implementation
- **Compiled** - Distributed as a binary wheel, not Python source
- **Fast** - Written in Rust, ~2-5x faster than Python
- **Optional** - Framework works without it (optimal metrics are skipped)

### Two Repositories

1. **labyrinth** (Public to students)
   - Main framework, agents, tests
   - Students clone and modify this
   - Contains NO solver implementation
   
2. **labyrinth-solver-wasm** (Private to instructors)
   - Rust A* implementation
   - Compiled to Python wheel
   - Instructors build this once, distribute to environment

---

## Quick Start (5 minutes)

### Prerequisites

- **Rust** - Install from https://rustup.rs/
- **Python 3.8+**
- **pip** or **conda**

### Build and Install

1. **Clone the private repository** (you should have access):
   ```bash
   git clone <private-repo-url> labyrinth-solver-wasm
   cd labyrinth-solver-wasm
   ```

2. **Install build tools**:
   ```bash
   pip install maturin
   ```

3. **Build the wheel**:
   ```bash
   ./build.sh          # macOS/Linux
   # or
   .\build.ps1         # Windows PowerShell
   ```

4. **Install locally**:
   ```bash
   pip install target/wheels/labyrinth_solver_wasm-*.whl
   ```

5. **Verify**:
   ```bash
   python -c "import labyrinth_solver_wasm; print('✅ Solver ready')"
   ```

Done! The framework now has optimal metrics.

---

## Detailed Setup

### Step 1: Access the Private Repository

The WASM solver is in a private repository. You should have access via:

- GitHub organization access
- Direct invite to private repo
- SSH key configured for git access

Test access:
```bash
git clone <private-repo-url>
```

If you get "404 Not Found", contact the course administrator to request access.

### Step 2: Install Rust (One-Time)

```bash
# Download and install
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Update PATH (or restart shell)
source $HOME/.cargo/env
```

Verify:
```bash
rustc --version      # Should show a version
cargo --version      # Should show a version
```

### Step 3: Build the Solver

Navigate to the solver repository:
```bash
cd labyrinth-solver-wasm
```

Check prerequisites:
```bash
rustc --version     # Rust compiler
python --version    # Python 3.8+
pip install maturin # PyO3 build tool
```

Build the wheel:
```bash
# Automatic (with checks)
./build.sh          # macOS/Linux
.\build.ps1         # Windows

# Manual
maturin build --release
```

First build takes ~90 seconds (compilation). Subsequent builds are faster.

**Output:**
```
target/wheels/labyrinth_solver_wasm-1.0.0-cp313-cp313-*.whl
```

Platform-specific wheels are generated for your OS/Python version.

### Step 4: Install to Your Environment

**Option A: Local Development**
```bash
pip install target/wheels/labyrinth_solver_wasm-*.whl
```

**Option B: Development Mode** (auto-recompile on changes)
```bash
maturin develop
```

**Option C: Uninstall Previous Version**
```bash
pip uninstall labyrinth-solver-wasm
pip install target/wheels/labyrinth_solver_wasm-*.whl
```

### Step 5: Test Installation

**Quick check:**
```bash
python -c "import labyrinth_solver_wasm; print('✅ OK')"
```

**Integration check:**
```bash
python -c "from utils.maze_core.wasm_solver import solve_maze; print('✅ Framework integration OK')"
```

**Full test suite:**
```bash
cd ../labyrinth
pytest tests/ -v
```

Look for entries like:
```
optimal_cost: 45.0  ← Solver is working!
optimal_solved: true
```

If tests show `optimal_solved: false` or `optimal_cost: 0.0`, the solver isn't installed.

---

## Deployment Scenarios

### Scenario 1: Local Grading

You evaluate student agents on your machine.

1. **Build once**: `maturin build --release`
2. **Install**: `pip install target/wheels/*.whl`
3. **Run evaluations**:
   ```bash
   cd labyrinth
   python labyrinth/cli/runner.py run --agent student_agent --maze generated
   ```
   Metrics will include optimal values.

### Scenario 2: Shared Lab Environment

Multiple instructors on same machine(s).

1. **Build on one machine**
2. **Install to shared Python environment**:
   ```bash
   pip install --target /shared/python/site-packages target/wheels/*.whl
   ```
3. **All users** point to shared environment (e.g., via `PYTHONPATH` or venv)

### Scenario 3: Student Machines (Lab)

Pre-configure lab machines.

1. **Build on your build machine**
2. **Copy wheel to lab setup script** or shared repo
3. **Lab setup includes**:
   ```bash
   pip install labyrinth
   pip install https://internal-server/labyrinth_solver_wasm-*.whl
   ```
4. **Students never see solver source**

### Scenario 4: Cloud / Remote Grading

If using remote servers (AWS, Azure, HPC cluster):

1. **Build for target OS** (Linux for most servers)
2. **Upload wheel to server**:
   ```bash
   scp target/wheels/*.whl grading-server:/opt/packages/
   ssh grading-server pip install /opt/packages/*.whl
   ```
3. **Run grading** on remote machine

### Scenario 5: Docker Container

For reproducible, containerized evaluation:

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y git
COPY labyrinth-solver-wasm-*.whl /tmp/
RUN pip install /tmp/labyrinth-solver-wasm-*.whl
RUN git clone <labyrinth-repo> /labyrinth
WORKDIR /labyrinth
CMD ["pytest", "tests/"]
```

Build and run:
```bash
docker build -t labyrinth-grader .
docker run labyrinth-grader
```

---

## Building for Multiple Platforms

If you support Windows, macOS, and Linux students:

### Approach 1: CI/CD (Recommended)

Set up GitHub Actions or similar to automatically build wheels for all platforms:

```yaml
# .github/workflows/build-wheels.yml
name: Build Wheels
on: [push, release]
jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12', '3.13']
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install maturin
      - run: maturin build --release
      - uses: actions/upload-artifact@v3
        with:
          name: wheels-${{ matrix.os }}-${{ matrix.python-version }}
          path: target/wheels/
```

Then collect all wheels from artifact downloads.

### Approach 2: Build Locally

Build on each platform you support:

```bash
# On Windows
maturin build --release
# → labyrinth_solver_wasm-1.0.0-cp313-cp313-win_amd64.whl

# On macOS
maturin build --release
# → labyrinth_solver_wasm-1.0.0-cp313-cp313-macosx_*.whl

# On Linux
maturin build --release
# → labyrinth_solver_wasm-1.0.0-cp313-cp313-manylinux_*.whl

# Collect all in one directory
mkdir dist/
cp */target/wheels/*.whl dist/
```

### Approach 3: Compatibility Libraries

For Linux, use `maturin` with `--zig` to cross-compile:

```bash
pip install zig
maturin build --release --zig
```

This can generate wheels for multiple architectures from one Linux machine (advanced).

---

## Distribution to Students

### Important Security Note

**Do NOT distribute:**
- Solver source code
- This BUILDING.md or DISTRIBUTION.md documents
- Installation instructions for the solver

**Do distribute:**
- The compiled `.whl` files
- Main `labyrinth` repository
- Student-facing documentation (agents, CLI, formats)

### Option 1: Pre-Installed Lab Machines

Best for **controlled lab environments**:
- Wheel is installed when lab machines are set up
- Students just clone labyrinth and code
- Solver is invisible to them

Steps:
1. Build wheel
2. Add to lab setup script/image
3. `pip install /admin/packages/labyrinth_solver_wasm-*.whl`
4. Students: `git clone labyrinth; pip install -r requirements.txt`

### Option 2: Private PyPI or Package Server

For **distributed courses** or **bring-your-own-device**:
- Set up private PyPI mirror or Artifactory
- Upload wheels to private repo
- Students install via pip (no source code visible)

Steps:
1. Build and upload wheel to private PyPI
2. Create combined `labyrinth-complete` package that depends on both labyrinth and solver
3. Students: `pip install labyrinth-complete`

Packages are installed from private repo, source isn't exposed.

### Option 3: Bundled Distribution (Docker/VM)

For **online courses** or **maximum control**:
- Create Docker image with both framework and solver
- Students run in container
- No local Python setup needed

Create `Dockerfile`:
```dockerfile
FROM python:3.11
COPY labyrinth-solver-wasm-*.whl /tmp/
RUN pip install /tmp/labyrinth-solver-wasm-*.whl
RUN git clone <labyrinth-repo> /home/student/labyrinth
WORKDIR /home/student/labyrinth
```

Students: `docker pull <image>; docker run -it <image> bash`

### Option 4: Git Submodule (Not Recommended)

If you must include the wheel in a student repo:
1. Create private `student-infrastructure` repository with wheel
2. Add as git submodule to student fork
3. `.gitignore` should prevent accidental commits

```bash
git submodule add <private-solver-repo> solver-wheel
pip install solver-wheel/*.whl
```

**Why not ideal:** Requires git access control, exposes wheel in repo.

---

## Troubleshooting

### Build Issues

**"command not found: maturin"**
```bash
pip install maturin
```

**"error: linker `cc` not found"** (Linux)
```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# Fedora/RHEL
sudo dnf install gcc g++
```

**"error: Microsoft Visual C++ 14.0 or greater is required"** (Windows)
Install Visual Studio Build Tools:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Installation Issues

**"ModuleNotFoundError: No module named 'labyrinth_solver_wasm'"**

Check installation:
```bash
pip list | grep labyrinth-solver-wasm
python -c "import labyrinth_solver_wasm"
```

If missing, reinstall:
```bash
pip install --force-reinstall target/wheels/labyrinth_solver_wasm-*.whl
```

**"ImportError: DLL load failed" (Windows)**

Missing Visual C++ runtime:
https://support.microsoft.com/en-us/help/2977003

**"ImportError: libssl.so not found" (Linux)**

```bash
# Ubuntu/Debian
sudo apt-get install libssl-dev

# Fedora/RHEL
sudo dnf install openssl-devel
```

### Testing Issues

**"optimal_solved: false" in test output**

The solver isn't installed. Run:
```bash
pip install target/wheels/labyrinth_solver_wasm-*.whl
pytest tests/ -v
```

**"WASM solver not available" error**

Same as above. Solver isn't installed in the active Python environment.

### Performance Issues

**Solver takes too long**

This shouldn't happen (A* is efficient). Check:
- Maze isn't unsolvable
- Goal is reachable
- Maze size isn't extreme (>1000x1000)

If still slow, it's likely the student agent, not the solver.

---

## Maintenance & Updates

### Getting Updates

When the solver is updated:

1. **Pull new version** from private repo:
   ```bash
   cd labyrinth-solver-wasm
   git pull origin main
   ```

2. **Rebuild**:
   ```bash
   maturin build --release
   ```

3. **Reinstall**:
   ```bash
   pip install --force-reinstall target/wheels/*.whl
   ```

4. **Notify students** if they pre-installed it

### Rollback

If a new version causes issues:

1. **Uninstall current**:
   ```bash
   pip uninstall labyrinth-solver-wasm
   ```

2. **Checkout old version**:
   ```bash
   git checkout <old-tag>
   maturin build --release
   pip install target/wheels/*.whl
   ```

### Version Management

Track versions in both repositories:

**labyrinth-solver-wasm/Cargo.toml:**
```toml
[package]
version = "1.0.0"
```

**labyrinth/docs/SOLVER_VERSION.md:**
```
# Solver Version

Requires: labyrinth-solver-wasm >= 1.0.0

Current: 1.0.0 (built 2024-01-15)
```

---

## Best Practices

1. **Build once, distribute widely** - Build locally once, then copy wheels to all environments.

2. **Test before distributing** - Run `pytest tests/` to verify solver works before giving to students.

3. **Version your builds** - Tag releases in labyrinth-solver-wasm so you can rollback if needed.

4. **Audit access** - Log who built/installed the solver and when (for compliance/investigation).

5. **Use separate Python environments** - Build in a clean venv to avoid version conflicts:
   ```bash
   python -m venv build-env
   source build-env/bin/activate
   pip install maturin
   maturin build --release
   ```

6. **Document your deployment** - Keep notes on how you deployed solver to your environment (helps troubleshoot later).

7. **Plan for offline** - Solver wheel works offline once installed. No internet needed at runtime.

8. **Platform consistency** - If students use Windows and you build on macOS, results may differ slightly due to floating-point precision. This is expected and minor.

---

## Support & Issues

If you encounter problems:

1. Check [BUILDING.md](../labyrinth-solver-wasm/BUILDING.md) in the solver repo
2. Check [DISTRIBUTION.md](../labyrinth-solver-wasm/DISTRIBUTION.md) for deployment guidance
3. Run the solver repo's test suite: `cargo test`
4. Ensure Python version matches wheel (e.g., cp313 = Python 3.13)

For bug reports or feature requests, contact the course administrator.

---

## FAQ

**Q: Can I give students the .whl file?**
A: Only if necessary (e.g., bring-your-own-device). Better to install on lab machines or use a package server that doesn't expose source.

**Q: What if students ask for the solver source?**
A: This is intentional. The educational goal is to implement A* themselves, not use our reference.

**Q: Do I need to rebuild every time I run evaluations?**
A: No. Build once, install once. Then use it for evaluations (unless you update the solver repo).

**Q: Can I modify the solver?**
A: You can in your local copy, but those changes won't affect installed wheels unless you rebuild and reinstall.

**Q: Is the solver faster than Python A*?**
A: Yes, ~2-5x faster due to Rust compilation and optimizations.

**Q: What if a student somehow gets the .whl and decompiles it?**
A: WASM is low-level bytecode, harder to decompile than Python. But don't assume it's impossible. This is a "security through obscurity" approach, not cryptographic protection.

---

**Remember:** The solver is part of the **teacher infrastructure**, not student-facing. Handle it accordingly.
