from flask import Flask, render_template, request, redirect, url_for
import redis
import json

app = Flask(__name__)

# Conexión a la base de datos Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/agregar_receta', methods=['POST'])
def agregar_receta():
    nombre = request.form['nombre']
    ingredientes = request.form['ingredientes']
    pasos = request.form['pasos']

    receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "pasos": pasos
    }

    # Almacenar la receta en Redis
    redis_client.hset(nombre, 'receta', json.dumps(receta))

    return redirect(url_for('ver_recetas'))

@app.route('/ver_recetas')
def ver_recetas():
    recetas_keys = redis_client.keys()
    recetas = []
    for key in recetas_keys:
        receta_json = redis_client.hget(key, 'receta')
        if receta_json:
            receta = json.loads(receta_json)
            recetas.append(receta)
    return render_template('ver_recetas.html', recetas=recetas)


@app.route('/editar_receta/<nombre>', methods=['GET', 'POST'])
def editar_receta(nombre):
    if request.method == 'POST':
        ingredientes = request.form['ingredientes']
        pasos = request.form['pasos']

        # Actualizar la receta en Redis
        redis_client.hset(nombre, 'ingredientes', ingredientes)
        redis_client.hset(nombre, 'pasos', pasos)

        return redirect(url_for('ver_recetas'))
    else:
        # Obtener los ingredientes y pasos de la receta
        ingredientes = redis_client.hget(nombre, 'ingredientes')
        pasos = redis_client.hget(nombre, 'pasos')

        # Crear un diccionario para pasar al template
        receta = {
            'nombre': nombre,
            'ingredientes': ingredientes,
            'pasos': pasos
        }

        return render_template('editar_receta.html', receta=receta)



@app.route('/eliminar_receta/<nombre>', methods=['POST'])
def eliminar_receta(nombre):
    redis_client.delete(nombre)
    return redirect(url_for('ver_recetas'))

@app.route('/confirmar_eliminar_receta/<nombre>')
def confirmar_eliminar_receta(nombre):
    receta = redis_client.hgetall(nombre)
    return render_template('confirmar_eliminar_receta.html', receta=receta)


if __name__ == "__main__":
    app.run(debug=True)
