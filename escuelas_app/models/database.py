import sqlite3 as sq3
from database.escuelas import escuelas
from database.alumnos import alumnos

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.con = None

    def conectar(self):
        """
        Conecta a la base de datos y la inicializa si no existe.
        """
        self.con = sq3.connect(self.db_path)
        self.inicializar_base_datos()
        return self.con.cursor()

    def cerrar(self):
        """
        Cierra la conexión a la base de datos.
        """
        if self.con:
            self.con.close()

    def inicializar_base_datos(self):
        """
        Crea las tablas y inserta los datos iniciales si no existen.
        """
        cur = self.con.cursor()

        # Crear tabla 'escuelas' si no existe
        cur.execute('''
            CREATE TABLE IF NOT EXISTS escuelas (
                _id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(45) DEFAULT NULL,
                localidad VARCHAR(45) DEFAULT NULL,
                provincia VARCHAR(45) DEFAULT NULL,
                capacidad INTEGER DEFAULT NULL
            )
        ''')

        # Crear tabla 'alumnos' si no existe
        cur.execute('''
            CREATE TABLE IF NOT EXISTS alumnos (
                _id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_escuela INTEGER DEFAULT NULL,
                legajo INTEGER DEFAULT NULL,
                apellido VARCHAR(50) DEFAULT NULL,
                nombre VARCHAR(50) DEFAULT NULL,
                nota DECIMAL(10, 0) DEFAULT NULL,
                grado INTEGER DEFAULT NULL,
                email VARCHAR(50) DEFAULT NULL,
                FOREIGN KEY (id_escuela) REFERENCES escuelas(_id)
            )
        ''')

        # Insertar datos iniciales en 'escuelas' si la tabla está vacía
        cur.execute("SELECT COUNT(*) FROM escuelas")
        if cur.fetchone()[0] == 0:
            cur.executemany("INSERT INTO escuelas VALUES (?, ?, ?, ?, ?)", escuelas)

        # Insertar datos iniciales en 'alumnos' si la tabla está vacía
        cur.execute("SELECT COUNT(*) FROM alumnos")
        if cur.fetchone()[0] == 0:
            cur.executemany("INSERT INTO alumnos VALUES (?, ?, ?, ?, ?, ?, ?, ?)", alumnos)

        self.con.commit()

    def ejecutar_query(self, query, params=None):
        """
        Ejecuta una consulta SQL y retorna los resultados.
        """
        try:
            cur = self.con.cursor()
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            self.con.commit()
            return cur.fetchall()
        except Exception as e:
            raise e