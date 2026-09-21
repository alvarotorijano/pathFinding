"""GUI maze visualizer using Tkinter."""

import tkinter as tk
from tkinter import ttk
import time
from .models import Maze, Position, Direction


class MazeGUIVisualizer:
    """Interactive GUI visualizer for maze solving using Tkinter."""

    # Colors
    COLOR_WALL = "#2c3e50"
    COLOR_PASSAGE = "#ecf0f1"
    COLOR_AGENT = "#e74c3c"
    COLOR_START = "#2ecc71"
    COLOR_GOAL = "#f39c12"
    COLOR_PATH = "#3498db"
    COLOR_FRONTIER = "#9b59b6"

    def __init__(self, maze: Maze, show_path: bool = True):
        """
        Initialize GUI visualizer.

        Parameters:
            maze: Maze to visualize
            show_path: Whether to show path taken by agent
        """
        self.maze = maze
        self.show_path = show_path
        self.path_taken = set()
        self.frontier = set()

        # GUI state
        self.running = False
        self.paused = False
        self.speed_multiplier = 1.0
        self.current_agent_pos = None
        self.step_count = 0
        self.path_cost = 0.0
        self.root = None
        self.canvas = None
        self.info_text = None
        self.play_button = None
        self.speed_label = None

        try:
            # Create window
            self.root = tk.Tk()
            self.root.title("Maze Solver Visualizer")
            self.root.geometry("1200x800")

            self._setup_ui()
            self.running = True
        except Exception as e:
            print(f"Warning: Could not initialize GUI visualizer: {e}")
            print("Continuing without visualization...")
            self.running = False

    def _setup_ui(self):
        """Set up the GUI components."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left side: Canvas for maze
        canvas_frame = ttk.LabelFrame(main_frame, text="Maze")
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.canvas = tk.Canvas(
            canvas_frame,
            bg=self.COLOR_PASSAGE,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Right side: Controls and info
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))

        # Control buttons
        controls_frame = ttk.LabelFrame(right_frame, text="Controls")
        controls_frame.pack(fill=tk.X, pady=(0, 10))

        self.play_button = ttk.Button(
            controls_frame,
            text="Pause",
            command=self._toggle_pause
        )
        self.play_button.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(
            controls_frame,
            text="Reset",
            command=self._reset
        ).pack(side=tk.LEFT, padx=5, pady=5)

        # Speed control
        speed_frame = ttk.LabelFrame(right_frame, text="Speed")
        speed_frame.pack(fill=tk.X, pady=(0, 10))

        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(
            speed_frame,
            from_=0.1,
            to=5.0,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            command=self._update_speed
        )
        speed_scale.pack(fill=tk.X, padx=5, pady=5)

        self.speed_label = ttk.Label(speed_frame, text="1.0x")
        self.speed_label.pack(padx=5, pady=(0, 5))

        # Info panel
        info_frame = ttk.LabelFrame(right_frame, text="Information")
        info_frame.pack(fill=tk.BOTH, expand=True)

        self.info_text = tk.Text(
            info_frame,
            height=20,
            width=30,
            state=tk.DISABLED,
            bg="#f8f9fa"
        )
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Initial draw
        self._draw_maze()

    def _draw_maze(self):
        """Draw the maze on the canvas."""
        if not self.running or self.canvas is None:
            return

        self.canvas.delete("all")

        # Calculate cell size based on canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, self._draw_maze)
            return

        cell_size_x = (canvas_width - 20) / self.maze.width
        cell_size_y = (canvas_height - 20) / self.maze.height

        self.cell_size = min(cell_size_x, cell_size_y)
        offset_x = 10
        offset_y = 10

        # Draw cells and walls
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                pos = Position(x, y)
                cell = self.maze.get_cell(pos)

                # Calculate cell coordinates
                x1 = offset_x + x * self.cell_size
                y1 = offset_y + y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Determine cell color
                if self.current_agent_pos and pos == self.current_agent_pos:
                    color = self.COLOR_AGENT
                elif pos == self.maze.start:
                    color = self.COLOR_START
                elif pos == self.maze.goal:
                    color = self.COLOR_GOAL
                elif self.show_path and pos in self.path_taken:
                    color = self.COLOR_PATH
                elif pos in self.frontier:
                    color = self.COLOR_FRONTIER
                else:
                    color = self.COLOR_PASSAGE

                # Draw cell
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="#bdc3c7",
                    width=1
                )

                # Draw walls
                if cell.has_wall(Direction.NORTH):
                    self.canvas.create_line(x1, y1, x2, y1, fill=self.COLOR_WALL, width=2)
                if cell.has_wall(Direction.SOUTH):
                    self.canvas.create_line(x1, y2, x2, y2, fill=self.COLOR_WALL, width=2)
                if cell.has_wall(Direction.WEST):
                    self.canvas.create_line(x1, y1, x1, y2, fill=self.COLOR_WALL, width=2)
                if cell.has_wall(Direction.EAST):
                    self.canvas.create_line(x2, y1, x2, y2, fill=self.COLOR_WALL, width=2)

    def _update_info(self):
        """Update information panel."""
        if not self.running or self.info_text is None:
            return

        info = f"""Maze Size: {self.maze.width}x{self.maze.height}

