from flask import Flask, render_template, request, redirect, url_for
from my_celery import Celery
from flask_mail import Mail

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

mail = Mail(app)

# tasks.py
from my_celery import Celery
from flask_mail import Message
from app import mail

# Configuración de la base de datos SQLite
DB_FILE = 'recetas.db'

def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            ingredientes TEXT,
            pasos TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_receta', methods=['GET', 'POST'])
def agregar_receta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ingredientes = request.form['ingredientes']
        pasos = request.form['pasos']

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO recetas (nombre, ingredientes, pasos) VALUES (?, ?, ?)
        ''', (nombre, ingredientes, pasos))
        conn.commit()
        conn.close()

        return redirect(url_for('ver_recetas'))
    else:
        return render_template('agregar_receta.html')

@app.route('/ver_recetas')
def ver_recetas():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre FROM recetas')
    recetas = cursor.fetchall()
    conn.close()
    return render_template('ver_recetas.html', recetas=recetas)

@app.route('/editar_receta/<int:id>', methods=['GET', 'POST'])
def editar_receta(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        ingredientes = request.form['ingredientes']
        pasos = request.form['pasos']

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE recetas SET nombre=?, ingredientes=?, pasos=? WHERE id=?
        ''', (nombre, ingredientes, pasos, id))
        conn.commit()
        conn.close()

        return redirect(url_for('ver_recetas'))
    else:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT nombre, ingredientes, pasos FROM recetas WHERE id=?', (id,))
        receta = cursor.fetchone()
        conn.close()
        return render_template('editar_receta.html', receta=receta)

@app.route('/eliminar_receta/<int:id>')
def eliminar_receta(id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM recetas WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('ver_recetas'))

@celery.task
def send_email(subject, sender, recipients, body):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = body
    mail.send(msg)


if __name__ == "__main__":
    app.run(debug=True)
