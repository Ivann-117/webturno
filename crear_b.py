import sqlite3

def create_table():
    try:
        # Se crea la base de datos si no existe
        conexion = sqlite3.connect('usuarios.db')
        cursor = conexion.cursor()

        # Crear la tabla con la nueva columna 'estado_turno'
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_documento TEXT NOT NULL,
            numero_documento TEXT NOT NULL,
            anio_nacimiento TEXT NOT NULL,
            nombre TEXT NOT NULL,
            apellido1 TEXT NOT NULL,
            apellido2 TEXT NOT NULL,
            rol TEXT DEFAULT 'usuario' NOT NULL,
            estado_turno TEXT DEFAULT 'pendiente' NOT NULL
        )
        ''')

        conexion.commit()
        conexion.close()
        print("Tabla 'usuarios' creada correctamente.")

    except sqlite3.Error as e:
        print(f"Error al crear la tabla: {e}")
        conexion.rollback()

def crear_admin():
    try:
        # Conectar a la base de datos
        conexion = sqlite3.connect('usuarios.db')
        cursor = conexion.cursor()

        # Datos del administrador
        tipo_documento = 'C.C.'  # Ejemplo: Cédula de ciudadanía
        numero_documento = '123456789'  # Número de documento (personalízalo)
        anio_nacimiento = '1980'  # Año de nacimiento
        nombre = 'Admin'
        apellido1 = 'Admin'
        apellido2 = 'Admin'
        rol = 'admin'  # Especificamos que este usuario es un admin
        estado_turno = 'activo'  # Estado del turno del administrador

        # Insertar el usuario con rol admin
        cursor.execute('''
        INSERT INTO usuarios (tipo_documento, numero_documento, anio_nacimiento, nombre, apellido1, apellido2, rol, estado_turno)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (tipo_documento, numero_documento, anio_nacimiento, nombre, apellido1, apellido2, rol, estado_turno))

        # Confirmar y cerrar la conexión
        conexion.commit()
        conexion.close()
        print("Administrador creado correctamente.")
    except sqlite3.Error as e:
        print(f"Error al crear el administrador: {e}")
        conexion.rollback()

# Llamar a la función para crear la tabla y luego insertar al administrador
create_table()
crear_admin()
