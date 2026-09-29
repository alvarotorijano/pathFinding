# Guía de Aprendizaje: Implementación de A*

Esta guía te ayuda a entender y implementar A* paso a paso.

## Conceptos Clave

### 1. Las Tres Variables Principales

```python
g(n)  # Costo real desde START hasta n
h(n)  # Heurística: estimación desde n hasta GOAL
f(n)  # f(n) = g(n) + h(n), lo que A* usa para decidir
```

**Analogía:**
- Imagina que estás en una ciudad y quieres llegar a otro lugar
- g(n) = cuánto dinero ya gastaste en transporte
- h(n) = cuánto dinero estimado te falta gastar
- f(n) = dinero total estimado del viaje completo

A* siempre expande el nodo con menor f(n).

### 2. Estructuras de Datos

```python
# Cola de prioridad (heap) para elegir siempre el menor f
open_set = []  # [( f_score, contador, posición ), ...]
heapq.heappush(open_set, (f, counter, pos))
f_min, _, pos = heapq.heappop(open_set)

# Conjunto para marcar explorados
closed_set = set()  # {Position, Position, ...}

# Diccionarios para rastrear costos y padres
g_score = {}      # {Position: float, ...}
parent = {}       # {Position: Position, ...}
```

**¿Por qué heap en lugar de lista?**
- Lista: buscar mínimo es O(n) → lento
- Heap: buscar mínimo es O(log n) → rápido
- Python: `heapq` implementa min-heap

### 3. La Heurística: Distancia Manhattan

```python
def manhattan_distance(from_pos, to_pos):
    """
    Distancia Manhattan = |Δx| + |Δy|
    
    Ejemplo en laberinto 5x5:
    pos = (1, 2), goal = (4, 3)
    h = |1-4| + |2-3| = 3 + 1 = 4
    
    ¿Por qué funciona en laberintos?
    - No puedes ir en diagonal
    - 4 movimientos cardinales (N, S, E, W)
    - Manhattan es mínimo teórico sin paredes
    - Nunca sobrestima → heurística admisible
    """
    dx = abs(from_pos.x - to_pos.x)
    dy = abs(from_pos.y - to_pos.y)
    return dx + dy
```

### 4. Inicialización

```python
def initialize(start, goal):
    """
    Paso 1 del algoritmo
    """
    # Limpiar todo
    open_set.clear()
    closed_set.clear()
    g_score.clear()
    parent.clear()
    
    # Calcular heurística del inicio
    h_start = manhattan_distance(start, goal)
    f_start = 0 + h_start  # g(start) siempre es 0
    
    # Añadir inicio a OPEN
    counter = 0  # Para romper empates
    heapq.heappush(open_set, (f_start, counter, start))
    
    # Inicializar diccionarios
    g_score[start] = 0.0
    parent[start] = None
```

### 5. El Loop Principal

```python
def search(maze, goal):
    """
    Pasos 2-6 del algoritmo
    """
    iteration = 0
    
    while open_set:  # Mientras haya nodos por explorar
        iteration += 1
        
        # Paso 2: Elegir mejor candidato
        f_current, _, current = heapq.heappop(open_set)
        print(f"Iteración {iteration}: expandiendo {current} con f={f_current}")
        
        # Paso 3: Comprobar si es el objetivo
        if current == goal:
            print(f"¡Objetivo encontrado en iteración {iteration}!")
            return reconstruct_path(start, goal)
        
        # Paso 4: Cerrarlo
        closed_set.add(current)
        
        # Paso 5: Examinar vecinos
        for neighbor in get_neighbors(maze, current):
            # 5a) Si está en CLOSED, ignóralo
            if neighbor in closed_set:
                continue
            
            # 5b) Calcular costo provisional
            g_current = g_score[current]
            neighbor_cell = maze.get_cell(neighbor)
            g_provisional = g_current + neighbor_cell.cost
            
            # 5c) Si no está en OPEN, añádelo
            if neighbor not in g_score:
                g_score[neighbor] = g_provisional
                h_neighbor = manhattan_distance(neighbor, goal)
                f_neighbor = g_provisional + h_neighbor
                parent[neighbor] = current
                
                counter += 1
                heapq.heappush(open_set, (f_neighbor, counter, neighbor))
                print(f"  → Nuevo nodo: {neighbor}, g={g_provisional}, h={h_neighbor}, f={f_neighbor}")
            
            # 5d) Si ya está pero con mejor costo, actualizar
            elif g_provisional < g_score[neighbor]:
                g_score[neighbor] = g_provisional
                h_neighbor = manhattan_distance(neighbor, goal)
                f_neighbor = g_provisional + h_neighbor
                parent[neighbor] = current
                
                counter += 1
                heapq.heappush(open_set, (f_neighbor, counter, neighbor))
                print(f"  → Mejor camino a {neighbor}: g={g_provisional}, f={f_neighbor}")
    
    # Sin solución
    print("No existe camino hacia el objetivo")
    return None
```

