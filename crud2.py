#Create Read Update Delete
from tkinter import *
from tkinter import messagebox
from tkinter import Frame, Button
import sqlite3 as sq3
import matplotlib.pyplot as plt
#import pylint

'''
*************************
    PARTE FUNCIONAL
*************************
'''
#****************** FUNCIONES VARIAS *********************

def buscar_escuelas(update_shool):
    try:
        con = sq3.connect("mi_bd_CAC.db") 
        cur = con.cursor() 
        if update_shool: 
            cur.execute("SELECT _id, localidad, provincia FROM escuelas  WHERE nombre =?", (escuela.get(),))
        else:   #Opcion que solo va a llenar lista desplegable de escuela en el menu
            cur.execute("SELECT nombre FROM escuelas")
        
        resultado = cur.fetchall() #recibe una lista de tuplas con un elemento "fantasma"
        retorno = [e[0] for e in resultado] #List comprehension
        con.close()
        return retorno
    except Exception as e:
        messagebox.showerror("Error", str(e))

#****************** MENU ******************

# BBDD

# Conectar        

def conectar():
    """
    Esta funcion conecta con la base de datos y devuelve un mensaje de conexion
    
    """
    try:
        with sq3.connect("mi_bd_CAC.db") as con:
            cur = con.cursor()
            messagebox.showinfo("Status", "Conexión exitosa. Comience a operar")
    except Exception as e:
        messagebox.showerror("Error", str(e))

    return cur
    
#   Listar

def listar():

    class Table():
        def __init__(self, ubicacion, num_rows, num_cols):
            nombre_cols = ['Legajo', 'Apellido', 'Nombre', 'Promedio', 'Email', 'Escuela', 'Localidad', 'Provincia']
            for i in range(num_cols):
                self.e = Entry(ubicacion)
                self.e.config(bg='black', fg='white')
                self.e.grid(row=0, column=i)
                self.e.insert(END, nombre_cols[i])

            for fila in range(num_rows):
                for col in range(num_cols):
                    self.e = Entry(ubicacion)
                    self.e.grid(row=fila + 1, column=col)
                    self.e.insert(END, resultado[fila][col])
                    self.e.config(state='readonly')

    raiz2 = Tk()
    raiz2.title('Listado alumnos')
    frameppa1 = Frame(raiz2)
    frameppa1.pack(fill='both')
    framecerrar = Frame(raiz2)
    framecerrar.config(bg=color_texto_boton)
    framecerrar.pack(fill='both')

    boton_cerrar = Button(framecerrar, text='Cerrar', command=raiz2.destroy)
    boton_cerrar.config(bg=color_fondo_boton, fg=color_texto_boton, pady=10, padx=0)
    boton_cerrar.pack(fill='both')

    con = sq3.connect('mi_bd_CAC.db')
    cur = con.cursor()
    query1 = '''
            SELECT alumnos.legajo, alumnos.apellido, alumnos.nombre, alumnos.nota, alumnos.email, escuelas.nombre, escuelas.localidad, escuelas.provincia 
            FROM alumnos INNER JOIN escuelas 
            ON alumnos.id_escuela = escuelas._id LIMIT 30'''

    cur.execute(query1)
    resultado = cur.fetchall()
    num_rows = len(resultado)
    num_cols = len(resultado[0])

    tabla = Table(frameppa1, num_rows, num_cols)
    con.close()
    raiz2.mainloop()

#if __name__ == '__main__':
#    listar()

#   Salir

def salir():
    resp = messagebox.askquestion("Confirme", "Seguro que quiere salir?")
    con = sq3.connect("mi_bd_CAC.db") 
    if resp == "yes":
        con.close()
        raiz.destroy()
        
#Graficas

#Alumnos por escuela

def plot_students_by_school():
    with sq3.connect("mi_bd_CAC.db") as con:
        cur = con.cursor()
        """
        Esta funcion imprime los numeros de estudiante por escuela
        """
        try:
            query_buscar = '''SELECT COUNT(alumnos.legajo) AS "total", escuelas.nombre FROM 
            alumnos INNER JOIN escuelas 
            ON alumnos.id_escuela=escuelas._id
            GROUP BY escuelas.nombre
            ORDER BY total DESC'''
            cur.execute(query_buscar)
            resultado = cur.fetchall()

            cantAlumn = []
            escuela = []

            for i in resultado:
                cantAlumn.append(i[0])
                escuela.append(i[1])

            plt.bar(escuela, cantAlumn)
            plt.xticks(rotation=45)
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

#Promedio por escuela

