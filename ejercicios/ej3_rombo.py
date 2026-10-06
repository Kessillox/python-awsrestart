"""
Ejercicio 3
Dibujar un rombo centrado a partir de un número ingresado.

El enunciado muestra la "mitad" del rombo (alineada a la izquierda):
    *
    **
    ***
    ****
    ***
    **
    *
y pide que quede centrado. Por eso dibujamos ambas versiones:
1) La figura del enunciado tal como aparece.
2) El rombo centrado (la versión pedida).

Valor agregado:
- Se puede elegir el carácter de relleno.
- Opción de rombo hueco (solo el borde).
- Validación del número ingresado.
"""


def pedir_entero(mensaje, minimo, maximo):
    """Pide un número entero dentro de un rango [minimo, maximo]."""
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit() and minimo <= int(valor) <= maximo:
            return int(valor)
        print(f"  ⚠ Ingresa un número entero entre {minimo} y {maximo}.")


def filas_del_rombo(n):
    """
    Devuelve la cantidad de símbolos por fila: 1, 2, ..., n, ..., 2, 1.
    Por ejemplo, para n=4 -> [1, 2, 3, 4, 3, 2, 1]
    """
    # Parte que crece: 1..n  +  parte que decrece: n-1..1
    return list(range(1, n + 1)) + list(range(n - 1, 0, -1))


def figura_enunciado(n, simbolo="*"):
    """Construye la figura tal como aparece en el enunciado (alineada a la izquierda)."""
    # Cada fila es el símbolo repetido 'cantidad' veces
    return [simbolo * cantidad for cantidad in filas_del_rombo(n)]


def rombo_centrado(n, simbolo="*", hueco=False):
    """
    Construye el rombo centrado.
    Cada fila tiene (n - cantidad) espacios a la izquierda y luego
    'cantidad' símbolos separados por un espacio, así la figura queda simétrica.
    """
    lineas = []
    for cantidad in filas_del_rombo(n):
        # Espacios a la izquierda para centrar la fila
        sangria = " " * (n - cantidad)
        if hueco and cantidad > 2:
            # Rombo hueco: símbolo en los extremos y espacios al medio
            # (cada "celda" ocupa 2 caracteres: símbolo + espacio)
            centro = "  " * (cantidad - 2)
            fila = simbolo + " " + centro + simbolo
        else:
            # " ".join pone un espacio entre cada símbolo: "* * *"
            fila = " ".join(simbolo * cantidad)
        lineas.append(sangria + fila)
    return lineas


def dibujar_rombo():
    """Función principal: pide los datos y dibuja las figuras."""
    print("=== Ejercicio 3: Rombo centrado ===")

    # Limitamos a 30 para que el dibujo quepa en la terminal
    n = pedir_entero("Tamaño del rombo (1-30): ", 1, 30)

    # Si el usuario no escribe nada, usamos '*' por defecto
    simbolo = input("Carácter a usar [*]: ").strip() or "*"
    # Usamos solo el primer carácter por si escribe varios
    simbolo = simbolo[0]

    # El rombo hueco es opcional
    hueco = input("¿Rombo hueco? (s/n) [n]: ").strip().lower() == "s"

    print("\n1) Figura del enunciado (sin centrar):")
    print("\n".join(figura_enunciado(n, simbolo)))

    print("\n2) Rombo centrado" + (" (hueco)" if hueco else "") + ":")
    print("\n".join(rombo_centrado(n, simbolo, hueco)))


def main():
    """Punto de entrada usado por el menú principal."""
    dibujar_rombo()


if __name__ == "__main__":
    main()
