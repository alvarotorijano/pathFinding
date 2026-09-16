# Reference Solver - NOTICE

⚠️ **The reference solver source code is NOT in this repository.**

## What Happened

The `solver.py` file that was previously here has been **removed intentionally**.

## Why

The reference solver is a **black box for fair evaluation**:

- Students should NOT see how optimal solutions are calculated
- Implementation is hidden to prevent cheating
- Everyone is evaluated against the same reference

## Where It Actually Is

The real reference solver is located in a **private repository**:

```
labyrinth-solver-wasm (PRIVATE)
├── src/lib.rs         (A* algorithm in Rust)
├── Cargo.toml         (Build config)
└── (compiled to WASM)
```

**Access:** Instructors only 🔒

## How It Works

When you run an agent:

1. Your agent solves the maze
2. Framework internally calls the WASM solver
3. Optimal solution is calculated (privately)
4. Your solution is compared to optimal
5. Metrics are displayed

**You see:** Only the results (optimality %)  
**You don't see:** How it calculates the result

## What This Means

✅ **You can:**
- View optimality metrics
- Compare your solution to optimal
- Improve your algorithm based on feedback

❌ **You cannot:**
- See the solver source code
- Copy the optimal algorithm
- Modify the reference implementation

---

**Bottom line:** The solver is intentionally hidden infrastructure. Your job is to implement YOUR OWN search algorithms and get as close to optimal as possible.

See [../docs/reference_solver.md](../docs/reference_solver.md) for more details.
