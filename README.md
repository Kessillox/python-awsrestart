# Ejercicios de Python

Colección de 8 ejercicios de Python: 4 de consola y 4 con interfaz gráfica
(tkinter). Todos se pueden abrir desde un **menú** (definido en `ejercicios/__init__.py`)
o ejecutar por separado. Además de lo que pide cada enunciado, cada ejercicio
incluye un "valor agregado" con mejoras.

El código está comentado línea a línea en español para facilitar su revisión.

---

## Requisitos

- **Python 3.10 o superior** (desarrollado y probado con Python 3.13).
- **tkinter**, solo para los ejercicios 5 a 8. Viene incluido con el instalador
  oficial de python.org. Para comprobar que está disponible:

  ```bash
  python3 -c "import tkinter; print(tkinter.TkVersion)"
  ```

  Si da error: en macOS con Homebrew instala `brew install python-tk`; en
  Ubuntu/Debian, `sudo apt install python3-tk`.

No se usan librerías externas: **no hace falta `pip install`**.

---

## Estructura del proyecto

```
PythonProject/
├── main.py                          # Lanzador: abre el menú de ejercicios/
├── README.md
├── .gitignore                       # Ignora .venv, __pycache__ y tareas.json
└── ejercicios/
    ├── __init__.py                  # Menú que llama a todos los ejercicios
    ├── __main__.py                  # Permite usar: python -m ejercicios
    ├── ej1_datos_personales.py      # Consola
    ├── ej2_contador_caracteres.py   # Consola
    ├── ej3_rombo.py                 # Consola
    ├── ej4_calculadora_basica.py    # Consola
    ├── ej5_calculadora_cientifica.py  # tkinter
    ├── ej6_lista_tareas.py          # tkinter (crea tareas.json al usarse)
    ├── ej7_gato.py                  # tkinter (ejercicio inventado)
    └── ej8_generador_contrasenas.py # tkinter (ejercicio inventado)
```

Cada módulo expone una función `main()`, que es la que llama el menú, y tiene
el bloque `if __name__ == "__main__":` para poder ejecutarse por sí solo.

El menú está en `ejercicios/__init__.py`: el diccionario `EJERCICIOS` asocia
cada número con su módulo, y `main()` muestra el menú o ejecuta directamente el
ejercicio indicado en la terminal. Para agregar un ejercicio nuevo basta con
importarlo ahí y sumarlo al diccionario.

---

## Cómo ejecutar

Desde la carpeta raíz del proyecto:

```bash
# Menú interactivo con los 8 ejercicios (0 para salir)
python3 main.py

# Ejecutar directamente un ejercicio por su número (1 a 8)
python3 main.py 5

# Lo mismo, usando el paquete directamente
python3 -m ejercicios
python3 -m ejercicios 5

# O ejecutar un archivo concreto
python3 ejercicios/ej3_rombo.py
```

En los ejercicios gráficos (5 a 8), al cerrar la ventana se vuelve al menú.

> `ejercicios/__init__.py` no se ejecuta como `python3 ejercicios/__init__.py`
> (Python no permite correr así un archivo de paquete); para eso existen
> `main.py` y `python3 -m ejercicios`.

**Desde PyCharm:** abrir la carpeta del proyecto, clic derecho en `main.py`
→ *Run 'main'*. Los ejercicios de consola se responden en la pestaña *Run*.

---

## Descripción de los ejercicios

### 1. Datos personales (consola)
**Enunciado:** mediante una función, pedir nombre, apellido y edad (y datos
extra) e imprimirlos en pantalla.

**Valor agregado:**
- Validación: nombre, apellido, ciudad y comida no pueden quedar vacíos y solo
  aceptan letras y espacios; la edad debe ser un entero entre 0 y 120. Si el dato
  es inválido se vuelve a pedir.
- Datos extra: ciudad y comida favorita.
- Cálculos: año aproximado de nacimiento, si es mayor de edad, días vividos
  aproximados y años que faltan para cumplir 100.
- La ficha final se muestra dentro de un recuadro.

### 2. Contador de caracteres (consola)
**Enunciado:** pedir una frase y mostrar el conteo de caracteres.

**Valor agregado:**
- Cuenta el total, sin espacios, letras (vocales/consonantes,
  mayúsculas/minúsculas), dígitos, espacios, signos y palabras.
