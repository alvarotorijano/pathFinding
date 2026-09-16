# Maze Storage

This directory stores `.maze` files - maze definitions in a standard portable format.

## Directory Structure

- **examples/** - Example mazes for learning and testing
  - `tiny_perfect.maze` - 5×5 perfect maze (single solution)
  - `small_perfect.maze` - 10×10 perfect maze
  - `small_multiple.maze` - 10×10 maze with multiple solutions

## Usage

### Running an agent on a stored maze

```bash
python -m labyrinth run --agent my_agent --maze-file mazes/examples/small_perfect.maze --visualize
```

### Saving a generated maze

```bash
# Generate and save
python -m labyrinth generate \
  --width 20 --height 20 --type perfect \
  --seed 42 --output mazes/my_custom_maze.maze

# Then run your agent on it
python -m labyrinth run \
  --agent my_agent \
  --maze-file mazes/my_custom_maze.maze \
  --visualize
```

### Maze File Format

Each `.maze` file contains:
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

The format is text-based and portable across all platforms/languages.

## Workflow for Students

1. **Choose a test maze** from `examples/`
2. **Develop your agent** in `agents/your_agent/agent.py`
3. **Test on mazes of increasing difficulty:**
   - Start with `tiny_perfect.maze` (5×5)
   - Progress to `small_perfect.maze` (10×10)
   - Try `small_multiple.maze` (10×10 with multiple paths)
4. **Generate custom mazes** as needed with `python -m labyrinth generate`
5. **Save working mazes** in this directory for regression testing