def plot_school_averages():
    with sq3.connect("mi_bd_CAC.db") as con:
        cur = con.cursor()
        query_buscar = '''SELECT AVG (alumnos.nota) AS "promedio", escuelas.nombre FROM alumnos INNER JOIN escuelas ON alumnos.id_escuela = escuelas._id GROUP BY escuelas.nombre ORDER BY promedio'''
        try:
            cur.execute(query_buscar)
            resultado = cur.fetchall()

            promedio = []
            school = []

            for i in resultado:
                promedio.append(i[0])
                school.append(i[1])

            plt.barh(school, promedio, height=0.5)

            for index, value in enumerate(promedio):
                plt.text(value, index, 
                 round(float(value), 2))
                
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# LIMPIAR

def limpiar():
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
    legajo_input.config(state="normal")

# ACERCA DE

# Licencia

def mostrarLicencia():
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

def mostrarAcercaDe():
    messagebox.showinfo("Sobre esta app", "Creado por Juan Orellana\npara el mundo!")

# **************** MENU CRUD (CREATE - READ - UPDATE - DELETE) ****************

# CREAR

def crear():
    with sq3.connect("mi_bd_CAC.db") as con:
        cur = con.cursor()
        try:
            id_escuela = int(buscar_escuelas(True)[0])
            datos = id_escuela, legajo.get(), apellido.get(), nombre.get(), calificacion.get(), email.get()
            cur.execute("INSERT INTO alumnos(id_escuela, legajo, apellido, nombre, nota, email) VALUES (?,?,?,?,?,?)", datos)
            con.commit()
            messagebox.showinfo("Status", "Registro agregado")
            limpiar()
        except Exception as e:
            messagebox.showerror("Error", str(e))


# LEER

def buscarLegajo():
    query_buscar = '''SELECT a.legajo, a.apellido, a.nombre, a.email, a.nota, e.nombre, e.localidad, e.provincia FROM alumnos a INNER JOIN escuelas e ON e._id=a.id_escuela WHERE a.legajo= ?'''
    try:
        con = sq3.connect("mi_bd_CAC.db")
        cur = con.cursor()
        cur.execute(query_buscar, (legajo.get(),))
        resultado = cur.fetchall()
        if resultado == []:
            messagebox.showerror("NO ENCONTRADO", "No se encuentra ese numero de legajo")
        else:
            legajo.set(resultado[0][0])
            apellido.set(resultado[0][1])
            nombre.set(resultado[0][2])
            email.set(resultado[0][3])
            calificacion.set(resultado[0][4])
            escuela.set(resultado[0][5])
            localidad.set(resultado[0][6])
            provincia.set(resultado[0][7])
            legajo_input.config(state="disabled")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        con.close()

# ACTUALIZAR

def actualizar():
    try:
        con = sq3.connect("mi_bd_CAC.db")
        id_escuela = int(buscar_escuelas(True)[0])
        datos2 = id_escuela, apellido.get(), nombre.get(), calificacion.get(), email.get()
        with con:
            cur = con.cursor()
            cur.execute("UPDATE alumnos set id_escuela=?, apellido=?, nombre=?, nota=?, email=? WHERE legajo = ?", datos2)
            con.commit()
            messagebox.showinfo("Status", "Registro actualizado")
            limpiar()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# BORRAR

def borrar():
    resp = messagebox.askquestion("Borrar", "¿Segura/o que desea borrar el registro?")
    if resp == "yes":
        with sq3.connect("mi_bd_CAC.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM alumnos WHERE legajo =" + legajo.get())
            con.commit()
            messagebox.showinfo("Stats", "Registro eliminado correctamente")
            limpiar()

'''
*************************
    INTERFAZ GRAFICA
*************************
'''

# Frame botones
fondo_framebotones = "plum"
color_fondo_boton = "black"
color_texto_boton = fondo_framebotones

raiz = Tk()
raiz.title("GUI - Juan Orellana")

# Frame campos
color_fondo = "cyan"
color_letra = "black"

# Barra de menú
barramenu = Menu(raiz)
raiz.config(menu=barramenu)

# Menú BBDD
bbddmenu = Menu(barramenu, tearoff=0)
bbddmenu.add_command(label="Conectar a la BBDD", command=conectar)
bbddmenu.add_command(label="Listado de alumnos", command=listar)
bbddmenu.add_command(label="Salir", command=salir)

# Menú Gráficas
grafmenu = Menu(barramenu, tearoff=0)
grafmenu.add_command(label="Alumnos por escuela", command=plot_students_by_school)
grafmenu.add_command(label="Calificaciones", command=plot_school_averages)

# Menú Limpiar
limpiarmenu = Menu(barramenu, tearoff=0)
limpiarmenu.add_command(label="Limpiar campos", command=limpiar)

