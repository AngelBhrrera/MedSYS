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
            session['role'] = user[3]
            return redirect(url_for('home'))
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

@app.route('/home')
def home():
    if 'loggedin' in session:
        if session['role'] == 0:
            return render_template('home_A.html')
        if session['role'] == '1':
            return render_template('home_M.html')
        if session['role'] == 2:
            return render_template('home_S.html')
        else:
            return render_template('home.html')
    return redirect(url_for('index'))

@app.route('/admin/CRUD/usuarios')
def admin_uCRUD():
    return render_template('CRUD_usuarios.html')

@app.route('/admin/CRUD/sintomas')
def admin_sintCRUD():
    return render_template('CRUD_sintomas.html')

@app.route('/admin/CRUD/signos')
def admin_signCRUD():
    return render_template('CRUD_signos.html')

@app.route('/admin/CRUD/enfermedades')
def admin_eCRUD():
    return render_template('CRUD_enfermedades.html')

@app.route('/admin/CRUD/pacientes')
def admin_pCRUD():
    return render_template('CRUD_pacientes.html')

@app.route('/admin/CRUD/pruebas')
def admin_prCRUD():
    return render_template('CRUD_pruebas.html')

@app.route('/admin/CRUD/citas')
def admin_cCRUD():
    return render_template('CRUD_citas.html')

@app.route('/medico/CRUD/pacientes')
def med_pCRUD():
    return render_template('CRUD_pacientes.html')

@app.route('/medico/CRUD/citas')
def med_cCRUD():
    return render_template('CRUD_citas.html')

@app.route('/secretaria/CRUD/pacientes')
def sec_pCRUD():
    return render_template('CRUD_pacientes.html')

@app.route('/secretaria/CRUD/citas')
def sec_cCRUD():
    return render_template('CRUD_citas.html')



if __name__ == '__main__':
    app.run(debug=True)