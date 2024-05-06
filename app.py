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
            session['id'] = user[0]
            session['name'] = user[1]
            session['role'] = role_map[user[3]]
            return redirect(url_for('home', role=session["role"],))
        else:
            return 'Usuario o contraseña incorrectos'
    return redirect(url_for('index'))

@app.route('/<string:role>/home')
def home(role):
    if 'loggedin' in session and session['role'] == role:
        if role == 'admin':    
            return render_template('home.html')
        elif role in ['medico', 'secretaria']:
            idu = session['id']
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM detalle_citas WHERE id_medico = %s AND estado = 1', (idu, ))
            citas = cursor.fetchall()
            return render_template('home.html', citas=citas)
        else:
            return "404 Not Found", 404
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
        if entity == 'Pruebas':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM pruebas')
            pruebas = cursor.fetchall()
            return render_template(f'CRUD_{entity}.html', pruebas = pruebas, role = role)
        if entity == 'Enfermedades':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT e.id_enfermedad, e.nombre, e.descripcion, e.id_prueba, p.nombre AS nombre_prueba FROM enfermedades e INNER JOIN pruebas p ON e.id_prueba = p.id_prueba')
            enfermedades = cursor.fetchall()
            cursor2 = mysql.connection.cursor()
            cursor2.execute('SELECT * FROM pruebas')
            pruebas = cursor2.fetchall()
            return render_template(f'CRUD_{entity}.html', enfermedades = enfermedades, pruebas = pruebas, role = role)
        if entity == 'Signos':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM signos_sintomas WHERE tipo = 1')
            signos = cursor.fetchall()
            cursor2 = mysql.connection.cursor()
            cursor2.execute('SELECT * FROM enfermedades')
            enfermedades = cursor2.fetchall()
            return render_template(f'CRUD_{entity}.html',signos = signos, enfermedades = enfermedades, role = role)
        if entity == 'Sintomas':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM signos_sintomas WHERE tipo = 2')
            sintomas = cursor.fetchall()
            cursor2 = mysql.connection.cursor()
            cursor2.execute('SELECT * FROM enfermedades')
            enfermedades = cursor2.fetchall()
            return render_template(f'CRUD_{entity}.html',sintomas = sintomas, enfermedades = enfermedades, role = role)

        return render_template(f'CRUD_{entity}.html')
    else:
        return "404 Not Found", 404

