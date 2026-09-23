# A* Agent - Student Assignment

AMIA - MUIAAp - Tema 2: Busqueda informada.

**Classification:** Informed Search
**Algorithm:** A* (A-star)
**Expected Performance:** Optimal, and much faster than uninformed search (BFS/DFS)

## Description

This is the agent you must implement. `agent.py` contains the class skeleton,
the constructor, the path-following logic and an already-implemented Manhattan
distance heuristic. The core A* search loop, marked with `YOUR CODE GOES HERE`
inside `_search()`, is left for you to complete.

## Algorithm

A* expands the frontier node with the lowest `f(n) = g(n) + h(n)`:

- `g(n)`: real accumulated cost from the start to node `n`.
- `h(n)`: estimated cost from `n` to the goal (here, Manhattan distance).

Since the agent receives the full maze in `observation.maze`, the search only
needs to run once per maze (see `step()`): the first call computes the full
optimal path with `_search()`, and every subsequent call just follows it.

**Properties:**
- **Complete:** finds a solution if one exists.
- **Optimal:** yes, as long as the heuristic is admissible (never overestimates
  the real remaining cost).
- **Memory:** O(b^d), keeps the frontier and the explored set in memory.
- **Time:** O(b^d) in the worst case, but in practice far fewer nodes than
  uninformed search thanks to the heuristic.

## Key Methods

- `step(observation)` — returns the next `Direction`, running `_search()` once
  per maze and then following the cached path.
- `_search(observation)` — **implement this**: runs A* and stores the result
  in `self.path`.
- `_heuristic(position, goal)` — already implemented: Manhattan distance.
- `debug_state()` — returns frontier/explored cells for `--visualize`.

## Usage Example

```bash
python -m labyrinth run --agent a_star_agent --maze-file maze.maze --visualize --speed 5
```

## When to Use

- Whenever an admissible heuristic to the goal is available and an optimal
  solution is needed with fewer expansions than BFS/Dijkstra.
- To compare against `random_agent` and `dfs_agent` on the same mazes.

## See Also

- [random_agent](../random_agent/) — baseline agent.
- [dfs_agent](../dfs_agent/) — uninformed search example with the same
  state-persistence pattern (`step()` called once per move, state kept
  between calls).