# Menú Acerca de
infomenu = Menu(barramenu, tearoff=0)
infomenu.add_command(label="Licencia", command=mostrarLicencia)
infomenu.add_command(label="Acerca de", command=mostrarAcercaDe)

# Comandos
barramenu.add_cascade(label="BBDD", menu=bbddmenu)
barramenu.add_cascade(label="Gráficas", menu=grafmenu)
barramenu.add_cascade(label="Limpiar", menu=limpiarmenu)
barramenu.add_cascade(label="Acerca de", menu=infomenu)

# Frame Campos
framecampos = Frame(raiz)
framecampos.config(bg=color_fondo)
framecampos.pack(fill="both")

# Función para configurar los labels
def configLabel(mi_label, fila):
    espaciado_labels = {"column": 0, "sticky": "e", "padx": 10, "pady": 10}
    color_labels = {"bg": color_fondo, "fg": color_letra}
    mi_label.grid(row=fila, **espaciado_labels)
    mi_label.config(**color_labels)
        
#Variables
legajo = StringVar()
apellido = StringVar()
nombre = StringVar()
email = StringVar()
calificacion = DoubleVar()
escuela = StringVar()
localidad = StringVar()
provincia = StringVar()

#Configuracion de los botones
legajo_label = Label(framecampos, text= "N° de legajo")
configLabel(legajo_label, 0)
apellido_label = Label(framecampos, text= "Apellido")
configLabel(apellido_label, 1)
nombre_label = Label(framecampos, text= "Nombre")
configLabel(nombre_label, 2)
email_label = Label(framecampos, text= "Email")
configLabel(email_label, 3)
promedio_label = Label(framecampos, text= "Promedio")
configLabel(promedio_label, 4)
escuela_label = Label(framecampos, text= "Escuela")
configLabel(escuela_label, 5)
localidad_label = Label(framecampos, text= "Localidad")
configLabel(localidad_label, 6)
provincia_label = Label(framecampos, text= "Provincia")
configLabel(provincia_label, 7)        

#Entrada
def config_input(mi_input, fila):
    espaciado_inputs = {"column":1, "padx":10, "pady":10, "ipadx":50}
    mi_input.grid(row = fila, **espaciado_inputs)
    
legajo_input = Entry(framecampos, textvariable=legajo)
apellido_input = Entry(framecampos, textvariable=apellido)
nombre_input = Entry(framecampos, textvariable=nombre)
email_input = Entry(framecampos, textvariable=email)
calificacion_input = Entry(framecampos, textvariable=calificacion)

#Menu desplegable

escuelas = buscar_escuelas(False)
escuela.set("Seleccione")
escuela_option = OptionMenu(framecampos, escuela, *escuelas)
escuela_option.grid(row=5, column=1, padx=10, pady=10, sticky='w', ipadx=50)

localidad_input = Entry(framecampos, textvariable=localidad)
localidad_input.config(state='readonly')
provincia_input = Entry(framecampos, textvariable=provincia)
provincia_input.config(state='readonly')

#Menu desplegable

entries = [
    legajo_input,
    apellido_input,
    nombre_input,
    email_input,
    calificacion_input,
    escuela_option,
    localidad_input,
    provincia_input,
]

for e in range(len(entries)):
    if entries[e] == "escuela_option":
        continue
    else:
        config_input(entries[e], e)
        
#FrameBotones
        

fondo_framebotones = "plum"
color_fondo_boton = "black"
color_texto_boton = fondo_framebotones

espaciado_buttons = {
    'row': 0,
    'padx': 5,
    'pady': 10,
    'ipadx': 12,
}

def config_button(button, **kwargs):
    button.config(bg=color_fondo_boton, fg=color_texto_boton, **kwargs)

framebotones = Frame(raiz)
framebotones.config(bg=fondo_framebotones)
framebotones.pack(fill='both')

botones = [
    Button(framebotones, text='Crear', command=crear),
    Button(framebotones, text='Buscar', command=buscarLegajo),
    Button(framebotones, text='Actualizar', command=actualizar),
    Button(framebotones, text='Eliminar', command=borrar),
]

for button in botones:
    config_button(button)
    
# *************** FRAMECOPY *******************

label_formatting = {
    'bg': 'black',
    'fg': 'white',
    'padx': 10,
    'pady': 10,
}

def config_label(label, **kwargs):
    label.config(**kwargs)

copyright_frame = Frame(raiz)
copyright_frame.config(bg='black')
copyright_frame.pack(fill='both')

copylabel = Label(copyright_frame, text="(2023) Por Juan Orellana")
config_label(copylabel, **label_formatting)

raiz.mainloop()
