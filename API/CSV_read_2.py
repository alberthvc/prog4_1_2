from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Leer el archivo CSV
df = pd.read_csv('API_WBank2.csv', delimiter='","', header=2, engine='python')

# Seleccionar una sola fila por su índice utilizando iloc[]
fila = df.iloc[185]  # se usa el indice

@app.route('/')
def mostrar_datos_fila():
    return render_template('datos_panama.html', fila=fila)

if __name__ == '__main__':
    app.run(debug=True)
