from tkinter import messagebox

def buscar_escuelas(con, nombre_escuela=None, update_shool=False):
    """
    Busca escuelas en la base de datos.
    
    Parámetros:
    - con: Conexión a la base de datos.
    - nombre_escuela: Nombre de la escuela a buscar (opcional).
    - update_shool: Si es True, busca detalles completos de la escuela.
    
    Retorna:
    - Lista de nombres de escuelas o detalles de una escuela específica.
    """
    try:
        cur = con.cursor()
        if update_shool and nombre_escuela:
            # Busca detalles completos de la escuela
            cur.execute("SELECT _id, localidad, provincia FROM escuelas WHERE nombre =?", (nombre_escuela,))
        else:
            # Busca solo los nombres de las escuelas
            cur.execute("SELECT nombre FROM escuelas")
        
        resultado = cur.fetchall()
        return [e[0] for e in resultado]  # Retorna una lista de nombres o detalles
    except Exception as e:
        raise e


def limpiar_campos(*campos):
    """
    Limpia los campos de entrada de la interfaz gráfica.
    
    Parámetros:
    - campos: Una lista de variables de Tkinter (StringVar, DoubleVar, etc.).
    """
    for campo in campos:
        campo.set("")


def mostrar_mensaje(titulo, mensaje, tipo="info"):
    """
    Muestra un mensaje en una ventana emergente.
    
    Parámetros:
    - titulo: Título de la ventana.
    - mensaje: Mensaje a mostrar.
    - tipo: Tipo de mensaje ("info", "error", "warning").
    """
    from tkinter import messagebox

    if tipo == "info":
        messagebox.showinfo(titulo, mensaje)
    elif tipo == "error":
        messagebox.showerror(titulo, mensaje)
    elif tipo == "warning":
        messagebox.showwarning(titulo, mensaje)
    else:
        messagebox.showinfo(titulo, mensaje)


def validar_campos(*campos):  # sourcery skip: invert-any-all, use-any
    """
    Valida que los campos de entrada no estén vacíos.
    
    Parámetros:
    - campos: Una lista de variables de Tkinter (StringVar, DoubleVar, etc.).
    
    Retorna:
    - True si todos los campos están llenos, False en caso contrario.
    """
    for campo in campos:
        if not campo.get():
            return False
    return True

def mostrar_mensaje(titulo, mensaje, tipo="info"):
    """
    Muestra un mensaje en una ventana emergente.
    
    Parámetros:
    - titulo: Título de la ventana.
    - mensaje: Mensaje a mostrar.
    - tipo: Tipo de mensaje ("info", "error", "warning").
    """
    if tipo == "info":
        messagebox.showinfo(titulo, mensaje)
    elif tipo == "error":
        messagebox.showerror(titulo, mensaje)
    elif tipo == "warning":
        messagebox.showwarning(titulo, mensaje)
    else:
        messagebox.showinfo(titulo, mensaje)