Step: {self.step_count}
Path Cost: {self.path_cost:.1f}

Status: {'PAUSED' if self.paused else 'RUNNING' if self.running else 'STOPPED'}

Legend:
  START (S)
  GOAL (G)
  AGENT (*)
  PATH (.)
  FRONTIER (#)
"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info)
        self.info_text.config(state=tk.DISABLED)

    def _toggle_pause(self):
        """Toggle pause state."""
        self.paused = not self.paused
        self.play_button.config(text="Resume" if self.paused else "Pause")

    def _reset(self):
        """Reset visualization."""
        self.path_taken.clear()
        self.frontier.clear()
        self.current_agent_pos = None
        self.step_count = 0
        self.path_cost = 0.0
        self._draw_maze()
        self._update_info()

    def _update_speed(self, value):
        """Update speed multiplier."""
        self.speed_multiplier = float(value)
        self.speed_label.config(text=f"{self.speed_multiplier:.1f}x")

    def show(self, agent_pos: Position = None, speed: float = 1.0):
        """
        Display maze and optionally update agent position.

        Parameters:
            agent_pos: Current agent position
            speed: Animation speed multiplier (higher = faster)
        """
        if not self.running or self.root is None:
            return

        self.current_agent_pos = agent_pos
        self._draw_maze()
        self._update_info()

        try:
            self.root.update()
        except Exception:
            return

        # Wait based on speed (account for manual speed control)
        effective_speed = speed * self.speed_multiplier
        if effective_speed > 0:
            wait_time = (1.0 / effective_speed) * 1000  # Convert to milliseconds
            # Break wait into small chunks to keep UI responsive
            for _ in range(int(wait_time / 50)):
                if not self.running:
                    break
                while self.paused and self.running:
                    time.sleep(0.1)
                    try:
                        self.root.update()
                    except Exception:
                        break
                time.sleep(0.05)

    def record_step(self, pos: Position):
        """Record that agent visited this position."""
        if self.show_path:
            self.path_taken.add(pos)

    def record_frontier(self, positions: set):
        """Record frontier positions for visualization."""
        self.frontier = positions.copy()

    def update_metrics(self, step_count: int, path_cost: float):
        """Update step and cost metrics."""
        self.step_count = step_count
        self.path_cost = path_cost

    def close(self, delay_ms: int = 3000):
        """
        Close the visualization window after a delay.

        Parameters:
            delay_ms: Milliseconds to wait before closing (default 3 seconds)
        """
        self.running = False
        if self.root is not None:
            try:
                self.root.after(delay_ms, self._do_close)
            except Exception:
                pass

    def _do_close(self):
        """Actually close the window."""
        if self.root is not None:
            try:
                self.root.quit()
            except Exception:
                pass

    def run_event_loop(self):
        """Run the Tkinter event loop (blocking)."""
        if self.root is None:
            return
        try:
            self.root.mainloop()
        except Exception:
            pass
        finally:
            self.running = False
