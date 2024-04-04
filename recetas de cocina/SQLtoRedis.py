import redis

# Conexión a la base de datos Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def agregar_receta():
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por comas): ")
    pasos = input("Pasos de la receta (separados por comas): ")

    receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "pasos": pasos
    }

    redis_client.hmset(nombre, receta)
    print("Receta agregada correctamente.")

def ver_recetas():
    recetas_keys = redis_client.keys()
    for key in recetas_keys:
        receta = redis_client.hgetall(key)
        print(f"Nombre: {receta[b'nombre'].decode('utf-8')}")
        print(f"Ingredientes: {receta[b'ingredientes'].decode('utf-8')}")
        print(f"Pasos: {receta[b'pasos'].decode('utf-8')}")
        print()

def buscar_receta():
    termino = input("Ingrese un ingrediente o palabra clave: ")
    recetas_keys = redis_client.keys()
    for key in recetas_keys:
        receta = redis_client.hgetall(key)
        ingredientes = receta[b'ingredientes'].decode('utf-8')
        if termino in ingredientes:
            print(f"Nombre: {receta[b'nombre'].decode('utf-8')}")
            print(f"Ingredientes: {ingredientes}")
            print(f"Pasos: {receta[b'pasos'].decode('utf-8')}")
            print()

def eliminar_receta():
    nombre_receta = input("Nombre de la receta a eliminar: ")
    resultado = redis_client.delete(nombre_receta)
    if resultado == 1:
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

if __name__ == "__main__":
    main()