- Reconoce vocales con tilde (`á` cuenta como vocal) y conserva la `ñ`.
- Muestra el carácter más repetido, la palabra más larga y si la frase es un
  palíndromo (ej: *"Anita lava la tina"*).
- Permite analizar varias frases; con una frase vacía (solo Enter) se sale.

### 3. Rombo centrado (consola)
**Enunciado:** a partir de un número, dibujar el rombo del enunciado centrado.

**Valor agregado:**
- Dibuja las dos versiones: la figura del enunciado (alineada a la izquierda) y
  el rombo centrado.
- Permite elegir el carácter de relleno y dibujar un rombo hueco.
- Valida el tamaño (1 a 30, para que quepa en la terminal).

Ejemplo con tamaño 4:
```
   *
  * *
 * * *
* * * *
 * * *
  * *
   *
```

### 4. Calculadora básica (consola)
**Enunciado:** elegir entre suma, resta, multiplicación y división y calcular
con dos valores.

**Valor agregado:**
- Menú que se repite hasta elegir `0) Salir`.
- Operaciones extra: potencia y módulo (resto).
- Acepta decimales con punto o coma (`3.5` o `3,5`).
- Controla división por cero, resultados demasiado grandes y resultados no
  reales (ej: raíz de un negativo con `^ 0.5`).
- Muestra el historial de operaciones al salir.

### 5. Calculadora científica (tkinter)
- Operaciones `+ − × ÷ %`, paréntesis, `xʸ`, `x²`, `√`, `1/x`, `|x|`, `n!`.
- Funciones trigonométricas e inversas con modo **DEG/RAD**; `ln` y `log`.
- Constantes `π` y `e`, y tecla `Ans` (último resultado).
- Historial lateral: clic en un cálculo para reutilizar su resultado.
- Uso con teclado: dígitos, `+ - * / ^ ( ) . %`, `Enter` (=),
  `Backspace` (borrar) y `Escape` (limpiar).
- **Evaluación segura:** no usa `eval()`. La expresión se analiza con el módulo
  `ast` y solo se permiten números, operadores y funciones conocidas; cualquier
  otra cosa (ej: `__import__('os')`) se rechaza.
- Muestra errores claros en pantalla: división por cero, `tan(90)` en grados,
  `√` de un negativo, exponentes gigantes, etc.

### 6. Lista de tareas (tkinter)
- Agregar tareas con prioridad (Alta / Media / Baja) y fecha de creación.
- Editar la tarea seleccionada (texto y prioridad). `Escape` cancela la edición.
- Marcar/desmarcar como completada: botón, doble clic o barra espaciadora.
- Eliminar (con confirmación; también con `Supr`/`Backspace`) y limpiar todas
  las completadas.
- Filtros: Todas / Pendientes / Completadas. Las tareas se ordenan por estado y
  prioridad, con colores según prioridad y en gris las completadas.
- Contador y barra de progreso.
- **Guardado automático** en `ejercicios/tareas.json` (ignorado por git), así
  las tareas se mantienen al cerrar la ventana.

### 7. Juego del Gato (tkinter, ejercicio inventado)
- Modo **contra la computadora** o **2 jugadores**.
- Dificultad *Fácil* (jugadas al azar) o *Imposible* (algoritmo **Minimax**:
  la computadora nunca pierde).
- Marcador de victorias y empates, resaltado de la línea ganadora y
  alternancia de quién empieza en cada partida.

### 8. Generador de contraseñas (tkinter, ejercicio inventado)
- Largo de 4 a 64 caracteres con un deslizador.
- Elección de mayúsculas, minúsculas, números y símbolos, con la opción de
  excluir caracteres confusos (`0 O o 1 l I |`).
- Garantiza al menos un carácter de cada tipo elegido y usa el módulo
  `secrets` (aleatoriedad criptográfica) en vez de `random`.
- Medidor de fortaleza según la entropía (bits), con barra de colores y tiempo
  estimado para descifrarla por fuerza bruta.
- Campo para evaluar una contraseña propia (se muestra oculta).
- Botón para copiar al portapapeles e historial de las últimas 5 generadas.

---

## Guía de revisión