@app.route('/<string:rol>/CRUD/<string:entity>/agregar', methods=['POST'])
def agregar_entidad(rol, entity):
    if rol in ['admin'] and entity == 'Usuarios':
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
    if rol in ['admin', 'medico'] and entity == 'Pruebas':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        tipo = request.form['tipo']
        valores_referencia = request.form['valores_referencia']
        resultado_optimo = request.form['resultado_optimo']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO pruebas (nombre, descripcion, tipo, valores_referencia, resultado_optimo) VALUES (%s, %s, %s, %s, %s)', (nombre, descripcion, tipo, valores_referencia, resultado_optimo,))
        mysql.connection.commit()
        return redirect(request.referrer)
    if rol in ['admin', 'medico'] and entity == 'Enfermedades':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        id_prueba = request.form['id_prueba']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO enfermedades (nombre, descripcion, id_prueba) VALUES (%s, %s, %s)', (nombre, descripcion, id_prueba,))
        mysql.connection.commit()
        cursor.close()
        return redirect(request.referrer)
    if rol in ['admin', 'medico'] and entity in ['Signos', 'Sintomas']:
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        frecuencia = request.form['frecuencia']
        if(entity == 'Signos'):
            tipo = 1;
        else:
            tipo = 2;
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO signos_sintomas (nombre, descripcion, frecuencia, tipo) VALUES (%s, %s, %s, %s)', (nombre, descripcion, frecuencia, tipo,))
        mysql.connection.commit()
        cursor.close()
        return redirect(request.referrer)
    if rol in ['secretaria', 'medico'] and entity == 'Citas':
        idm = request.form['id_medico']
        idp = request.form['id_paciente']
        fecha = request.form['fecha']  
        hora = request.form['hora']  
        observaciones = request.form['observaciones']  
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO citas (id_medico, id_paciente, fecha, hora, observaciones) VALUES (%s, %s, %s, %s, %s)', (idm, idp, fecha, hora, observaciones,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('home', role=session["role"]))
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
        cursor.execute('UPDATE pacientes SET nombre = %s, apellido = %s, fecha_nacimiento = %s, estatura = %s, edad = %s, peso = %s, sexo = %s, nacionalidad = %s WHERE id_paciente = %s',
                  (nombre, apellido, fecha_n, estatura, edad, peso, sexo, nacionalidad, id))
        mysql.connection.commit()
        return redirect(request.referrer)
    if rol in ['admin', 'medico'] and entity == 'Pruebas':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        tipo = request.form['tipo']
        valores_referencia = request.form['valores_referencia']
        resultado_optimo = request.form['resultado_optimo']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE pruebas SET nombre = %s, descripcion = %s, tipo = %s, valores_referencia = %s, resultado_optimo = %s WHERE id_prueba = %s', (nombre, descripcion, tipo, valores_referencia, resultado_optimo, id,))
        mysql.connection.commit()      
        return redirect(request.referrer)
    if rol in ['admin', 'medico'] and entity == 'Enfermedades':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        id_prueba = request.form['id_prueba']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE enfermedades SET nombre = %s, descripcion = %s, id_prueba = %s WHERE id_enfermedad = %s', (nombre, descripcion, id_prueba, id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(request.referrer)
    if rol in ['admin', 'medico'] and (entity == 'Signos' or entity == 'Sintomas'):
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        frecuencia = request.form['frecuencia']        
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE signos_sintomas SET nombre = %s, descripcion = %s, frecuencia = %s, WHERE id_si = %s', (nombre, descripcion, frecuencia, id,))
        mysql.connection.commit()
        cursor.close()
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
    if rol in ['admin', 'medico', 'secretaria'] and entity == 'Pacientes':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM pacientes WHERE id_paciente = %s', (id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(request.referrer)
    if rol in ['admin', 'medico'] and entity == 'Pruebas':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM pruebas WHERE id_prueba = %s', (id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(request.referrer)
    if rol in ['admin', 'medico'] and entity == 'Enfermedades':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM enfermedades WHERE id_enfermedad = %s', (id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(request.referrer)
    if rol in ['admin', 'medico'] and (entity == 'Signos' or entity == 'Sintomas'):
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM signos_sintomas WHERE id_si = %s', (id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(request.referrer)
    if rol in ['medico', 'secretaria'] and entity == 'Citas':
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE citas SET estado = 3 WHERE id_cita = %s', (id, ))
        mysql.connection.commit()
        return redirect(request.referrer)
    else:
        return "404 Not Found", 404
    
    

@app.route('/<string:rol>/Signos/relacionar', methods=['POST'])
def relacionar_enfermedadSigno(rol):
        id_enfermedad = request.form['enfermedad']
        id_si = request.form['signo']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO motor_inferencia (id_enfermedad, id_si) VALUES (%s, %s)', (id_enfermedad, id_si,))
        mysql.connection.commit()
        cursor.close()
        return redirect(request.referrer)

@app.route('/<string:rol>/Sintomas/relacionar', methods=['POST'])
def relacionar_enfermedadSintoma(rol):
        id_enfermedad = request.form['enfermedad']
        id_si = request.form['sintoma']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO motor_inferencia (id_enfermedad, id_si) VALUES (%s, %s)', (id_enfermedad, id_si,))
        mysql.connection.commit()
        cursor.close()
        return redirect(request.referrer)
    
    
@app.route('/<string:role>/<string:action>/<string:idp>',  methods=['GET'])
def historial(role, action, idp):
    if role in ['medico'] and action in ['Historial']:
       cursor = mysql.connection.cursor()
       cursor.execute("""SELECT ci.fecha AS citas, p.nombre AS paciente, p.apellido, e.nombre AS enfermedad, co.resultado_prueba AS pruebas, co.id_consulta
            FROM consultas co
            INNER JOIN citas ci ON co.id_cita = ci.id_cita
            INNER JOIN pacientes p ON co.id_paciente = p.id_paciente
            INNER JOIN enfermedades e ON co.enfermedad_diagnosticada = e.id_enfermedad
            WHERE co.id_paciente = %s
            """, (idp,))
       historial = cursor.fetchall()
       return render_template(f'{action.lower()}.html',  historial = historial, role = role)
    elif role in ['medico'] and action in ['Consulta_Medica']:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM signos_sintomas WHERE tipo = 1')
        signos = cursor.fetchall()
        cursor2 = mysql.connection.cursor()
        cursor2.execute('SELECT * FROM signos_sintomas WHERE tipo = 2')
        sintomas = cursor2.fetchall()
        cursor3 = mysql.connection.cursor()
        cursor3.execute('SELECT id_paciente FROM citas WHERE id_cita = %s', idp)
        id_paciente_tuple = cursor3.fetchone()
        id_paciente = id_paciente_tuple[0]
        return render_template(f'{action.lower()}.html', role = role, signos = signos, sintomas = sintomas, id_cita = idp, id_paciente =id_paciente)
    else:
       return "404 Not Found", 404
   
    
