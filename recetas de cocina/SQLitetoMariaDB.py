import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexión a la base de datos MariaDB
engine = create_engine('mysql+mysqlconnector://root:rubik02@localhost/bd_recetas')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Definir la clase Receta utilizando SQLAlchemy ORM
class Receta(Base):
    __tablename__ = 'recetas'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    ingredientes = Column(Text)
    pasos = Column(Text)

# Crear la tabla si no existe
Base.metadata.create_all(engine)

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

    nueva_receta = Receta(nombre=nombre, ingredientes=ingredientes, pasos=pasos_completos)
    session.add(nueva_receta)
    session.commit()
    print("Receta agregada correctamente.")

def actualizar_receta():
    id_receta = input("ID de la receta a actualizar: ")
    receta = session.query(Receta).filter_by(id=id_receta).first()

    if receta:
        print("Receta actual:")
        print(f"Nombre: {receta.nombre}")
        print(f"Ingredientes: {receta.ingredientes}")
        print(f"Pasos: {receta.pasos}")

        nuevo_nombre = input("Nuevo nombre (dejar vacío para mantener el mismo): ")
        nuevo_ingredientes = input("Nuevos ingredientes (dejar vacío para mantener los mismos): ")
        nuevo_pasos = input("Nuevos pasos (dejar vacío para mantener los mismos): ")

        if nuevo_nombre:
            receta.nombre = nuevo_nombre
        if nuevo_ingredientes:
            receta.ingredientes = nuevo_ingredientes
        if nuevo_pasos:
            receta.pasos = nuevo_pasos

        session.commit()
        print("Receta actualizada correctamente.")
    else:
        print("No se encontró ninguna receta con ese ID.")

def eliminar_receta():
    id_receta = input("ID de la receta a eliminar: ")
    receta = session.query(Receta).filter_by(id=id_receta).first()

    if receta:
        confirmacion = input(f"¿Estás seguro de que deseas eliminar la receta '{receta.nombre}'? (s/n): ")
        if confirmacion.lower() == 's':
            session.delete(receta)
            session.commit()
            print("Receta eliminada correctamente.")
    else:
        print("No se encontró ninguna receta con ese ID.")

def ver_recetas():
    recetas = session.query(Receta).all()
    for receta in recetas:
        print(f"{receta.id}. {receta.nombre}")

def buscar_receta():
    termino = input("Ingrese un ingrediente o palabra clave: ")
    resultados = session.query(Receta).filter(Receta.ingredientes.like(f'%{termino}%')).all()
    for resultado in resultados:
        print(f"Receta: {resultado.nombre}\nIngredientes: {resultado.ingredientes}\nPasos: {resultado.pasos}\n")

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

    session.close()

if __name__ == "__main__":
    main()
