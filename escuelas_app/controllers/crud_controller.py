from escuelas_app.models.database import Database
from escuelas_app.utils.helpers import validar_campos, mostrar_mensaje, buscar_escuelas, limpiar_campos
from tkinter import messagebox
import sqlite3 as sq3
import matplotlib.pyplot as plt

class CrudController:
    def __init__(self):
        self.db = Database("data/mi_bd_CAC.db")
        self.db.conectar()

    def conectar(self):
        """
        Conecta a la base de datos y muestra un mensaje de confirmación.
        """
        try:
            self.db.conectar()
            return "Conexión exitosa. Comience a operar"
        except Exception as e:
            return f"Error: {str(e)}"
        
    def salir(self):
        """
        Cierra la conexión a la base de datos y sale de la aplicación.
        """
        resp = messagebox.askquestion("Confirme", "¿Seguro que quiere salir?")
        if resp == "yes":
            self.db.cerrar()  # Cierra la conexión a la base de datos
            self.root.destroy()  # Cierra la ventana principal de la aplicación
       
    def listar(self):
        """
        Retorna una lista de todos los alumnos con sus detalles.
        """
        try:
            query = '''
                SELECT a.legajo, a.apellido, a.nombre, a.nota, a.email, e.nombre, e.localidad, e.provincia
                FROM alumnos a
                INNER JOIN escuelas e ON a.id_escuela = e._id
                LIMIT 30
            '''
            resultado = self.db.ejecutar_query(query)
            return resultado
        except Exception as e:
            mostrar_mensaje("Error", str(e), tipo="error")
            return []

    def plot_students_by_school(self):
        """
        Genera un gráfico de barras que muestra la cantidad de alumnos por escuela.
        """
        try:
            query = '''
                SELECT COUNT(a.legajo) AS total, e.nombre
                FROM alumnos a
                INNER JOIN escuelas e ON a.id_escuela = e._id
                GROUP BY e.nombre
                ORDER BY total DESC
            '''
            resultado = self.db.ejecutar_query(query)

            # Extraer los datos para el gráfico
            escuelas = [escuela for total, escuela in resultado]
            total_alumnos = [total for total, escuela in resultado]

            # Crear el gráfico de barras
            plt.bar(escuelas, total_alumnos)
            plt.xlabel("Escuelas")
            plt.ylabel("Cantidad de alumnos")
            plt.title("Alumnos por escuela")
            plt.xticks(rotation=45)  # Rotar los nombres de las escuelas para mejor visualización
            plt.tight_layout()  # Ajustar el layout para que no se corten los textos
            plt.show()
        except Exception as e:
            mostrar_mensaje("Error", str(e), tipo="error")
            
    def plot_school_averages(self):
        """
        Genera un gráfico de barras horizontales que muestra el promedio de calificaciones por escuela.
        """
        try:
            query = '''
                SELECT AVG(a.nota) AS promedio, e.nombre
                FROM alumnos a
                INNER JOIN escuelas e ON a.id_escuela = e._id
                GROUP BY e.nombre
                ORDER BY promedio
            '''
            resultado = self.db.ejecutar_query(query)

            # Extraer los datos para el gráfico
            promedios = [promedio for promedio, escuela in resultado]
            escuelas = [escuela for promedio, escuela in resultado]

            # Crear el gráfico de barras horizontales
            plt.barh(escuelas, promedios, height=0.5)
            plt.xlabel("Promedio de calificaciones")
            plt.ylabel("Escuelas")
            plt.title("Promedio de calificaciones por escuela")

            # Mostrar los valores de los promedios en las barras
            for index, value in enumerate(promedios):
                plt.text(value, index, f"{value:.2f}")

            plt.tight_layout()  # Ajustar el layout para que no se corten los textos
            plt.show()
        except Exception as e:
            mostrar_mensaje("Error", str(e), tipo="error")

    def crear(self, legajo, apellido, nombre, email, calificacion, escuela):
        """
        Crea un nuevo registro en la base de datos.
        
        Parámetros:
        - legajo: Variable de Tkinter (StringVar) con el número de legajo.
        - apellido: Variable de Tkinter (StringVar) con el apellido.
        - nombre: Variable de Tkinter (StringVar) con el nombre.
        - email: Variable de Tkinter (StringVar) con el email.
        - calificacion: Variable de Tkinter (DoubleVar) con la calificación.
        - escuela: Variable de Tkinter (StringVar) con el nombre de la escuela.
        """
        if not validar_campos(legajo, apellido, nombre, email, calificacion, escuela):
            mostrar_mensaje("Error", "Todos los campos son obligatorios", tipo="error")
            return

        try:
            # Obtener el ID de la escuela
            id_escuela = buscar_escuelas(self.db.con, nombre_escuela=escuela.get(), update_shool=True)[0]
            
            # Preparar los datos para la inserción
            datos = (
                id_escuela,
                legajo.get(),
                apellido.get(),
                nombre.get(),
                calificacion.get(),
                email.get()
            )
            
            # Ejecutar la consulta SQL
            self.db.ejecutar_query(
                "INSERT INTO alumnos(id_escuela, legajo, apellido, nombre, nota, email) VALUES (?,?,?,?,?,?)",
                datos
            )
            
            # Mostrar mensaje de éxito
            mostrar_mensaje("Éxito", "Registro agregado correctamente", tipo="info")
            
            # Limpiar los campos de entrada
            limpiar_campos(legajo, apellido, nombre, email, calificacion, escuela)
        except Exception as e:
            # Mostrar mensaje de error
            mostrar_mensaje("Error", str(e), tipo="error")

    def buscar_legajo(self, legajo):
        """
        Busca un registro por número de legajo.
        
        Parámetros:
        - legajo: Variable de Tkinter (StringVar) con el número de legajo.
        
        Retorna:
        - Una tupla con los datos del alumno si se encuentra, o None si no.
        """
        try:
            query = '''
                SELECT a.legajo, a.apellido, a.nombre, a.email, a.nota, e.nombre, e.localidad, e.provincia
                FROM alumnos a
                INNER JOIN escuelas e ON a.id_escuela = e._id
                WHERE a.legajo = ?
            '''
            resultado = self.db.ejecutar_query(query, (legajo.get(),))
            return resultado[0] if resultado else None
        except Exception as e:
            mostrar_mensaje("Error", str(e), tipo="error")
            return None
        
    def actualizar(self, legajo, apellido, nombre, email, calificacion, escuela):
        """
        Actualiza un registro en la base de datos.
        
        Parámetros:
        - legajo: Variable de Tkinter (StringVar) con el número de legajo.
        - apellido: Variable de Tkinter (StringVar) con el apellido.
        - nombre: Variable de Tkinter (StringVar) con el nombre.
        - email: Variable de Tkinter (StringVar) con el email.
        - calificacion: Variable de Tkinter (DoubleVar) con la calificación.
        - escuela: Variable de Tkinter (StringVar) con el nombre de la escuela.
        """
        if not validar_campos(legajo, apellido, nombre, email, calificacion, escuela):
            mostrar_mensaje("Error", "Todos los campos son obligatorios", tipo="error")
            return

        try:
            # Obtener el ID de la escuela
            resultado_escuela = buscar_escuelas(self.db.con, nombre_escuela=escuela.get(), update_shool=True)
            if not resultado_escuela:
                mostrar_mensaje("Error", "La escuela no existe", tipo="error")
                return
            id_escuela = resultado_escuela[0]

            # Preparar los datos para la actualización
            datos = (
                id_escuela,
                apellido.get(),
                nombre.get(),
                calificacion.get(),
                email.get(),
                legajo.get()
            )

            # Depuración: Imprimir los datos antes de la actualización
            print("Datos a actualizar:", datos)

            # Verificar si el legajo existe
            query_verificar = "SELECT COUNT(*) FROM alumnos WHERE legajo = ?"
            resultado = self.db.ejecutar_query(query_verificar, (legajo.get(),))
            if resultado[0][0] == 0:
                mostrar_mensaje("Error", "El legajo no existe", tipo="error")
                return

            # Ejecutar la consulta SQL de actualización
            self.db.ejecutar_query(
                "UPDATE alumnos SET id_escuela=?, apellido=?, nombre=?, nota=?, email=? WHERE legajo=?",
                datos
            )

            # Confirmar los cambios en la base de datos
            self.db.con.commit()

            # Mostrar mensaje de éxito
            mostrar_mensaje("Éxito", "Registro actualizado correctamente", tipo="info")
        except Exception as e:
            # Mostrar mensaje de error
            mostrar_mensaje("Error", str(e), tipo="error")
            
    def limpiar(self, legajo, apellido, nombre, email, calificacion, escuela, localidad, provincia): #, legajo_input
        """
        This function clears all of the input fields and enables the legajo_input widget.
        """
        legajo.set("")
        apellido.set("")
        nombre.set("")
        email.set("")
        calificacion.set("")
        escuela.set("Seleccione")
        localidad.set("")
        provincia.set("")
        #legajo_input.config(state="normal")

    def borrar(self, legajo):
        """
        Borra un registro de la base de datos.
        
        Parámetros:
        - legajo: Variable de Tkinter (StringVar) con el número de legajo.
        """
        try:
            # Ejecutar la consulta SQL
            self.db.ejecutar_query("DELETE FROM alumnos WHERE legajo=?", (legajo.get(),))
            
            # Mostrar mensaje de éxito
            mostrar_mensaje("Éxito", "Registro eliminado correctamente", tipo="info")
        except Exception as e:
            # Mostrar mensaje de error
            mostrar_mensaje("Error", str(e), tipo="error")
            
    def mostrarLicencia(self):
        txt = '''
            Sistema CRUD en Python
            Copyright (C) 2023 - xxxxx xxxx
            Email: juanmarcoso@gmail.com\n
            This program is free software: you can redistribute it 
            and/or modify it under the terms of the GNU General Public 
            License as published by the Free Software Foundation, 
            either version 3 of the License, or (at your option) any 
            later version.
            This program is distributed in the hope that it will be 
            useful, but WITHOUT ANY WARRANTY; without even the 
            implied warranty of MERCHANTABILITY or FITNESS FOR A 
            PARTICULAR PURPOSE.  See the GNU General Public License 
            for more details.
            You should have received a copy of the GNU General Public 
            License along with this program.  
            If not, see <https://www.gnu.org/licenses/>.'''
        messagebox.showinfo("Licencia", txt)
        
    # Acerca de

    def mostrarAcercaDe(self):
        messagebox.showinfo("Sobre esta app", "Creado por Juan Orellana\npara el mundo!")