import requests

# Obtener todas las películas
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()

# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(f"ID: {pelicula_agregada['id']}, Título: {pelicula_agregada['titulo']}, Género: {pelicula_agregada['genero']}")
else:
    print("Error al agregar la película.")
print()

# Obtener detalles de una película específica
id_pelicula = 1  # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()

# Actualizar los detalles de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(f'http://localhost:5000/peliculas/{id_pelicula}', json=datos_actualizados)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(f"ID: {pelicula_actualizada['id']}, Título: {pelicula_actualizada['titulo']}, Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()

# Eliminar una película
id_pelicula = 1  # ID de la película a eliminar
response = requests.delete(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    print("Película eliminada correctamente.")
else:
    print("Error al eliminar la película.")
print()

# Obtener peliculas de un género especifico ver la vuelta de la api
genero = "Acción"
response = requests.get(f'http://localhost:5000/peliculas/{genero}')
if response.status_code == 200:
    peliculas = response.json()
    print(f"Películas existentes del género {genero}:")
    for pelicula in peliculas:
        print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print(f"No hay películas disponibles del género {genero}.")
print()

# Obtener una película que tenga determinado string en el título

# obtener una pelicula random
response = requests.get(f'http://localhost:5000/peliculas/random')
if response.status_code == 200:
    pelicula = response.json()
    print(f"Películas aleatoria: ")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()

# Obtener una pelicula aleatoria de un género especifico
genero = "Acción"
response = requests.get(f'http://localhost:5000/peliculas/random/{genero}')
if response.status_code == 200:
    pelicula = response.json()
    print(f"Película aleatoria del género {genero}:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print(f"No hay películas disponibles del género {genero}.")
print()

# Obtener una pelicula segun el feriado mas cercano
# genero = "Acción"
# response = requests.get(f'http://localhost:5000/peliculas/random/{genero}')
# if response.status_code == 200:
#     pelicula = response.json()
#     print(pelicula)
#     print(f"Película aleatoria del género {genero}:")
#     # print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}, Motivo: {pelicula['motivo']}, Mes: {pelicula['mes']}, Dia: {pelicula['dia']}")
# else:
#     print(f"No hay películas disponibles del género {genero}.")
# print()
