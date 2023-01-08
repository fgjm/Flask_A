from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)# inicializa la app


# Conexión MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pr'

conexion = MySQL(app)


@app.before_request
def before_request():
    print("Antes de la petición...")


@app.after_request
def after_request(response):
    print("Después de la petición")    
    return response


@app.route('/')
def index():
    cursos = ['PHP', 'Python', 'Java', 'Kotlin', 'Dart', 'JavaScript']
    data={
        'titulo':'index', 'bienvenida':'Saludo!',
        'cursos': cursos,
        'numero_cursos': len(cursos)
    }
    return render_template('index.html', data=data)

@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data = {
        'titulo': 'Contacto',
        'nombre': nombre,
        'edad': edad
    }
    return render_template('contacto.html', data=data)


def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "Ok"


@app.route('/cursos')
def listar_cursos():
    data = {}
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT nproducto, Producto, valorProducto, Cantidad FROM ventas ORDER BY Producto ASC"
        cursor.execute(sql)
        cursos = cursor.fetchall()
        # print(cursos)
        data['cursos'] = cursos
        data['mensaje'] = 'Exito 3'; print('flask_backend 2Commit')
    except Exception as ex:
        data['mensaje'] = 'Error...'
    return jsonify(data)


def pagina_no_encontrada(error):
    return render_template('404.html'), 404
    #return redirect(url_for('index')) #redirigir a index

if __name__=='__main__':    
    app.add_url_rule('/query_string', view_func=query_string) #otra forma de enlazar funcion con la url
    app.register_error_handler(404, pagina_no_encontrada) #manejador del error
    app.run(debug=True, port=5021)