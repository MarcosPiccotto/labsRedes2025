from flask import jsonify
from random import randint
from .utils import input_invalido, id_invalido
from .data import peliculas
from proximo_feriado.proximo_feriado import NextHoliday

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