## Ejemplo Paso a Paso

```
Laberinto 3x3:
┌───────────┐
│ S . . │   │ S = Start (0,0)
│ . │ . . .│ G = Goal (2,2)
│ . . . . G│
└───────────┘

Inicialización:
━━━━━━━━━━━━━━━━━━━━━
open_set = [(4, 0, (0,0))]  # f=0+4=4
closed_set = {}
g_score = {(0,0): 0}
parent = {(0,0): None}

─────────────────────────

Iteración 1: Pop (4, 0, (0,0))
Vecinos de (0,0): [(1,0), (0,1)]
  (1,0): g_prov=1, h=3, f=4 → añadir
  (0,1): g_prov=1, h=3, f=4 → añadir
open_set = [(4, 1, (1,0)), (4, 2, (0,1))]
closed_set = {(0,0)}

─────────────────────────

Iteración 2: Pop (4, 1, (1,0))  # Desempate por contador
Vecinos de (1,0): [(2,0), (0,0), (1,1)]
  (2,0): g_prov=2, h=2, f=4 → añadir
  (0,0): en closed_set → ignorar
  (1,1): pared → no vecino
open_set = [(4, 2, (0,1)), (4, 3, (2,0))]
closed_set = {(0,0), (1,0)}

─────────────────────────

... (continuar hasta encontrar G)

Iteración N: Pop (..., (2,2))  # Es el objetivo
¡Éxito! Reconstruir camino:
(2,2) ← parent → (2,1) ← (1,1) ← (1,0) ← (0,0)
Camino: [(0,0), (1,0), (2,0), (2,1), (2,2)]
```

## Trampas Comunes

### ❌ Trampa 1: Olvidar el contador en el heap

```python
# MAL: dos elementos con mismo f pueden causar error
heapq.heappush(open_set, (f, position))  # ← error: Position no es comparable

# BIEN: usar contador como segunda clave
heapq.heappush(open_set, (f, counter, position))
counter += 1
```

### ❌ Trampa 2: No actualizar nodos en OPEN

```python
# MAL: si encuentras mejor camino, solo actualizar g_score
g_score[neighbor] = g_provisional  # ← Pero el heap tiene el valor viejo!

# BIEN: cuando actualizas, vuelve a añadir a heap
g_score[neighbor] = g_provisional
heapq.heappush(open_set, (new_f, counter, neighbor))
counter += 1
# El nodo viejo se ignorará (lazy deletion)
```

### ❌ Trampa 3: Heurística que sobrestima

```python
# MAL: distancia euclidiana en laberinto
h = sqrt((x-goal_x)**2 + (y-goal_y)**2)  # ← Puede ser menor que Manhattan

# BIEN: Manhattan nunca sobrestima en laberintos
h = abs(x - goal_x) + abs(y - goal_y)
```

### ❌ Trampa 4: Reconstruir camino incorrectamente

```python
# MAL: seguir padres adelante
path = [start]
while path[-1] != goal:
    next_pos = parent[path[-1]]  # ← Error, parent apunta hacia atrás

# BIEN: seguir padres hacia atrás, luego invertir
path = []
current = goal
while current is not None:
    path.append(current)
    current = parent[current]
path.reverse()  # Ahora: start → ... → goal
```

## Checklist de Implementación

- [ ] Inicializar open_set, closed_set, g_score, parent
- [ ] Implementar heurística (Manhattan)
- [ ] Implementar loop principal con condición de salida
- [ ] Marcar nodos como visitados (closed_set)
- [ ] Calcular g provisional para vecinos
- [ ] Añadir nuevos nodos a open_set
- [ ] Actualizar nodos con mejor costo
- [ ] Detectar cuando se alcanza el objetivo
- [ ] Reconstruir camino correctamente
- [ ] Convertir posiciones a Directions
- [ ] Manejar lista vacía (sin solución)
- [ ] Integrar con Agent.step() para hacer un paso a la vez

## Debugging

### Imprimir estado en cada iteración

```python
print(f"OPEN size: {len(open_set)}")
print(f"CLOSED size: {len(closed_set)}")
print(f"Current node: {current}, f={f_current}")
print(f"g_score[current]: {g_score[current]}")
```

### Verificar que f nunca disminuye

```python
prev_f = float('inf')
# En cada iteración:
f_current, _, current = heapq.heappop(open_set)
assert f_current >= prev_f  # Debe ser monotónico
prev_f = f_current
```

### Verificar admisibilidad de heurística

```python
for pos in maze:
    h = manhattan_distance(pos, goal)
    true_cost = bfs_to_goal(pos, goal)
    assert h <= true_cost  # h nunca debe sobrestimar
```
