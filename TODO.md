
# A-Maze-ing — Explicación del proyecto

## ¿Qué hay que hacer en resumen?

Un programa Python que:

1. Lee un fichero de configuración
2. Genera un laberinto aleatorio (con ciertas reglas)
3. Lo guarda en un fichero de salida con formato hexadecimal
4. Lo muestra visualmente (terminal o ventana gráfica)
5. Permite interactuar (regenerar, mostrar solución, cambiar colores)

---

## Flujo de ejecución

```text
python3 a_maze_ing.py config.txt
        │
        ▼
  Leer config.txt
  (KEY=VALUE, ignorar #)
        │
        ▼
  Validar parámetros
  (WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT)
        │
        ▼
  Crear el laberinto
  (clase MazeGenerator, algoritmo aleatorio + seed)
        │
        ├── Si PERFECT=True → laberinto perfecto (un único camino)
        ├── Dibujar el patrón "42" en células cerradas
        └── Verificar que no hay zonas 3x3 abiertas
        │
        ▼
  Calcular el camino más corto (BFS típicamente)
        │
        ▼
  Escribir output file (hex + entrada + salida + camino)
        │
        ▼
  Mostrar visualmente + loop de interacción
  (re-generar / mostrar path / cambiar colores)
```

---

## Estructura de ficheros del proyecto

```text
A-Maze-ing/
├── a_maze_ing.py          ← orquestador
├── config_parser.py       ← fuera de mazegen
├── display.py             ← fuera de mazegen
├── config.txt
├── Makefile
├── README.md
├── .gitignore
├── pyproject.toml
└── mazegen/
    ├── __init__.py
    ├── generator.py       ← solo lógica pura del laberinto
    ├── pathfinder.py      ← solo pathfinding
```


### Por qué cada fichero

* **a_maze_ing.py** — Solo orquesta. Llama al parser, crea el generador, llama al display. Poca lógica aquí.
* **config.txt** — El fichero por defecto que piden obligatoriamente en el repo.
* **Makefile** — Obligatorio con las reglas: install, run, debug, clean, lint.
* **README.md** — Obligatorio con todo lo que lista el enunciado.
* **.gitignore** — Para no subir `.venv/`, `dist/`, `__pycache__/`, `*.whl`...
* **pyproject.toml** — Le dice a `uv build` cómo construir el paquete `mazegen`.
* **mazegen/**init**.py** — Vacío o con imports, pero necesario para que Python trate la carpeta como paquete.
* **mazegen/generator.py** — El núcleo. La clase `MazeGenerator` con el algoritmo, la seed, el patrón 42, la restricción 3x3, y el modo perfecto.
* **mazegen/pathfinder.py** — BFS que recibe el laberinto y devuelve el camino más corto de entrada a salida.
* **mazegen/display.py** — Dibuja el laberinto en terminal con ASCII, gestiona las teclas para interactuar.
* **mazegen/config_parser.py** — Lee el `config.txt`, valida que estén todas las claves, lanza errores claros si algo falla.

```text
a_maze_ing.py arranca
        │
        ▼
config_parser lee config.txt
        │
        ├── si algo falla → imprime error y el programa para
        │
        └── si todo ok → devuelve diccionario limpio
                {
                    "width": 20,
                    "height": 15,
                    "entry": (0, 0),
                    "exit": (19, 14),
                    "output_file": "maze.txt",
                    "perfect": True
                }
                        │
                        ▼
                MazeGenerator recibe ese diccionario
                y ya puede generar el laberinto
```

---

## Capítulo VI — Módulo reutilizable

Esta es la parte que más suele confundir.

Lo que pide el subject es:

- La clase `MazeGenerator` debe vivir en un fichero independiente.
- Ese módulo debe poder instalarse mediante:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

- Después de instalarlo, cualquier otro proyecto Python debería poder usarlo mediante:

```python
from mazegen import MazeGenerator
```

- El paquete debe construirse usando el sistema estándar de empaquetado de Python (`pyproject.toml` o equivalente).
- Deben generarse ambos archivos:

```text
mazegen-1.0.0-py3-none-any.whl
mazegen-1.0.0.tar.gz
```

- El programa principal `a_maze_ing.py` debe importar el módulo exactamente igual que una librería externa.

### Qué harán en la evaluación

1. Crear un entorno virtual limpio.
2. Instalar tu `.whl`.
3. Ejecutar `a_maze_ing.py`.
4. Verificar que el programa funciona usando únicamente el paquete instalado.

---

## Lista de tareas

### Fase 1 — Base del proyecto

- [X] Crear estructura de carpetas y ficheros
- [X] Crear `.gitignore`
- [X] Crear `Makefile` con las reglas requeridas
- [X] Implementar `config_parser.py`
- [X] Leer líneas `KEY=VALUE`
- [X] Ignorar comentarios `#`
- [X] Validar parámetros obligatorios
- [X] Gestionar todos los errores posibles

#### Casos de error a probar

- [X] Clave obligatoria ausente
- [X] Formato incorrecto
- [X] Booleano inválido
- [X] Coordenadas fuera de rango
- [X] Anchura o altura inválidas
- [X] Entrada y salida mal definidas

---

### Fase 2 — Generador de laberintos

- [X] Elegir algoritmo de generación
- [X] Entender Recursive Backtracker
- [X] Implementar clase `MazeGenerator`
- [X] Crear cuadrícula con paredes
- [X] Generar usando una seed reproducible
- [X] Implementar modo `PERFECT=True`
- [X] Garantizar un único camino entre dos celdas
- [X] Aplicar restricción de zonas 3×3 abiertas
- [X] Dibujar el patrón `"42"` usando celdas cerradas
- [X] Validar consistencia entre paredes vecinas

---

### Fase 3 — Pathfinding y output

- [X] Implementar `pathfinder.py`
- [X] Encontrar el camino más corto mediante BFS
- [X] Generar fichero de salida
- [X] Exportar laberinto en hexadecimal
- [X] Guardar entrada y salida
- [X] Guardar el camino calculado
- [ ] Validar usando `output_validator.py`

---

### Fase 4 — Visualización

- [X] Mostrar entrada y salida
- [X] Mostrar camino solución
- [X] Crear bucle interactivo

#### Acciones interactivas

- [X] Regenerar laberinto
- [X] Mostrar/Ocultar solución
- [X] Cambiar colores

- [X] MLX
- [X] Crear ventana gráfica
- [X] CREAR MENU EN LA VENTANA GRAFICA

---

### Fase 5 — Empaquetado (Capítulo VI)

- [ ] Crear `pyproject.toml`
- [ ] Definir paquete `mazegen`
- [ ] Generar `.whl`
- [ ] Generar `.tar.gz`
- [ ] Probar instalación en virtualenv limpio
- [ ] Verificar importación externa
- [ ] Documentar uso del módulo

---

### Fase 6 — README y limpieza

- [ ] Completar README
- [ ] Documentar instalación
- [ ] Documentar ejecución
- [ ] Documentar formato del fichero de configuración
- [ ] Documentar formato del output
- [ ] Pasar `flake8`
- [ ] Pasar `mypy`
- [ ] Revisar hoja de corrección completa

---

### Bonus

- [X] Soporte para múltiples algoritmos
- [ ] Exportación visual adicional

---

## Orden recomendado

### 3. Pathfinding

Una vez generado el laberinto:

- BFS
- Camino más corto

### 4. Exportación

Generar correctamente el fichero hexadecimal.

### 5. Visualización

Mostrar el resultado e implementar la interacción.

### 6. Empaquetado

Dejar para el final:

- `pyproject.toml`
- `.whl`
- `.tar.gz`
