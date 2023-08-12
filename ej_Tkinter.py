from tkinter import *

raiz = Tk() #Raiz es objeto de la clase tkinter
raiz.title("GUI - Juan Orellana")

#Frame campos
color_fondo = "cyan"
color_letra = "black"

#Frame botones
fondo_framebotones = "plum"
color_fondo_boton = "black"
color_texto_boton = fondo_framebotones

#Barramenu
barramenu = Menu(raiz)
raiz.config(menu = barramenu)

#Menu BBDD
bbddmenu = Menu(barramenu, tearoff=0)
bbddmenu.add_command(label= "Conectar a la BBDD")
bbddmenu.add_command(label= "Listado de alumnos")
bbddmenu.add_command(label= "Salir")

#Menu Graficas
grafmenu = Menu(barramenu, tearoff=0)
grafmenu.add_command(label= "Alumnos por escuela")
grafmenu.add_command(label= "Calificaciones")

#Menu Limpiar
limpiarmenu = Menu(barramenu, tearoff=0)
limpiarmenu.add_command(label="Limpiar campos")

#Menu Acerca de
infomenu = Menu(barramenu, tearoff=0)
infomenu.add_command(label="Licencia")
infomenu.add_command(label="Acerca de")

#Comandos
barramenu.add_cascade(label="BBDD", menu=bbddmenu)
barramenu.add_cascade(label="Graficas", menu=grafmenu)
barramenu.add_cascade(label="Limpiar", menu=limpiarmenu)
barramenu.add_cascade(label="Acerca de", menu=infomenu)

#Frame Campos
framecampos = Frame(raiz)
framecampos.config(bg=color_fondo)
framecampos.pack(fill="both") #Metodo pack es para ensanchar o ajustar a como yo le indique

''' STICKY
        n
    nw      ne
w               e
    sw      se
        s        
'''

#Creo funcion que sirva para configurar todos los labels
def configLabel(mi_label, fila):
    espaciado_labels = {"column":0, "sticky": "e", "padx":10, "pady":10}
    color_labels = {"bg":color_fondo, "fg":color_letra}
    mi_label.grid(row=fila,**espaciado_labels) #**escuela... Me indica que agarra todo lo que esta en los diccionarios
    mi_label.config(**color_labels)


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

raiz.mainloop()