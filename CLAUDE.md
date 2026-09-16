# Project Instructions & Constraints

This document captures the durable rules and constraints for the Maze Search Algorithms
course project. These rules override any default behavior and must be followed exactly.

## File Paths

- **Never commit or reference absolute/local machine paths** in any project file.
- **Always use relative paths** from the project root.
- Example ✅: `./agents/my_agent/agent.py`, `docs/README.md`, `mazes/generated/maze_001.maze`
- Example ❌: `/home/user/projects/labyrinth/utils/...` or `C:\Users\...\labyrinth\...`
- This ensures the project is portable and works on any machine/environment.

## Code & Documentation Language

- **All code** (function names, variables, imports, comments, docstrings, log output, CLI messages)
  must be written in **English**.
- Documentation that is historical (e.g., `docs/original_prompt.md`) may remain in its original language
  for archival purposes.

## Git Operations

- **Claude must never perform git write operations** in this repository.
  - No `git add`, `git commit`, `git push`, or any other commands that modify git state.
  - The user retains all responsibility for git operations and repository management.
  - This is a hard constraint, even if it would be convenient for the workflow.

## Code Quality

- **Every function and method must have a docstring.**
  - Docstrings should explain the purpose, parameters, return value, and any notable behavior.
  - Keep docstrings concise; prefer clarity over verbosity.
- **Implementation approach:**
  - Always create an implementation plan and get user approval before writing code.
  - Don't add features or abstractions beyond what the specification requires.
  - Avoid unnecessary error handling, fallbacks, or validation for impossible scenarios.

## Architecture & Structure

- **Run locally only.** No external services or cloud dependencies.
- **Agent isolation:** Each agent is a separate module/file, allowing students to add their own
  without modifying core code.
- **Maze format:** Standardized `.maze` text format for portability and reproducibility.
- **Configuration externalization:** Generation parameters and maze properties are defined in
  `config.json` and loaded at runtime, not hard-coded.
- **Reference solver:** Kept separate from student code (distributed as compiled binary/WASM).

## Core Concepts & Semantics

### Maze Representation

- **Topology:** Each cell's walls are represented as 4-bit values (North, East, South, West).
  - `1` = wall exists / passage open in that direction
  - `0` = wall does not exist / passage blocked
  - Example: `0101` means North blocked, East open, South blocked, West open.

- **Costs:** Each cell has a numeric cost (default 1.0, must be positive).
  - Cost represents the "difficulty" of moving into that cell.
  - Moving from cell A to cell B costs `cost(B)`.

### Maze Generation

- **Topology generation:** Determines maze connectivity (perfect, multiple solutions, unsolvable, etc.).
- **Cost map generation:** Independently determines cell costs (uniform, random, heatmap).
- **Seed:** Every generated maze must use a reproducible seed for consistency.

### Visibility/Observability

- **Full map:** Agent receives the complete maze topology and costs.
  - Suitable for classical search (BFS, DFS, Dijkstra, A*, Greedy).
  - Default case for standard practices.

- **Partial map:** Agent receives only discovered/visible cells.
  - Future extension for online search practices.
  - Controlled via CLI `--visibility` flag.

### Reference Solver

- The reference solver is **NOT part of the student API** and is completely hidden from students.
- It is executed independently by the framework to calculate optimal solutions (A* algorithm).
- Students never see solver code or have direct access to `solve()` or `optimal_path()` methods.
- **Implementation:** Private WASM (WebAssembly) repository ([labyrinth-solver-wasm](../labyrinth-solver-wasm))
- **Access:** Private - source code and binaries not available to students
- Students see only the **results**: optimal cost and optimality metrics for comparison

## Testing & Verification

- All functionality must have corresponding tests in the `tests/` folder.
- Tests must use pytest.
- A `tests/run_tests.py` convenience wrapper should exist to run the full test suite.
- Tests should verify:
  - Maze generation and validation (connectivity, solution count, topology).
  - Agent execution (valid moves, path finding, state persistence).
  - Reference solver calculations (optimal cost, path length).
  - CLI argument parsing and configuration loading.
  - Maze file format (generation, loading, serialization).

## Style Guidelines

### Python Code Style

- **Naming:** Use `snake_case` for functions and variables, `PascalCase` for classes.
- **Imports:** Organize as: stdlib → third-party → local imports (one blank line between groups).
- **Line length:** Prefer under 100 characters; break long lines for readability.
- **Type hints:** Use type annotations for function signatures (e.g., `def step(...) -> Direction:`).
- **Comments:** Avoid obvious comments. Comment *why*, not *what*.
  - ✅ `# Heatmap smoothing ensures realistic terrain clustering`
  - ❌ `# Generate a heatmap`

### Docstring Format

Every function must have a docstring. Use this format:

```python
def function_name(param1: Type, param2: Type) -> ReturnType:
    """
    Brief description of what the function does.
    
    Parameters:
        param1: Description of param1.
        param2: Description of param2.
    
    Returns:
        Description of return value.
    """
```

Keep docstrings **concise and complete**. One or two sentences for the description; list parameters and returns even if brief.

### Folder & File Organization

- **One agent per folder:** `agents/<agent_name>/agent.py` (lowercase, underscore-separated).
- **Utilities per folder:** `utils/<tool_name>/run_<tool_name>.py` + `README.md`.
  - Example: `utils/maze_generator/run_generator.py`
