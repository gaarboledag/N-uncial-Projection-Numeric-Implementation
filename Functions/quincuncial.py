from mpmath import *
import numpy as np

def quincuncial(punto):
    coordenada = encontrar_octante(punto)
    theta = coordenada[0][0]  # Extrae el ángulo theta
    p = coordenada[0][1]  # Extrae el ángulo p
    octante = coordenada[1]  # Extrae el octante
    K = 1.854074677  # Constante K
    
    # Fórmulas de la proyección quincuncial en el Teorema 2.4
    x=0.5*ellipf(np.arccos(round((2*(np.tan(p/2)**2)-np.sqrt((1+np.tan(p/2)**4)**2-4*np.tan(p/2)**4*np.cos(2*theta)**2))/(1+(2*np.tan(p/2)**2)*np.cos(2*theta)-np.tan(p/2)**4), 9)), 0.5)
    y=0.5*ellipf(np.arccos(round((1+(2*np.tan(p/2)**2)*np.cos(2*theta)-np.tan(p/2)**4)/(2*(np.tan(p/2)**2)+np.sqrt((1+np.tan(p/2)**4)**2-4*np.tan(p/2)**4*np.cos(2*theta)**2)), 9)), 0.5)

    # Devuelve las coordenadas cartesianas transformadas según el octante
    if octante == 1:# 3 ¿?
        #pass
        return (float(x),-float(y))
    if octante == 2:# 4
        #pass
        return (2*K-float(x),-float(y))
    if octante == 3:# 1
        #pass
        return (float(x),float(y))
    if octante == 4:# 2
        #pass
        return (2*K-float(x),float(y))
    if octante == 5: #...
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

# Función para determinar en qué octante se encuentra un punto dado
def encontrar_octante(punto):
    theta = punto[0]
    p = punto[1]
    octante=40
    

    if p < np.pi/2:
        if theta >= 0 and theta < np.pi/2:
            octante = 1 # 3
            theta=theta-np.pi/2
        if theta > 3*np.pi/2 and theta <= 2*np.pi:
            octante = 2 # 4
            theta=theta+np.pi/2
        if theta >= np.pi/2 and theta < np.pi:
            octante = 3 # 1
            theta=theta-np.pi/2
        if  theta >= np.pi and theta <= 3*np.pi/2:
            octante = 4 # 2
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
    return ((theta, p), octante) # Devuelve el ángulo ajustado y el octante determinado


