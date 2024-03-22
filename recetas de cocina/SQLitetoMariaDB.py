from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexión a la base de datos MariaDB
engine = create_engine('mysql+mysqlconnector://usuario:contraseña@localhost/nombre_basedatos')
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
