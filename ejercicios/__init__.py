"""
Paquete que agrupa los 8 ejercicios y el menú para elegirlos.

Cada módulo expone una función main() que ejecuta el ejercicio completo.
La función main() de este paquete muestra el menú.

Uso:
    python main.py            -> muestra el menú
    python main.py 5          -> ejecuta directamente el ejercicio 5
    python -m ejercicios      -> lo mismo, sin pasar por main.py
"""

# sys.argv contiene los argumentos escritos en la terminal
import sys

# Importamos cada ejercicio como módulo ("." = este mismo paquete)
from . import (ej1_datos_personales, ej2_contador_caracteres, ej3_rombo,
               ej4_calculadora_basica, ej5_calculadora_cientifica,
               ej6_lista_tareas, ej7_gato, ej8_generador_contrasenas)

# Número de ejercicio -> (descripción, módulo)
EJERCICIOS = {
    "1": ("Datos personales", ej1_datos_personales),
    "2": ("Contador de caracteres", ej2_contador_caracteres),
    "3": ("Rombo centrado", ej3_rombo),
    "4": ("Calculadora básica", ej4_calculadora_basica),
    "5": ("Calculadora científica (tkinter)", ej5_calculadora_cientifica),
    "6": ("Lista de tareas (tkinter)", ej6_lista_tareas),
    "7": ("Juego del Gato (tkinter)", ej7_gato),
    "8": ("Generador de contraseñas (tkinter)", ej8_generador_contrasenas),
}


def ejecutar(opcion):
    """Ejecuta el main() del ejercicio elegido."""
    nombre, modulo = EJERCICIOS[opcion]
    print(f"\n>>> Ejecutando ejercicio {opcion}: {nombre}\n")
    modulo.main()


def menu():
    """Muestra el menú en un ciclo hasta que el usuario elija salir."""
    while True:
        print("\n========== EJERCICIOS ==========")
        for numero, (nombre, _) in EJERCICIOS.items():
            print(f"  {numero}) {nombre}")
        print("  0) Salir")
        opcion = input("Elige un ejercicio: ").strip()
        if opcion == "0":
            print("¡Hasta luego!")
            break
        if opcion in EJERCICIOS:
            ejecutar(opcion)
        else:
            print("  ⚠ Opción no válida.")


def main():
    """Punto de entrada: ejecuta el ejercicio indicado en la terminal o el menú."""
    # Si se pasó un número como argumento y existe, se ejecuta ese ejercicio
    if len(sys.argv) > 1 and sys.argv[1] in EJERCICIOS:
        ejecutar(sys.argv[1])
    else:
        menu()
