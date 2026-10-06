"""
Ejercicio 6
Lista de tareas con tkinter: agregar, editar y marcar tareas.

Características:
- Agregar tareas con prioridad (Alta / Media / Baja) y fecha de creación.
- Editar la tarea seleccionada (texto y prioridad).
- Marcar / desmarcar como completada (botón, doble clic o barra espaciadora).
- Eliminar una tarea o limpiar todas las completadas.
- Filtrar: Todas / Pendientes / Completadas.
- Colores según prioridad y tareas completadas en gris.
- Contador de progreso y barra de avance.
- Guardado automático en un archivo JSON (las tareas no se pierden al cerrar).
"""

# json permite guardar y leer las tareas en un archivo de texto
import json
import tkinter as tk
from datetime import datetime
# Path facilita trabajar con rutas de archivos
from pathlib import Path
# ttk ofrece widgets más modernos (Treeview, Combobox, Progressbar)
from tkinter import messagebox, ttk

# El archivo de datos se guarda en la misma carpeta que este script
ARCHIVO_DATOS = Path(__file__).with_name("tareas.json")

# Prioridades disponibles y el color con que se muestran
PRIORIDADES = ["Alta", "Media", "Baja"]
COLORES_PRIORIDAD = {"Alta": "#c0392b", "Media": "#d68910", "Baja": "#1e8449"}

# Símbolos para el estado de la tarea
MARCADA = "☑"
SIN_MARCAR = "☐"


