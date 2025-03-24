from flask import Flask, jsonify, request
from random import randint
from proximo_feriado import NextHoliday
from re import fullmatch

app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'indiana_jones', 'genero': 'accion'},
    {'id': 2, 'titulo': 'star_wars', 'genero': 'accion'},
    {'id': 3, 'titulo': 'interstellar', 'genero': 'ciencia_ficcion'},
    {'id': 4, 'titulo': 'jurassic_park', 'genero': 'aventura'},
    {'id': 5, 'titulo': 'the_avengers', 'genero': 'accion'},
    {'id': 6, 'titulo': 'back_to_the_future', 'genero': 'ciencia_ficcion'},
    {'id': 7, 'titulo': 'the_lord_of_the_rings', 'genero': 'fantasia'},
    {'id': 8, 'titulo': 'the_dark_knight', 'genero': 'accion'},
    {'id': 9, 'titulo': 'inception', 'genero': 'ciencia_ficcion'},
    {'id': 10, 'titulo': 'the_shawshank_redemption', 'genero': 'drama'},
    {'id': 11, 'titulo': 'pulp_fiction', 'genero': 'crimen'},
    {'id': 12, 'titulo': 'fight_club', 'genero': 'drama'}
]

# Funciones Auxiliares
def id_invalido(id):
    '''
    Verfica que un id este en rango valido

    Retorna:
    True si esta en rango valido
    False si no esta en rango valido
    '''
    return id < 1 or id > len(peliculas)


def input_invalido(input):
    '''
    Verfica que un url este en el formato correcto

    Criterios de validación:
    - Solo debe contener letras minúsculas, números y guiones bajos (_).
    - No debe tener espacios ni caracteres especiales.
    - No puede comenzar ni terminar con un guion bajo.
    - No debe haber múltiples guiones bajos seguidos (__).

    Retorna:
    True: Esta en formato incorrecto
    False: Esta en formato correcto
    '''
    patron = r'^[a-z0-9]+(?:_[a-z0-9]+)*$'
    return not bool(fullmatch(patron, input))

def obtener_nuevo_id():
    '''
    Obtener un nuevo id.

    Retorna:
    Un id (int).
    '''
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1


# Funciones CREATE
def agregar_pelicula():
    '''
    Agrega una nueva película a la lista.

    Retorna:
    201 si la película se agregó correctamente, junto con la película agregada.
    202 si la pelicula ya está en la base de datos
    400 si faltan parámetros obligatorios.
    '''
    pelicula_nueva = request.json
    campos_pelicula_nueva = pelicula_nueva.keys()

    for pelicula in peliculas:
        if pelicula['titulo'].replace('_', '') == pelicula_nueva['titulo'].replace('_', ''):
            return jsonify(pelicula), 202

    if 'titulo' not in campos_pelicula_nueva or 'genero' not in campos_pelicula_nueva:
        return jsonify({"Error": "Faltan campos"}), 400

    if input_invalido(pelicula_nueva['titulo']) or input_invalido(pelicula_nueva['genero']):
        return jsonify({"error": "Formato inválido"}), 400

    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': pelicula_nueva['titulo'],
        'genero': pelicula_nueva['genero']
    }
    peliculas.append(nueva_pelicula)
    return jsonify(nueva_pelicula), 201


# Funciones READ
def obtener_peliculas():
    '''
    Obtiene la lista completa de películas disponibles.

    Retorna:
    Un objeto JSON con la lista de películas.
    '''
    return jsonify(peliculas)


def obtener_pelicula(id):
    '''
    Busca una película por su ID y devuelve sus detalles en formato JSON.

    Parámetros:
    id (int): Identificador de la película a buscar.

    Assert:
    comprobamos si id esta en rango valido (0 < id < len peliculas).

    Retorna:
    200 si la película se agregó correctamente.
    400 si el id es invalido.
    '''
    if(id_invalido(id)):
        return jsonify({"Error": "ID de película inválido"}), 400

    pelicula_encontrada = peliculas[id-1]
    return jsonify(pelicula_encontrada), 200


def obtener_peliculas_genero(genero):
    '''
    Devuelve el listado de peliculas segun el genero

    Parametros:
    genero (string)

    Retorna:
    200: Listado de peliculas de cierto genero
    400: El genero no se encuentra.
    '''
    if input_invalido(genero):
        return jsonify({"error": "Formato de género inválido"}), 400

    peliculas_gen = []
    for pelicula in peliculas:
        if pelicula["genero"] == genero:
            peliculas_gen.append(pelicula)

    if not peliculas_gen:
        return jsonify({"error":"Género no encontrado"}), 200

    return jsonify(peliculas_gen), 200


def obtener_peliculas_palabra(palabra):
    '''
    Devuelve un listado de películas que contienen el string de la variable palabra en el título.

    Parámetros:
    palabra (string)

    Retorna:
    200: Listado de peliculas con la palabra incluida
    400: No hay peliculas con esa palabra.
    '''
    if input_invalido(palabra):
        return jsonify({"error": "Formato de la palabra inválido"}), 400
    
    peliculas_palabra = []
    for pelicula in peliculas:
        if palabra in pelicula['titulo']:
            peliculas_palabra.append(pelicula)

    return jsonify(peliculas_palabra), 200


