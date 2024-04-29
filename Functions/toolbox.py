import math
import random
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from mpl_toolkits.mplot3d import Axes3D
from shapely.geometry import Point

from .quincuncial import *  # Importación de una librería personalizada llamada 'quincuncial'
from .n_uncial import *  # Importación de una librería personalizada llamada 'nuncial'


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



def plot_myp(meridianos, paralelos, funcion):
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

def distancia(p1, p2):
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def plot_proyeccion(lista_parejas_ordenadas, funcion, titulo):
    plt.figure(figsize=(15, 12))
    for continente in lista_parejas_ordenadas:
        x = []
        y = []
        r2_proyectado = None
        for punto in continente:
            punto_proyectado = funcion((punto[0], punto[1]))
            if punto_proyectado is not None:
                if r2_proyectado is not None and distancia(punto_proyectado, r2_proyectado) > 0.5:
                    if len(x) > 1 and len(y) > 1:
                        plt.plot(x, y, color='blue', linestyle='-')  # Líneas azules para los continentes
                    x = []
                    y = []
                x.append(punto_proyectado[0])
                y.append(punto_proyectado[1])
                r2_proyectado = punto_proyectado
            else:
                if len(x) > 1 and len(y) > 1:
                    plt.plot(x, y, color='blue', linestyle='-')  # Líneas azules para los continentes
                x = []
                y = []
                r2_proyectado = None
        if len(x) > 1 and len(y) > 1:
            plt.plot(x, y, color='blue', linestyle='-')  # Líneas azules para los continentes
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.title(titulo)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')
    plt.show()

