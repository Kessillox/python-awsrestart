"""
Ejercicio 2
Al ejecutar una función se pide ingresar una frase cualquiera y se muestra
el conteo de caracteres.

Valor agregado:
- Conteo total, sin espacios, letras, dígitos, vocales, consonantes,
  espacios, signos/símbolos, palabras, mayúsculas y minúsculas.
- Carácter más repetido y palabra más larga.
- Indica si la frase es un palíndromo.
- Permite analizar varias frases seguidas.
"""

# Counter cuenta automáticamente cuántas veces aparece cada elemento
from collections import Counter
# unicodedata permite quitar tildes (á -> a) para detectar vocales y palíndromos
import unicodedata

# Conjunto de vocales (sin tilde, porque normalizamos antes de comparar)
VOCALES = set("aeiou")


def quitar_tildes(texto):
    """Devuelve el texto sin tildes ni diéresis (la ñ se conserva)."""
    resultado = []
    for caracter in texto:
        # La ñ se descompone en n + ~, así que la tratamos aparte
        if caracter in "ñÑ":
            resultado.append(caracter)
            continue
        # NFD separa la letra base de su tilde: 'á' -> 'a' + '´'
        descompuesto = unicodedata.normalize("NFD", caracter)
        # Nos quedamos solo con lo que no es una marca diacrítica (categoría 'Mn')
        resultado.append("".join(c for c in descompuesto
                                 if unicodedata.category(c) != "Mn"))
    return "".join(resultado)


def analizar_frase(frase):
    """Calcula todas las estadísticas de la frase y las devuelve en un diccionario."""
    # Versión en minúsculas y sin tildes, útil para comparar vocales
    normalizada = quitar_tildes(frase.lower())

    # Contadores que iremos incrementando al recorrer la frase
    letras = digitos = vocales = consonantes = espacios = otros = 0
    mayusculas = minusculas = 0

    # Recorremos ambas versiones a la vez con zip()
    for original, simple in zip(frase, normalizada):
        if original.isalpha():
            letras += 1
            # Clasificamos en vocal o consonante
            if simple in VOCALES:
                vocales += 1
            else:
                consonantes += 1
            # Clasificamos en mayúscula o minúscula
            if original.isupper():
                mayusculas += 1
            else:
                minusculas += 1
        elif original.isdigit():
            digitos += 1
        elif original.isspace():
            espacios += 1
        else:
            # Todo lo demás: signos de puntuación, símbolos, emojis...
            otros += 1

    # split() sin argumentos separa por cualquier cantidad de espacios
    palabras = frase.split()

    # Carácter más repetido ignorando espacios (most_common devuelve [(car, n)])
    sin_espacios = [c for c in normalizada if not c.isspace()]
    mas_repetido = Counter(sin_espacios).most_common(1)

    # Palabra más larga quitando signos pegados (ej: "hola," -> "hola")
    palabras_limpias = [p.strip(".,;:¡!¿?\"'()") for p in palabras]
    palabra_larga = max(palabras_limpias, key=len) if palabras_limpias else ""

    # Palíndromo: se lee igual al revés considerando solo letras y números
    solo_alfanum = [c for c in normalizada if c.isalnum()]
    es_palindromo = len(solo_alfanum) > 1 and solo_alfanum == solo_alfanum[::-1]

    # Devolvemos todo agrupado en un diccionario
    return {
        "Total de caracteres": len(frase),
        "Caracteres sin espacios": len(frase) - espacios,
        "Letras": letras,
        "  · Vocales": vocales,
        "  · Consonantes": consonantes,
        "  · Mayúsculas": mayusculas,
        "  · Minúsculas": minusculas,
        "Dígitos": digitos,
        "Espacios": espacios,
        "Signos / símbolos": otros,
        "Palabras": len(palabras),
        "Carácter más repetido": (f"'{mas_repetido[0][0]}' ({mas_repetido[0][1]} veces)"
                                  if mas_repetido else "-"),
        "Palabra más larga": palabra_larga or "-",
        "¿Es palíndromo?": "Sí" if es_palindromo else "No",
    }


def contar_caracteres():
    """Función principal: pide frases y muestra su análisis."""
    print("=== Ejercicio 2: Contador de caracteres ===")
    print("(Deja la frase vacía y presiona Enter para salir)")

    while True:
        frase = input("\nIngresa una frase: ")
        # Una frase vacía termina el ejercicio
        if not frase:
            print("¡Hasta luego!")
            break

        resultado = analizar_frase(frase)

        # Alineamos las etiquetas usando el largo de la más extensa
        ancho = max(len(clave) for clave in resultado)
        print("-" * (ancho + 25))
        for clave, valor in resultado.items():
            print(f"{clave.ljust(ancho)} : {valor}")
        print("-" * (ancho + 25))


def main():
    """Punto de entrada usado por el menú principal."""
    contar_caracteres()


if __name__ == "__main__":
    main()
