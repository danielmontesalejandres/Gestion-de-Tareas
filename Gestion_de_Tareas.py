import tkinter as tk
from tkinter import messagebox
import sqlite3

#Crear base de datos 
conn = sqlite3.connect('tareas.db')
cursor = conn.cursor()

#Eliminar la tabla si ya existe
cursor.execute('DROP TABLE IF EXISTS tareas')
conn.commit()

#Crear tabla tareas
cursor.execute('''CREATE TABLE IF NOT EXISTS tareas
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                completada BOOLEAN NOT NULL DEFAULT 0 )
                ''')
conn.commit()

class AppGestionTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Tareas")
        self.root.geometry("400x400")

        #Cuadro de entrada para nueva tarea
        self.entrada_tarea = tk.Entry(root, width=40)
        self.entrada_tarea.pack(pady=10)

        #Botones
        self.boton_agregar = tk.Button(root, text="Agregar Tarea", command=self.agregar_tareas)
        self.boton_agregar.pack(pady=5)

        self.boton_eliminar = tk.Button(root, text="Eliminar tarea", command=self.eliminar_tarea)
        self.boton_eliminar.pack(pady=5)

        self.boton_marcar = tk.Button(root, text="Marcar como completada", command=self.marcar_completada)
        self.boton_marcar.pack(pady=5)

        #Lista de tareas
        self.lista_tareas = tk.Listbox(root, selectmode=tk.SINGLE, width=50, height=15)
        self.lista_tareas.pack(pady=10)

        self.cargar_tareas()
    def agregar_tareas(self):
        tarea = self.entrada_tarea.get()
        if tarea:
            cursor.execute("INSERT INTO tareas (descripcion, completada) VALUES (?,0)", (tarea,))
            conn.commit()
            self.entrada_tarea.delete(0, tk.END)
            self.cargar_tareas()
        else:
            messagebox.showwarning("Entrada vacía", "Por favor introducca una tarea.")
    def eliminar_tarea(self):
        try:
            seleccion = self.lista_tareas.curselection()[0]
            tarea_id = self.lista_tareas.get(seleccion).split(" - ")[0]
            cursor.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
            conn.commit()
            self.cargar_tareas()
        except IndexError:
            messagebox.showwarning("Selección inválida", "Porfavor selecciones una tarea para eliminar.")
    def marcar_completada(self):
        try:
            seleccion = self.lista_tareas.curselection()[0]
            tarea_id = self.lista_tareas.get(seleccion).split(" - ")[0]
            cursor.execute("UPDATE tareas SET completada = 1 WHERE id = ?", (tarea_id,))
            conn.commit()
            self.cargar_tareas()
        except IndexError:
            messagebox.showwarning("Selección inválida", "Porfavor selecciones una tarea para marcar como completada.")
    def cargar_tareas(self):
        self.lista_tareas.delete(0, tk.END)
        cursor.execute("SELECT * FROM tareas")
        tareas = cursor.fetchall()
        for tarea in tareas:
            tarea_texto = f"{tarea[0]} - {tarea[1]}"
            if tarea[2]:
                tarea_texto += "(Completada)"
            self.lista_tareas.insert(tk.END, tarea_texto)
# Crear ventana principal 
root = tk.Tk()
app = AppGestionTareas(root)
root.mainloop()

# Cerrar la conexión a la base de datos al cerrar la app
conn.close()
