"""
Ejercicio 5
Calculadora "casi científica" con tkinter.

Características:
- Operaciones básicas: + − × ÷, paréntesis, potencias (xʸ, x²), raíz, 1/x.
- Funciones: sin, cos, tan, asin, acos, atan, ln, log, factorial, valor absoluto.
- Constantes π y e, y la tecla "Ans" (último resultado).
- Modo DEG / RAD para las funciones trigonométricas.
- Historial de cálculos (clic en uno para reutilizar su resultado).
- Soporte de teclado (números, operadores, Enter, Backspace, Escape).
- Evaluación SEGURA: no usamos eval() directo; analizamos la expresión con
  el módulo ast y solo permitimos números, operadores y funciones conocidas.
"""

# ast analiza el texto como árbol de sintaxis de Python (sin ejecutarlo)
import ast
# math aporta las funciones matemáticas (sin, cos, log, ...)
import math
# operator entrega los operadores como funciones (add, sub, ...)
import operator
import tkinter as tk

# ---------------------------------------------------------------------------
# Paleta de colores de la interfaz
# ---------------------------------------------------------------------------
COLOR_FONDO = "#1e1f26"
COLOR_PANTALLA = "#2a2c36"
COLOR_TEXTO = "#f2f2f2"
COLOR_TEXTO_SUAVE = "#9aa0b4"
COLOR_NUMERO = "#3a3d4d"
COLOR_FUNCION = "#2f4a6d"
COLOR_OPERADOR = "#e08a1e"
COLOR_ESPECIAL = "#a33b3b"
COLOR_IGUAL = "#2e8b57"

# Operadores binarios permitidos: tipo de nodo ast -> función que lo calcula
OPERADORES_BINARIOS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

# Operadores de un solo término: +x y -x
OPERADORES_UNARIOS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Traducción de los símbolos "bonitos" de la pantalla a sintaxis de Python
TRADUCCIONES = {
    "×": "*",
    "÷": "/",
    "−": "-",
    "^": "**",
    "π": "pi",
    "√": "sqrt",
}


class EvaluadorSeguro:
    """Evalúa expresiones matemáticas recorriendo el árbol ast."""

    def __init__(self):
        # True = grados, False = radianes
        self.grados = True
        # Último resultado calculado (tecla Ans)
        self.ans = 0.0

    # --- Funciones trigonométricas que respetan el modo DEG/RAD ---
    def _a_radianes(self, x):
        """Convierte x a radianes solo si estamos en modo grados."""
        return math.radians(x) if self.grados else x

    def _desde_radianes(self, x):
        """Convierte un ángulo en radianes al modo actual."""
        return math.degrees(x) if self.grados else x

    def _funciones(self):
        """Diccionario de funciones que el usuario puede usar."""
        return {
            "sin": lambda x: math.sin(self._a_radianes(x)),
            "cos": lambda x: math.cos(self._a_radianes(x)),
            "tan": self._tangente,
            "asin": lambda x: self._desde_radianes(math.asin(x)),
            "acos": lambda x: self._desde_radianes(math.acos(x)),
            "atan": lambda x: self._desde_radianes(math.atan(x)),
            "ln": math.log,          # logaritmo natural
            "log": math.log10,       # logaritmo base 10
            "sqrt": math.sqrt,
            "abs": abs,
            "fact": self._factorial,
        }

    def _tangente(self, x):
        """tan(x) que detecta los ángulos donde no está definida (90°, 270°...)."""
        if self.grados and x % 180 == 90:
            raise ValueError("tan no definida")
        return math.tan(self._a_radianes(x))

    @staticmethod
    def _factorial(x):
        """Factorial que solo acepta enteros no negativos y no demasiado grandes."""
        if x < 0 or x != int(x):
            raise ValueError("factorial solo para enteros ≥ 0")
        if x > 170:
            # 171! ya no cabe en un float
            raise OverflowError("número demasiado grande")
        return float(math.factorial(int(x)))

    def evaluar(self, texto):
        """Traduce el texto de la pantalla y lo evalúa de forma segura."""
        # 1) Reemplazamos los símbolos visuales por los de Python
        for simbolo, python in TRADUCCIONES.items():
            texto = texto.replace(simbolo, python)
        # 2) Cerramos automáticamente los paréntesis que falten
        texto += ")" * (texto.count("(") - texto.count(")"))
        # 3) Convertimos el texto en árbol (mode="eval" = una sola expresión)
        arbol = ast.parse(texto, mode="eval")
        # 4) Recorremos el árbol calculando el resultado
        resultado = self._nodo(arbol.body)
        # Potencias como (-8)^0.5 dan un número complejo, que no mostramos
        if isinstance(resultado, complex):
            raise ValueError("el resultado no es un número real")
        # 5) Redondeamos a 12 cifras significativas para limpiar decimales
        resultado = float(f"{resultado:.12g}")
        # 6) Los restos de precisión casi nulos se toman como 0: así sin(180)
        #    da 0 y no 1.2e-16
        if abs(resultado) < 1e-12:
            resultado = 0.0
        self.ans = resultado
        return resultado

    def _nodo(self, nodo):
        """Evalúa recursivamente un nodo del árbol."""
        # Número literal (ej: 3.5)
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
            return nodo.value
        # Operación binaria (ej: 2 + 3)
        if isinstance(nodo, ast.BinOp) and type(nodo.op) in OPERADORES_BINARIOS:
            izquierda = self._nodo(nodo.left)
            derecha = self._nodo(nodo.right)
            # Evitamos potencias gigantes que congelarían el programa
            if isinstance(nodo.op, ast.Pow) and abs(derecha) > 1000:
                raise OverflowError("exponente demasiado grande")
            return OPERADORES_BINARIOS[type(nodo.op)](izquierda, derecha)
        # Operación unaria (ej: -5)
        if isinstance(nodo, ast.UnaryOp) and type(nodo.op) in OPERADORES_UNARIOS:
            return OPERADORES_UNARIOS[type(nodo.op)](self._nodo(nodo.operand))
        # Constantes con nombre
        if isinstance(nodo, ast.Name):
            constantes = {"pi": math.pi, "e": math.e, "Ans": self.ans}
            if nodo.id in constantes:
                return constantes[nodo.id]
        # Llamada a función (ej: sin(30)) con exactamente un argumento
        if (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name)
                and len(nodo.args) == 1 and not nodo.keywords):
            funcion = self._funciones().get(nodo.func.id)
            if funcion:
                return funcion(self._nodo(nodo.args[0]))
        # Cualquier otra cosa (variables, imports, etc.) se rechaza
        raise ValueError("expresión no permitida")


