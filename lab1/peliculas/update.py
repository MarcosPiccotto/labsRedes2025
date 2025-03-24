from flask import jsonify, request
from .utils import id_invalido, input_invalido
from .data import peliculas

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
