import pymongo

# MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["recetas"]
recetas_collection = db["recetas"]

def agregar_receta():
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por comas): ").split(",")
    pasos = input("Pasos de la receta (separados por comas): ").split(",")

    receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "pasos": pasos
    }

    recetas_collection.insert_one(receta)
    print("Receta agregada correctamente.")

def ver_recetas():
    recetas = recetas_collection.find({})
    for receta in recetas:
        print(f"Nombre: {receta['nombre']}")
        print(f"Ingredientes: {', '.join(receta['ingredientes'])}")
        print(f"Pasos: {', '.join(receta['pasos'])}")
        print()

def buscar_receta():
    termino = input("Ingrese un ingrediente o palabra clave: ")
    recetas = recetas_collection.find({"ingredientes": {"$regex": f".*{termino}.*"}})
    for receta in recetas:
        print(f"Nombre: {receta['nombre']}")
        print(f"Ingredientes: {', '.join(receta['ingredientes'])}")
        print(f"Pasos: {', '.join(receta['pasos'])}")
        print()

def eliminar_receta():
    nombre_receta = input("Nombre de la receta a eliminar: ")
    resultado = recetas_collection.delete_one({"nombre": nombre_receta})
    if resultado.deleted_count == 1:
        print("Receta eliminada correctamente.")
    else:
        print("No se encontró ninguna receta con ese nombre.")

def main():
    while True:
        print("\n--- Libro de Recetas ---")
        print("a) Agregar nueva receta")
        print("b) Ver listado de recetas")
        print("c) Buscar ingredientes y pasos de receta")
        print("d) Eliminar receta")
        print("e) Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == 'a':
            agregar_receta()
        elif opcion == 'b':
            ver_recetas()
        elif opcion == 'c':
            buscar_receta()
        elif opcion == 'd':
            eliminar_receta()
        elif opcion == 'e':
            break
        else:
            print("Opción no válida. Intente nuevamente.")

    client.close()

if __name__ == "__main__":
    main()