class Alumno:
    def __init__(self, legajo, apellido, nombre, email, nota, id_escuela):
        self.legajo = legajo
        self.apellido = apellido
        self.nombre = nombre
        self.email = email
        self.nota = nota
        self.id_escuela = id_escuela

class Escuela:
    def __init__(self, nombre, localidad, provincia):
        self.nombre = nombre
        self.localidad = localidad
        self.provincia = provincia