class ListaTareas:
    """Ventana principal de la lista de tareas."""

    def __init__(self, raiz, archivo=ARCHIVO_DATOS):
        self.raiz = raiz
        self.archivo = archivo
        # Cada tarea es un diccionario: {texto, prioridad, hecha, creada}
        self.tareas = self._cargar()
        # Índice de la tarea que se está editando (None = modo "agregar")
        self.editando = None

        raiz.title("Ejercicio 6 · Lista de tareas")
        raiz.geometry("720x480")
        raiz.minsize(600, 400)

        self._crear_formulario()
        self._crear_tabla()
        self._crear_botones()
        self._crear_pie()
        self.refrescar()

    # ------------------------------------------------------------ archivo
    def _cargar(self):
        """Lee las tareas del archivo JSON (si existe)."""
        try:
            return json.loads(self.archivo.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            # Si no existe o está dañado, comenzamos con una lista vacía
            return []

    def _guardar(self):
        """Escribe las tareas en el archivo JSON."""
        # ensure_ascii=False conserva tildes y ñ legibles en el archivo
        self.archivo.write_text(json.dumps(self.tareas, ensure_ascii=False, indent=2),
                                encoding="utf-8")

    # ----------------------------------------------------------------- UI
    def _crear_formulario(self):
        """Campo de texto, selector de prioridad y botón Agregar/Guardar."""
        marco = ttk.Frame(self.raiz, padding=10)
        marco.pack(fill="x")

        ttk.Label(marco, text="Tarea:").pack(side="left")
        self.var_texto = tk.StringVar()
        self.entrada = ttk.Entry(marco, textvariable=self.var_texto)
        self.entrada.pack(side="left", fill="x", expand=True, padx=5)
        # Enter agrega (o guarda) y Escape cancela la edición
        self.entrada.bind("<Return>", lambda _e: self.agregar_o_guardar())
        self.entrada.bind("<Escape>", lambda _e: self.cancelar_edicion())
        self.entrada.focus()

        ttk.Label(marco, text="Prioridad:").pack(side="left")
        self.var_prioridad = tk.StringVar(value="Media")
        # state="readonly" impide escribir valores que no estén en la lista
        ttk.Combobox(marco, textvariable=self.var_prioridad, values=PRIORIDADES,
                     width=7, state="readonly").pack(side="left", padx=5)

        self.boton_agregar = ttk.Button(marco, text="Agregar",
                                        command=self.agregar_o_guardar)
        self.boton_agregar.pack(side="left")

    def _crear_tabla(self):
        """Tabla (Treeview) donde se listan las tareas."""
        marco = ttk.Frame(self.raiz, padding=(10, 0))
        marco.pack(fill="both", expand=True)

        columnas = ("estado", "tarea", "prioridad", "creada")
        # show="headings" oculta la primera columna vacía del Treeview
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings",
                                  selectmode="browse")
        encabezados = {"estado": "✓", "tarea": "Tarea",
                       "prioridad": "Prioridad", "creada": "Creada"}
        anchos = {"estado": 40, "tarea": 380, "prioridad": 90, "creada": 130}
        for columna in columnas:
            self.tabla.heading(columna, text=encabezados[columna])
            # stretch solo para la columna "tarea", que ocupa el espacio sobrante
            self.tabla.column(columna, width=anchos[columna],
                              anchor="w" if columna == "tarea" else "center",
                              stretch=(columna == "tarea"))

        # Estilos (tags) para colorear filas según prioridad o si está completada
        for prioridad, color in COLORES_PRIORIDAD.items():
            self.tabla.tag_configure(prioridad, foreground=color)
        self.tabla.tag_configure("hecha", foreground="#999999")

        # Barra de desplazamiento vertical
        barra = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        # Atajos sobre la tabla
        self.tabla.bind("<Double-1>", lambda _e: self.marcar())
        self.tabla.bind("<space>", lambda _e: self.marcar())
        self.tabla.bind("<Delete>", lambda _e: self.eliminar())
        self.tabla.bind("<BackSpace>", lambda _e: self.eliminar())

    def _crear_botones(self):
        """Botones de acciones y filtros."""
        marco = ttk.Frame(self.raiz, padding=10)
        marco.pack(fill="x")

        # (texto, función) de cada botón de acción
        acciones = [("✔ Marcar / desmarcar", self.marcar),
                    ("✎ Editar", self.editar),
                    ("✖ Eliminar", self.eliminar),
                    ("Limpiar completadas", self.limpiar_completadas)]
        for texto, funcion in acciones:
            ttk.Button(marco, text=texto, command=funcion).pack(side="left", padx=2)

        # Filtros con botones de opción (solo uno puede estar activo)
        self.var_filtro = tk.StringVar(value="Todas")
        for filtro in ("Completadas", "Pendientes", "Todas"):
            ttk.Radiobutton(marco, text=filtro, value=filtro,
                            variable=self.var_filtro,
                            command=self.refrescar).pack(side="right")
        ttk.Label(marco, text="Ver:").pack(side="right")

    def _crear_pie(self):
        """Barra de progreso y contador."""
        marco = ttk.Frame(self.raiz, padding=(10, 0, 10, 10))
        marco.pack(fill="x")
        self.var_contador = tk.StringVar()
        ttk.Label(marco, textvariable=self.var_contador).pack(side="left")
        self.progreso = ttk.Progressbar(marco, maximum=100, length=200)
        self.progreso.pack(side="right")

    # ------------------------------------------------------------- lógica
    def refrescar(self):
        """Vuelve a dibujar la tabla según las tareas y el filtro actual."""
        # Borramos todas las filas actuales
        self.tabla.delete(*self.tabla.get_children())

        filtro = self.var_filtro.get()
        # Ordenamos: primero pendientes, luego por prioridad (Alta, Media, Baja)
        orden = sorted(range(len(self.tareas)),
                       key=lambda i: (self.tareas[i]["hecha"],
                                      PRIORIDADES.index(self.tareas[i]["prioridad"])))
        for indice in orden:
            tarea = self.tareas[indice]
            # Aplicamos el filtro
            if filtro == "Pendientes" and tarea["hecha"]:
                continue
            if filtro == "Completadas" and not tarea["hecha"]:
                continue
            estado = MARCADA if tarea["hecha"] else SIN_MARCAR
            etiqueta = "hecha" if tarea["hecha"] else tarea["prioridad"]
            # Usamos el índice de la lista como id de la fila (iid) para ubicarla
            self.tabla.insert("", "end", iid=str(indice), tags=(etiqueta,),
                              values=(estado, tarea["texto"], tarea["prioridad"],
                                      tarea["creada"]))

        # Actualizamos contador y barra de progreso
        total = len(self.tareas)
        hechas = sum(1 for t in self.tareas if t["hecha"])
        self.var_contador.set(f"{hechas} de {total} tareas completadas"
                              f" · {total - hechas} pendientes")
        self.progreso["value"] = (hechas / total * 100) if total else 0

    def _indice_seleccionado(self):
        """Devuelve el índice de la tarea seleccionada o None (con aviso)."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Primero selecciona una tarea.")
            return None
        return int(seleccion[0])

    def _seleccionar(self, indice):
        """Vuelve a seleccionar una fila después de refrescar (si está visible)."""
        if self.tabla.exists(str(indice)):
            self.tabla.selection_set(str(indice))
            self.tabla.focus(str(indice))

    def agregar_o_guardar(self):
        """Agrega una tarea nueva o guarda los cambios de la que se edita."""
        texto = self.var_texto.get().strip()
        if not texto:
            messagebox.showwarning("Tarea vacía", "Escribe el texto de la tarea.")
            return

        if self.editando is None:
            # Modo agregar: creamos una tarea nueva
            self.tareas.append({
                "texto": texto,
                "prioridad": self.var_prioridad.get(),
                "hecha": False,
                "creada": datetime.now().strftime("%d-%m-%Y %H:%M"),
            })
            indice = len(self.tareas) - 1
        else:
            # Modo edición: actualizamos la tarea existente
            indice = self.editando
            self.tareas[indice]["texto"] = texto
            self.tareas[indice]["prioridad"] = self.var_prioridad.get()

        self.cancelar_edicion()   # limpia el formulario y vuelve al modo agregar
        self._guardar()
        self.refrescar()
        self._seleccionar(indice)

    def editar(self):
        """Carga la tarea seleccionada en el formulario para modificarla."""
        indice = self._indice_seleccionado()
        if indice is None:
            return
        self.editando = indice
        self.var_texto.set(self.tareas[indice]["texto"])
        self.var_prioridad.set(self.tareas[indice]["prioridad"])
        # Cambiamos el botón para que el usuario sepa que está editando
        self.boton_agregar.configure(text="Guardar")
        self.entrada.focus()
        # Seleccionamos todo el texto para reemplazarlo fácilmente
        self.entrada.select_range(0, "end")

    def cancelar_edicion(self):
        """Limpia el formulario y vuelve al modo 'agregar'."""
        self.editando = None
        self.var_texto.set("")
        self.boton_agregar.configure(text="Agregar")

    def marcar(self):
        """Alterna el estado completada/pendiente de la tarea seleccionada."""
        indice = self._indice_seleccionado()
        if indice is None:
            return
        # not invierte el valor booleano
        self.tareas[indice]["hecha"] = not self.tareas[indice]["hecha"]
        self._guardar()
        self.refrescar()
        self._seleccionar(indice)

    def eliminar(self):
        """Elimina la tarea seleccionada previa confirmación."""
        indice = self._indice_seleccionado()
        if indice is None:
            return
        texto = self.tareas[indice]["texto"]
        if messagebox.askyesno("Eliminar", f"¿Eliminar la tarea “{texto}”?"):
            del self.tareas[indice]
            self.cancelar_edicion()
            self._guardar()
            self.refrescar()

    def limpiar_completadas(self):
        """Elimina todas las tareas marcadas como completadas."""
        hechas = sum(1 for t in self.tareas if t["hecha"])
        if hechas == 0:
            messagebox.showinfo("Nada que limpiar", "No hay tareas completadas.")
            return
        if messagebox.askyesno("Limpiar", f"¿Eliminar {hechas} tarea(s) completada(s)?"):
            # Nos quedamos solo con las pendientes
            self.tareas = [t for t in self.tareas if not t["hecha"]]
            self.cancelar_edicion()
            self._guardar()
            self.refrescar()


def main():
    """Crea la ventana y arranca el ciclo de eventos de tkinter."""
    raiz = tk.Tk()
    ListaTareas(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
