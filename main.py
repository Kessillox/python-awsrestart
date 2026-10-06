"""
Lanzador del proyecto: abre el menú definido en ejercicios/__init__.py.

Uso:
    python main.py        -> muestra el menú
    python main.py 5      -> ejecuta directamente el ejercicio 5
"""

# El menú y la lista de ejercicios viven en el paquete "ejercicios"
from ejercicios import main

# Solo se ejecuta si se corre este archivo directamente
if __name__ == "__main__":
    main()
