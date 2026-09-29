# Detección de Primera Llamada en A*

## El problema

El método `step()` se llama **muchas veces** durante una partida:
- Llamada 1: Debe inicializar todo
- Llamada 2-100: Solo debe continuar la búsqueda

¿Cómo sabemos si es la primera?

## La solución: Usar una bandera

### En `__init__()`:

```python
def __init__(self):
    self.start_pos: Optional[Position] = None  # ← BANDERA
    self.goal_pos: Optional[Position] = None
    # ... resto de inicialización
```

**Inicialmente**: `self.start_pos == None` (no hemos buscado nada)

### En `step()`:

```python
def step(self, observation: Observation) -> Direction:
    # Detectar primera llamada
    if self.start_pos is None:
        # Primera vez: inicializar
        self._initialize_search(observation.current, observation.goal)
        # Después de esto, self.start_pos ya NO es None
    
    # Siguientes llamadas: self.start_pos != None, así que se salta
    # ...continuar búsqueda...
```

---

## Diagrama de flujo

```
┌─────────────────────────────────────────────┐
│  step() es llamado por el Simulator        │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ ¿start_pos is None?  │
        └──────────┬───────┬───┘
                   │       │
                 SÍ│       │NO
                   │       │
        ┌──────────▼────┐  │
        │ PRIMERA LLAMADA   │
        │ Ejecutar:         │  ┌──────────────────────────┐
        │ _initialize_  │  │  │ LLAMADAS POSTERIORES      │
        │ search()      │  │  │ - path ya está calculado  │
        │              │  │  │ - Solo retornar next dir  │
        │ Resultado:    │  │  └──────────────────────────┘
        │ - OPEN tiene  │  │
        │   nodo inicio │  │
        │ - g_score     │  │
        │   inicializado│  │
        │ - parent set  │  │
        │ - start_pos   │  │
        │   != None     │  │
        └──────────┬────┘  │
                   │       │
                   └───┬───┘
                       │
                       ▼
        ┌─────────────────────────────┐
        │ Continuar búsqueda          │
        │ (Pasos 2-6 de A*)           │
        └─────────────────────────────┘
```

---

## Ejemplo en tiempo real

### Partida: Laberinto 5x5, START=(0,0), GOAL=(4,4)

```
LLAMADA 1 (Simulator.run() iteración 1):
┌─────────────────────────────────────┐
│ step(observation)                   │
│   - observation.current = (0,0)     │
│   - observation.goal = (4,4)        │
│                                     │
│ if self.start_pos is None:          │
│   ✓ TRUE (es None)                  │
│                                     │
│ Ejecutar: _initialize_search(...)   │
│   - self.start_pos = Position(0,0)  │
│   - self.goal_pos = Position(4,4)   │
│   - OPEN = [(8.0, Position(0,0))]   │
│   - g_score = {(0,0): 0.0}          │
│   - parent = {(0,0): None}          │
│                                     │
│ Retornar: Direction.NORTH (primera │
│           dirección del camino)     │
└─────────────────────────────────────┘

ESTADO DESPUÉS:
  self.start_pos = Position(0,0)  ← Ya NO es None


LLAMADA 2 (Simulator.run() iteración 2):
┌─────────────────────────────────────┐
│ step(observation)                   │
│   - observation.current = (0,1)     │
│   - observation.goal = (4,4)        │
│                                     │
│ if self.start_pos is None:          │
│   ✗ FALSE (es Position(0,0))        │
│   Se salta la inicialización        │
│                                     │
│ if self.path:                       │
│   ✓ TRUE (ya tenemos camino)        │
│   Retornar siguiente dirección      │
│                                     │
│ Retornar: Direction.EAST            │
└─────────────────────────────────────┘


LLAMADA 3, 4, 5... (misma lógica)
┌─────────────────────────────────────┐
│ step(observation)                   │
│                                     │
│ if self.start_pos is None:          │
│   ✗ FALSE (saltado)                 │
│                                     │
│ if self.path:                       │
│   ✓ TRUE                            │
│   Retornar siguiente dirección      │
└─────────────────────────────────────┘
```

---

## Alternativas y por qué usamos esta

### ❌ Alternativa 1: Parámetro adicional

```python
def step(self, observation, is_first=False):
    if is_first:
        _initialize_search(...)
```

**Problema:** El Simulator no pasaría `is_first`, sería incómodo.

### ❌ Alternativa 2: Usar un contador

```python
def __init__(self):
    self.call_count = 0

def step(self, observation):
    if self.call_count == 0:
        _initialize_search(...)
    self.call_count += 1
```

**Problema:** Más complicado, innecesario.

### ✅ Solución elegida: Usar None como bandera

```python
def __init__(self):
    self.start_pos = None  # ← Inicialmente None

def step(self, observation):
    if self.start_pos is None:  # ← Primera vez
        _initialize_search(...)
        # Después: self.start_pos != None para siempre
```

**Ventajas:**
- Simple y elegante
- Self-explanatory (el nombre de la variable dice qué es)
- Solo un chequeo lógico
- En el futuro, sabemos dónde empezó la búsqueda

---

## Código actual en agent.py

```python
# __init__
self.start_pos: Optional[Position] = None  # Bandera
self.goal_pos: Optional[Position] = None

# step()
if self.start_pos is None:                  # ¿Primera llamada?
    self._initialize_search(                # SÍ: Inicializar
        observation.current,
        observation.goal
    )
```

---

## Resumen

| Aspecto | Detalle |
|---------|---------|
| **Bandera** | `self.start_pos` |
| **Valor inicial** | `None` |
| **Valor después de init** | `Position(...)` |
| **Primera llamada** | `self.start_pos is None` → True |
| **Siguientes llamadas** | `self.start_pos is None` → False |
| **Ubicación del chequeo** | Inicio del método `step()` |

Cuando `_initialize_search()` se ejecuta, automáticamente establece `self.start_pos = start`, así que el chequeo solo es True una vez.
