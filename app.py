from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_123'

# Función para obtener la conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('usuarios.db')  # Usar la base de datos usuarios.db
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    tipo_documento = request.form['tipo_documento']
    numero_documento = request.form['numero_documento']
    fecha_nacimiento = request.form['fecha_nacimiento']
    
    # Validación del tipo de documento
    tipos_validos = ['C.C.', 'T.I.', 'C.E.']
    if tipo_documento not in tipos_validos:
        flash('Tipo de documento inválido. Por favor, seleccione una opción válida.')
        return redirect(url_for('home'))

    # Validación del número de documento (solo números)
    if not numero_documento.isdigit():
        flash('El número de documento debe ser un valor numérico.')
        return redirect(url_for('home'))

    # Validación de la fecha de nacimiento (solo el año)
    if not fecha_nacimiento.isdigit() or len(fecha_nacimiento) != 4:
        flash('Fecha de nacimiento no válida. Debe ser un año en formato 4 dígitos (ejemplo: 2004).')
        return redirect(url_for('home'))

    # Procesamiento de la consulta a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM usuarios WHERE tipo_documento = ? AND numero_documento = ? AND anio_nacimiento = ?''',
                   (tipo_documento, numero_documento, fecha_nacimiento))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['usuario'] = {
            'documento': numero_documento,
            'nombre': user['nombre'],
            'apellido1': user['apellido1'],
            'apellido2': user['apellido2']
        }
        return redirect(url_for('turnos'))
    else:
        flash('Documento no encontrado. ¿Eres Nuevo? ¿Deseas Registrarte?')
        session['datos_previos'] = {
            'tipo': tipo_documento,
            'numero': numero_documento,
            'fecha': fecha_nacimiento
        }
        return redirect(url_for('home'))

@app.route('/turnos')
def turnos():
    cedes = {
        'Facebook': 'https://www.facebook.com',
        'YouTube': 'https://www.youtube.com',
        'Twitter': 'https://www.twitter.com',
        'Instagram': 'https://www.instagram.com',
        'TikTok': 'https://www.tiktok.com'
    }

    # Recuperar el nombre
    usuario = session.get('usuario')
    if usuario:
        nombre_usuario = f"{usuario['nombre']} {usuario['apellido1']} {usuario['apellido2']}"
    else:
        nombre_usuario = "Usuario desconocido"

    return render_template('turnos.html', cedes=cedes, nombre_usuario=nombre_usuario)

@app.route('/asignar_turno/<lugar>')
def asignar_turno(lugar):
    cedes = {
        'Facebook': 'https://www.facebook.com',
        'YouTube': 'https://www.youtube.com',
        'Twitter': 'https://www.twitter.com',
        'Instagram': 'https://www.instagram.com',
        'TikTok': 'https://www.tiktok.com'
    }

    if lugar in cedes:
        return redirect(cedes[lugar])
    else:
        return redirect(url_for('turnos'))

# Registro de nuevos usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Recogemos los datos del formulario
        tipo_doc = request.form['tipo_documento']
        numero_doc = request.form['numero_documento']
        fecha_completa = request.form['fecha_nacimiento']
        nombre = request.form['nombre']
        apellido1 = request.form['apellido1']
        apellido2 = request.form['apellido2']

        # Extraer solo el año de la fecha
        año = fecha_completa[:4]

        # Verificar si el usuario ya existe
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM usuarios WHERE tipo_documento = ? AND numero_documento = ?''', (tipo_doc, numero_doc))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('¡El usuario ya está registrado!')
            return redirect(url_for('login'))

        # Guardamos en la base de datos
        cursor.execute('''INSERT INTO usuarios (tipo_documento, numero_documento, anio_nacimiento, nombre, apellido1, apellido2)
                          VALUES (?, ?, ?, ?, ?, ?)''', (tipo_doc, numero_doc, año, nombre, apellido1, apellido2))
        conn.commit()
        conn.close()

        flash('¡Registro exitoso!')
        return redirect(url_for('home'))  # Redirigir al login después del registro

    return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True)
