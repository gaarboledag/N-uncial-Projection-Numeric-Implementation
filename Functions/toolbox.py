import math
import random
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from mpl_toolkits.mplot3d import Axes3D
from shapely.geometry import Point

from .quincuncial import *  # Importación de una librería personalizada llamada 'quincuncial'

def generar_meridianos(num_meridianos, num_puntos_por_meridiano):
    # Genera coordenadas de puntos a lo largo de los meridianos en una esfera
    coordenadas = []
    angulo_meridiano = 2 * math.pi / num_meridianos
    for meridiano in range(num_meridianos):
        theta = angulo_meridiano*meridiano
        for punto in range(num_puntos_por_meridiano):
            # Calcular la latitud en radianes
            p = punto*np.pi/num_puntos_por_meridiano
            # Agregar las coordenadas a la lista
            if punto == num_puntos_por_meridiano:
                theta = theta - 0.00001  # Corrección mínima para evitar solapamientos
            coordenadas.append((theta, p))
    return coordenadas

def generar_paralelos(num_paralelos, num_puntos_por_paralelo):
    # Genera coordenadas de puntos a lo largo de los paralelos en una esfera
    coordenadas = []
    angulo_paralelos = math.pi / num_paralelos
    for paralelo in range(num_paralelos): 
        p = paralelo*angulo_paralelos
        for punto in range(num_puntos_por_paralelo):
            # Calcular la longitud en radianes
            theta = punto*2*np.pi/num_puntos_por_paralelo
            # Agregar las coordenadas a la lista
            coordenadas.append((theta, p))
    return coordenadas

def generar_puntos_en_continentes(mapamundi, num_puntos):
    # Genera puntos aleatorios dentro de los continentes de un mapa
    gdf = gpd.read_file(mapamundi)
    continentes = gdf['geometry']
    coordenadas_puntos = []
    for _ in range(num_puntos):
        continente = random.choice(continentes)
        punto_en_continente = generar_punto_en_continente(continente)
        coordenadas_puntos.append(punto_en_continente)
    return coordenadas_puntos

def generar_punto_en_continente(continente):
    # Genera un punto aleatorio dentro de un continente
    xmin, ymin, xmax, ymax = continente.bounds
    punto_x = random.uniform(xmin, xmax)
    punto_y = random.uniform(ymin, ymax)
    punto = Point(punto_x, punto_y)
    while not punto.within(continente):
        punto_x = random.uniform(xmin, xmax)
        punto_y = random.uniform(ymin, ymax)
        punto = Point(punto_x, punto_y)
    return math.radians(punto.x), math.radians(punto.y)

def plot_esfera(puntos):
    # Lista para almacenar las coordenadas x, y, z
    x_data = []
    y_data = []
    z_data = []

    # Iterar sobre los puntos y calcular las coordenadas x, y, z
    for coordenada in puntos:
        theta = coordenada[0]
        p = coordenada[1]
        x = math.sin(p) * math.cos(theta)
        y = math.sin(p) * math.sin(theta)
        z = math.cos(p)
        x_data.append(x)
        y_data.append(y)
        z_data.append(z)

    # Crear un gráfico de dispersión 3D en Plotly
    scatter_plot = go.Scatter3d(x=x_data, y=y_data, z=z_data, mode='markers', marker=dict(color='blue', size=1))

    # Configurar el diseño del gráfico
    layout = go.Layout(scene=dict(xaxis=dict(title='X'),
                                   yaxis=dict(title='Y'),
                                   zaxis=dict(title='Z')),
                       title='Puntos sobre la esfera')

    # Crear figura
    fig = go.Figure(data=[scatter_plot], layout=layout)

    # Mostrar el gráfico interactivo
    fig.show()




def plot_generated_mapamundi(mapamundi, coordenadas_puntos):
    # Grafica puntos sobre un mapa del mundo (estereográfico)
    gdf = gpd.read_file(mapamundi)
    fig, ax = plt.subplots(figsize=(12, 8))
    longitudes, latitudes = zip(*coordenadas_puntos)
    ax.scatter(longitudes, latitudes, color='red', marker='o', s=50)  # Puntos rojos para los puntos generados
    ax.set_title('Distribución de Puntos en Continentes')
    ax.set_xlabel('Longitud (radianes)')
    ax.set_ylabel('Latitud (radianes)')
    plt.gca().set_aspect('equal', adjustable='box')  # Escala 1x1
    plt.show()

def plot_coordenadas(meridianos, paralelos, funcion):
    # Grafica los meridianos y paralelos mapeados según la proyección pasada como función
    img_meridianos = [funcion(punto) for punto in meridianos]
    img_paralelos = [funcion(punto) for punto in paralelos]
    x_meridianos, y_meridianos = zip(*img_meridianos)
    x_paralelos, y_paralelos = zip(*img_paralelos)
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
    axes[0].plot(x_meridianos, y_meridianos,  marker='o', linestyle='none', markersize=0.5)
    axes[0].set_title("Proyeccion quincuncial de meridianos")
    axes[0].set_aspect('equal', adjustable='box')
    axes[1].plot(x_paralelos, y_paralelos,  marker='o', linestyle='none', markersize=0.5, color='orange')
    axes[1].set_title("Proyeccion quincuncial de paralelos")
    axes[1].set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show()

def plot_proyeccion(coordenadas_puntos, funcion):
    # Grafica el mapeo del mapamundi según la proyección pasada como función
    map = []
    for punto in coordenadas_puntos:
        map.append(funcion((punto[0] + np.pi, punto[1] + np.pi/2)))
    filtered_map = [coord for coord in map if coord is not None]
    x, y = zip(*filtered_map)
    plt.plot(x, y, color='blue', marker='o', markersize=0.1, linestyle='none')  # Puntos azules para la proyección
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.title('Peirce Quincuncial Projection')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
