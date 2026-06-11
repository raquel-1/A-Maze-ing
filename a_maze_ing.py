#!/usr/bin/env python3

from typing import cast
import config_parser
from mazegen.generator import MazeGenerator
# Importamos las funciones del pathfinder (asumiendo que está en pathfinder.py)
from mazegen.pathfinder import find_short_path


def main() -> None:
    # 1. Leemos los datos reales de tu config.txt usando tu parser
    config = config_parser.parse_config("config.txt")

    # 2. Forzamos los tipos con 'cast' para que mypy se quede tranquilo
    width = cast(int, config["width"])
    height = cast(int, config["height"])
    entry = cast(tuple[int, int], config["entry"])
    exit_cell = cast(tuple[int, int], config["exit"])  # Evitamos usar 'exit' que es palabra reservada
    perfect = cast(bool, config["perfect"])

    # La seed puede ser int o None, usamos config.get por si no existe
    seed = cast(int | None, config.get("seed"))

    # 3. Le pasamos los datos ya limpios y tipados al generador
    generador = MazeGenerator(
        width=width,
        height=height,
        entry=entry,
        exit=exit_cell,
        perfect=perfect,
        seed=seed,
    )

    # 4. Encendemos el machete para que cave la selva
    mapa = generador.machete()

    # 5. Calculamos el camino más corto usando el pathfinder
    camino_coordenadas = find_short_path(mapa, entry, exit_cell)
    # Lo convertimos a set para buscar eficientemente dentro del bucle
    conjunto_camino = set(camino_coordenadas)

    # 6. ¡Pintamos el resultado con el camino incluido!
    print(f"\n--- LABERINTO GENERADO (Seed: {generador.seed}) ---")

    # Dibuja el borde exterior del Norte (el techo del laberinto)
    print(" " + "_" * (width * 2 - 1))

    # Usamos enumerate para saber en qué fila (y) y columna (x) estamos
    for y, fila in enumerate(mapa):
        # Cada fila empieza con la pared exterior del Oeste
        linea = "|"

        for x, celda in enumerate(fila):
            # bit 0=N, bit 1=E, bit 2=S, bit 3=W
            tiene_este = bool(celda & 2)
            tiene_sur = bool(celda & 4)

            if celda == 15:
                linea += "██"  # celda del 42, totalmente cerrada
            else:
                # Comprobamos si esta celda actual (x, y) pertenece al camino corto
                es_camino = (x, y) in conjunto_camino

                # 1. Pintamos el suelo (Sur)
                # Si es camino y NO tiene pared abajo, ponemos un punto o espacio, 
                # pero si tiene pared abajo, respetamos el suelo '_'
                espacio_suelo = "_" if tiene_sur else ("*" if es_camino else " ")
                linea += espacio_suelo

                # 2. Pintamos la pared lateral (Este)
                if tiene_este:
                    linea += "|"
                else:
                    # Si no hay pared al Este y la celda de abajo tiene suelo, arrastramos el '_'
                    if tiene_sur:
                        linea += "_"
                    # Si no hay suelo abajo, pero la celda actual es del camino, podemos dejarlo libre
                    else:
                        linea += " "

        print(linea)


if __name__ == "__main__":
    main()