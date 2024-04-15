#pip install flask
#pip install flask_mysqldb

from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la conexión a MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
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
    # Aquí irá la lógica para verificar las credenciales de inicio de sesión
    # Si las credenciales son válidas, redirigir a la página de inicio
    # De lo contrario, redirigir de nuevo al formulario de inicio de sesión con un mensaje de error
    return redirect(url_for('home'))

@app.route('/admin/home')
def home():
    return render_template('home_A.html')

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

@app.route('/admin/CRUD/citas')
def admin_cCRUD():
    return render_template('CRUD_citas.html')

@app.route('/medico/home')
def homeM():
    return render_template('home_M.html')

@app.route('/medico/CRUD/pacientes')
def med_pCRUD():
    return render_template('CRUD_pacientes.html')

@app.route('/medico/CRUD/citas')
def med_cCRUD():
    return render_template('CRUD_citas.html')

@app.route('/secretaria/home')
def homeS():
    return render_template('home_S.html')

@app.route('/secretaria/CRUD/pacientes')
def sec_pCRUD():
    return render_template('CRUD_pacientes.html')

@app.route('/secretaria/CRUD/citas')
def sec_cCRUD():
    return render_template('CRUD_citas.html')



@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)