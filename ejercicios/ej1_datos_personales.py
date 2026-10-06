"""
Ejercicio 1
Mediante una función pedir nombre, apellido y edad (más datos extra)
e imprimir los datos en pantalla.

Valor agregado:
- Validación de cada dato (no vacío, solo letras, edad numérica y en rango).
- Datos extra: ciudad y comida favorita.
- Cálculos derivados: año aproximado de nacimiento, mayoría de edad,
  días aproximados vividos y años que faltan para cumplir 100.
- Ficha final presentada dentro de un recuadro.
"""

# datetime nos permite conocer el año actual para calcular el año de nacimiento
from datetime import date


def pedir_texto(mensaje):
    """Pide un texto que no esté vacío y que contenga solo letras/espacios."""
    # Repetimos hasta que el usuario ingrese un valor válido
    while True:
        # strip() elimina espacios al inicio y al final
        valor = input(mensaje).strip()
        # Comprobamos que no esté vacío y que (sin espacios) sean solo letras
        if valor and valor.replace(" ", "").isalpha():
            # title() deja la primera letra de cada palabra en mayúscula
            return valor.title()
        print("  ⚠ Dato inválido: ingresa solo letras (no puede quedar vacío).")


def pedir_edad(mensaje):
    """Pide una edad entera entre 0 y 120."""
    while True:
        valor = input(mensaje).strip()
        # isdigit() verifica que sean solo dígitos (descarta negativos y decimales)
        if valor.isdigit() and 0 <= int(valor) <= 120:
            return int(valor)
        print("  ⚠ Edad inválida: ingresa un número entero entre 0 y 120.")


def imprimir_ficha(lineas):
    """Imprime una lista de líneas dentro de un recuadro de texto."""
    # El ancho del recuadro depende de la línea más larga
    ancho = max(len(linea) for linea in lineas)
    print("┌" + "─" * (ancho + 2) + "┐")
    for linea in lineas:
        # ljust() rellena con espacios para que todas las líneas midan lo mismo
        print("│ " + linea.ljust(ancho) + " │")
    print("└" + "─" * (ancho + 2) + "┘")


def datos_personales():
    """Función principal del ejercicio: pide los datos y los muestra."""
    print("=== Ejercicio 1: Datos personales ===")

    # --- Pedir los datos obligatorios ---
    nombre = pedir_texto("Nombre: ")
    apellido = pedir_texto("Apellido: ")
    edad = pedir_edad("Edad: ")

    # --- Datos extra ---
    ciudad = pedir_texto("Ciudad donde vives: ")
    comida = pedir_texto("Comida favorita: ")

    # --- Cálculos derivados a partir de la edad ---
    anio_actual = date.today().year
    # Es aproximado porque no sabemos si ya cumplió años este año
    anio_nacimiento = anio_actual - edad
    # Operador ternario para elegir el texto según la edad
    mayoria = "Sí" if edad >= 18 else "No"
    # 365.25 considera los años bisiestos
    dias_vividos = int(edad * 365.25)
    # max() evita mostrar números negativos si ya tiene 100 o más
    faltan_100 = max(0, 100 - edad)

    # --- Mostrar la ficha en pantalla ---
    print()
    imprimir_ficha([
        "FICHA PERSONAL",
        "",
        f"Nombre completo : {nombre} {apellido}",
        f"Edad            : {edad} años",
        f"Ciudad          : {ciudad}",
        f"Comida favorita : {comida}",
        "",
        f"Nació aprox. en : {anio_nacimiento - 1} o {anio_nacimiento}",
        f"Mayor de edad   : {mayoria}",
        # {:,} agrega separador de miles; luego cambiamos ',' por '.'
        f"Días vividos    : ~{dias_vividos:,}".replace(",", "."),
        f"Faltan para 100 : {faltan_100} años",
    ])


def main():
    """Punto de entrada usado por el menú principal."""
    datos_personales()


# Permite ejecutar este archivo directamente: python ej1_datos_personales.py
if __name__ == "__main__":
    main()
