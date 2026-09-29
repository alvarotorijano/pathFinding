"""A* (A-Star) pathfinding agent for maze solving."""

import heapq
from typing import Dict, Tuple, Set, Optional, List

from utils.maze_core.agent import Agent
from utils.maze_core.models import Observation, Direction, Position


class AStarAgent(Agent):
    """
    Agent that implements the A* algorithm to find optimal paths in mazes.

    A* combines actual cost (g) and heuristic estimate (h) to efficiently
    find the shortest path: f(n) = g(n) + h(n)
    """

    def __init__(self):
        """
        Initialize A* agent.

        Sets up data structures for the A* algorithm:
        - open_set: Priority queue of nodes to explore
        - closed_set: Set of nodes already explored
        - g_score: Actual cost from start to each node
        - parent: Tracks path for reconstruction
        """
        self.open_set: List[Tuple[float, int, Position]] = []
        self.closed_set: Set[Position] = set()
        self.g_score: Dict[Position, float] = {}
        self.parent: Dict[Position, Optional[Position]] = {}
        self.path: List[Direction] = []
        self.path_index: int = 0
        self.start_pos: Optional[Position] = None
        self.goal_pos: Optional[Position] = None
        self.counter: int = 0

    def step(self, observation: Observation) -> Direction:
        """
        Execute one step of the A* algorithm.

        On first call, initializes the algorithm with start position.

        Parameters:
            observation: Current maze state and agent position

        Returns:
            Direction: Next movement direction (NORTH, SOUTH, EAST, WEST)
        """
        # PASO 1: Detectar primera llamada e inicializar
        if self.start_pos is None:
            # Es la primera vez que se llama a step()
            # Inicializar todas las estructuras de A*
            self._initialize_search(observation.current, observation.goal)

        # TODO: Implementar PASO 2-6 del algoritmo A*
        # Por ahora solo retornamos una dirección cualquiera
        return Direction.NORTH

    def _initialize_search(self, start: Position, goal: Position) -> None:
        """
        Initialize A* search structures.

        PASO 1: Inicializar
        Prepara todas las estructuras de datos para comenzar la búsqueda A*.

        Parameters:
            start: Starting position
            goal: Goal position
        """
        # 1. Limpiar estructuras de búsquedas anteriores
        self.open_set.clear()
        self.closed_set.clear()
        self.g_score.clear()
        self.parent.clear()

        # 2. Limpiar camino y índice de búsquedas anteriores
        self.path.clear()
        self.path_index = 0

        # 3. Guardar posiciones de referencia
        self.start_pos = start
        self.goal_pos = goal

        # 4. Calcular valores del nodo inicial
        # h(inicio) = heurística desde inicio al objetivo
        h_start = self._heuristic(start, goal)

        # g(inicio) siempre es 0 (estamos en el inicio)
        g_start = 0.0

        # f(inicio) = g(inicio) + h(inicio)
        f_start = g_start + h_start

        # 5. Añadir nodo inicial a OPEN
        # OPEN es una lista de tuplas (f_score, posición)
        self.open_set.append((f_start, start))

        # 6. Guardar costos reales en g_score
        # g_score[posición] = costo real desde inicio
        self.g_score[start] = g_start

        # 7. Guardar relación padre-hijo en parent
        # parent[posición] = posición_padre (None para el inicio)
        self.parent[start] = None

    def _search_step(self, maze: 'Maze', goal: Position) -> Optional[List[Direction]]:
        """
        Execute one iteration of the A* main loop.

        Implements steps 2-6 of the algorithm:
        - PASO 2: Pick best node from OPEN (minimum f)
        - PASO 3: Check if it's the goal
        - PASO 4: Move it to CLOSED
        - PASO 5: Expand neighbors
        - PASO 6: Return None to continue

        Parameters:
            maze: The maze to search
            goal: Goal position

        Returns:
            Path as list of Directions if goal found, None if still searching
        """
        # PASO 2: Elegir el mejor candidato
        # ¿Hay nodos en OPEN?
        if not self.open_set:
            # OPEN está vacía: sin solución
            return None

        # Encontrar el nodo con menor f
        # OPEN es una lista de tuplas (f, Position)
        best_node = min(self.open_set, key=lambda x: x[0])
        f_current, current_pos = best_node

        # Sacarlo de OPEN
        self.open_set.remove(best_node)

        # PASO 3: ¿Es el objetivo?
        if current_pos == goal:
            # ¡Encontramos la solución!
            # Reconstruir el camino desde inicio hasta objetivo
            path = self._reconstruct_path(self.start_pos, current_pos)
            return path

        # PASO 4: Cerrar el nodo
        # Mover el nodo actual de OPEN a CLOSED
        # (ya lo sacamos de OPEN en PASO 2)
        # Ahora marcarlo como explorado
        self.closed_set.add(current_pos)

        # PASO 5: Examinar vecinos
        # TODO: Expandir y actualizar costos

        # PASO 6: Continuar búsqueda
        return None

    def _heuristic(self, position: Position, goal: Position) -> float:
        """
        Calculate heuristic estimate from position to goal.

        Uses Manhattan distance (also called taxicab distance):
        h(n) = |x_n - x_goal| + |y_n - y_goal|

        This is admissible: never overestimates actual cost.

        Parameters:
            position: Current position
            goal: Goal position

        Returns:
            Estimated cost to reach goal from position
        """
        # Distancia Manhattan: suma de diferencias absolutas en x e y
        dx = abs(position.x - goal.x)
        dy = abs(position.y - goal.y)
        return float(dx + dy)

    def _get_neighbors(self, maze: 'Maze', position: Position) -> List[Position]:
        """
        Get valid neighboring positions in the maze.

        Checks all four cardinal directions (N, S, E, W) and returns
        only positions that don't have walls between them.

        Parameters:
            maze: The maze
            position: Current position

        Returns:
            List of valid neighboring positions
        """
        # TODO: Implement neighbor discovery
        # 1. Try all four directions: NORTH, SOUTH, EAST, WEST
        # 2. For each direction, check maze.can_move_to(position, direction)
        # 3. If valid, add position.move(direction) to list
        # 4. Return list of valid neighbors
        pass

    def _reconstruct_path(self, start: Position, goal: Position) -> List[Direction]:
        """
        Reconstruct path from goal to start using parent pointers.

        Follows parent chain backwards from goal to start, then
        reverses to get path from start to goal. Converts positions
        to Direction movements.

        Parameters:
            start: Starting position
            goal: Goal position (current position)

        Returns:
            List of Directions representing the path
        """
        # Paso 1: Construir cadena de posiciones hacia atrás
        # Empezar desde el objetivo y seguir los padres hasta el inicio
        position_chain = []
        current = goal

        while current is not None:
            position_chain.append(current)
            current = self.parent[current]

        # Paso 2: Invertir la cadena para ir de inicio a objetivo
        # Ahora: start → ... → goal
        position_chain.reverse()

        # Paso 3: Convertir posiciones consecutivas a Directions
        directions = []
        for i in range(len(position_chain) - 1):
            from_pos = position_chain[i]
            to_pos = position_chain[i + 1]
            direction = self._position_to_direction(from_pos, to_pos)
            directions.append(direction)

        # Paso 4: Retornar como lista de Directions
        return directions

    def _position_to_direction(self, from_pos: Position, to_pos: Position) -> Direction:
        """
        Convert movement between two positions to a Direction.

        Determines which direction the movement goes by comparing coordinates.

        Parameters:
            from_pos: Starting position
            to_pos: Target position

        Returns:
            Direction of movement (NORTH, SOUTH, EAST, WEST)
        """
        # Calcular diferencias de coordenadas
        dx = to_pos.x - from_pos.x
        dy = to_pos.y - from_pos.y

        # Convertir a Direction basado en el movimiento
        # dy < 0 significa mover hacia arriba (NORTH)
        if dy < 0:
            return Direction.NORTH
        # dy > 0 significa mover hacia abajo (SOUTH)
        elif dy > 0:
            return Direction.SOUTH
        # dx > 0 significa mover hacia la derecha (EAST)
        elif dx > 0:
            return Direction.EAST
        # dx < 0 significa mover hacia la izquierda (WEST)
        elif dx < 0:
            return Direction.WEST

        # No debería llegar aquí (las posiciones son idénticas)
        return Direction.NORTH

    def debug_state(self) -> Dict[str, any]:
        """
        Return debug information about agent's internal state.

        Returns:
            Dictionary with metrics for visualization/analysis
        """
        # TODO: Implement debug state
        # Return dict with:
        # - open_size: len(open_set)
        # - closed_size: len(closed_set)
        # - path_length: len(path)
        # - path_index: current position in path
        pass
