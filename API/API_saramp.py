from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Leer el archivo CSV
df = pd.read_csv('API_WBank2.csv', delimiter='","', header=2, engine='python')

# Obtener datos de la fila con Country Name igual a "Panama"
@app.route('/datos/panama', methods=['GET'])
def obtener_datos_panama():
    fila_panama = df.loc[df['Country Name'] == 'Panama']
    if fila_panama.empty:
        return jsonify({"mensaje": "No se encontraron datos para Panama"}), 404
    return jsonify(fila_panama.to_dict(orient='records')[0])

if __name__ == '__main__':
    app.run(debug=True)
