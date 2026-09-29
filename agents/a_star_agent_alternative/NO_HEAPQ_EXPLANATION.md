# A* Sin heapq - Explicación y Trade-offs

## ¿Qué cambió?

Eliminamos la importación de `heapq` y ahora usamos **listas simples de Python**.

### Antes (con heapq):
```python
import heapq

open_set = []
heapq.heappush(open_set, (f_score, contador, posición))
f_min, _, pos = heapq.heappop(open_set)
```

### Después (sin heapq):
```python
open_set = []

# Añadir nodo
open_set.append((f_score, posición))

# Extraer nodo con menor f
f_min, pos = min(open_set, key=lambda x: x[0])
open_set.remove((f_min, pos))
```

## Estructura de datos simplificada

### OPEN (lista de tuplas)
```python
open_set = [
    (8.0, Position(0,0)),   # (f_score, posición)
    (7.5, Position(1,0)),
    (7.5, Position(0,1)),
    (9.2, Position(2,0)),
]

# Antes: heap (árbol)
# Ahora: lista simple (secuencia)
```

## Cómo extraer el mejor nodo (Paso 2)

### Opción 1: Buscar mínimo (recomendado para este ejercicio)

```python
def extract_best_from_open():
    """Extraer el nodo con menor f de OPEN."""
    
    # Encontrar el nodo con menor f
    best_node = min(self.open_set, key=lambda x: x[0])
    f_best, pos_best = best_node
    
    # Eliminarlo de OPEN
    self.open_set.remove(best_node)
    
    return f_best, pos_best
```

**Complejidad:**
- `min()`: O(n) - escanea toda la lista
- `remove()`: O(n) - búsqueda + eliminación
- **Total: O(n) por iteración**

### Opción 2: Mantener lista ordenada (alternativa)

```python
def add_to_open_sorted(f_score, position):
    """Mantener OPEN ordenada por f."""
    
    # Encontrar posición correcta
    for i, (f, pos) in enumerate(self.open_set):
        if f_score < f:
            self.open_set.insert(i, (f_score, position))
            return
    
    # Si llegamos aquí, va al final
    self.open_set.append((f_score, position))

def extract_best_from_open():
    """El primero siempre es el mejor."""
    return self.open_set.pop(0)  # O(n) por el desplazamiento
```

**Complejidad:**
- `insert()`: O(n) - desplaza elementos
- `pop(0)`: O(n) - desplaza elementos
- **Total: O(n) por iteración**

## Comparación: heapq vs Lista Simple

```
Operación        | heapq    | Lista simple
─────────────────────────────────────────
Insertar nodo    | O(log n) | O(n)
Extraer mínimo   | O(log n) | O(n)
Buscar mínimo    | O(1)     | O(n)
─────────────────────────────────────────
Por iteración    | O(log n) | O(n)
Laberinto 10x10  | ~100 ops | ~1000 ops ⚠️
Laberinto 100x100| ~10k ops | ~100k ops ⚠️
```

## ¿Por qué es más lento?

En cada iteración de A*, hacemos:

1. **Buscar el nodo con menor f**: O(n)
2. **Eliminarlo de la lista**: O(n)
3. **Examinar sus vecinos** y añadirlos: O(n)

Con heapq:
- Insertar: O(log n)
- Extraer: O(log n)
- **Mucho más rápido**

Con lista simple:
- Insertar: O(1) (solo append)
- Extraer: O(n) (buscar + eliminar)
- **Más lento pero más simple**

## Cuándo es aceptable la lista simple

✓ **Laberintos pequeños** (< 20x20)
  - 400 celdas máximo
  - La diferencia es imperceptible

✓ **Fines educativos**
  - Entender el algoritmo sin abstracciones
  - Sin dependencias externas
  - Código más legible

✗ **Laberintos grandes** (> 50x50)
  - 2500+ celdas
  - Notablemente más lento

✗ **Producción**
  - Usar heapq siempre
  - Las diferencias de complejidad importan

## Implementación en el código actual

### En `_initialize_search()`:

```python
# Paso 1: Añadir nodo inicial a OPEN
# (usando lista simple, solo append)
self.open_set.append((f_start, start))
```

### En `_search_step()` (que implementaremos en Paso 2):

```python
# Paso 2: Elegir el mejor candidato
if not self.open_set:
    return None  # No hay solución

# Encontrar el nodo con menor f
best = min(self.open_set, key=lambda x: x[0])
f_current, current = best
self.open_set.remove(best)
```

### En el loop de vecinos (Paso 5):

```python
# Paso 5b: Añadir vecino a OPEN si es nuevo
self.open_set.append((f_new, neighbor))

# Paso 5d: Si ya está y hay mejor camino, actualizar
# (aquí necesitamos buscar y actualizar)
```

## El problema con actualizar nodos

Con heapq, si encuentras un camino mejor a un nodo existente, simplemente lo añades de nuevo. El heap automáticamente ignora versiones antiguas.

Con una lista simple, necesitas **eliminar la versión anterior**:

```python
# Encontrar y eliminar el nodo anterior
for i, (f_old, pos) in enumerate(self.open_set):
    if pos == neighbor:
        self.open_set.pop(i)  # Eliminar versión vieja
        break

# Añadir la versión nueva
self.open_set.append((f_new, neighbor))
```

## Próximos pasos

Para la implementación sin heapq:

1. ✅ **Paso 1**: Inicializar (ya hecho)
2. **Paso 2**: Elegir mejor candidato
   - Usar `min()` para encontrar
   - Usar `remove()` para eliminar

3. **Paso 3**: Comprobar si es objetivo
   - Straightforward

4. **Paso 4**: Cerrar nodo
   - Añadir a closed_set

5. **Paso 5**: Examinar vecinos
   - El tricky: buscar y actualizar nodos existentes

6. **Paso 6**: Reconstruir camino

## Conclusión

La lista simple **es más lenta pero más educativa**:
- ✓ Sin librerías externas
- ✓ Algoritmo completamente visible
- ✓ Fácil de debuggear
- ✗ O(n) en lugar de O(log n)

**Es perfecta para aprender**, pero en producción siempre usa heapq.
