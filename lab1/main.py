from flask import Flask, jsonify, request

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

def id_valido(id):
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

    if(id_valido(id)):
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
    
    if id_valido(id):
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

    if id_valido(id):
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


app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])


if __name__ == '__main__':
    app.run()

