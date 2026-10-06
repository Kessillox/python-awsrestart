"""
Ejercicio 7 (inventado)
Juego del Gato (Tic-Tac-Toe) con tkinter.

Características:
- Modo 2 jugadores o contra la computadora.
- Dos niveles de dificultad para la computadora:
    · Fácil: juega al azar.
    · Imposible: usa el algoritmo Minimax (nunca pierde).
- Marcador de victorias y empates.
- Resalta la línea ganadora.
- Alterna quién comienza en cada partida.
"""

# random se usa para el nivel fácil y para variar las jugadas de la IA
import random
import tkinter as tk

# Todas las combinaciones ganadoras: índices de las casillas (0..8)
#  0 | 1 | 2
#  3 | 4 | 5
#  6 | 7 | 8
LINEAS_GANADORAS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # filas
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columnas
    (0, 4, 8), (2, 4, 6),             # diagonales
]

# Colores de la interfaz
COLOR_FONDO = "#14213d"
COLOR_CASILLA = "#e5e5e5"
COLOR_X = "#d62828"
COLOR_O = "#1d3557"
COLOR_GANADORA = "#fcbf49"


def ganador(tablero):
    """Devuelve ('X' u 'O', línea) si alguien ganó, ('empate', None) o (None, None)."""
    for a, b, c in LINEAS_GANADORAS:
        # Las tres casillas tienen el mismo símbolo y no están vacías
        if tablero[a] and tablero[a] == tablero[b] == tablero[c]:
            return tablero[a], (a, b, c)
    # Si no quedan casillas vacías, es empate
    if all(tablero):
        return "empate", None
    return None, None


def minimax(tablero, turno, ia):
    """
    Algoritmo Minimax: prueba todas las jugadas posibles hasta el final
    del juego y devuelve (puntaje, mejor_casilla).
    Puntaje: +10 si gana la IA, -10 si gana el humano, 0 si empate.
    Se resta/suma la profundidad para preferir ganar rápido y perder tarde.
    """
    resultado, _ = ganador(tablero)
    if resultado == ia:
        return 10, None
    if resultado == "empate":
        return 0, None
    if resultado is not None:
        return -10, None

    humano = "O" if ia == "X" else "X"
    mejor_casilla = None
    # La IA busca maximizar el puntaje; el humano, minimizarlo
    mejor_puntaje = -100 if turno == ia else 100

    # Casillas vacías mezcladas para que la IA no juegue siempre igual
    vacias = [i for i, v in enumerate(tablero) if not v]
    random.shuffle(vacias)

    for casilla in vacias:
        # Probamos la jugada...
        tablero[casilla] = turno
        siguiente = humano if turno == ia else ia
        puntaje, _ = minimax(tablero, siguiente, ia)
        # ...y la deshacemos para probar la siguiente
        tablero[casilla] = ""
        # Ajuste por profundidad: un resultado lejano vale un poco menos
        puntaje -= 1 if puntaje > 0 else (-1 if puntaje < 0 else 0)

        if (turno == ia and puntaje > mejor_puntaje) or \
                (turno != ia and puntaje < mejor_puntaje):
            mejor_puntaje, mejor_casilla = puntaje, casilla

    return mejor_puntaje, mejor_casilla


