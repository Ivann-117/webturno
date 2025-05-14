from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
from admin import admin_bp  # Importa el Blueprint de admin

app = Flask(__name__)
app.secret_key = 'clave_123'

# Registrar el Blueprint de admin
app.register_blueprint(admin_bp)

def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    tipo_documento = request.form['tipo_documento']
    numero_documento = request.form['numero_documento']
    fecha_nacimiento = request.form['fecha_nacimiento'][:4]
    # ... validaciones ...
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuarios WHERE tipo_documento=? AND numero_documento=? AND anio_nacimiento=?",
        (tipo_documento, numero_documento, fecha_nacimiento)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        flash('Documento no encontrado. ¿Deseas registrarte?')
        return redirect(url_for('home'))

    session['usuario'] = dict(user)
    if user['rol'] == 'admin':
        return redirect(url_for('admin.admin_login'))
    return redirect(url_for('turnos'))

@app.route('/registro', methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        tipo = request.form['tipo_documento']
        numero = request.form['numero_documento']
        anio = request.form['fecha_nacimiento'][:4]
        nombre = request.form['nombre']
        ap1 = request.form['apellido1']
        ap2 = request.form['apellido2']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM usuarios WHERE tipo_documento=? AND numero_documento=?",
            (tipo, numero)
        )
        if cursor.fetchone():
            flash('El usuario ya está registrado')
            return redirect(url_for('home'))

        cursor.execute(
            "INSERT INTO usuarios (tipo_documento, numero_documento, anio_nacimiento, nombre, apellido1, apellido2, rol) "
            "VALUES (?,?,?,?,?,?, 'usuario')",
            (tipo, numero, anio, nombre, ap1, ap2)
        )
        conn.commit()
        conn.close()
        flash('Registro exitoso')
        return redirect(url_for('home'))
    return render_template('registro.html')
# Boton para cerrar sesion en el dashboar admin
@app.route('/logout')
def logout():
    session.clear()  # o session.pop('usuario', None)
    return redirect(url_for('admin.admin_login'))
#cerrar sesion en boton de turnos
@app.route('/logout_turno')
def logout_turno():
    session.clear()  # o session.pop('usuario', None)
    return redirect(url_for('home'))

@app.route('/turnos')
def turnos():
    if 'usuario' not in session:
        return redirect(url_for('home'))
    usuario = session['usuario']
    nombre_usuario = f"{usuario['nombre']} {usuario['apellido1']} {usuario['apellido2']}"
    cedes = {
        'Facebook':'https://facebook.com',
        'YouTube':'https://youtube.com',
        'Twitter':'https://twitter.com',
        'Instagram':'https://instagram.com',
        'TikTok':'https://tiktok.com'
    }
    return render_template('turnos.html', cedes=cedes, nombre_usuario=nombre_usuario)

@app.route('/asignar_turno/<lugar>')
def asignar_turno(lugar):
    cedes = {
        'Facebook':'https://facebook.com',
        'YouTube':'https://youtube.com',
        'Twitter':'https://twitter.com',
        'Instagram':'https://instagram.com',
        'TikTok':'https://tiktok.com'
    }
    return redirect(cedes.get(lugar, url_for('turnos')))

if __name__ == '__main__':
    app.run(debug=True)
