import sqlite3

def create_table():
    
# Crear la base de datos y la tabla usuarios si no existe
    conexion = sqlite3.connect('usuarios.db')
    cursor = conexion.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_documento TEXT NOT NULL,
        numero_documento TEXT NOT NULL,
        anio_nacimiento TEXT NOT NULL,
        nombre TEXT NOT NULL,
        apellido1 TEXT NOT NULL,
        apellido2 TEXT NOT NULL
    )
    ''')
    conexion.commit()
    conexion.close()
# Llamar a la función para asegurarse de que la tabla esté creada
create_table()
