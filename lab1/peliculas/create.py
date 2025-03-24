from flask import jsonify, request
from .utils import obtener_nuevo_id, input_invalido
from .data import peliculas

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

    for i in range(0, len(peliculas)-1):
        if peliculas[i]['titulo'] == pelicula_nueva['titulo']:
            return jsonify(peliculas[i]), 202
        
    if 'titulo' not in campos_pelicula_nueva or 'genero' not in campos_pelicula_nueva:
        return jsonify({"Error": "ID de película inválido"}), 400
    
    if input_invalido(pelicula_nueva['titulo']) or input_invalido(pelicula_nueva['genero']):
        return jsonify({"error": "Formato inválido"}), 400
    
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': pelicula_nueva['titulo'],
        'genero': pelicula_nueva['genero']
    }
    peliculas.append(nueva_pelicula)
    return jsonify(nueva_pelicula), 201