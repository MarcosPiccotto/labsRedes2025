from flask import jsonify
from .utils import id_invalido
from .data import peliculas

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
