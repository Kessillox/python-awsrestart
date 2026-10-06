"""
Ejercicio 8 (inventado)
Generador y evaluador de contraseñas seguras con tkinter.

Características:
- Largo configurable con un deslizador (4 a 64 caracteres).
- Elegir qué tipos de caracteres usar: mayúsculas, minúsculas,
  números y símbolos; opción para excluir caracteres confusos (0/O/o, 1/l/I/|).
- Garantiza al menos un carácter de cada tipo seleccionado.
- Usa el módulo `secrets` (aleatoriedad criptográfica, no `random`).
- Medidor de fortaleza basado en la entropía (bits) con barra de colores
  y tiempo estimado para descifrarla por fuerza bruta.
- Evaluador: escribe tu propia contraseña y mira qué tan segura es.
- Copiar al portapapeles e historial de las últimas contraseñas generadas.
"""

# math.log2 se usa para calcular la entropía
import math
# secrets genera números aleatorios seguros para contraseñas
import secrets
# string contiene los conjuntos de caracteres (ascii_lowercase, digits, ...)
import string
import tkinter as tk
from tkinter import ttk

# Conjuntos de caracteres disponibles: nombre -> caracteres
CONJUNTOS = {
    "Mayúsculas (A-Z)": string.ascii_uppercase,
    "Minúsculas (a-z)": string.ascii_lowercase,
    "Números (0-9)": string.digits,
    "Símbolos (!@#…)": "!@#$%&*+-=?_.:;",
}
# Caracteres que se confunden fácilmente al leerlos
CONFUSOS = set("0Oo1lI|")

# Niveles de fortaleza: (bits mínimos, nombre, color)
NIVELES = [
    (0, "Muy débil", "#c0392b"),
    (36, "Débil", "#e67e22"),
    (60, "Aceptable", "#f1c40f"),
    (80, "Fuerte", "#27ae60"),
    (110, "Muy fuerte", "#1e8449"),
]

# Intentos por segundo que supone un atacante con hardware potente
INTENTOS_POR_SEGUNDO = 1e10


def generar_contrasena(largo, conjuntos, excluir_confusos=False):
    """Genera una contraseña con al menos un carácter de cada conjunto elegido."""
    # Quitamos los caracteres confusos de cada conjunto si se pidió
    if excluir_confusos:
        conjuntos = ["".join(c for c in conjunto if c not in CONFUSOS)
                     for conjunto in conjuntos]
    # Unimos todos los caracteres posibles en un solo texto
    todos = "".join(conjuntos)
    # 1) Un carácter obligatorio de cada conjunto
    caracteres = [secrets.choice(conjunto) for conjunto in conjuntos]
    # 2) Completamos el largo con caracteres de cualquier conjunto
    caracteres += [secrets.choice(todos) for _ in range(largo - len(caracteres))]
    # 3) Mezclamos para que los obligatorios no queden siempre al inicio
    secrets.SystemRandom().shuffle(caracteres)
    return "".join(caracteres)


def calcular_entropia(contrasena):
    """
    Estima la entropía en bits: largo × log2(tamaño del alfabeto usado).
    Mientras más bits, más combinaciones debe probar un atacante.
    """
    if not contrasena:
        return 0.0
    alfabeto = 0
    # Sumamos el tamaño de cada tipo de carácter que aparezca
    if any(c in string.ascii_lowercase for c in contrasena):
        alfabeto += 26
    if any(c in string.ascii_uppercase for c in contrasena):
        alfabeto += 26
    if any(c in string.digits for c in contrasena):
        alfabeto += 10
    # Símbolo = todo lo que no sea letra ni dígito ASCII (incluye "²", "½", etc.)
    if any(not (c.isascii() and c.isalnum()) and not c.isalpha() for c in contrasena):
        alfabeto += 33  # símbolos ASCII imprimibles aproximados
    if any(c.isalpha() and not c.isascii() for c in contrasena):
        alfabeto += 20  # letras con tilde, ñ, etc.
    entropia = len(contrasena) * math.log2(alfabeto)
    # Penalizamos las repeticiones: "aaaaaaaa" no es segura aunque sea larga
    distintos = len(set(contrasena))
    return entropia * (distintos / len(contrasena)) ** 0.5


