# Cosas a consultar en clase

- preguntar si siempre el id va a ser +1 en de la pos del arreglo o es cuestion de diseño
- se puede editar el id de una pelicula ??
- se puede editar solo un campo una pelicula o tiene que ser todo completo ?
- en agregar peliculas deberiamos obligar que llene todos los campos ?
- para preguntar por genero ser estrictos o flexibles.

------

# Cosas que tenemos que hacer

- agregar docstrings en todas las funciones
- revisar si faltan revisar index o condiciones
- update esta bien ?

------

# Cosas que tenemos que charlar

- estan bien todas las respuestas de las rutas ?
- en agregar peliculas deberiamos obligar que llene todos los campos ?

# Cosas que poner en el readme
- queriamos que los codigo de http sean algunos otros como el 204 y demas, pero lo cambiamos por los tests
- por lo visto la funcion actualizar debe devolver lo que actualizaste

## envir peticiones
### postman
### curl ej
   
'''
    curl -X PUT http://localhost:5000/peliculas/1 \
    -H "Content-Type: application/json" \
    -d '{"titulo": "Tenet"}'

'''