from re import fullmatch
from .data import peliculas

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