def obtener_pelicula_random():
    '''
    Obtiene una pelicula random.
    
    Retorna:
    200: JSON con detalles de una pelicula random
    '''
    rand = randint(0, len(peliculas)-1)
    peli_random = peliculas[rand]
    return jsonify(peli_random), 200


def obtener_pelicula_random_gen(genero):
    '''
    Crea una lista con las peliculas del genero elegido.

    Parametros:
    genero (string)

    Retorna:
    200: JSON con detalles de una pelicula random de cierto genero
    400: No hay peliculas de este genero
    '''
    if input_invalido(genero):
        return jsonify({"error": "Formato de género inválido"}), 400

    pelicula_rand_gen = []
    for pelicula in peliculas:
        if pelicula["genero"] == genero:
            pelicula_rand_gen.append(pelicula)
 
    if not pelicula_rand_gen:
        return jsonify({"Error": "No hay películas de ese género"}), 200

    rand_gen = randint(0, len(pelicula_rand_gen) - 1)
    peli_random_gen = pelicula_rand_gen[rand_gen]
    return jsonify(peli_random_gen), 200

def obtener_pelicula_feriado(genero):
    '''
    Obtiene el proximo feriado con la API externa y una pelicula random segun algun genero.

    Parametros:
    genero (string)

    Retorna:
    200: JSON con detalles de una pelicula random de cierto genero
    400: No hay peliculas de este genero
    '''
    if input_invalido(genero):
        return jsonify({"error": "Formato de género inválido"}), 400

    next_holiday = NextHoliday()
    next_holiday.fetch_holidays()

    pelicula_rand_gen = []
    for pelicula in peliculas:
        if pelicula["genero"] == genero:
            pelicula_rand_gen.append(pelicula)
    if not pelicula_rand_gen:
        return jsonify({"error": "No hay películas de ese género"}), 200

    rand_gen = randint(0, len(pelicula_rand_gen) - 1)
    peli_random_gen = pelicula_rand_gen[rand_gen]

    eleccion = {
        'id': peli_random_gen['id'],
        'titulo': peli_random_gen['titulo'],
        'genero': peli_random_gen['genero'],
        'motivo': next_holiday.holiday['motivo'],
        'dia': next_holiday.holiday['dia'],
        'mes': next_holiday.holiday['mes']
    }

    return jsonify(eleccion), 200


# Funciones Update
def actualizar_pelicula(id):
    '''
    Actualiza una película por su ID y devuelve sus detalles en formato JSON.

    Parámetros:
    id (int): Identificador de la película a buscar.

    Retorna:
    200 si la película se agregó correctamente.
    400 si el id es invalido o se intenta modificar el id.
    '''
    if id_invalido(id):
        return jsonify({"error": "ID de película inválido"}), 400

    pelicula_nueva = request.json
    if "id" in pelicula_nueva.keys():
        return jsonify({"error": "No esta permitido editar el ID"}), 400
    if input_invalido(pelicula_nueva['titulo']) or input_invalido(pelicula_nueva['genero']):
        return jsonify({"error": "Formato inválido"}), 400

    pelicula_nueva = {
        "id":id,
        **pelicula_nueva
    }
    peliculas[id-1] = pelicula_nueva
    return jsonify(pelicula_nueva), 200


# Funciones DELETE
def eliminar_pelicula(id):
    '''
    Elimina una película por su ID.

    Parámetros:
    id (int): Identificador de la película a buscar.

    Assert:
    comprobamos si id esta en rango valido (0 < id < len peliculas).

    Retorna:
    200 si la película se agregó correctamente.
    400 si el id es invalido o se intenta modificar el id.
    '''
    if id_invalido(id):
        return jsonify({"error": "ID de película inválido"}), 400

    del peliculas[id-1]
    for i in range(id-1, len(peliculas)):
        peliculas[i]["id"] -= 1
    return f'Pelicula numero {id} eliminada.', 200


app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])

app.add_url_rule('/peliculas/genero/<string:genero>', 'obtener_peliculas_genero', obtener_peliculas_genero, methods=['GET'])
app.add_url_rule('/peliculas/<string:palabra>', 'obtener_peliculas_palabra', obtener_peliculas_palabra, methods=['GET'])
app.add_url_rule('/peliculas/random', 'obtener_pelicula_random', obtener_pelicula_random, methods=['GET'])
app.add_url_rule('/peliculas/random/<string:genero>', 'obtener_pelicula_random_gen', obtener_pelicula_random_gen, methods=['GET'])

app.add_url_rule('/peliculas/feriado/<string:genero>', 'obtener_pelicula_feriado', obtener_pelicula_feriado, methods=['GET'])

if __name__ == '__main__':
    app.run()

