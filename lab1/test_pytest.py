import requests
import pytest
import requests_mock
from proximo_feriado import NextHoliday

@pytest.fixture
def mock_response():
    with requests_mock.Mocker() as m:
        # Simulamos la respuesta para obtener todas las películas
        m.get('http://localhost:5000/peliculas', json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])

        # Simulamos la respuesta para agregar una nueva película
        m.post('http://localhost:5000/peliculas', status_code=201, json={'id': 3, 'titulo': 'Pelicula de prueba', 'genero': 'Acción'})

        # Simulamos la respuesta para obtener detalles de una película específica
        m.get('http://localhost:5000/peliculas/1', json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})

        # Simulamos la respuesta para actualizar los detalles de una película
        m.put('http://localhost:5000/peliculas/1', status_code=200, json={'id': 1, 'titulo': 'Nuevo título', 'genero': 'Comedia'})

        # Simulamos la respuesta para eliminar una película
        m.delete('http://localhost:5000/peliculas/1', status_code=200)

        # Simulamos la respuesta para obtener peliculas segun el genero
        m.get('http://localhost:5000/peliculas/genero/crimen', status_code=200, json=[{'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'crimen'}])

        # Simulamos la respuesta para obtener una pelicula random
        m.get('http://localhost:5000/peliculas/random', status_code=200)

        # Simulamos la respuesta para obtener una pelicula random segun el genero
        m.get('http://localhost:5000/peliculas/random/crimen', status_code=200, json=[{'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'}])

        # Simulamos la respuesta para obtener la lista de peliculas si la palabra esta en el titulo
        m.get('http://localhost:5000/peliculas/pulp', status_code=200, json=[{'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'crimen'}])


        # next_holiday = NextHoliday()
        # next_holiday.fetch_holidays()
        #next_holiday={"dia":24, "mes":3,"motivo":"dia de verdad"}
        # Simulamos la respuesta para obtener una pelicula segun el genero para el proximo feriado
        #m.get('http://localhost:5000/peliculas/feriado/crimen', status_code=200, json=[{"dia": next_holiday["dia"],
                                                                                        # "genero": "crimen",
                                                                                        # "mes": next_holiday["mes"],
                                                                                        # "motivo": next_holiday["motivo"],
                                                                                        # "titulo": "pulp_fiction"
                                                                                        # }])
        
        yield m

def test_obtener_peliculas(mock_response):
    response = requests.get('http://localhost:5000/peliculas')
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_agregar_pelicula(mock_response):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
    assert response.status_code == 201
    assert response.json()['id'] == 3

def test_obtener_detalle_pelicula(mock_response):
    response = requests.get('http://localhost:5000/peliculas/1')
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Indiana Jones'

def test_actualizar_detalle_pelicula(mock_response):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put('http://localhost:5000/peliculas/1', json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Nuevo título'

def test_eliminar_pelicula(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/1')
    assert response.status_code == 200

def test_obtener_peliculas_genero(mock_response):
    response = requests.get('http://localhost:5000/peliculas/genero/crimen')
    assert response.status_code == 200
    assert response.json()[0]['genero'] == 'crimen'

def test_obtener_pelicula_random(mock_response):
    mock_response.get('http://localhost:5000/peliculas/random', status_code=200,
                    text='{"id": 1, "titulo": "Fake", "genero": "crimen"}')
    response = requests.get('http://localhost:5000/peliculas/random')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert set(data.keys()) == {'id', 'titulo', 'genero'}

def test_obtener_pelicula_random_gen(mock_response):
    response = requests.get('http://localhost:5000/peliculas/random/crimen')
    assert response.status_code == 200
    assert response.json()[0]['genero'].lower() == 'crimen'

def test_obtener_peliculas_palabra(mock_response):
    response = requests.get('http://localhost:5000/peliculas/pulp')
    assert response.status_code == 200
    assert response.json()[0]['titulo'].lower() == 'pulp fiction'

# def test_obtener_pelicula_feriado(mock_response):
#     next_holiday = NextHoliday()
#     response = requests.get('http://localhost:5000/peliculas/feriado/crimen')
#     assert response.status_code == 200
#     # assert response.json()[0]['motivo'] == next_holiday.fetch_holidays().holidays['motivo']
#     assert response.json()[0]['genero'] == 'crimen'