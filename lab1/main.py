from flask import Flask, jsonify, request
from random import randint
from proximo_feriado import NextHoliday

app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]

def id_invalido(id):
    """
    Verfica que un id este en rango valido

    Retorna:
    True si esta en rango valido
    False si no esta en rango valido
    """
    return id < 1 or id > len(peliculas)  


def obtener_peliculas():
    """
    Obtiene la lista completa de películas disponibles.

    Retorna:
    Un objeto JSON con la lista de películas.
    """
    return jsonify(peliculas)


def obtener_pelicula(id):
    """
    Busca una película por su ID y devuelve sus detalles en formato JSON.

    Parámetros:
    id (int): Identificador de la película a buscar.

    Assert: 
    comprobamos si id esta en rango valido (0 < id < len peliculas).

    Retorna: 
    200 si la película se agregó correctamente.
    400 si el id es invalido.
    """

    if(id_invalido(id)):
        return jsonify({"Error": "ID de película inválido"}), 400
    
    pelicula_encontrada = peliculas[id-1]
    return jsonify(pelicula_encontrada), 200


def agregar_pelicula():
    """
    Agrega una nueva película a la lista.

    Assert: recibir un JSON con los campos 'nombre' y 'genero'.

    Retorna:
    201 si la película se agregó correctamente, junto con la película agregada.
    400 si faltan parámetros obligatorios.
    """

    campos_pelicula_nueva = request.json.keys()
    if 'titulo' not in campos_pelicula_nueva or 'genero' not in campos_pelicula_nueva:
        return jsonify({"Error": "ID de película inválido"}), 400
    
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id):
    """
    Actualiza una película por su ID y devuelve sus detalles en formato JSON.

    Parámetros:
    id (int): Identificador de la película a buscar.

    Assert: 
    comprobamos si id esta en rango valido (0 < id < len peliculas).

    Retorna: 
    200 si la película se agregó correctamente.
    400 si el id es invalido o se intenta modificar el id.
    """
    
    if id_invalido(id):
        return jsonify({"error": "ID de película inválido"}), 400
    
    nueva_pelicula = request.json
    if "id" in nueva_pelicula.keys():
        return jsonify({"error": "No esta permitido editar el ID"}), 400
    
    nueva_pelicula = {
        "id":id,
        **nueva_pelicula
    }
    peliculas[id-1] = nueva_pelicula
    return jsonify(nueva_pelicula), 200


def eliminar_pelicula(id):
    """
    Elimina una película por su ID.

    Parámetros:
    id (int): Identificador de la película a buscar.

    Assert: 
    comprobamos si id esta en rango valido (0 < id < len peliculas).

    Retorna: 
    200 si la película se agregó correctamente.
    400 si el id es invalido o se intenta modificar el id.
    """

    if id_invalido(id):
        return jsonify({"error": "ID de película inválido"}), 400
    
    del peliculas[id-1]
    for i in range(id-1, len(peliculas)):
        peliculas[i]["id"] -= 1 
    return '', 200


def obtener_nuevo_id():
    """
    Obtener un nuevo id.

    Retorna: 
    Un id (int).
    """
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1


def obtener_peliculas_genero(genero):
    """"
    Devuelve el listado de peliculas segun el genero

    Parametros:
    genero (string)

    Retorna
    Un objeto JSON con la lista de películas del genero pasado ?.
    """
    genero = genero.capitalize()

    peliculas_gen = []
    for pelicula in peliculas:
        if pelicula["genero"] == genero:
            peliculas_gen.append(pelicula)

    if not peliculas_gen:
        return jsonify({"error": "Género no encontrado"}), 400
    return jsonify(peliculas_gen), 200


def obtener_pelicula_random():
    '''
    Obtiene una pelicula random.
    
    Retorna:
    Una JSON con detalles de una pelicula random.
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
    Una pelicula random de esa lista.
    '''
    pelicula_rand_gen = []
    for pelicula in peliculas:
        if pelicula["genero"] == genero:
            pelicula_rand_gen.append(pelicula)
    if not pelicula_rand_gen:
        return jsonify({"Error": "No hay películas de ese género"}), 400
    rand_gen = randint(0, len(pelicula_rand_gen) - 1)
    peli_random_gen = pelicula_rand_gen[rand_gen]
    return jsonify(peli_random_gen), 200

def obtener_pelicula_feriado(genero):
    '''
    Obtiene el proximo feriado con la API externa y una pelicula random segun algun genero.
    
    Parametros:
    genero (string)
    
    Retorna: 
    Un JSON con toda información.
    '''
    next_holiday = NextHoliday()
    next_holiday.fetch_holidays("inamovible")
    
    pelicula_rand_gen = []
    for pelicula in peliculas:
        if pelicula["genero"] == genero:
            pelicula_rand_gen.append(pelicula)
    if not pelicula_rand_gen:
        return jsonify({"Error": "No hay películas de ese género"}), 400
    
    rand_gen = randint(0, len(pelicula_rand_gen) - 1)
    peli_random_gen = pelicula_rand_gen[rand_gen]
    
    eleccion = {'titulo': peli_random_gen['titulo'],
                'genero': peli_random_gen['genero'],
                'motivo': next_holiday.holiday['motivo'],
                'dia': next_holiday.holiday['dia'],
                'mes': next_holiday.holiday['mes']}
    
    return jsonify(eleccion), 200


app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])

app.add_url_rule('/peliculas/<string:genero>', 'obtener_peliculas_genero', obtener_peliculas_genero, methods=['GET'])
app.add_url_rule('/peliculas/random', 'obtener_pelicula_random', obtener_pelicula_random, methods=['GET'])
app.add_url_rule('/peliculas/random/<string:genero>', 'obtener_pelicula_random_gen', obtener_pelicula_random_gen, methods=['GET'])

app.add_url_rule('/peliculas/feriado/<string:genero>', 'obtener_pelicula_feriado', obtener_pelicula_feriado, methods=['GET'])

if __name__ == '__main__':
    app.run()

