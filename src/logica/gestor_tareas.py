import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# Clase para representar una tarea individual
class Tarea:
    def __init__(self, titulo, descripcion, fecha_inicio, fecha_limite):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_limite = fecha_limite
        self.completada = False

    def __str__(self):
        estado = "Completada" if self.completada else "Pendiente"
        fecha_inicio_str = self.fecha_inicio.strftime("%d-%m %H:%M")
        fecha_limite_str = self.fecha_limite.strftime("%d-%m %H:%M")
        return f"{self.titulo} - {estado} (Inicio: {fecha_inicio_str}, Límite: {fecha_limite_str})"


# Clase para gestionar una lista de tareas
class GestorTareas:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, titulo, descripcion, fecha_inicio, fecha_limite):
        if not titulo:
            raise ValueError("El título no puede estar vacío")
        if len(titulo) > 50:
            raise ValueError("El título es demasiado largo")
        if len(descripcion) > 200:
            raise ValueError("La descripción es demasiado larga")

        # Validar formato de fechas
        fecha_inicio_dt = self._parse_fecha(fecha_inicio)
        fecha_limite_dt = self._parse_fecha(fecha_limite)
        if fecha_limite_dt < fecha_inicio_dt:
            raise ValueError("La fecha límite no puede ser anterior a la fecha de inicio")

        # Agregar tarea a la lista
        tarea = Tarea(titulo, descripcion, fecha_inicio_dt, fecha_limite_dt)
        self.tareas.append(tarea)

    def obtener_tareas(self):
        return self.tareas

    def marcar_completada(self, indice):
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].completada = True
        else:
            raise IndexError("Índice fuera de rango")

    def eliminar_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            del self.tareas[indice]
        else:
            raise IndexError("Índice fuera de rango")

    @staticmethod
    def _parse_fecha(fecha_str):
        try:
            return datetime.strptime(fecha_str, "%d-%m %H:%M")
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use DD-MM HH:MM")


# Clase para la interfaz gráfica del gestor de tareas
class GestorTareasGUI:
    def __init__(self, root, gestor):
        self.gestor = gestor
        self.root = root
        self.root.title("Gestor de Tareas")

        self._crear_widgets()
        self._configurar_layout()
        self.actualizar_lista()

    def _crear_widgets(self):
        # Entradas y etiquetas para título, descripción y fechas
        self.titulo_label = ttk.Label(self.root, text="Título:")
        self.titulo_entry = ttk.Entry(self.root, width=30)

        self.descripcion_label = ttk.Label(self.root, text="Descripción:")
        self.descripcion_entry = ttk.Entry(self.root, width=60)

        self.fecha_inicio_label = ttk.Label(self.root, text="Fecha de Inicio (DD-MM HH:MM):")
        self.fecha_inicio_entry = ttk.Entry(self.root, width=20)

        self.fecha_limite_label = ttk.Label(self.root, text="Fecha Límite (DD-MM HH:MM):")
        self.fecha_limite_entry = ttk.Entry(self.root, width=20)

        # Botones de acción
        self.agregar_btn = ttk.Button(self.root, text="Agregar Tarea", command=self.agregar_tarea)
        self.completar_btn = ttk.Button(self.root, text="Marcar como Completada", command=self.marcar_completada)
        self.eliminar_btn = ttk.Button(self.root, text="Eliminar Tarea", command=self.eliminar_tarea)
        self.salir_btn = ttk.Button(self.root, text="Salir", command=self.root.quit)

        # Listbox con scrollbar para mostrar las tareas
        self.tareas_listbox = tk.Listbox(self.root, height=10, width=80)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tareas_listbox.yview)
        self.tareas_listbox.config(yscrollcommand=self.scrollbar.set)

    def _configurar_layout(self):
        # Organizar los widgets en la ventana
        self.titulo_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.titulo_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        self.descripcion_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.descripcion_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        self.fecha_inicio_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.fecha_inicio_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        self.fecha_limite_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.fecha_limite_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        self.agregar_btn.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        self.completar_btn.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        self.eliminar_btn.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        self.salir_btn.grid(row=7, column=1, sticky=tk.W, padx=5, pady=5)

        self.tareas_listbox.grid(row=8, column=1, sticky=tk.W, padx=5, pady=5)
        self.scrollbar.grid(row=8, column=2, sticky=(tk.N, tk.S))

    def agregar_tarea(self):
        titulo = self.titulo_entry.get().strip()
        descripcion = self.descripcion_entry.get().strip()
        fecha_inicio = self.fecha_inicio_entry.get().strip()
        fecha_limite = self.fecha_limite_entry.get().strip()

        try:
            self.gestor.agregar_tarea(titulo, descripcion, fecha_inicio, fecha_limite)
            self.actualizar_lista()
            self._limpiar_campos()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_lista(self):
        self.tareas_listbox.delete(0, tk.END)
        for indice, tarea in enumerate(self.gestor.obtener_tareas()):
            tarea_str = f"{indice + 1}. {tarea}"
            self.tareas_listbox.insert(tk.END, tarea_str)
            if tarea.completada:
                self.tareas_listbox.itemconfig(tk.END, {'fg': 'gray'})

    def marcar_completada(self):
        seleccion = self.tareas_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            self.gestor.marcar_completada(indice)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para marcar como completada")

    def eliminar_tarea(self):
        seleccion = self.tareas_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            if messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar esta tarea?"):
                self.gestor.eliminar_tarea(indice)
                self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para eliminar")

    def _limpiar_campos(self):
        self.titulo_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)
        self.fecha_inicio_entry.delete(0, tk.END)
        self.fecha_limite_entry.delete(0, tk.END)


def run():
    root = tk.Tk()
    gestor = GestorTareas()
    app = GestorTareasGUI(root, gestor)
    root.mainloop()


if __name__ == "__main__":
    run()