class JuegoGato:
    """Ventana del juego."""

    def __init__(self, raiz):
        self.raiz = raiz
        # El tablero es una lista de 9 textos: "", "X" u "O"
        self.tablero = [""] * 9
        # Marcador acumulado
        self.marcador = {"X": 0, "O": 0, "empate": 0}
        # Quién comienza la próxima partida (se alterna)
        self.comienza = "X"
        self.turno = "X"
        self.terminado = False
        # Id de la jugada pendiente de la computadora (para poder cancelarla)
        self.jugada_pendiente = None

        raiz.title("Ejercicio 7 · Juego del Gato")
        raiz.configure(bg=COLOR_FONDO, padx=15, pady=15)
        raiz.resizable(False, False)

        self._crear_opciones()
        self._crear_tablero()
        self._crear_estado()
        self.nueva_partida()

    # ----------------------------------------------------------------- UI
    def _crear_opciones(self):
        """Selector de modo y dificultad."""
        marco = tk.Frame(self.raiz, bg=COLOR_FONDO)
        marco.pack(fill="x", pady=(0, 10))

        # Modo de juego
        self.var_modo = tk.StringVar(value="ia")
        for texto, valor in (("vs Computadora", "ia"), ("2 Jugadores", "dos")):
            tk.Radiobutton(marco, text=texto, value=valor, variable=self.var_modo,
                           command=self.reiniciar_marcador, bg=COLOR_FONDO,
                           fg="white", selectcolor=COLOR_FONDO,
                           activebackground=COLOR_FONDO).pack(side="left")

        # Dificultad (solo aplica contra la computadora)
        self.var_dificultad = tk.StringVar(value="Imposible")
        tk.OptionMenu(marco, self.var_dificultad, "Fácil", "Imposible").pack(
            side="right")
        tk.Label(marco, text="Dificultad:", bg=COLOR_FONDO, fg="white").pack(
            side="right")

    def _crear_tablero(self):
        """Crea las 9 casillas del tablero en una grilla de 3x3."""
        marco = tk.Frame(self.raiz, bg=COLOR_FONDO)
        marco.pack()
        self.casillas = []
        for i in range(9):
            # Label en vez de Button para que los colores funcionen en macOS
            casilla = tk.Label(marco, text="", width=4, height=2,
                               font=("Helvetica", 40, "bold"),
                               bg=COLOR_CASILLA, cursor="hand2")
            # divmod(i, 3) entrega (fila, columna) de la casilla i
            fila, columna = divmod(i, 3)
            casilla.grid(row=fila, column=columna, padx=4, pady=4)
            casilla.bind("<Button-1>", lambda _e, n=i: self.jugar_humano(n))
            self.casillas.append(casilla)

    def _crear_estado(self):
        """Mensaje de turno, marcador y botones."""
        self.var_estado = tk.StringVar()
        tk.Label(self.raiz, textvariable=self.var_estado, bg=COLOR_FONDO,
                 fg="white", font=("Helvetica", 16, "bold")).pack(pady=(10, 0))

        self.var_marcador = tk.StringVar()
        tk.Label(self.raiz, textvariable=self.var_marcador, bg=COLOR_FONDO,
                 fg=COLOR_GANADORA, font=("Helvetica", 13)).pack(pady=5)

        botones = tk.Frame(self.raiz, bg=COLOR_FONDO)
        botones.pack()
        tk.Button(botones, text="Nueva partida",
                  command=self.nueva_partida).pack(side="left", padx=5)
        tk.Button(botones, text="Reiniciar marcador",
                  command=self.reiniciar_marcador).pack(side="left", padx=5)

    # ------------------------------------------------------------- lógica
    def contra_ia(self):
        """True si se está jugando contra la computadora."""
        return self.var_modo.get() == "ia"

    def nueva_partida(self):
        """Limpia el tablero y comienza otra partida."""
        # Si la computadora tenía una jugada programada, la cancelamos para que
        # no aparezca en la partida nueva
        if self.jugada_pendiente:
            self.raiz.after_cancel(self.jugada_pendiente)
            self.jugada_pendiente = None
        self.tablero = [""] * 9
        self.terminado = False
        self.turno = self.comienza
        # La próxima partida la comienza el otro jugador
        self.comienza = "O" if self.comienza == "X" else "X"
        for casilla in self.casillas:
            casilla.configure(text="", bg=COLOR_CASILLA)
        self._actualizar_textos()
        # En modo IA el humano es X; si comienza O, juega la computadora
        if self.contra_ia() and self.turno == "O":
            self.jugada_pendiente = self.raiz.after(400, self.jugar_ia)

    def reiniciar_marcador(self):
        """Pone el marcador en cero y empieza de nuevo."""
        self.marcador = {"X": 0, "O": 0, "empate": 0}
        self.comienza = "X"
        self.nueva_partida()

    def jugar_humano(self, casilla):
        """Se ejecuta al hacer clic en una casilla."""
        # Ignoramos clics si terminó, si la casilla está ocupada
        # o si es el turno de la computadora
        if self.terminado or self.tablero[casilla]:
            return
        if self.contra_ia() and self.turno == "O":
            return
        self._marcar(casilla)
        # Si sigue el juego y es contra la IA, la computadora responde
        if not self.terminado and self.contra_ia():
            # after() espera un momento para que parezca que "piensa"
            self.jugada_pendiente = self.raiz.after(400, self.jugar_ia)

    def jugar_ia(self):
        """Turno de la computadora (siempre juega con O)."""
        self.jugada_pendiente = None
        if self.terminado:
            return
        vacias = [i for i, v in enumerate(self.tablero) if not v]
        if self.var_dificultad.get() == "Fácil":
            casilla = random.choice(vacias)
        elif len(vacias) == 9:
            # Con el tablero vacío Minimax revisaría ~550.000 jugadas; sabemos
            # que el centro o una esquina son las mejores aperturas.
            casilla = random.choice([0, 2, 4, 6, 8])
        else:
            # Pasamos una copia para no modificar el tablero real
            _, casilla = minimax(self.tablero[:], "O", "O")
        self._marcar(casilla)

    def _marcar(self, casilla):
        """Coloca el símbolo del turno actual y revisa si terminó el juego."""
        simbolo = self.turno
        self.tablero[casilla] = simbolo
        self.casillas[casilla].configure(
            text=simbolo, fg=COLOR_X if simbolo == "X" else COLOR_O)

        resultado, linea = ganador(self.tablero)
        if resultado:
            self.terminado = True
            self.marcador[resultado] += 1
            # Pintamos la línea ganadora
            if linea:
                for i in linea:
                    self.casillas[i].configure(bg=COLOR_GANADORA)
            self._actualizar_textos(resultado)
        else:
            # Cambiamos de turno
            self.turno = "O" if simbolo == "X" else "X"
            self._actualizar_textos()

    def _actualizar_textos(self, resultado=None):
        """Actualiza el mensaje de estado y el marcador."""
        # Nombres a mostrar según el modo
        nombres = ({"X": "Tú (X)", "O": "Computadora (O)"} if self.contra_ia()
                   else {"X": "Jugador X", "O": "Jugador O"})
        if resultado == "empate":
            self.var_estado.set("¡Empate!")
        elif resultado:
            self.var_estado.set(f"¡Gana {nombres[resultado]}!")
        else:
            self.var_estado.set(f"Turno de {nombres[self.turno]}")
        self.var_marcador.set(f"{nombres['X']}: {self.marcador['X']}   "
                              f"{nombres['O']}: {self.marcador['O']}   "
                              f"Empates: {self.marcador['empate']}")


def main():
    """Crea la ventana y arranca el ciclo de eventos de tkinter."""
    raiz = tk.Tk()
    JuegoGato(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
