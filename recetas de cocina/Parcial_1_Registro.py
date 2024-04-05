import json

# Función para cargar los datos del archivo JSON
def cargar_datos():
    try:
        with open('presupuesto.json', 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []

# Función para guardar los datos en el archivo JSON
def guardar_datos(datos):
    with open('presupuesto.json', 'w') as archivo:
        json.dump(datos, archivo, indent=4)

# Función para registrar un nuevo artículo en el presupuesto
def registrar_articulo():
    nombre = input("Ingrese el nombre del artículo: ")
    cantidad = float(input("Ingrese la cantidad: "))
    precio_unitario = float(input("Ingrese el precio unitario: "))

    nuevo_articulo = {
        "nombre": nombre,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario
    }

    datos = cargar_datos()
    datos.append(nuevo_articulo)
    guardar_datos(datos)
    print("Artículo registrado correctamente.")

# Función para buscar un artículo por nombre
def buscar_articulo():
    nombre_buscar = input("Ingrese el nombre del artículo a buscar: ")
    datos = cargar_datos()
    for articulo in datos:
        if articulo["nombre"] == nombre_buscar:
            print("Artículo encontrado:")
            print(articulo)
            return
    print("No se encontró ningún artículo con ese nombre.")

# Función para editar un artículo por nombre
def editar_articulo():
    nombre_editar = input("Ingrese el nombre del artículo a editar: ")
    datos = cargar_datos()
    for articulo in datos:
        if articulo["nombre"] == nombre_editar:
            print("Artículo encontrado:")
            print(articulo)
            cantidad = float(input("Ingrese la nueva cantidad: "))
            precio_unitario = float(input("Ingrese el nuevo precio unitario: "))
            articulo["cantidad"] = cantidad
            articulo["precio_unitario"] = precio_unitario
            guardar_datos(datos)
            print("Artículo editado correctamente.")
            return
    print("No se encontró ningún artículo con ese nombre.")

# Función para eliminar un artículo por nombre
def eliminar_articulo():
    nombre_eliminar = input("Ingrese el nombre del artículo a eliminar: ")
    datos = cargar_datos()
    for articulo in datos:
        if articulo["nombre"] == nombre_eliminar:
            datos.remove(articulo)
            guardar_datos(datos)
            print("Artículo eliminado correctamente.")
            return
    print("No se encontró ningún artículo con ese nombre.")

# Función principal para el menú de la aplicación
def main():
    while True:
        print("\n******* Bienvenido al sistema de registro de presupuesto *******")
        print("1. Registrar artículo")
        print("2. Buscar artículo")
        print("3. Editar artículo")
        print("4. Eliminar artículo")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_articulo()
        elif opcion == "2":
            buscar_articulo()
        elif opcion == "3":
            editar_articulo()
        elif opcion == "4":
            eliminar_articulo()
        elif opcion == "5":
            print("Gracias por usar el sistema de registro de presupuesto. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()
