# Project Prompts

This file saves all prompts and instructions given to Claude during project development.
Each entry is timestamped for reference.

---

## Prompt 1: Initial Project Vision & Requirements (2026-09-07)

### Language: Spanish

Ok, quiero hacer una herramienta para que los alumnos puedan hacer practicas de algoritmos de busqueda de rutas. Quiero primero poder generar laberintos procedimentalmente. Laberintos con una sola solucion, sin solucion, con varias soluciones, con un solo camino y una sola solucion, de diferentes tamaños etc. Hay alguna herramienta que haya ya esto en modo texto y me permita guardarlo en texto para que luego ellos puedan cargar este fichero y desde cada casilla puedan ver facilmente en que direccion ir.

(Conversation with ChatGPT exploring maze generation libraries and framework design)

### Key Decisions from Prompt 1:

1. **Maze generation:** Use existing library (recommended `mazelib`) for topology generation.
2. **Custom `.maze` format:** Create a standardized text format for portability.
3. **Student agents:** Receive maze, position, and goal; return next move.
4. **Framework responsibilities:** Generation, validation, simulation, visualization.
5. **Informed search focus:** BFS, DFS, Dijkstra, A*, Greedy Best-First.

---

## Prompt 2: Requirements Clarification & Scope (2026-09-07)

### Language: Spanish

Ok, lo de no darles o si el mapa completo es muy buena idea, quiero poder decidirlo desde la linea de comandos cuando ejecute el agente. Las competiciones están bien, el hecho de representar el laberinto como tuplas de 4 bits tambien es buena representacion, el resto de ideas de cometicion tambien están bien. Ahora quiero que añadas a los requisitos alguna forma de poder generar laberintos y que cuando un agente corra un laberito que se vea como va avanzando y como va descubriendo el laberitno, asi que es necesario que el agente muestre tambien cual es su horizonte, cuantos movimientos lleva y de alguna forma me gustaria poder saber cual es el mejor camino para resolverlo, por lo tanto las celdas del laberinto tienen que tener un coste tambien que por defecto sea 1 pero que puedan generarse tambien aleatoriamente como si fueran mapas de calor (para que haya zonas que sean mas dificiles o no. No tengo claro cual es la forma de poder tener un solucionador de rutas pero que los alumnos no puedan ver el codigo y aun así que lo puedan ejecutar en los 3 sistemas operativos (mac win y linux) y que pueda correrse en cualquier otra arquitectura.

Luego quiero poder combinar por la linea de comandos que laberinto quiero que se genere, si se le va a dar al agente o no el mapa completo y todas las variables que hemos mencionado antes.

### Key Decisions from Prompt 2:

1. **Visibility control:** CLI flag `--visibility` to choose full/partial map mode.
2. **Cell costs:** Every cell has numeric cost (default 1.0, can be random/heatmap).
3. **Reference solver:** Distributed as compiled binary or WASM, separate from student code.
4. **Visualization:** Show agent position, moves, frontier, discovered maze.
5. **CLI power:** Combine all parameters for flexible experimentation.

---

## Prompt 3: Project Scope Refinement & Educational Focus (2026-09-07)

### Language: Spanish

A ver, a mi como profesor lo que me interesa es hacer practicas de la busqueda informada y la no informada.

### Key Clarification:

Primary objective: **Teach uninformed vs. informed search algorithms**.

This refocuses the framework to:
- Make **full maze + known goal** the canonical problem.
- Use the same maze to compare different algorithms.
- Keep partial-map visibility as an **optional extension**.
- Demonstrate differences between:
  - **Uninformed:** BFS, DFS, UCS/Dijkstra, IDDFS
  - **Informed:** Greedy Best-First, A*

---

## Prompt 4: Final Architectural Decisions & Implementation Go-Ahead (2026-09-07)

### Language: Spanish

User provided final decisions on critical architectural questions:

1. **Reference Solver:** WebAssembly implementation in separate repository
2. **Partial Observability:** Implement full support in V1 (--visibility full/radius/local/line-of-sight)
3. **Maze Generation:** Use `mazelib` library + Python virtual environments
4. **Maze Format:** Basic metadata sufficient (SIZE, SEED, START, GOAL, TOPOLOGY, COSTS)
5. **CLI:** Unified CLI tool from the beginning (not separate scripts)
6. **Visualization:** Terminal-based ASCII visualization only
7. **Metrics:** Solved, Steps, Path Cost, Optimal Cost, Nodes Explored, Execution Time
8. **Example Agents:** BFS, DFS provided; students implement others (Dijkstra, Greedy, A*, etc.)

### Implementation Go-Ahead

User approved full implementation following all CLAUDE.md guidelines.

### Phase 1 Status: COMPLETE ✅ (2026-09-07)

**Completed:**
- ✅ Core data models: Direction, Position, Cell, Maze, Observation, AgentDebugState, MazeResult
- ✅ All 33 model tests passing
- ✅ Project structure setup: requirements.txt, config.json, .gitignore, README.md
- ✅ Test infrastructure: pytest, conftest.py, run_tests.py

**Next:** Phase 2 - Maze Generation & Validation

---

## Intent & Summary

**Prompt 1** establishes the complete specification for a maze-based search algorithm learning platform. The conversation explores maze generation, representation, visibility modes, and reference solutions.

**Prompt 2** clarifies the need for flexible CLI control, cell costs, reference solver hiding, and visualization of agent progress.

**Prompt 3** refocuses the scope on the core educational objective: comparing uninformed vs. informed search algorithms on the same problem instances.

**Prompt 4** finalizes architectural decisions and authorizes full implementation.

---

## Guidelines for Future Prompts

When adding new prompts to this file:
1. Include the timestamp (date)
2. Specify the language
3. Preserve the prompt verbatim
4. Add a brief "Intent" section describing what was requested
5. List any key architectural decisions or clarifications

This file serves as a historical record of project evolution and requirements changes, demonstrating how the project was built iteratively with human-AI collaboration.
