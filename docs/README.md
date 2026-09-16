# Maze Search Algorithms - Project Documentation

Welcome to the maze-based search algorithms learning platform. This directory contains all technical documentation and specifications for the project.

---

## Documentation Files

### Core Documentation

- **[CLAUDE.md](./CLAUDE.md)** — Project constraints, coding standards, and architectural guidelines
- **[prompts.md](./prompts.md)** — Historical record of all project requirements and decisions
- **[requirements.md](./requirements.md)** — Technical specifications and implementation requirements
- **[architecture.md](./architecture.md)** — System design, component relationships, and data flow

### Guides

- **[student_guide.md](./student_guide.md)** — Step-by-step walkthrough for students implementing their first agent
- **[maze_format.md](./maze_format.md)** — Specification of the `.maze` file format and examples
- **[api_reference.md](./api_reference.md)** — Complete API reference for agents and framework

### Implementation

- **[implementation_plan.md](./implementation_plan.md)** — Phased implementation strategy and checklist
- **[maze_generation.md](./maze_generation.md)** — Maze generation algorithms and configuration

---

## Quick Reference

### For Students

1. **First time?** Start with [student_guide.md](./student_guide.md)
2. **Implementing an agent?** Check [api_reference.md](./api_reference.md)
3. **Understanding maze files?** See [maze_format.md](./maze_format.md)

### For Developers

1. **Architecture overview:** [architecture.md](./architecture.md)
2. **Technical requirements:** [requirements.md](./requirements.md)
3. **Style and standards:** [CLAUDE.md](./CLAUDE.md)

---

## Project Overview

This is a framework for teaching **uninformed and informed search algorithms** through practical implementations. Students write agents that navigate randomly generated mazes using algorithms like:

**Uninformed Search**
- Depth-First Search (DFS)
- Breadth-First Search (BFS)
- Uniform Cost Search (Dijkstra)
- Iterative Deepening (IDDFS)

**Informed Search**
- Greedy Best-First Search
- A*

The framework provides:
- Procedural maze generation with configurable properties
- Visualization of agent progress and search frontier
- Evaluation metrics (path cost, nodes expanded, execution time)
- Comparison against optimal solutions

---

## Key Features

✅ Full map and partial visibility modes  
✅ Configurable cell costs (uniform, random, heatmap)  
✅ Reproducible maze generation with seeds  
✅ Real-time visualization and step-by-step replay  
✅ Automatic optimal solution calculation  
✅ Cross-platform support (Windows, macOS, Linux)  
✅ No external dependencies (offline-first)

---

## File Organization

```
labyrinth/
├── agents/              # Student agent implementations
│   ├── bfs_agent/
│   ├── dfs_agent/
│   └── ...
├── mazes/               # Generated and example mazes
│   ├── examples/
│   └── generated/
├── utils/               # Framework tools and utilities
│   ├── maze_generator/
│   ├── maze_runner/
│   ├── maze_visualizer/
│   └── ...
├── tests/               # Test suite
│   ├── test_maze.py
│   ├── test_agents.py
│   └── ...
├── docs/                # This directory
│   ├── CLAUDE.md
│   ├── prompts.md
│   ├── requirements.md
│   ├── architecture.md
│   └── ...
├── CLAUDE.md            # Project constraints (root level)
├── README.md            # Main project README
├── config.json          # Configuration file
└── requirements.txt     # Python dependencies
```

---

## Next Steps

1. **Read:** [requirements.md](./requirements.md) for full technical specification
2. **Understand:** [architecture.md](./architecture.md) for system design
3. **Implement:** Follow [implementation_plan.md](./implementation_plan.md)
4. **Learn:** Students start with [student_guide.md](./student_guide.md)