def tiempo_para_descifrar(bits):
    """Convierte la entropía en un tiempo legible para un ataque de fuerza bruta."""
    # En promedio se encuentra la clave tras probar la mitad de combinaciones
    segundos = 2 ** bits / 2 / INTENTOS_POR_SEGUNDO
    unidades = [("años", 31_557_600), ("días", 86_400), ("horas", 3_600),
                ("minutos", 60), ("segundos", 1)]
    if segundos < 1:
        return "instantáneo"
    for nombre, duracion in unidades:
        if segundos >= duracion:
            cantidad = segundos / duracion
            # Números enormes se muestran en notación científica
            if cantidad >= 1e6:
                return f"{cantidad:.1e} {nombre}"
            return f"{cantidad:,.0f} {nombre}".replace(",", ".")
    return "instantáneo"


def nivel_de(bits):
    """Devuelve (nombre, color) del nivel correspondiente a esos bits."""
    nombre, color = NIVELES[0][1], NIVELES[0][2]
    for minimo, n, c in NIVELES:
        if bits >= minimo:
            nombre, color = n, c
    return nombre, color


class GeneradorContrasenas:
    """Ventana del generador."""

    def __init__(self, raiz):
        self.raiz = raiz
        raiz.title("Ejercicio 8 · Generador de contraseñas")
        raiz.resizable(False, False)

        # Marco principal con margen
        self.marco = ttk.Frame(raiz, padding=15)
        self.marco.pack(fill="both", expand=True)

        self._crear_opciones()
        self._crear_resultado()
        self._crear_evaluador()
        self._crear_historial()
        # Generamos una contraseña de inmediato para que la ventana no parta vacía
        self.generar()

    # ----------------------------------------------------------------- UI
    def _crear_opciones(self):
        """Deslizador de largo y casillas de tipos de caracteres."""
        caja = ttk.LabelFrame(self.marco, text="Opciones", padding=10)
        caja.pack(fill="x")

        # Largo de la contraseña
        self.var_largo = tk.IntVar(value=16)
        fila = ttk.Frame(caja)
        fila.pack(fill="x")
        ttk.Label(fila, text="Largo:").pack(side="left")
        # El Scale entrega decimales; los redondeamos al moverlo
        ttk.Scale(fila, from_=4, to=64, variable=self.var_largo, length=260,
                  command=lambda v: self.var_largo.set(round(float(v)))).pack(
            side="left", padx=8)
        ttk.Label(fila, textvariable=self.var_largo, width=3).pack(side="left")

        # Una casilla (Checkbutton) por cada conjunto de caracteres
        self.vars_conjuntos = {}
        rejilla = ttk.Frame(caja)
        rejilla.pack(fill="x", pady=(8, 0))
        for i, nombre in enumerate(CONJUNTOS):
            variable = tk.BooleanVar(value=True)
            self.vars_conjuntos[nombre] = variable
            ttk.Checkbutton(rejilla, text=nombre, variable=variable).grid(
                row=i // 2, column=i % 2, sticky="w", padx=(0, 20))

        self.var_confusos = tk.BooleanVar(value=False)
        ttk.Checkbutton(caja, text="Excluir caracteres confusos (0 O o 1 l I |)",
                        variable=self.var_confusos).pack(anchor="w", pady=(5, 0))

    def _crear_resultado(self):
        """Campo con la contraseña generada, botones y medidor."""
        caja = ttk.LabelFrame(self.marco, text="Contraseña generada", padding=10)
        caja.pack(fill="x", pady=10)

        self.var_contrasena = tk.StringVar()
        # Entry de solo lectura con letra monoespaciada (más fácil de leer)
        ttk.Entry(caja, textvariable=self.var_contrasena, font=("Menlo", 15),
                  state="readonly", width=34).pack(fill="x")

        botones = ttk.Frame(caja)
        botones.pack(fill="x", pady=8)
        ttk.Button(botones, text="⟳ Generar", command=self.generar).pack(
            side="left")
        ttk.Button(botones, text="Copiar", command=self.copiar).pack(
            side="left", padx=5)
        # Mensaje temporal ("¡Copiada!")
        self.var_aviso = tk.StringVar()
        ttk.Label(botones, textvariable=self.var_aviso, foreground="#27ae60").pack(
            side="left", padx=5)

        # Medidor de fortaleza de la contraseña generada
        self.medidor_generada = self._crear_medidor(caja)

    def _crear_evaluador(self):
        """Campo donde el usuario puede escribir y evaluar su propia contraseña."""
        caja = ttk.LabelFrame(self.marco, text="Evalúa tu contraseña", padding=10)
        caja.pack(fill="x")
        self.var_propia = tk.StringVar()
        # trace_add llama a la función cada vez que cambia el texto
        self.var_propia.trace_add(
            "write", lambda *_: self._actualizar_medidor(self.medidor_propia,
                                                         self.var_propia.get()))
        ttk.Entry(caja, textvariable=self.var_propia, show="•",
                  font=("Menlo", 13)).pack(fill="x")
        self.medidor_propia = self._crear_medidor(caja)

    def _crear_historial(self):
        """Lista con las últimas contraseñas generadas."""
        caja = ttk.LabelFrame(self.marco, text="Historial (últimas 5)", padding=10)
        caja.pack(fill="x", pady=(10, 0))
        self.lista = tk.Listbox(caja, height=5, font=("Menlo", 11))
        self.lista.pack(fill="x")

    def _crear_medidor(self, padre):
        """Crea una barra de colores + texto. Devuelve (canvas, variable de texto)."""
        lienzo = tk.Canvas(padre, height=12, width=380, bg="#dddddd",
                           highlightthickness=0)
        lienzo.pack(fill="x", pady=(8, 2))
        texto = tk.StringVar()
        ttk.Label(padre, textvariable=texto).pack(anchor="w")
        return lienzo, texto

    # ------------------------------------------------------------- lógica
    def generar(self):
        """Genera una contraseña nueva con las opciones elegidas."""
        # Conjuntos marcados por el usuario
        elegidos = [CONJUNTOS[n] for n, v in self.vars_conjuntos.items() if v.get()]
        if not elegidos:
            self.var_aviso.set("Elige al menos un tipo de carácter")
            return
        contrasena = generar_contrasena(self.var_largo.get(), elegidos,
                                        self.var_confusos.get())
        self.var_contrasena.set(contrasena)
        self.var_aviso.set("")
        self._actualizar_medidor(self.medidor_generada, contrasena)

        # Agregamos al historial y dejamos solo las 5 más recientes
        self.lista.insert(0, contrasena)
        self.lista.delete(5, "end")

    def copiar(self):
        """Copia la contraseña actual al portapapeles."""
        self.raiz.clipboard_clear()
        self.raiz.clipboard_append(self.var_contrasena.get())
        self.var_aviso.set("¡Copiada!")
        # Borramos el aviso después de 2 segundos
        self.raiz.after(2000, lambda: self.var_aviso.set(""))

    def _actualizar_medidor(self, medidor, contrasena):
        """Dibuja la barra de fortaleza según la entropía de la contraseña."""
        lienzo, texto = medidor
        bits = calcular_entropia(contrasena)
        nombre, color = nivel_de(bits)
        # La barra se llena por completo a los 128 bits
        lienzo.update_idletasks()
        ancho_total = lienzo.winfo_width() or 380
        ancho = ancho_total * min(bits / 128, 1)
        lienzo.delete("all")
        lienzo.create_rectangle(0, 0, ancho, 12, fill=color, width=0)
        if contrasena:
            texto.set(f"{nombre} · {bits:.0f} bits · "
                      f"fuerza bruta: {tiempo_para_descifrar(bits)}")
        else:
            texto.set("")


def main():
    """Crea la ventana y arranca el ciclo de eventos de tkinter."""
    raiz = tk.Tk()
    GeneradorContrasenas(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
