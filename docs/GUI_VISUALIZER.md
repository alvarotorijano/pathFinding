# GUI Maze Visualizer

La nueva visualización de laberintos ahora usa una interfaz gráfica moderna con **Tkinter**, proporcionando una experiencia mucho más interactiva y clara que la anterior visualización ASCII de terminal.

## Características

### Visualización del Laberinto
- **Renderizado gráfico** con celdas cuadradas de colores
- **Código de colores intuitivo:**
  - 🟢 **Verde**: Posición inicial (START)
  - 🟠 **Naranja**: Posición objetivo (GOAL)  
  - 🔴 **Rojo**: Posición actual del agente
  - 🔵 **Azul**: Camino recorrido por el agente
  - 🟣 **Púrpura**: Frontera explorada (opcional)
  - Gris oscuro: Paredes del laberinto

### Panel de Control
- **Pausa/Reanudación**: Pausar y reanudar la simulación en cualquier momento
- **Reset**: Reiniciar la visualización
- **Control de velocidad**: Deslizador para ajustar la velocidad de animación (0.1x - 5.0x)

### Panel de Información
Muestra métricas en tiempo real:
- Tamaño del laberinto
- Número de pasos actuales
- Costo acumulado del camino
- Estado actual (EN EJECUCIÓN, PAUSADO, DETENIDO)

## Uso

### Desde CLI

```bash
# Ejecutar agente con visualización GUI
python -m labyrinth run --agent random_agent --maze-file path/to/maze.maze --visualize

# Con control de velocidad base (1.0x = normal, 2.0 = 2x más rápido)
python -m labyrinth run --agent dfs_agent --width 20 --height 20 --visualize --speed 2.0
```

### Desde Python

```python
from utils.maze_core.generator import MazeGenerator, TopologyType, CostMapType
from utils.maze_core.simulator import Simulator
from agents.dfs_agent.agent import DFSAgent

# Generar laberinto
gen = MazeGenerator(20, 20, seed=42)
maze = gen.generate(topology=TopologyType.PERFECT)

# Crear agente
agent = DFSAgent()

# Ejecutar con visualización
simulator = Simulator(maze, agent, visualize=True, speed=2.0)
result = simulator.run()

print(f"Resuelto: {result.solved}")
print(f"Pasos: {result.steps}")
print(f"Costo: {result.path_cost}")
```

## Comportamiento

### Durante la Ejecución
- La GUI se actualiza en tiempo real conforme el agente se mueve
- El camino recorrido se marca en azul
- Los pasos y costos se actualizan en el panel de información
- Puedes pausar/reanudar en cualquier momento con el botón

### Al Terminar
- Cuando el agente resuelve el laberinto o alcanza el máximo de pasos, la GUI muestra el resultado final
- La ventana se cierra automáticamente después de **3 segundos**
- Los resultados de la simulación se imprimen en la consola

## Fallback en Modo Headless

Si se ejecuta en un entorno sin display gráfico (servidor, CI/CD):
- La inicialización de la GUI falla gracefully
- La simulación continúa normalmente sin visualización
- Se muestra un mensaje de advertencia indicando que no se pudo inicializar la GUI

Ejemplo:
```
Warning: Could not initialize GUI visualizer: no display available
Continuing without visualization...
```

## Requisitos

- Python 3.8+
- Tkinter (incluido en la mayoría de instalaciones de Python)
- En Linux, puede ser necesario instalar: `python3-tk` o similar

### Instalación de Tkinter (si es necesario)

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
Tkinter viene incluido con Python oficial

**Windows:**
Tkinter viene incluido con Python oficial

## Mejoras Respecto a la Versión ASCII

| Aspecto | ASCII Terminal | GUI Tkinter |
|--------|-----------------|-------------|
| Legibilidad | Caracteres ASCII limitados | Gráficos claros y colores |
| Interactividad | Solo lectura | Pausa, reset, control de velocidad |
| Tamaño de laberinto | Limitado por terminal (~20x20) | Escala hasta 100x100+ con zoom |
| Rendimiento | Lento en terminales | Fluido y responsivo |
| Información | Mínima | Métricas en tiempo real |
| Portabilidad | Funciona en cualquier terminal | Requiere display gráfico (con fallback) |
