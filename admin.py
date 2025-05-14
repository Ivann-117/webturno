import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, make_response

admin_bp = Blueprint('admin', __name__, template_folder='templates')

def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

@admin_bp.route('/admin_login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        usuario_admin = request.form.get('usuario_admin')
        contraseña_admin = request.form.get('contraseña_admin')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM usuarios WHERE nombre=? AND rol='admin'",
            (usuario_admin,)
        )
        adm = cursor.fetchone()
        conn.close()

        if adm and contraseña_admin == adm['numero_documento'][::-1]:
            session['admin'] = adm['id']
            return redirect(url_for('admin.admin_dashboard'))

        flash('Credenciales incorrectas.')
        return redirect(url_for('admin.admin_login'))

    return render_template('admin_login.html')

@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        flash('Debes iniciar sesión como administrador.')
        return redirect(url_for('admin.admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, numero_documento, nombre, apellido1, apellido2, rol,
               COALESCE(estado_turno,'') AS estado_turno
        FROM usuarios
    """)
    users = cursor.fetchall()
    conn.close()

    # Prevenir que el navegador almacene en caché esta vista
    response = make_response(render_template('admin_dashboard.html', users=users))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@admin_bp.route('/admin_create', methods=['POST'])
def admin_create():
    if 'admin' not in session:
        flash('Sesión expirada. Inicia sesión nuevamente.')
        return redirect(url_for('admin.admin_login'))

    tipo = request.form['tipo_documento']
    numero = request.form['numero_documento']
    anio = request.form['fecha_nacimiento'][:4]
    nombre = request.form['nombre']
    ap1 = request.form['apellido1']
    ap2 = request.form['apellido2']
    rol = request.form['rol']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO usuarios (tipo_documento, numero_documento, anio_nacimiento, nombre, apellido1, apellido2, rol) '
        'VALUES (?,?,?,?,?,?,?)',
        (tipo, numero, anio, nombre, ap1, ap2, rol)
    )
    conn.commit()
    conn.close()
    flash('Usuario/Admin creado correctamente.')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin_update', methods=['POST'])
def admin_update():
    if 'admin' not in session:
        return jsonify(success=False, error='Sesión expirada.')

    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE usuarios SET numero_documento=?, nombre=?, apellido1=?, apellido2=?, rol=? WHERE id=?',
        (data['doc'], data['nombre'], data['apellido1'], data['apellido2'], data['rol'], data['id'])
    )
    conn.commit()
    conn.close()
    return jsonify(success=True)

@admin_bp.route('/admin_delete', methods=['POST'])
def admin_delete():
    if 'admin' not in session:
        return jsonify(success=False, error='Sesión expirada.')

    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=?", (data['id'],))
    conn.commit()
    conn.close()
    return jsonify(success=True)
