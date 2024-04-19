from mpmath import *
import numpy as np
import matplotlib.pyplot as plt

def estereografica(theta, p):
    z = np.tan(p/ 2) * np.exp(1j * theta)
    return z

def plot_estereografica(estereo):
    # Extraer las partes real e imaginaria de los puntos en el mapa
    real_part = np.real(estereo)
    imaginary_part = np.imag(estereo)

    # Calcular la distancia al origen para cada punto
    distance_to_origin = real_part**2 + imaginary_part**2

    # Graficar los puntos en el plano complejo
    plt.figure(figsize=(10, 10))
    plt.scatter(real_part[distance_to_origin < 1], imaginary_part[distance_to_origin < 1], color='blue', s=10)
    plt.scatter(real_part[distance_to_origin >= 1], imaginary_part[distance_to_origin >= 1], color='red', s=10)
    plt.xlabel('Parte Real')
    plt.ylabel('Parte Imaginaria')
    plt.xlim(-5, 5)  # Set x-axis limits
    plt.ylim(-5, 5)  # Set y-axis limits
    plt.title('Proyección Estereográfica')
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
