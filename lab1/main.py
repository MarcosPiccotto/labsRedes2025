from flask import Flask
from peliculas.create import agregar_pelicula
from peliculas.read import (
    obtener_peliculas, obtener_pelicula, obtener_peliculas_genero, 
    obtener_pelicula_random, obtener_peliculas_palabra, 
    obtener_pelicula_random_gen, obtener_pelicula_feriado
)
from peliculas.update import actualizar_pelicula
from peliculas.delete import eliminar_pelicula

app = Flask(__name__)     

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

