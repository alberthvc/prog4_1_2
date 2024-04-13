import requests

def obtener_cantidad_peliculas_con_planetas_aridos():
    url = 'https://swapi.dev/api/films/?format=json'
    response = requests.get(url)
    data = response.json()
    cantidad_peliculas_con_aridos = 0
    for pelicula in data['results']:
        planetas_url = pelicula['planets']
        for planeta_url in planetas_url:
            planeta_response = requests.get(planeta_url)
            planeta_data = planeta_response.json()
            if 'arid' in planeta_data['climate']:
                cantidad_peliculas_con_aridos += 1
                break  # No necesitamos seguir buscando en esta película si ya encontramos un planeta árido
    return cantidad_peliculas_con_aridos

def obtener_cantidad_wookies():
    url = 'https://swapi.dev/api/species/3/'
    response = requests.get(url)
    data = response.json()
    cantidad_wookies = data['people']
    return len(cantidad_wookies)

def obtener_nombre_aeronave_mas_pequena():
    url = 'https://swapi.dev/api/films/1/'
    response = requests.get(url)
    data = response.json()
    starship_url = data['starships'][0]
    starship_response = requests.get(starship_url)
    starship_data = starship_response.json()
    return starship_data['name']

if __name__ == "__main__":

    print("\nConsumiendo API de SWAPI para respoder preguntas... \n")
    print("A FEW MOMETS LATER ****** ...")
    cantidad_planetas_aridos = obtener_cantidad_peliculas_con_planetas_aridos()
    print("a) ¿En cuántas películas aparecen planetas cuyo clima sea árido?")
    print(f"En la saga de Star Wars hay {cantidad_planetas_aridos} planetas cuyo clima es árido.")

    cantidad_wookies = obtener_cantidad_wookies()
    print("\n\nb) ¿Cuántos Wookies aparecen en toda la saga?")
    print(f"En toda la saga aparecen {cantidad_wookies} Wookies.")

    nombre_aeronave_mas_pequena = obtener_nombre_aeronave_mas_pequena()
    print("\n\nc) ¿Cuál es el nombre de la aeronave más pequeña en la primera película?")
    print(f"El nombre de la aeronave más pequeña en la primera película es: {nombre_aeronave_mas_pequena}")
