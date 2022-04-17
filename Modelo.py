# -------------------------------------------------------------------------------------------------------------
# Modelo epidemiologico SIRS implementado con un modelo NIMFA
# Realizado por: Juan Diego Gonzalez Gomez - 201911031
# Basado en el modelo SIS de: https://github.com/MartinGalvanCastro/NimdaModel
# -------------------------------------------------------------------------------------------------------------

# -------------------- Imports -----------------------
import os
import numpy as np
import matplotlib as mpl

from Grafo import Grafo
from pprint import pprint
from random import uniform, seed
from matplotlib import pyplot as plt

# -------------------- Variables globales -----------------------
rngSeed = 32
np.random.seed(rngSeed)
seed(rngSeed)

# -------------------- Clase que representa el modelo --------------------
class Modelo:
    # Funcion que declara e inicializa las variables del modelo
    def __init__(self, adjMatrix: np.array, graph: Grafo, alfaI: float, deltaI: float):
        self.adjMatrix = adjMatrix
        self.n = len(self.adjMatrix)

        self.m = 10
        self.v = np.zeros(self.n)
        self.colors = mpl.colors.Normalize(vmin=0, vmax=1, clip=True)
        self.v[:] = [uniform(0, 0.05) for _ in range(self.n)]
        self.graph = graph
        self.degrees = self.graph.get_degree_of_nodes()

        self.nodes_infected = []
        self.nodes_infected.append(0)

        self.alfaI = alfaI
        self.deltaI = deltaI
        self.alfa = np.zeros(shape=(self.n, self.n))
        self.delta = np.ones(shape=(self.n)) * deltaI

    # Funcion que ejecuta la simulacion del modelo
    def run(self):
        diff = 1
        self.t = 0
        vinit = self.v
        epsilon = 0.0001
        self.calcularalfa(self.t)
        while diff > epsilon:
            pprint(self.alfa)
            u = np.ones(self.n)
            
            temp = self.matrixMul([np.diag(u-self.delta), vinit]) + self.matrixMul([np.diag(u-vinit), self.alfa, vinit])
            vnext = self.checkLimit(temp)
            diff = np.linalg.norm(vnext - vinit)
            vinit = vnext
            self.nodes_infected.append(len(list(filter(lambda x: x >= 0.65, vinit))))
            self.graph.updateValue(vinit)

            print('-------------------- Fin de la iteracion # {} --------------------'.format(str(self.t)))
            self.t += 1
            self.calcularalfa(self.t)

    # -------------------- Otras funciones de la clase --------------------
    # Funcion que calcula la matriz alfa
    def calcularalfa(self,t:int):
        for i in range(self.n):
            if self.nodes_infected[t] == self.n:
                for j in range(self.n):
                    self.alfa[i][j] = self.alfaI
            else:
                alfa = self.alfaI*(1 - (self.nodes_infected[t]/self.n))
                for j in range(self.n):
                    self.alfa[i][j] = alfa * self.adjMatrix[i][j]

    # Funcion que valida si el resultado esta dentro del limite
    def checkLimit(self, v: np.array) -> np.array:
        for i in range(self.n):
            print(self.delta[i])
            tao = (np.sum(self.alfa[i,:])/self.degrees[i][1])/self.delta[i]
            upperBound = 1 - 1/(1 + (tao*self.degrees[i][1]))
            if v[i] < 0:
                v[i] = 0
            elif v[i] > upperBound:
                v[i] = upperBound
        return v

    # Funcion que multiplica las matrices que llegan por parametro
    def matrixMul(self, matrixArray: list) -> np.array:
        resultado = matrixArray[0]
        for i in range(1, len(matrixArray)):
            resultado = np.matmul(resultado, matrixArray[i])
        return resultado

    # Funcion que grafica la evolcion de la infeccion en el tiempo
    def plotTime(self):
        plt.figure()
        t = np.linspace(0, self.t, num=len(self.nodes_infected), endpoint=True)
        plt.title('Nodos infectados vs Tiempo')
        plt.xlabel('Instantes de tiempo')
        plt.ylabel('# de nodos infectados')
        plt.plot(t, self.nodes_infected)
        plt.show()

# Funcion que ejecuta un modelo de prueba en caso de que este archivo sea ejecutado
if __name__=='__main__':
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'Grafos Guardados/5Nodos.json')
    g = Grafo(1, path)
    model = Modelo(g.adjM, g, 0.33, 0.16)
    model.run()

    print("\nEsta fue una ejecucion de prueba para el modelo.\n")
    print("Para ejecutar la aplicacion completa debe ejecutar el archivo \"main.py\".")

    model.plotTime()
