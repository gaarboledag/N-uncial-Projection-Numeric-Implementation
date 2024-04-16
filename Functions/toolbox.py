import math
import numpy as np
import matplotlib.pyplot as plt
from .quincuncial import *
import geopandas as gpd
from shapely.geometry import Point
import random
import math
import matplotlib.pyplot as plt



def generar_meridianos(num_meridianos, num_puntos_por_meridiano):
    coordenadas = []
    angulo_meridiano = 2 * math.pi / num_meridianos
    for meridiano in range(num_meridianos+1):
        theta = angulo_meridiano*meridiano
        for punto in range(num_puntos_por_meridiano+1):
            # Calcular la latitud en radianes
            p = punto*np.pi/num_puntos_por_meridiano
            # Agregar las coordenadas a la lista
            
            if punto == num_puntos_por_meridiano + 1:
                theta = theta - 0.00001
            
            coordenadas.append((theta, p))
            
            
    return coordenadas

def generar_paralelos(num_paralelos, num_puntos_por_paralelo):
    coordenadas = []
    angulo_paralelos = math.pi / num_paralelos
    for paralelo in range(num_paralelos+1):   # Ajuste para incluir el ecuador
        p = paralelo*angulo_paralelos
        for punto in range(num_puntos_por_paralelo+1):
            # Calcular la longitud en radianes
            theta = punto*2*np.pi/num_puntos_por_paralelo
            # Agregar las coordenadas a la lista
            coordenadas.append((theta, p))
    return coordenadas

def generar_puntos_en_continentes(mapamundi, num_puntos):
    gdf = gpd.read_file(mapamundi)
    continentes = gdf['geometry']
    coordenadas_puntos = []

    for _ in range(num_puntos):
        continente = random.choice(continentes)
        punto_en_continente = generar_punto_en_continente(continente)
        coordenadas_puntos.append(punto_en_continente)

    return coordenadas_puntos

def generar_punto_en_continente(continente):
    xmin, ymin, xmax, ymax = continente.bounds
    punto_x = random.uniform(xmin, xmax)
    punto_y = random.uniform(ymin, ymax)
    punto = Point(punto_x, punto_y)

    while not punto.within(continente):
        punto_x = random.uniform(xmin, xmax)
        punto_y = random.uniform(ymin, ymax)
        punto = Point(punto_x, punto_y)

    return math.radians(punto.x), math.radians(punto.y)


def plot_esfera(meridianos, paralelos):
    # Graficar los puntos en una esfera
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for coordenada in meridianos:
        theta = coordenada[0]
        p = coordenada[1]

        x = math.sin(p) * math.cos(theta)
        y = math.sin(p) * math.sin(theta)
        z = math.cos(p)

        ax.scatter(x, y, z, color='b')

    for coordenada in paralelos:
        theta = coordenada[0]
        p = coordenada[1]

        x = math.sin(p) * math.cos(theta)
        y = math.sin(p) * math.sin(theta)
        z = math.cos(p)

        ax.scatter(x, y, z, color='r')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Meridianos y Paralelos Generados')

    plt.show(meridianos, paralelos) 

def plot_coord_quinc(meridianos, paralelos):
    img_meridianos = [quincuncial(punto) for punto in meridianos]
    img_paralelos = [quincuncial(punto) for punto in paralelos]
    
    # Desempaquetar las coordenadas
    x_meridianos, y_meridianos = zip(*img_meridianos)
    x_paralelos, y_paralelos = zip(*img_paralelos)

    #Crear un cuadro de subgráficos con 1 fila y 2 columnas
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

    # Primer gráfico
    axes[0].plot(x_meridianos, y_meridianos,  marker='o', linestyle='none', markersize=0.5)
    axes[0].set_title("Proyeccion quincuncial de meridianos")
    axes[0].set_aspect('equal', adjustable='box')

    # Segundo gráfico
    axes[1].plot(x_paralelos, y_paralelos,  marker='o', linestyle='none', markersize=0.5, color='orange')
    axes[1].set_title("Proyeccion quincuncial de paralelos")
    axes[1].set_aspect('equal', adjustable='box')

    # Ajustar el diseño
    plt.tight_layout()

    plt.show()

def plot_generated_mapamundi(mapamundi, coordenadas_puntos):
    gdf = gpd.read_file(mapamundi)
    fig, ax = plt.subplots(figsize=(12, 8))

    # Extraer las coordenadas de latitud y longitud de los puntos
    longitudes, latitudes = zip(*coordenadas_puntos)

    # Graficar los puntos sobre el mapa
    ax.scatter(longitudes, latitudes, color='red', marker='o', s=50)

    # Configuración adicional del gráfico
    ax.set_title('Distribución de Puntos en Continentes')
    ax.set_xlabel('Longitud (radianes)')
    ax.set_ylabel('Latitud (radianes)')
    
    # Configurar la escala 1x1
    plt.gca().set_aspect('equal', adjustable='box')

    # Mostrar el gráfico
    plt.show()

def plot_quincuncial(coordenadas_puntos):
    map = []
    for punto in coordenadas_puntos:
        map.append(quincuncial((punto[0] + np.pi, punto[1] + np.pi/2)))
    
    # Filtrar los valores no nulos
    filtered_map = [coord for coord in map if coord is not None]
    
    # Desempaquetar las coordenadas
    x, y = zip(*filtered_map)
    
    # Graficar líneas en lugar de puntos
    plt.plot(x, y, color='blue', marker='o', markersize=0.1, linestyle='none')
    
    # Configurar etiquetas y título
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.title('Peirce Quincuncial Projection')
    
    # Configurar la escala 1x1
    plt.gca().set_aspect('equal', adjustable='box')
    
    # Mostrar la gráfica
    plt.show()
