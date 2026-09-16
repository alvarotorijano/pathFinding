# Implementation Plan - Maze Search Algorithms Framework

**Status:** Ready to Begin  
**Date:** 2026-09-07  
**Scope:** Full V1 Implementation

---

## Overview

This document outlines the phased implementation of the complete maze search algorithms framework, following all CLAUDE.md guidelines and architectural decisions from Prompt 4.

---

## Phase 1: Core Data Model & Infrastructure

### 1.1 Project Setup
- [ ] Create `requirements.txt` with dependencies (mazelib, pytest, etc.)
- [ ] Create `.gitignore` for virtual environments, caches, outputs
- [ ] Create `config.json` with default configuration
- [ ] Setup folder structure (agents/, mazes/, utils/, tests/)
- [ ] Create `README.md` with quick start guide

**Files to create:**
- `requirements.txt`
- `.gitignore`
- `config.json`
- `README.md`

### 1.2 Core Data Structures
- [ ] `utils/maze_core/` directory with core classes
- [ ] `Position` class (x, y coordinates)
- [ ] `Direction` enum (NORTH, SOUTH, EAST, WEST)
- [ ] `Cell` class (walls as 4-bit, cost as float)
- [ ] `Maze` class (grid, start, goal, metadata)
- [ ] `Observation` class (what agent receives each step)
- [ ] `AgentDebugState` class (frontier, explored, discovered, current_path)
- [ ] `MazeResult` class (solved, steps, cost, optimal_cost, explored, time, trace)

**Files to create:**
- `utils/maze_core/__init__.py`
- `utils/maze_core/models.py` (all classes)
- `utils/maze_core/README.md`

**Tests:**
- `tests/test_models.py` (instantiation, properties)

---

## Phase 2: Maze Generation & Validation

### 2.1 Maze Generator
- [ ] `MazeGenerator` class wrapping mazelib
- [ ] Support topology types: perfect, multiple, unsolvable, corridor, open
- [ ] Support cost maps: uniform, random, heatmap
- [ ] Seed-based reproducibility
- [ ] Start/goal position selection
- [ ] Solution count validation

**Files to create:**
- `utils/maze_core/generator.py`
  - `MazeGenerator` class
  - `TopologyType` enum
  - `CostMapType` enum
  - Helper functions for cost generation

### 2.2 Maze Validator
- [ ] Validate connectivity (start reachable to goal)
- [ ] Count actual solutions
- [ ] Detect dead ends, loops
- [ ] Cost validation (all positive)

**Files to create:**
- `utils/maze_core/validator.py`
  - `MazeValidator` class with validation methods

### 2.3 CLI: `maze generate` command
- [ ] Argument parsing (width, height, type, solutions, cost-map, cost-range, seed, output)
- [ ] Error handling and validation
- [ ] Output maze file and metadata

**Files to create:**
- `utils/maze_generator/run_generator.py` (main CLI script)
- `utils/maze_generator/README.md`

**Tests:**
- `tests/test_generator.py` (generation, reproducibility, validation)

---

## Phase 3: Maze Format (`.maze`)

### 3.1 Maze File Format
- [ ] Design `.maze` text format specification
- [ ] Include: metadata, topology, costs
- [ ] Version/schema info for future compatibility

### 3.2 Maze Parser & Serializer
- [ ] `MazeFormat` class with load/save methods
- [ ] Error handling for corrupted files
- [ ] Version compatibility

**Files to create:**
- `utils/maze_core/formats.py`
  - `MazeFormat` class
  - Load/save logic

**Tests:**
- `tests/test_formats.py` (parse, serialize, round-trip)

---

## Phase 4: Reference Solver (A*)

### 4.1 Reference Solver Implementation
- [ ] A* algorithm implementation
- [ ] Heuristic: Manhattan distance
- [ ] Returns: path, cost, nodes_expanded
- [ ] Internal only, never exposed to agents

**Files to create:**
- `utils/maze_core/solver.py`
  - `ReferenceSolver` class (internal use only)
  - A* implementation

**Tests:**
- `tests/test_solver.py` (correctness on sample mazes)

---

## Phase 5: Simulator & Environment

