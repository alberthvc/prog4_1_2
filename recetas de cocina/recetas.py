import sqlite3

# Conexión a la base de datos SQLite
conn = sqlite3.connect('recetas.db')
cursor = conn.cursor()

# Crear tabla para almacenar recetas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS recetas (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        ingredientes TEXT,
        pasos TEXT
    )
''')
conn.commit()

def agregar_receta():
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por comas): ")

    pasos = []
    contador_pasos = 1

    while True:
        paso = input(f"Paso {contador_pasos}: Agrega un paso de la receta (escribe 'fin' para terminar): ")
        if paso.lower() == 'fin':
            break
        pasos.append(f"{contador_pasos}. {paso}")
        contador_pasos += 1

    pasos_completos = "\n".join(pasos)

    cursor.execute('INSERT INTO recetas (nombre, ingredientes, pasos) VALUES (?, ?, ?)',
                   (nombre, ingredientes, pasos_completos))
    conn.commit()
    print("Receta agregada correctamente.")

def actualizar_receta():
    id_receta = input("ID de la receta a actualizar: ")
    nombre = input("Nuevo nombre de la receta: ")
    ingredientes = input("Nuevos ingredientes: ")
    pasos = input("Nuevos pasos: ")

    cursor.execute('''
        UPDATE recetas
        SET nombre=?, ingredientes=?, pasos=?
        WHERE id=?
    ''', (nombre, ingredientes, pasos, id_receta))
    conn.commit()
    print("Receta actualizada correctamente.")

def eliminar_receta():
    id_receta = input("ID de la receta a eliminar: ")

    cursor.execute('SELECT * FROM recetas WHERE id=?', (id_receta,))
    receta_existente = cursor.fetchone()

    if receta_existente:
        cursor.execute('DELETE FROM recetas WHERE id=?', (id_receta,))
        conn.commit()
        print("Receta eliminada correctamente.")
    else:
        print("No se encontró ninguna receta con ese ID.")



def ver_recetas():
    cursor.execute('SELECT id, nombre FROM recetas')
    recetas = cursor.fetchall()
    for receta in recetas:
        print(f"{receta[0]}. {receta[1]}")

def buscar_receta():
    termino = input("Ingrese un ingrediente o palabra clave: ")
    cursor.execute('SELECT nombre, ingredientes, pasos FROM recetas WHERE ingredientes LIKE ?',
                   ('%' + termino + '%',))
    resultados = cursor.fetchall()
    for resultado in resultados:
        print(f"Receta: {resultado[0]}\nIngredientes: {resultado[1]}\nPasos: {resultado[2]}\n")

def main():
    while True:
        print("\n--- Libro de Recetas ---")
        print("a) Agregar nueva receta")
        print("b) Actualizar receta existente")
        print("c) Eliminar receta existente")
        print("d) Ver listado de recetas")
        print("e) Buscar ingredientes y pasos de receta")
        print("f) Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == 'a':
            agregar_receta()
        elif opcion == 'b':
            actualizar_receta()
        elif opcion == 'c':
            eliminar_receta()
        elif opcion == 'd':
            ver_recetas()
        elif opcion == 'e':
            buscar_receta()
        elif opcion == 'f':
            break
        else:
            print("Opción no válida. Intente nuevamente.")

    conn.close()

if __name__ == "__main__":
    main()