- **Tests mirror structure:** `tests/test_<component>.py` for each major component.
- **Maze files:** `mazes/` directory for storing `.maze` files (generated and manual).
- **No deeply nested folders:** Maximum 3 levels (e.g., `utils/maze_generator/generators/perfect.py` is ok; `utils/a/b/c/d` is not).

### CLI Scripts

- Use `argparse` for command-line argument parsing.
- Provide `--help` with clear usage examples.
- Exit with status code 0 on success, 1 on error.
- Print results to stdout; errors to stderr.
- Support flexible maze specifications:
  - Generated: `--maze generated --width 50 --height 50 --type perfect --seed 123`
  - Loaded from file: `--maze path/to/file.maze`

### Terminal Output & Color Codes

All CLI scripts must use ANSI color codes for terminal output to improve readability and guide users:

**Define color constants at the top of each script:**
```python
RED = "\033[91m"      # Errors and critical issues
GREEN = "\033[92m"    # Success messages and positive information
YELLOW = "\033[93m"   # Warnings and important information (paths, etc.)
WHITE = "\033[97m"    # Neutral information and details
RESET = "\033[0m"     # Reset to default terminal color
```

**Usage Guidelines:**
- **Red (Errors):** `f"{RED}Error: {message}{RESET}"` for errors and failures
- **Green (Success):** `f"{GREEN}Agent solved the maze!{RESET}"` for positive outcomes
- **Yellow (Warnings):** `f"{YELLOW}Generated maze at: {path}{RESET}"` for important paths/info
- **White (Info):** `f"{WHITE}   - agent_name{RESET}"` for listing details
- Always include `{RESET}` at the end of colored sections to avoid color bleed

**Examples:**
```python
# Error message
print(f"{RED}Error: Maze file not found.{RESET}", file=sys.stderr)

# Success message
print(f"{GREEN}Tournament complete! Results saved.{RESET}")

# Warning with path info
print(f"{YELLOW}Maze generated: {maze_path}{RESET}")

# Neutral details
print(f"{WHITE}   - bfs_agent{RESET}")
```

Never use emojis (❌, ✅, 📍, etc.) in terminal output — use colors instead.

### CSV Output & File Formats

- Use CSV format (comma-separated, quoted strings for safety).
- Include headers (column names as first row).
- One row per logical unit (one row per agent result, one row per maze property).
- Ensure consistency: same column order, same column types across all rows.

### `.maze` File Format

- Text-based, human-readable format for portability.
- Includes metadata (size, seed, start, goal, topology, costs).
- Can be generated or manually created.
- Can be version-controlled in git.

Structure:
```
SIZE <width> <height>
SEED <seed_value>
START <x> <y>
GOAL <x> <y>

TOPOLOGY
<4-bit walls per cell>

COSTS
<numeric cost per cell>
```

### Error Handling

- **Do not silence errors.** Let exceptions propagate or log them explicitly.
- **Do not validate impossible scenarios.** Trust framework contracts and types.
- **Validate only at boundaries:** CLI inputs, file I/O, user-provided data.
- **Use assertions for internal invariants:** `assert 0 < cost <= 1000`.

## Documentation Standards

### File Structure
- Every major component has a `README.md` explaining its purpose and usage.
- Each script has example CLI invocations in its README.
- Technical docs are in `docs/`; prose is user-facing.

### Content Quality
- **Accuracy:** Docs must match the code. Update docs when code changes.
- **Completeness:** Explain *what*, *why*, and *how*.
- **Clarity:** Use plain language. Define jargon (e.g., "frontier: the set of states a search algorithm is considering next").
- **Examples:** Provide realistic examples in every README and guide.

### Relative References
- Always use relative paths in documentation: `./agents/bfs_agent/agent.py`, `mazes/generated/example.maze`.
- Do not reference absolute machine paths (e.g., no `C:\Users\...`).

## Workflow & Versioning

### Implementation Phases
1. **Planning:** Create detailed plan, document requirements, get approval.
2. **Implementation:** Write code (core library → maze generation → visualization → agents → tools → tests).
3. **Testing:** Run full test suite; verify manually with example mazes.
4. **Documentation:** Finalize README/docstring; ensure accuracy.

### Prompt Tracking
- All user prompts are saved in `docs/prompts.md` (verbatim).
- Each new prompt is added with timestamp and language.
- Prompts form the historical record of requirements.

### Avoiding Drift
- Docstrings describe *why*, not *what* the code does.
- Comments explain non-obvious logic or constraints.
- No comments needed for self-explanatory code (good naming + clear structure = self-documenting).

## Project Assumptions

- Students have basic Python knowledge but may not understand maze generation or search algorithms in depth.
- Students will submit agents with various code styles and quality levels; the system must handle them robustly.
- The instructor may adjust maze parameters and cost ranges; all such values go in `config.json`.
- No internet or external services are available during execution (everything is local).
- The reference solver should run fast enough for real-time visualization and benchmarks.
- Students should not be able to trivially access the reference solver or optimal solution during development.

## Search Algorithm Focus

The framework is primarily designed to teach:

**Uninformed Search**
- Depth-First Search (DFS)
- Breadth-First Search (BFS)
- Uniform Cost Search (Dijkstra)
- Iterative Deepening (IDDFS)

**Informed Search**
- Greedy Best-First Search
- A*

Students implement their agent's `step(observation)` method and maintain internal state to implement these algorithms. The framework provides:
- The maze and agent state
- Metrics for evaluation (path cost, nodes expanded, execution time)
- Visualization of the search frontier
- Comparison against optimal solution
