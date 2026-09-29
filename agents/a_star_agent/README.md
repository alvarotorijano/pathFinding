# A* Agent (Estrella)

Agente que implementa el algoritmo de búsqueda informada **A*** (A-Star) para resolver laberintos.

## ¿Qué es A*?

A* es un algoritmo de búsqueda informada que combina:
- **g(n)**: Costo real desde el nodo inicial hasta el nodo actual
- **h(n)**: Heurística que estima el costo desde el nodo actual hasta el objetivo
- **f(n) = g(n) + h(n)**: Costo total estimado del camino completo

A* expande nodos de manera inteligente, eligiendo siempre el nodo con menor `f(n)`, 
lo que lo hace más eficiente que búsqueda no informada (BFS, DFS).

## Algoritmo A* - Paso a Paso

### Paso 1: Inicializar
```
- Mete el nodo inicial en la lista abierta (OPEN)
  - g(inicio) = 0
  - h(inicio) = heurística(inicio)
  - f(inicio) = 0 + h(inicio)
- La lista cerrada (CLOSED) empieza vacía
```

### Paso 2: Elegir el mejor candidato
```
- De OPEN, toma el nodo con menor f(n)
- Llámalo "actual"
- Si OPEN está vacía y no has encontrado el objetivo → NO HAY SOLUCIÓN
```

### Paso 3: Comprobar si es el objetivo
```
- Si actual == objetivo:
  - ¡ÉXITO! Has encontrado la solución
  - Reconstruye el camino siguiendo los padres hacia atrás hasta el inicio
  - Retorna el camino
```

### Paso 4: Cerrar el nodo
```
- Elimina "actual" de OPEN
- Añade "actual" a CLOSED
```

### Paso 5: Examinar vecinos
```
Para cada vecino de "actual":

  a) Si el vecino está en CLOSED:
     - Ignóralo (ya lo hemos explorado)

  b) Calcula el costo provisional:
     - g_provisional = g(actual) + coste(actual → vecino)
     
  c) Si el vecino NO está en OPEN:
     - Añádelo a OPEN
     - Guarda:
       - padre(vecino) = actual
       - g(vecino) = g_provisional
       - h(vecino) = heurística(vecino)
       - f(vecino) = g(vecino) + h(vecino)
     
  d) Si el vecino YA está en OPEN:
     - SI g_provisional < g(vecino):
       - Encontraste un camino mejor al vecino
       - Actualiza:
         - g(vecino) = g_provisional
         - f(vecino) = g(vecino) + h(vecino)
         - padre(vecino) = actual
     - SI g_provisional >= g(vecino):
       - No hagas nada (el camino anterior era mejor)
```

### Paso 6: Repetir
```
- Vuelve al Paso 2
```

### Sin Solución
```
- Si OPEN se queda vacía sin haber alcanzado el objetivo
- No existe camino desde inicio a objetivo
```

## Estructuras de Datos

### Nodo (Node)
```
class Node:
    posición (x, y)
    padre → referencia al nodo del que viene
    g → costo real acumulado desde inicio
    h → heurística estimada hasta objetivo
    f → f = g + h (lo que A* usa para elegir)
```

### Listas
- **OPEN**: Conjunto de nodos candidatos a explorar (cola de prioridad)
- **CLOSED**: Conjunto de nodos ya explorados

## Heurística

Para un laberinto, usamos **distancia Manhattan** (también llamada distancia de Manhattan):

```
h(n) = |x_actual - x_objetivo| + |y_actual - y_objetivo|
```

Esta heurística es **admisible** (nunca sobrestima), lo que garantiza que A* encuentra 
el camino óptimo.

### ¿Por qué Manhattan?
- En un laberinto, no puedes moverte en diagonal
- Manhattan es el costo mínimo teórico ignorando paredes
- Nunca sobrestima el costo real
- Garantiza optimalidad en A*

## Ejemplo Visual

```
Laberinto 5x5, S=inicio, G=objetivo, * = en exploración

Paso 1 - Inicializar:
┌─────────────────┐
│ S . . . .│      OPEN: [S(g=0, h=4, f=4)]
│ . │ . . .│      CLOSED: []
│ . . . │ .│
│ . . . . .│
│ . . . . G│
└─────────────────┘

Paso 2 - Elegir mejor (S tiene f=4, es el único):
actual = S
OPEN: [...]        (otros vecinos de S)
CLOSED: [S]

Paso 5 - Expandir vecinos de S:
- Arriba: fuera de límites (ignorar)
- Abajo: posición (0,1), g=1, h=manhattan((0,1)→G)=7, f=8 → añadir a OPEN
- Derecha: posición (1,0), g=1, h=manhattan((1,0)→G)=7, f=8 → añadir a OPEN
- Izquierda: fuera de límites (ignorar)

OPEN: [(0,1,f=8), (1,0,f=8), ...]
CLOSED: [S]

Paso 2 - Elegir mejor de OPEN: uno de los dos con f=8
...y así sucesivamente...
```

## Ventajas vs Desventajas

### ✓ Ventajas
- **Óptimo**: Encuentra el camino más corto (si h es admisible)
- **Completo**: Encuentra solución si existe
- **Eficiente**: Mucho más rápido que BFS/DFS gracias a la heurística
- **Flexible**: Funciona con cualquier heurística admisible

### ✗ Desventajas
- **Memoria**: Almacena todos los nodos en OPEN y CLOSED
- **Cálculo de heurística**: Cada nodo requiere calcular h(n)
- **Complejidad**: Más complejo de implementar que BFS

## Complejidad

- **Tiempo**: O(b^d) en el peor caso, pero mucho mejor en práctica
- **Espacio**: O(b^d) para almacenar nodos abiertos y cerrados
  - b = factor de ramificación (máximo 4 en un laberinto)
  - d = profundidad de la solución

Con una buena heurística, A* expande significativamente menos nodos que BFS.

## Implementación en el Proyecto

### Archivos
- `a_star_agent/agent.py`: Clase `AStarAgent`
- `a_star_agent/README.md`: Este documento

### Clase Principal
```python
class AStarAgent(Agent):
    """
    Agente que implementa A* para resolver laberintos.
    """
    def step(self, observation: Observation) -> Direction:
        """
        Determina el siguiente movimiento usando A*.
        """
        pass
```

### Métodos a Implementar
1. `__init__()`: Inicializar listas OPEN y CLOSED
2. `step()`: Implementar el loop principal de A*
3. `_calculate_heuristic()`: Distancia Manhattan
4. `_reconstruct_path()`: Reconstruir camino cuando se encuentra objetivo
5. Métodos auxiliares según sea necesario

## Referencias

- "Artificial Intelligence: A Modern Approach" - Russell & Norvig
- A* Search Algorithm - Demystified
- Pathfinding: A*

## Notas para Aprendizaje

1. **Entender la diferencia g, h, f**:
   - g = dinero gastado hasta ahora
   - h = dinero que estimamos gastar
   - f = dinero total estimado

2. **Por qué OPEN es una cola de prioridad**:
   - Siempre necesitas el nodo con menor f
   - Con lista normal sería O(n) cada vez
   - Con heap es O(log n)

3. **Por qué CLOSED es importante**:
   - Evita explorar el mismo nodo dos veces
   - Optimiza búsqueda

4. **Admisibilidad = Optimalidad**:
   - Si h nunca sobrestima → A* es óptimo
   - Si h sobrestima → A* no garantiza optimalidad
