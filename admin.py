import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from functools import wraps

admin_bp = Blueprint('admin', __name__, template_folder='templates')

def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

# Decorador para proteger rutas de administrador
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            flash('Debes iniciar sesión como administrador.')
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        usuario_admin = request.form.get('usuario_admin', '').strip()
        contraseña_admin = request.form.get('contraseña_admin', '').strip()

        if not usuario_admin or not contraseña_admin:
            flash('Debes completar todos los campos.')
            return redirect(url_for('admin.admin_login'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM usuarios WHERE nombre=? AND rol='admin'",
                (usuario_admin,)
            )
            adm = cursor.fetchone()
        finally:
            conn.close()

        if adm and contraseña_admin == adm['numero_documento'][::-1]:
            session['admin'] = adm['id']
            return redirect(url_for('admin.admin_dashboard'))

        flash('Credenciales incorrectas.')
        return redirect(url_for('admin.admin_login'))

    return render_template('admin_login.html')

@admin_bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, numero_documento, nombre, apellido1, apellido2, rol,
                   COALESCE(estado_turno,'') AS estado_turno
            FROM usuarios
        """)
        users = cursor.fetchall()
    finally:
        conn.close()

    response = make_response(render_template('admin_dashboard.html', users=users))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@admin_bp.route('/admin_create', methods=['POST'])
@login_required
def admin_create():
    tipo = request.form.get('tipo_documento', '').strip()
    numero = request.form.get('numero_documento', '').strip()
    fecha_nac = request.form.get('fecha_nacimiento', '').strip()
    anio = fecha_nac[:4] if len(fecha_nac) >= 4 else ''
    nombre = request.form.get('nombre', '').strip()
    ap1 = request.form.get('apellido1', '').strip()
    ap2 = request.form.get('apellido2', '').strip()
    rol = request.form.get('rol', '').strip()

    if not all([tipo, numero, anio, nombre, ap1, ap2, rol]):
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('admin.admin_dashboard'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO usuarios (tipo_documento, numero_documento, anio_nacimiento, nombre, apellido1, apellido2, rol) '
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (tipo, numero, anio, nombre, ap1, ap2, rol)
        )
        conn.commit()
    finally:
        conn.close()

    flash('Usuario/Admin creado correctamente.')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin_update', methods=['POST'])
@login_required
def admin_update():
    data = request.get_json()
    if not data:
        return jsonify(success=False, error='Datos faltantes.')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE usuarios SET numero_documento=?, nombre=?, apellido1=?, apellido2=?, rol=? WHERE id=?',
            (data['doc'], data['nombre'], data['apellido1'], data['apellido2'], data['rol'], data['id'])
        )
        conn.commit()
    finally:
        conn.close()

    return jsonify(success=True)

@admin_bp.route('/admin_delete', methods=['POST'])
@login_required
def admin_delete():
    data = request.get_json()
    if not data or 'id' not in data:
        return jsonify(success=False, error='ID faltante.')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=?", (data['id'],))
        conn.commit()
    finally:
        conn.close()

    return jsonify(success=True)