### 5.1 Simulator
- [ ] Load maze from file or generator
- [ ] Initialize agent
- [ ] Step loop: call agent.step(observation) → validate → update position → record metrics
- [ ] Handle invalid moves (agent tries to go through wall)
- [ ] Track execution trace (JSON-serializable)
- [ ] Termination: reached goal or max steps

**Files to create:**
- `utils/maze_core/simulator.py`
  - `Simulator` class with step/run methods
  - Execution trace recording

### 5.2 Metrics Calculation
- [ ] Calculate: solved, steps, cost, optimal_cost, nodes_expanded, execution_time
- [ ] Cost ratio, optimality percentage
- [ ] Mark invalid moves

**Files to create:**
- `utils/maze_core/metrics.py`
  - `MetricsCalculator` class

**Tests:**
- `tests/test_simulator.py` (step validation, metrics)

---

## Phase 6: Agent Base Class & Interface

### 6.1 Agent Base Class
- [ ] Abstract `Agent` class
- [ ] Required: `__init__`, `step(observation)` → Direction
- [ ] Optional: `debug_state()` → AgentDebugState
- [ ] Persistent state between steps

**Files to create:**
- `utils/maze_core/agent.py`
  - `Agent` abstract base class
  - `AgentDebugState` dataclass

### 6.2 Agent Discovery
- [ ] Scan `agents/` folder for agent implementations
- [ ] Load agents dynamically by class name
- [ ] List available agents

**Files to create:**
- `utils/maze_core/agent_loader.py`
  - `AgentLoader` class

**Tests:**
- `tests/test_agent.py` (agent loading, interface)

---

## Phase 7: Example Agents

### 7.1 BFS Agent
- [ ] Implement BFS algorithm
- [ ] Maintain queue, visited set
- [ ] Implement debug_state (frontier, explored, current_path)

### 7.2 DFS Agent
- [ ] Implement DFS algorithm
- [ ] Maintain stack, visited set
- [ ] Implement debug_state

**Files to create:**
- `agents/bfs_agent/agent.py`
- `agents/bfs_agent/README.md`
- `agents/dfs_agent/agent.py`
- `agents/dfs_agent/README.md`

**Tests:**
- `tests/test_example_agents.py` (correctness on known mazes)

---

## Phase 8: Visualizer

### 8.1 Terminal Visualizer
- [ ] Real-time visualization during agent execution
- [ ] Display:
  - Maze with walls (█), visited (·), frontier (○), current position (A), goal (G)
  - For partial observability: show unknown (?), discovered (·)
  - Legend and current metrics
- [ ] Adjustable speed (--speed flag)
- [ ] Color-coded output (walls, path, frontier, etc.)

**Files to create:**
- `utils/maze_core/visualizer.py`
  - `TerminalVisualizer` class
  - Maze rendering methods

### 8.2 Replay from Trace
- [ ] Load JSON execution trace
- [ ] Replay step-by-step
- [ ] Pause, resume, speed control

**Files to create:**
- `utils/maze_visualizer/run_replay.py`
- `utils/maze_visualizer/README.md`

**Tests:**
- `tests/test_visualizer.py` (rendering correctness)

---

## Phase 9: CLI - Unified Interface

### 9.1 Main CLI Entry Point
- [ ] Create `maze` command (or `python -m labyrinth`)
- [ ] Subcommands: generate, run, benchmark, list

### 9.2 `maze generate` (refine from Phase 2)
- [ ] All topology and cost options
- [ ] Example: `maze generate --width 20 --height 20 --type perfect --seed 42 --output maze.maze`

### 9.3 `maze run` (main agent execution)
- [ ] Load maze (file or generate inline)
- [ ] Load agent
- [ ] Run simulator
- [ ] Visualize (real-time or dump JSON)
- [ ] Print results
- [ ] Example: `maze run --maze maze.maze --agent bfs_agent --visualize --speed 10`

### 9.4 `maze benchmark`
- [ ] Run multiple agents on multiple mazes
- [ ] Output CSV with comparative results
- [ ] Example: `maze benchmark --directory ./mazes --agents bfs_agent,dfs_agent --output results.csv`

### 9.5 `maze list`
- [ ] List available agents
- [ ] List available mazes
- [ ] Example: `maze list --agents`, `maze list --mazes`

### 9.6 `maze replay`
- [ ] Replay execution trace
- [ ] Example: `maze replay result.json --visualize`

