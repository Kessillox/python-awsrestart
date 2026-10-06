"""
Ejercicio 4
Crear una función donde se elija entre suma, resta, multiplicación y división
y se efectúe el cálculo con dos valores ingresados.

Valor agregado:
- Menú repetible hasta que el usuario decida salir.
- Operaciones extra: potencia y módulo (resto).
- Acepta decimales con punto o con coma (3,5 o 3.5).
- Controla la división (y el módulo) por cero.
- Guarda un historial de operaciones y lo muestra al salir.
"""

# operator contiene las operaciones aritméticas como funciones (add, sub, ...)
import operator

# Diccionario de operaciones: opción -> (nombre, símbolo, función)
# Usar un diccionario evita una larga cadena de if/elif.
OPERACIONES = {
    "1": ("Suma", "+", operator.add),
    "2": ("Resta", "-", operator.sub),
    "3": ("Multiplicación", "×", operator.mul),
    "4": ("División", "÷", operator.truediv),
    "5": ("Potencia", "^", operator.pow),
    "6": ("Módulo (resto)", "mod", operator.mod),
}


def pedir_numero(mensaje):
    """Pide un número (entero o decimal) y lo devuelve como float."""
    while True:
        # Reemplazamos la coma por punto para aceptar el formato chileno
        texto = input(mensaje).strip().replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            # float() lanza ValueError si el texto no es un número
            print("  ⚠ Eso no es un número válido, intenta de nuevo.")


def formatear(numero):
    """Muestra 5.0 como 5 y redondea decimales largos."""
    # Si el número no tiene parte decimal, lo mostramos como entero
    if isinstance(numero, float) and numero.is_integer():
        return str(int(numero))
    # round evita resultados como 0.30000000000000004
    return str(round(numero, 10))


def mostrar_menu():
    """Imprime el menú de opciones."""
    print("\n¿Qué operación deseas realizar?")
    for clave, (nombre, simbolo, _) in OPERACIONES.items():
        print(f"  {clave}) {nombre} ({simbolo})")
    print("  0) Salir")


def calculadora():
    """Función principal: muestra el menú y realiza los cálculos."""
    print("=== Ejercicio 4: Calculadora básica ===")
    # Lista donde guardaremos cada operación realizada
    historial = []

    while True:
        mostrar_menu()
        opcion = input("Opción: ").strip()

        # Opción para terminar el programa
        if opcion == "0":
            break

        # Validamos que la opción exista en el diccionario
        if opcion not in OPERACIONES:
            print("  ⚠ Opción no válida.")
            continue

        # Desempaquetamos la tupla de la operación elegida
        nombre, simbolo, funcion = OPERACIONES[opcion]
        print(f"\n-- {nombre} --")
        a = pedir_numero("Primer valor: ")
        b = pedir_numero("Segundo valor: ")

        try:
            # Ejecutamos la función asociada a la operación
            resultado = funcion(a, b)
        except ZeroDivisionError:
            # Ocurre en división o módulo cuando b es 0
            print("  ⚠ No se puede dividir por cero.")
            continue
        except OverflowError:
            # Ocurre con potencias demasiado grandes
            print("  ⚠ El resultado es demasiado grande.")
            continue

        # Potencias como (-8) ^ 0.5 dan un número complejo; lo informamos
        if isinstance(resultado, complex):
            print("  ⚠ El resultado no es un número real.")
            continue

        texto = f"{formatear(a)} {simbolo} {formatear(b)} = {formatear(resultado)}"
        print("  Resultado:", texto)
        historial.append(texto)

    # Al salir, mostramos el historial (si hay operaciones)
    if historial:
        print("\nHistorial de operaciones:")
        # enumerate entrega el índice y el valor; start=1 para empezar en 1
        for i, operacion in enumerate(historial, start=1):
            print(f"  {i}. {operacion}")
    print("¡Hasta luego!")


def main():
    """Punto de entrada usado por el menú principal."""
    calculadora()


if __name__ == "__main__":
    main()
