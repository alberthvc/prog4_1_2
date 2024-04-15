from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import requests

app = Flask(__name__)
api = Api(app)

# Definir la clase Recetas para manejar las operaciones CRUD
class Recetas(Resource):
    def get(self):
        # Implementar la lógica para obtener todas las recetas
        response = requests.get('http://localhost:5000/recetas')
        return response.json()

    def post(self):
        # Implementar la lógica para agregar una nueva receta
        data = request.get_json()
        response = requests.post('http://localhost:5000/recetas', json=data)
        return response.json(), response.status_code
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import requests

app = Flask(__name__)
api = Api(app)

# Simulación de una base de datos de recetas
recetas = {
    1: {'nombre': 'Receta 1', 'ingredientes': ['ingrediente1', 'ingrediente2'], 'pasos': 'Paso 1'},
    2: {'nombre': 'Receta 2', 'ingredientes': ['ingrediente3', 'ingrediente4'], 'pasos': 'Paso 2'}
}

class Recetas(Resource):
    def get(self):
        return jsonify(recetas)

    def post(self):
        data = request.get_json()
        receta_id = max(recetas.keys()) + 1
        recetas[receta_id] = data
        return jsonify({'receta_id': receta_id, 'mensaje': 'Receta agregada'}), 201

class Receta(Resource):
    def get(self, receta_id):
        if receta_id in recetas:
            return jsonify(recetas[receta_id])
        else:
            return jsonify({'mensaje': 'Receta no encontrada'}), 404

    def put(self, receta_id):
        if receta_id in recetas:
            data = request.get_json()
            recetas[receta_id] = data
            return jsonify({'mensaje': 'Receta actualizada'}), 200
        else:
            return jsonify({'mensaje': 'Receta no encontrada'}), 404

    def delete(self, receta_id):
        if receta_id in recetas:
            del recetas[receta_id]
            return jsonify({'mensaje': 'Receta eliminada'}), 200
        else:
            return jsonify({'mensaje': 'Receta no encontrada'}), 404

api.add_resource(Recetas, '/recetas')
api.add_resource(Receta, '/recetas/<int:receta_id>')

if __name__ == '__main__':
    app.run(debug=True)