class CalculadoraCientifica:
    """Ventana de la calculadora científica."""

    # Distribución de botones: (texto visible, texto a insertar, color)
    # Usamos None como "texto a insertar" para los botones con acción especial.
    BOTONES = [
        [("sin", "sin(", COLOR_FUNCION), ("cos", "cos(", COLOR_FUNCION),
         ("tan", "tan(", COLOR_FUNCION), ("C", None, COLOR_ESPECIAL),
         ("⌫", None, COLOR_ESPECIAL), ("(", "(", COLOR_OPERADOR),
         (")", ")", COLOR_OPERADOR)],
        [("sin⁻¹", "asin(", COLOR_FUNCION), ("cos⁻¹", "acos(", COLOR_FUNCION),
         ("tan⁻¹", "atan(", COLOR_FUNCION), ("7", "7", COLOR_NUMERO),
         ("8", "8", COLOR_NUMERO), ("9", "9", COLOR_NUMERO),
         ("÷", "÷", COLOR_OPERADOR)],
        [("ln", "ln(", COLOR_FUNCION), ("log", "log(", COLOR_FUNCION),
         ("√", "√(", COLOR_FUNCION), ("4", "4", COLOR_NUMERO),
         ("5", "5", COLOR_NUMERO), ("6", "6", COLOR_NUMERO),
         ("×", "×", COLOR_OPERADOR)],
        [("x²", "^2", COLOR_FUNCION), ("xʸ", "^", COLOR_FUNCION),
         ("n!", "fact(", COLOR_FUNCION), ("1", "1", COLOR_NUMERO),
         ("2", "2", COLOR_NUMERO), ("3", "3", COLOR_NUMERO),
         ("−", "−", COLOR_OPERADOR)],
        [("π", "π", COLOR_FUNCION), ("e", "e", COLOR_FUNCION),
         ("1/x", "1÷(", COLOR_FUNCION), ("0", "0", COLOR_NUMERO),
         (".", ".", COLOR_NUMERO), ("%", "%", COLOR_OPERADOR),
         ("+", "+", COLOR_OPERADOR)],
        [("DEG", None, COLOR_ESPECIAL), ("|x|", "abs(", COLOR_FUNCION),
         ("Ans", "Ans", COLOR_FUNCION), ("=", None, COLOR_IGUAL)],
    ]

    def __init__(self, raiz):
        self.raiz = raiz
        self.evaluador = EvaluadorSeguro()
        # Indica si lo que hay en pantalla es un resultado recién calculado
        self.mostrando_resultado = False

        raiz.title("Ejercicio 5 · Calculadora científica")
        raiz.configure(bg=COLOR_FONDO, padx=10, pady=10)
        raiz.resizable(False, False)

        self._crear_pantalla()
        self._crear_botones()
        self._crear_historial()
        self._asociar_teclado()

    # ------------------------------------------------------------------ UI
    def _crear_pantalla(self):
        """Crea las dos líneas de pantalla: la operación anterior y la actual."""
        marco = tk.Frame(self.raiz, bg=COLOR_PANTALLA, padx=10, pady=8)
        marco.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Línea pequeña superior: muestra la última operación y el modo
        self.var_previa = tk.StringVar(value="")
        self.var_modo = tk.StringVar(value="DEG")
        superior = tk.Frame(marco, bg=COLOR_PANTALLA)
        superior.pack(fill="x")
        tk.Label(superior, textvariable=self.var_modo, bg=COLOR_PANTALLA,
                 fg=COLOR_OPERADOR, font=("Helvetica", 11, "bold")).pack(side="left")
        tk.Label(superior, textvariable=self.var_previa, bg=COLOR_PANTALLA,
                 fg=COLOR_TEXTO_SUAVE, font=("Helvetica", 13), anchor="e").pack(
            side="right")

        # Línea principal: la expresión que se está escribiendo
        self.var_pantalla = tk.StringVar(value="0")
        tk.Label(marco, textvariable=self.var_pantalla, bg=COLOR_PANTALLA,
                 fg=COLOR_TEXTO, font=("Helvetica", 28, "bold"), anchor="e",
                 width=20).pack(fill="x")

    def _crear_botones(self):
        """Crea la grilla de botones a partir de la lista BOTONES."""
        marco = tk.Frame(self.raiz, bg=COLOR_FONDO)
        marco.grid(row=1, column=0)

        for fila, botones in enumerate(self.BOTONES):
            columna = 0
            for texto, insertar, color in botones:
                # El botón "=" ocupa 4 columnas en la última fila
                ancho_columnas = 4 if texto == "=" else 1
                # Usamos Label como botón porque en macOS tk.Button ignora el color
                boton = tk.Label(marco, text=texto, bg=color, fg=COLOR_TEXTO,
                                 font=("Helvetica", 15, "bold"),
                                 width=4 * ancho_columnas + (ancho_columnas - 1),
                                 height=2, cursor="hand2")
                boton.grid(row=fila, column=columna, columnspan=ancho_columnas,
                           padx=3, pady=3, sticky="nsew")
                # Asociamos el clic a la acción correspondiente.
                # Los valores por defecto (t=texto, i=insertar) "congelan" el valor
                # actual en cada iteración del ciclo.
                boton.bind("<Button-1>",
                           lambda _e, t=texto, i=insertar: self.presionar(t, i))
                # Guardamos el botón DEG para poder cambiar su texto después
                if texto == "DEG":
                    self.boton_modo = boton
                columna += ancho_columnas

    def _crear_historial(self):
        """Crea el panel lateral con el historial de cálculos."""
        marco = tk.Frame(self.raiz, bg=COLOR_FONDO, padx=10)
        marco.grid(row=0, column=1, rowspan=2, sticky="ns")
        tk.Label(marco, text="Historial", bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=("Helvetica", 13, "bold")).pack(anchor="w")
        self.lista_historial = tk.Listbox(marco, width=26, height=20,
                                          bg=COLOR_PANTALLA, fg=COLOR_TEXTO,
                                          selectbackground=COLOR_FUNCION,
                                          font=("Menlo", 11), borderwidth=0,
                                          highlightthickness=0)
        self.lista_historial.pack(fill="y", expand=True, pady=5)
        # Al seleccionar un elemento, insertamos su resultado en la pantalla
        self.lista_historial.bind("<<ListboxSelect>>", self._usar_historial)
        tk.Label(marco, text="Clic para reutilizar", bg=COLOR_FONDO,
                 fg=COLOR_TEXTO_SUAVE, font=("Helvetica", 10)).pack(anchor="w")

    def _asociar_teclado(self):
        """Permite usar la calculadora con el teclado."""
        # Equivalencias entre teclas y lo que se inserta
        teclas = {"*": "×", "/": "÷", "-": "−", "+": "+", "^": "^",
                  "(": "(", ")": ")", ".": ".", ",": ".", "%": "%"}
        for tecla, simbolo in teclas.items():
            self.raiz.bind(tecla, lambda _e, s=simbolo: self.presionar(s, s))
        # Dígitos del 0 al 9
        for digito in "0123456789":
            self.raiz.bind(digito, lambda _e, d=digito: self.presionar(d, d))
        self.raiz.bind("<Return>", lambda _e: self.presionar("=", None))
        self.raiz.bind("<KP_Enter>", lambda _e: self.presionar("=", None))
        self.raiz.bind("<BackSpace>", lambda _e: self.presionar("⌫", None))
        self.raiz.bind("<Escape>", lambda _e: self.presionar("C", None))

    # ------------------------------------------------------------- lógica
    def presionar(self, texto, insertar):
        """Se ejecuta al presionar cualquier botón (o tecla)."""
        actual = self.var_pantalla.get()

        if texto == "C":
            # Borra todo
            self.var_pantalla.set("0")
            self.var_previa.set("")
        elif texto == "⌫":
            # Borra el último carácter (si queda vacío, mostramos 0)
            self.var_pantalla.set(actual[:-1] or "0")
        elif texto == "DEG":
            self._cambiar_modo()
        elif texto == "=":
            self._calcular()
            return
        else:
            # ¿Lo presionado continúa lo que hay en pantalla? (ej: "8" y luego "×",
            # o "0" y luego ".")
            continua = insertar[0] in "+−×÷^%" or (insertar == "." and actual == "0")
            # Si en pantalla hay "0", "Error" o un resultado y se escribe un número
            # o función, comenzamos una expresión nueva.
            if actual in ("0", "Error") or (self.mostrando_resultado and not continua):
                # Si es un operador tras un resultado, seguimos desde ese resultado
                actual = "" if not continua or actual == "Error" else actual
            self.var_pantalla.set(actual + insertar)

        self.mostrando_resultado = False

    def _cambiar_modo(self):
        """Alterna entre grados y radianes."""
        self.evaluador.grados = not self.evaluador.grados
        modo = "DEG" if self.evaluador.grados else "RAD"
        self.var_modo.set(modo)
        # El botón muestra el modo actual
        self.boton_modo.configure(text=modo)

    def _calcular(self):
        """Evalúa la expresión en pantalla y muestra el resultado."""
        expresion = self.var_pantalla.get()
        try:
            resultado = self.evaluador.evaluar(expresion)
        except ZeroDivisionError:
            self._mostrar_error(expresion, "División por cero")
            return
        except (ValueError, OverflowError, SyntaxError, TypeError) as error:
            # ValueError: dominio inválido (ej: √-1, ln 0) o expresión no permitida
            # SyntaxError: expresión mal escrita (ej: "3++")
            self._mostrar_error(expresion, str(error) or "Expresión inválida")
            return

        texto_resultado = self.formatear(resultado)
        self.var_previa.set(expresion + " =")
        self.var_pantalla.set(texto_resultado)
        self.mostrando_resultado = True
        # Agregamos al historial (al principio de la lista)
        self.lista_historial.insert(0, f"{expresion} = {texto_resultado}")

    def _mostrar_error(self, expresion, mensaje):
        """Muestra un mensaje de error en la pantalla."""
        self.var_previa.set(f"{expresion}  ⚠ {mensaje}")
        self.var_pantalla.set("Error")
        self.mostrando_resultado = True

    @staticmethod
    def formatear(numero):
        """Muestra enteros sin '.0' y usa notación científica si es muy grande."""
        if numero.is_integer() and abs(numero) < 1e15:
            return str(int(numero))
        return f"{numero:.10g}"

    def _usar_historial(self, _evento):
        """Inserta en pantalla el resultado del cálculo seleccionado."""
        seleccion = self.lista_historial.curselection()
        if not seleccion:
            return
        # El texto es "expresión = resultado"; tomamos lo que está después del '='
        resultado = self.lista_historial.get(seleccion[0]).rsplit("= ", 1)[1]
        self.var_pantalla.set(resultado)
        self.mostrando_resultado = True


def main():
    """Crea la ventana y arranca el ciclo de eventos de tkinter."""
    raiz = tk.Tk()
    CalculadoraCientifica(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