@app.route('/<string:role>/<string:action>')
def action(role, action):
    if role  in ['medico','secretaria'] and action in ['Citas']:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM usuarios u WHERE u.role = 1')
        medicos = cursor.fetchall()
        cursor2 = mysql.connection.cursor()
        cursor2.execute('SELECT * FROM pacientes')
        pacientes = cursor2.fetchall()
        cursor3 = mysql.connection.cursor()
        cursor3.execute('SELECT * FROM detalle_citas')
        citas = cursor3.fetchall()
        return render_template(f'{action.lower()}.html', pacientes = pacientes, medicos = medicos, citas=citas, role = role)
    elif role in ['medico'] and action in ['Consultas']:
        idu = session['id']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM detalle_citas WHERE id_medico = %s AND estado = 1 ORDER BY fecha ASC, hora ASC', (idu, ))
        citas = cursor.fetchall()
        return render_template(f'{action.lower()}.html', citas=citas, role = role)
    else:
        return "404 Not Found", 404


@app.route('/ruta/a/tu/funcion', methods=['POST'])
def recibir_datos():
    id_paciente = request.form['id_paciente']
    id_cita = request.form['id_cita']
    signos = request.form.getlist('signos[]')
    sintomas = request.form.getlist('sintomas[]')
    
    cursor = mysql.connection.cursor()

    # Crear la vista totales_inferencia
    # Este bloque comentado se debe correr la primera vez que hagas un diagnostico y despues comentarlo,
    # se puede solucionar usando try e importando el modulo MySQLdb
    # no pude, no me da la cabeza ya, llevo 9 dias sin dormir mas de 4 horas


    #cursor.execute("""
    #    CREATE VIEW totales_inferencia AS 
    #    SELECT enfermedades.nombre, SUM(signos_sintomas.frecuencia) AS total 
    #    FROM motor_inferencia 
    #    JOIN signos_sintomas ON motor_inferencia.id_si = signos_sintomas.id_si 
    #    JOIN enfermedades ON motor_inferencia.id_enfermedad = enfermedades.id_enfermedad  
    #   GROUP BY enfermedades.nombre;
    #""")
    #db.commit()

    # Fin del codigo que se debe comentar

    # Ejecutar el query para obtener los resultados
    ids_concatenados = ', '.join(signos + sintomas)
    cursor.execute(f"""SELECT
                        enfermedades.nombre,
                        pruebas.nombre AS pruebas,
                        SUM(signos_sintomas.frecuencia) AS frecuencia,
                        totales_inferencia.total, (SUM(signos_sintomas.frecuencia) * 100.0 / totales_inferencia.total) AS porcentaje
                        FROM motor_inferencia
                        JOIN signos_sintomas ON motor_inferencia.id_si = signos_sintomas.id_si
                        JOIN enfermedades ON motor_inferencia.id_enfermedad = enfermedades.id_enfermedad
                        JOIN totales_inferencia ON totales_inferencia.nombre = enfermedades.nombre
                        JOIN pruebas ON enfermedades.id_prueba = pruebas.id_prueba
                        WHERE motor_inferencia.id_si IN ({ids_concatenados}) GROUP BY enfermedades.nombre
                        ORDER BY porcentaje DESC;
                """)
    resultados = cursor.fetchall()
    print(resultados)
    # Aqui va el query y eso
    return render_template('motor.html', id_paciente=id_paciente, id_cita=id_cita, signos=signos, sintomas=sintomas, resultados = resultados)


if __name__ == '__main__':
    app.run(debug=True)
