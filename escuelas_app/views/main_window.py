import tkinter as tk
from tkinter import messagebox, Menu, ttk
from escuelas_app.controllers.crud_controller import CrudController
from escuelas_app.utils.helpers import *

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Python CRUD")
        self.controller = CrudController()

        # Configuración de colores
        self.color_fondo = "cyan"
        self.color_texto = "black"
        self.color_fondo_boton = "black"
        self.color_texto_boton = "white"

        # Configuración de la interfaz gráfica
        self.setup_menu()
        self.setup_ui() 

    def setup_menu(self):
        """
        Configura la barra de menú superior.
        """
        barramenu = Menu(self.root)
        self.root.config(menu=barramenu)

        # Menú BBDD
        bbddmenu = Menu(barramenu, tearoff=0)
        bbddmenu.add_command(label="Conectar a la BBDD", command=self.controller.conectar)
        bbddmenu.add_command(label="Listado de alumnos", command=self.controller.listar)
        bbddmenu.add_command(label="Salir", command=self.controller.salir)
        barramenu.add_cascade(label="BBDD", menu=bbddmenu)

        # Menú Gráficas
        grafmenu = Menu(barramenu, tearoff=0)
        grafmenu.add_command(label="Alumnos por escuela", command=self.controller.plot_students_by_school)
        grafmenu.add_command(label="Calificaciones", command=self.controller.plot_school_averages)
        barramenu.add_cascade(label="Gráficas", menu=grafmenu)

        # Menú Limpiar
        limpiarmenu = Menu(barramenu, tearoff=0)
        limpiarmenu.add_command(label="Limpiar campos", command=self.limpiar_campos)
        barramenu.add_cascade(label="Limpiar", menu=limpiarmenu)

        # Menú Acerca de
        infomenu = Menu(barramenu, tearoff=0)
        infomenu.add_command(label="Licencia", command=self.controller.mostrarLicencia)
        infomenu.add_command(label="Acerca de", command=self.controller.mostrarAcercaDe)
        barramenu.add_cascade(label="Acerca de", menu=infomenu)

    def setup_ui(self):
        """
        Configura los campos de entrada, botones y el pie de página.
        """
        # Frame para los campos de entrada
        framecampos = tk.Frame(self.root)
        framecampos.config(bg="cyan")
        framecampos.pack(fill="both", padx=10, pady=10)

        # Variables de Tkinter para los campos de entrada
        self.legajo = tk.StringVar()
        self.apellido = tk.StringVar()
        self.nombre = tk.StringVar()
        self.email = tk.StringVar()
        self.calificacion = tk.DoubleVar()
        self.escuela = tk.StringVar()
        self.localidad = tk.StringVar()
        self.provincia = tk.StringVar()

        # Configuración de los labels y campos de entrada
        self.config_label_entry(framecampos, "N.º de Legajo", self.legajo, 0)
        self.config_label_entry(framecampos, "Apellido", self.apellido, 1)
        self.config_label_entry(framecampos, "Nombre", self.nombre, 2)
        self.config_label_entry(framecampos, "Email", self.email, 3)
        self.config_label_entry(framecampos, "Promedio", self.calificacion, 4)
        
        # Configuración del Combobox para la escuela
        label_escuela = tk.Label(framecampos, text="Escuela")
        label_escuela.config(bg=self.color_fondo, fg=self.color_texto)
        label_escuela.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.combo_escuela = ttk.Combobox(framecampos, textvariable=self.escuela)
        self.combo_escuela.grid(row=5, column=1, padx=10, pady=10, ipadx=50)

        # Cargar las escuelas en el Combobox
        self.cargar_escuelas()

        self.config_label_entry(framecampos, "Localidad", self.localidad, 6)
        self.config_label_entry(framecampos, "Provincia", self.provincia, 7)

        # Frame para los botones
        framebotones = tk.Frame(self.root)
        framebotones.config(bg="black")
        framebotones.pack(fill="both", padx=10, pady=10)

        # Botones CRUD
        botones = [
            ("Crear", lambda: self.controller.crear(self.legajo, self.apellido, self.nombre, self.email, self.calificacion, self.escuela)),
            ("Leer", lambda: self.buscar_legajo()),
            ("Actualizar", lambda: self.controller.actualizar(self.legajo, self.apellido, self.nombre, self.email, self.calificacion, self.escuela)),
            ("Borrar", lambda: self.controller.borrar(self.legajo))
        ]

        for texto, comando in botones:
            boton = tk.Button(framebotones, text=texto, command=comando)
            boton.config(bg="black", fg="white", padx=10, pady=5)
            boton.pack(side="left", padx=5, pady=5)

        # Frame para el pie de página
        framecopy = tk.Frame(self.root)
        framecopy.config(bg="black")
        framecopy.pack(fill="both", padx=10, pady=10)

        # Etiqueta de copyright
        copy_label = tk.Label(framecopy, text="(2023) por Juan Orellana")
        copy_label.config(bg="black", fg="white", padx=10, pady=10)
        copy_label.pack()
        
    def buscar_legajo(self):
        """
        Busca un registro por número de legajo y muestra los datos en los campos de entrada.
        """
        resultado = self.controller.buscar_legajo(self.legajo)
        if resultado:
            legajo, apellido, nombre, email, nota, escuela, localidad, provincia = resultado
            self.legajo.set(legajo)
            self.apellido.set(apellido)
            self.nombre.set(nombre)
            self.email.set(email)
            self.calificacion.set(nota)
            self.escuela.set(escuela)
            self.localidad.set(localidad)
            self.provincia.set(provincia)
        else:
            return mostrar_mensaje("Error", "No se encontró el legajo especificado", tipo="error")
        
    def limpiar_campos(self):
        self.controller.limpiar(
            self.legajo,
            self.apellido,
            self.nombre,
            self.email,
            self.calificacion,
            self.escuela,
            self.localidad,
            self.provincia,
            
        )
    def config_label_entry(self, frame, texto, variable, fila):
        """
        Configura un label y un campo de entrada en la fila especificada.
        """
        label = tk.Label(frame, text=texto)
        label.config(bg=self.color_fondo, fg=self.color_texto)
        label.grid(row=fila, column=0, padx=10, pady=10, sticky="e")

        entry = tk.Entry(frame, textvariable=variable)
        entry.grid(row=fila, column=1, padx=10, pady=10, ipadx=50)
        
    def cargar_escuelas(self):
        """
        Carga las escuelas desde la base de datos y las muestra en el Combobox.
        """
        try:
            escuelas = buscar_escuelas(self.controller.db.con)
            self.combo_escuela["values"] = escuelas
            if escuelas:
                self.combo_escuela.current(0)  # Selecciona la primera escuela por defecto
        except Exception as e:
            mostrar_mensaje("Error", f"No se pudieron cargar las escuelas: {str(e)}", tipo="error")

# Punto de entrada de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()