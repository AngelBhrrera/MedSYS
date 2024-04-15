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

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/doctor/CRUD')
def dCRUD():
    return render_template('CRUD.html')

@app.route('/admin/CRUD')
def aCRUD():
    return render_template('CRUD.html')

@app.route('/secretaria/CRUD')
def sCRUD():
    return render_template('CRUD.html')


@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)