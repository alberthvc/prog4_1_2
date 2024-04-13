import requests

def obtener_cantidad_planetas_aridos():
    url = 'https://swapi.dev/api/planets/?format=json'
    response = requests.get(url)
    data = response.json()
    planetas_aridos = [planeta for planeta in data['results'] if 'arid' in planeta['climate']]
    return len(planetas_aridos)

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
    cantidad_planetas_aridos = obtener_cantidad_planetas_aridos()
    print(f"En la saga de Star Wars hay {cantidad_planetas_aridos} planetas cuyo clima es árido.")

    cantidad_wookies = obtener_cantidad_wookies()
    print(f"En toda la saga aparecen {cantidad_wookies} Wookies.")

    nombre_aeronave_mas_pequena = obtener_nombre_aeronave_mas_pequena()
    print(f"El nombre de la aeronave más pequeña en la primera película es: {nombre_aeronave_mas_pequena}")