Pasos sugeridos para comprobar que todo funciona:

1. **Compilar todo** (detecta errores de sintaxis sin abrir ventanas):
   ```bash
   python3 -m py_compile main.py ejercicios/*.py && echo OK
   ```
2. **Menú:** `python3 main.py` (o `python3 -m ejercicios`), probar una opción
   inválida (ej: `9`) y luego `0`.
3. **Ejercicio 1:** dejar el nombre vacío o escribir `123` → debe volver a
   pedirlo. Edad `150` o `-5` → inválida.
4. **Ejercicio 2:** `Anita lava la tina` → palíndromo *Sí*; `¡Árbol 123!` →
   cuenta la `Á` como vocal y mayúscula.
5. **Ejercicio 3:** tamaño `4`, carácter `#`, hueco `s`.
6. **Ejercicio 4:** división `5 ÷ 0` → aviso; `3,5 + 1,5` → `5`; al salir se
   muestra el historial.
7. **Ejercicio 5:** probar `sin(30)` → `0.5`; `sin(180)` → `0`; cambiar a RAD
   y `cos(π)` → `-1`; botón `n!` y luego `5` → `120`; `1÷0` → error; `√(−4)` → error.
8. **Ejercicio 6:** agregar tareas, editarlas, marcarlas, filtrar, cerrar la
   ventana y volver a abrirla → las tareas siguen ahí.
9. **Ejercicio 7:** en *Imposible* intentar ganarle a la computadora (no
   debería poder); en *Fácil* sí es posible.
10. **Ejercicio 8:** cambiar el largo y los tipos, desmarcar todos los tipos →
    aviso; escribir `123456` en el evaluador → *Muy débil*.

### Prueba rápida de la lógica (sin ventanas)

Las funciones de cálculo están separadas de la interfaz, por lo que se pueden
probar directamente desde la consola de Python en la raíz del proyecto:

```python
from ejercicios.ej2_contador_caracteres import analizar_frase
from ejercicios.ej3_rombo import rombo_centrado
from ejercicios.ej5_calculadora_cientifica import EvaluadorSeguro
from ejercicios.ej7_gato import minimax
from ejercicios.ej8_generador_contrasenas import generar_contrasena, calcular_entropia

analizar_frase("Anita lava la tina")["¿Es palíndromo?"]  # 'Sí'
print("\n".join(rombo_centrado(4)))                      # rombo centrado
EvaluadorSeguro().evaluar("2+3×4")                        # 14.0
minimax(["X", "X", "", "", "O", "", "", "", ""], "O", "O")[1]  # 2 (bloquea a X)
calcular_entropia(generar_contrasena(16, ["abc", "123"]))
```

---

## Revisión y correcciones realizadas

Se revisó todo el código y se probaron las funciones de lógica y las ventanas.
Se corrigieron estos detalles:

| Ejercicio | Problema | Corrección |
|---|---|---|
| 5 | `sin(180)` mostraba `1.22e-16` en vez de `0` (el redondeo a 12 cifras significativas no lo eliminaba). | Los valores menores que `1e-12` se muestran como `0`. |
| 5 | `(−8)^0.5` mostraba un error técnico en inglés. | Ahora muestra "el resultado no es un número real". |
| 7 | Si se presionaba *Nueva partida* (o se cambiaba de modo) mientras la computadora "pensaba", su jugada aparecía en la partida nueva. | La jugada pendiente se cancela al iniciar otra partida. |
| 8 | Escribir caracteres como `²` en el evaluador provocaba un error interno (`math domain error`) y el medidor no se actualizaba. | Esos caracteres se cuentan como símbolos. |
| 8 | La etiqueta de "caracteres confusos" no mencionaba `o` ni `\|`, que también se excluyen. | Etiqueta actualizada. |

### Limitaciones conocidas
- **Ej. 1:** nombres con guion o apóstrofo (ej: `O'Higgins`) se rechazan, porque
  solo se aceptan letras y espacios.
- **Ej. 5:** algunos mensajes de error vienen directo de Python y están en
  inglés (ej: `math domain error` al calcular `ln(0)`).
- **Ej. 5 y 7:** los botones son `Label` en vez de `Button` porque en macOS
  `tk.Button` ignora el color de fondo; funcionan igual con clic.
