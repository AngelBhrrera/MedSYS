#pip install flask
#pip install flask_mysqldb

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = '303429043809'

# Configuración de la conexión a MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'medsys'

# Inicialización de la extensión MySQL
mysql = MySQL(app)
# Configuración para la carpeta estática
app.static_folder = 'static'
role_map = {0: 'admin', 1: 'medico', 2: 'secretaria'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = %s AND password = %s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['name'] = user[1]
            session['role'] = role_map[user[3]]
            return redirect(url_for('home', role=session["role"]))
        else:
            return 'Usuario o contraseña incorrectos'
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'role' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO usuarios (name, email, password, role) VALUES (%s, %s, %s, %s)', (name, email, password, role,))
        mysql.connection.commit()
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/<string:role>/home')
def home(role):
    if 'loggedin' in session and session['role'] == role:
        return render_template('home.html')
    return redirect(url_for('index'))

@app.route('/<string:role>/CRUD/<string:entity>', methods=['GET'])
def crud(role, entity):
    if role in ['admin', 'medico', 'secretaria'] and entity in ['Usuarios', 'Sintomas', 'Signos', 'Enfermedades', 'Pacientes', 'Pruebas', 'Citas']:
        if entity == 'Usuarios':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM usuarios')
            usuarios = cursor.fetchall()
            return render_template(f'CRUD_{entity}.html',usuarios = usuarios, role = role)
        if entity == 'Pacientes':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM pacientes')
            pacientes = cursor.fetchall()
            return render_template(f'CRUD_{entity}.html',pacientes = pacientes, role = role)
        if entity == 'Enfermedades':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM enfermedades')
            enfermedades = cursor.fetchall()
            return render_template(f'CRUD_{entity}.html',enfermedades = enfermedades, role = role)
        if entity == 'Signos':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM signos_sintomas WHERE tipo = 0')
            signos = cursor.fetchall()
            return render_template(f'CRUD_{entity}.html',signos = signos, role = role)
        if entity == 'Sintomas':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM signos_sintomas WHERE tipo = 1')
            sintomas = cursor.fetchall()
            return render_template(f'CRUD_{entity}.html',sintomas = sintomas, role = role)

        return render_template(f'CRUD_{entity}.html')
    else:
        return "404 Not Found", 404

@app.route('/<string:rol>/CRUD/<string:entity>/agregar', methods=['POST'])
def agregar_entidad(rol, entity):
    if rol in ['admin', 'medico', 'secretaria'] and entity == 'Usuarios':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO usuarios (name, email, password, role) VALUES (%s, %s, %s, %s)', (name, email, password, role,))
        mysql.connection.commit()
        return redirect(request.referrer)
    if rol in ['admin', 'medico', 'secretaria'] and entity == 'Pacientes':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_n = request.form['fecha_n']
        estatura = request.form['estatura']
        edad = request.form['edad']
        peso = request.form['peso']
        sexo = request.form['sexo']
        nacionalidad = request.form['nacionalidad']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO pacientes (nombre, apellido, fecha_nacimiento, estatura, edad, peso, sexo, nacionalidad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (nombre, apellido, fecha_n, estatura, edad, peso, sexo, nacionalidad,))
        mysql.connection.commit()
        return redirect(request.referrer)
    else:
        return "404 Not Found", 404

@app.route('/<string:rol>/CRUD/<string:entity>/editar/<id>', methods=['POST'])
def editar_entidad(rol, entity, id):
    if rol in ['admin', 'medico', 'secretaria'] and entity == 'Usuarios':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE usuarios SET name = %s, email = %s, role = %s WHERE id = %s', (name, email, role, id))
        mysql.connection.commit()
        return redirect(request.referrer)
    else:
        return "404 Not Found", 404

@app.route('/<string:rol>/CRUD/<string:entity>/eliminar/<id>', methods=['POST'])
def eliminar_entidad(rol, entity, id):
    if rol in ['admin', 'medico', 'secretaria'] and entity == 'Usuarios':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT role FROM usuarios WHERE id = %s', (id,))
        current_role = cursor.fetchone()[0]
        new_role = 3 if current_role == 0 else 0 if current_role == 3 else 4 if current_role == 1 else 1 if current_role == 4 else 5 if current_role == 2 else 2
        cursor.execute('UPDATE usuarios SET role = %s WHERE id = %s', (new_role, id))
        mysql.connection.commit()
        return redirect(request.referrer)
    else:
        return "404 Not Found", 404
    
@app.route('/<string:role>/<string:action>')
def action(role, action):
    if role in ['admin', 'medico'] and action in ['Historial', 'Seguimiento_Diagnostico']:
        return render_template(f'{action.lower()}.html')
    else:
        return "404 Not Found", 404

if __name__ == '__main__':
    app.run(debug=True)