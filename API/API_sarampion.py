from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Leer el archivo CSV
df = pd.read_csv('API_WBank2.csv', delimiter='","', header=2, engine='python')

# Obtener todos los datos
@app.route('/datos', methods=['GET'])
def obtener_todos_los_datos():
    return jsonify(df.to_dict())

# Obtener datos de una fila específica por índice
@app.route('/datos/185', methods=['GET'])
def obtener_datos_fila_185():
    return jsonify(df.iloc[185].to_dict())

if __name__ == '__main__':
    app.run(debug=True)
