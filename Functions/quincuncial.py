from mpmath import *
from mpl_toolkits.mplot3d import Axes3D
import geopandas as gpd
import math
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import random
import math
import matplotlib.pyplot as plt


def quincuncial(punto):
    coordenada = encontrar_octante(punto)
    theta = coordenada[0][0]
    p = coordenada[0][1]
    octante = coordenada[1]
    K=1.854074677
    
    x=0.5*ellipf(np.arccos(round((2*(np.tan(p/2)**2)-np.sqrt((1+np.tan(p/2)**4)**2-4*np.tan(p/2)**4*np.cos(2*theta)**2))/(1+(2*np.tan(p/2)**2)*np.cos(2*theta)-np.tan(p/2)**4), 9)), 0.5)
    y=0.5*ellipf(np.arccos(round((1+(2*np.tan(p/2)**2)*np.cos(2*theta)-np.tan(p/2)**4)/(2*(np.tan(p/2)**2)+np.sqrt((1+np.tan(p/2)**4)**2-4*np.tan(p/2)**4*np.cos(2*theta)**2)), 9)), 0.5)

     
    if octante == 1:#cuad 3
        #pass
        return (float(x),-float(y))
    if octante == 2:# cuad 4
        #pass
        return (2*K-float(x),-float(y))
    if octante == 3:# cuad 1
        #pass
        return (float(x),float(y))
    if octante == 4:#cuad 2
        #pass
        return (2*K-float(x),float(y))
    if octante == 5:
        #pass
        return (-float(x),float(y))
    if octante == 6:
        #pass
        return (-float(x),2*K-float(y))
    if octante == 7:
        #pass
        return (float(x),float(y))
    if octante == 8:
        #pass
        return (float(x), 2*K-float(y))


def encontrar_octante(punto):
    theta = punto[0]
    p = punto[1]
    octante=40
    
    if p < np.pi/2:
        if theta >= 0 and theta < np.pi/2:
            octante = 1 # cuad 3
            theta=theta-np.pi/2
        if theta > 3*np.pi/2 and theta <= 2*np.pi:
            octante = 2 # cuad 4
            theta=theta+np.pi/2
        if theta >= np.pi/2 and theta < np.pi:
            octante = 3 # cuad 1
            theta=theta-np.pi/2
        if  theta >= np.pi and theta <= 3*np.pi/2:
            octante = 4 # cuad 2
            theta=theta+np.pi/2

    elif p >= np.pi/2:
        if theta >= 0 and theta < np.pi/2:
            octante = 5
            theta=theta-np.pi/2
        if theta > 3*np.pi/2 and theta <= 2*np.pi:
            octante = 6
            theta=theta+np.pi/2
        if theta >= np.pi/2 and theta < np.pi:
            octante = 7
            theta=theta-np.pi/2
        if  theta >= np.pi and theta <= 3*np.pi/2:
            theta=theta+np.pi/2
            octante = 8
    return ((theta, p), octante)