**Files to create:**
- `labyrinth/__init__.py` (package marker)
- `labyrinth/__main__.py` (CLI entry point)
- `labyrinth/cli/` directory
  - `__init__.py`
  - `commands.py` (command implementations)
  - `runner.py` (main CLI dispatcher)

**Tests:**
- `tests/test_cli.py` (argument parsing, error handling)

---

## Phase 10: Full Integration & Testing

### 10.1 End-to-End Tests
- [ ] Generate maze → run agent → validate results → metrics
- [ ] Multiple agent types on same maze
- [ ] Reproducibility (seed-based)

### 10.2 Configuration System
- [ ] Load defaults from `config.json`
- [ ] Override via CLI arguments
- [ ] Documentation of all options

**Files to create:**
- `utils/maze_core/config.py`
  - `Config` class with defaults

**Tests:**
- `tests/test_integration.py` (E2E scenarios)
- `tests/test_config.py` (config loading)

### 10.3 Test Runner Convenience
- [ ] `tests/run_tests.py` to execute full test suite with pytest

**Files to create:**
- `tests/run_tests.py`
- `tests/conftest.py` (pytest fixtures)

---

## Phase 11: Documentation

### 11.1 API Reference
- [ ] Document Agent class interface
- [ ] Document Maze format
- [ ] Document CLI commands and options

**Files to create:**
- `docs/api_reference.md`
- `docs/maze_format.md`

### 11.2 Student Guide
- [ ] Step-by-step for implementing first agent
- [ ] Code templates
- [ ] Common algorithms (BFS, DFS, Dijkstra, A* examples)
- [ ] Debugging tips

**Files to create:**
- `docs/student_guide.md`

### 11.3 Examples
- [ ] Example mazes (trivial, perfect, multiple, unsolvable)
- [ ] Example agents (BFS, DFS)

**Files to create:**
- `mazes/examples/trivial_5x5.maze`
- `mazes/examples/perfect_20x20.maze`
- `mazes/examples/multiple_20x20.maze`
- `mazes/examples/unsolvable_10x10.maze`

### 11.4 Update Root README
- [ ] Quick start
- [ ] Installation
- [ ] Usage examples
- [ ] Project structure

---

## Phase 12: Polish & Optimization

### 12.1 Performance
- [ ] Profile simulator
- [ ] Optimize pathfinding in reference solver
- [ ] Optimize visualization rendering

### 12.2 Error Messages
- [ ] User-friendly error messages (using colors from CLAUDE.md)
- [ ] Helpful hints for common mistakes

### 12.3 Code Quality
- [ ] Type hints throughout
- [ ] Docstring review
- [ ] Code style check (PEP 8)

---

## Optional Extensions (Future)

- [ ] Partial observability modes (radius, line-of-sight, local)
- [ ] Additional cost map types (Perlin noise, predefined patterns)
- [ ] Agent timeout handling
- [ ] Memory usage tracking
- [ ] Web-based visualizer
- [ ] Statistics and analysis tools
- [ ] Difficulty ratings for mazes
- [ ] Tournament mode (round-robin)

---

## Implementation Order Summary

```
Phase 1: Core Models
    ↓
Phase 2: Generation & Validation
    ↓
Phase 3: Maze Format
    ↓
Phase 4: Reference Solver
    ↓
Phase 5: Simulator
    ↓
Phase 6: Agent Interface
    ↓
Phase 7: Example Agents
    ↓
Phase 8: Visualizer
    ↓
Phase 9: CLI (unified)
    ↓
Phase 10: Integration & Testing
    ↓
Phase 11: Documentation
    ↓
Phase 12: Polish
```

Each phase builds on previous ones. No major dependencies between phases, but recommended order above.

---

## Estimated Task Count

- **Code files:** ~35
- **Test files:** ~15
- **Documentation files:** ~8
- **Data files (example mazes):** ~4
- **Configuration files:** ~3

**Total:** ~65 files

---

## Definition of Done (V1)

✅ All 12 phases complete  
✅ All tests passing  
✅ CLI works end-to-end  
✅ Example agents (BFS, DFS) complete and tested  
✅ Documentation complete and accurate  
✅ Students can run: `maze run --maze maze.maze --agent bfs_agent --visualize`  
✅ No hard-coded paths (all relative)  
✅ All code in English  
✅ Every function has docstring  
