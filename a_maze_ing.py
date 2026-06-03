#!/usr/bin/env python3

import config_parser
from mazegen.generator import MazeGenerator


def main() -> None:
    # 1. Leemos los datos reales de tu config.txt usando tu parser
    config = config_parser.parse_config("config.txt")

    # 2. Le pasamos los datos del diccionario al generador
    generador = MazeGenerator(
        width=config["width"],
        height=config["height"],
        entry=config["entry"],
        exit=config["exit"],
        perfect=config["perfect"],
        seed=config.get("seed"),  # Usamos .get por si la seed es opcional (None)
    )

    # 3. Encendemos el machete para que cave la selva
    mapa = generador.machete()

    # 4. ¡Pintamos el resultado en la terminal con todos sus bordes delimitados!
    print(f"\n--- LABERINTO GENERADO (Seed: {generador.seed}) ---")

    # Dibuja el borde exterior del Norte (el techo del laberinto)
    print(" " + "_" * (config["width"] * 2 - 1))

    for fila in mapa:
        # Cada fila empieza con la pared exterior del Oeste
        linea = "|"

        for celda in fila:
            # bit 0=N, bit 1=E, bit 2=S, bit 3=W
            tiene_este = bool(celda & 2)
            tiene_sur = bool(celda & 4)

            if celda == 15:
                linea += "██"  # celda del 42, totalmente cerrada
            else:
                # 1. Pintamos el suelo (Sur)
                espacio_suelo = "_" if tiene_sur else " "
                linea += espacio_suelo

                # 2. Pintamos la pared lateral (Este)
                if tiene_este:
                    linea += "|"
                else:
                    # Si no hay pared al Este pero hay suelo, arrastramos el suelo
                    # para mantener la estética uniforme en la terminal
                    linea += "_" if tiene_sur else " "
        print(linea)


if __name__ == "__main__":
    main()