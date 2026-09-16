"""ASCII maze visualizer for terminal display."""

import time
from .models import Maze, Position, Direction


class MazeVisualizer:
    """Render maze and agent position in ASCII terminal."""

    # Symbols
    WALL_H = "─"      # Horizontal wall
    WALL_V = "│"      # Vertical wall
    CORNER = "┼"      # Corner
    CORNER_TL = "┌"   # Top-left
    CORNER_TR = "┐"   # Top-right
    CORNER_BL = "└"   # Bottom-left
    CORNER_BR = "┘"   # Bottom-right
    WALL_T = "┬"      # T-junction top
    WALL_B = "┴"      # T-junction bottom
    WALL_L = "├"      # T-junction left
    WALL_R = "┤"      # T-junction right
    PASSAGE = " "     # Open passage
    AGENT = "●"       # Agent position
    START = "S"       # Start position
    GOAL = "G"        # Goal position
    PATH = "·"        # Path taken

    def __init__(self, maze: Maze, show_path: bool = True):
        """
        Initialize visualizer.

        Parameters:
            maze: Maze to visualize
            show_path: Whether to show path taken by agent
        """
        self.maze = maze
        self.show_path = show_path
        self.path_taken = set()

    def render(self, agent_pos: Position = None) -> str:
        """
        Render maze as ASCII string.

        Parameters:
            agent_pos: Current agent position (if any)

        Returns:
            ASCII representation of maze
        """
        lines = []

        # Top border
        lines.append(self._render_top_border())

        # Rows
        for y in range(self.maze.height):
            # Row with cells
            lines.append(self._render_row(y, agent_pos))

            # Bottom walls
            if y < self.maze.height - 1:
                lines.append(self._render_wall_row(y))

        # Bottom border
        lines.append(self._render_bottom_border())

        return "\n".join(lines)

    def _render_top_border(self) -> str:
        """Render top border."""
        result = self.CORNER_TL
        for x in range(self.maze.width):
            result += self.WALL_H * 2
            if x < self.maze.width - 1:
                result += self.WALL_T
            else:
                result += self.CORNER_TR
        return result

    def _render_bottom_border(self) -> str:
        """Render bottom border."""
        result = self.CORNER_BL
        for x in range(self.maze.width):
            result += self.WALL_H * 2
            if x < self.maze.width - 1:
                result += self.WALL_B
            else:
                result += self.CORNER_BR
        return result

    def _render_row(self, y: int, agent_pos: Position) -> str:
        """Render one row of cells."""
        result = self.WALL_V

        for x in range(self.maze.width):
            pos = Position(x, y)
            cell = self.maze.get_cell(pos)

            # Determine symbol
            if agent_pos and pos == agent_pos:
                symbol = self.AGENT
            elif pos == self.maze.start:
                symbol = self.START
            elif pos == self.maze.goal:
                symbol = self.GOAL
            elif self.show_path and pos in self.path_taken:
                symbol = self.PATH
            else:
                symbol = self.PASSAGE

            result += symbol

            # Right wall
            if cell.has_wall(Direction.EAST):
                result += self.WALL_V
            else:
                result += self.PASSAGE

        result += self.WALL_V
        return result

    def _render_wall_row(self, y: int) -> str:
        """Render walls between rows."""
        result = self.WALL_L

        for x in range(self.maze.width):
            pos = Position(x, y)
            cell = self.maze.get_cell(pos)

            # Bottom wall
            if cell.has_wall(Direction.SOUTH):
                result += self.WALL_H * 2
            else:
                result += self.PASSAGE * 2

            # Corner
            if x < self.maze.width - 1:
                result += self.CORNER
            else:
                result += self.WALL_R

        return result

    def show(self, agent_pos: Position = None, speed: float = 1.0):
        """
        Display maze in terminal with optional delay.

        Parameters:
            agent_pos: Current agent position
            speed: Animation speed multiplier (higher = faster)
        """
        output = self.render(agent_pos)
        print(output)

        if speed > 0:
            time.sleep(1.0 / speed)

    def record_step(self, pos: Position):
        """Record that agent visited this position."""
        if self.show_path:
            self.path_taken.add(pos)

    def clear_screen(self):
        """Clear terminal screen."""
        print("\033[2J\033[H", end="")
