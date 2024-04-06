from flask import Flask, render_template, request, redirect, url_for
import redis

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

    redis_client.hmset(nombre, receta)
    return redirect(url_for('ver_recetas'))

@app.route('/ver_recetas')
def ver_recetas():
    recetas_keys = redis_client.keys()

    print("Claves de las recetas:", recetas_keys)

    recetas = []
    for key in recetas_keys:
        receta = redis_client.hgetall(key)
        recetas.append(receta)
    return render_template('ver_recetas.html', recetas=recetas)



if __name__ == "__main__":
    app.run(debug=True)
