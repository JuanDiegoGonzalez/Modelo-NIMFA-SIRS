# -------------------------------------------------------------------------------------------------------------
# Heterogeneous NIMFA model with infection constant as a relation betweeen current I and P
# Author: Martin Galvan
# Class for making a simulation of NIMFA model with infection constant as a relation betweeen current I and P
# Version: 1.0
# -------------------------------------------------------------------------------------------------------------

import os
from Modelo import NIMFA
from Graph import Graph
import numpy as np
from matplotlib import pyplot as plt
from pprint import pprint











class NIMFA_Fixed(NIMFA):
    def __init__(self, adjMatrix: np.array, graph: Graph, delta:float):
        self.adjMatrix = adjMatrix
        self.n = len(self.adjMatrix)
        self.m = 10
        self.v = np.zeros(self.n)
        self.colors = mpl.colors.Normalize(vmin=0, vmax=1, clip=True)
        self.v[:] = [uniform(0, 0.05) for _ in range(self.n)]
        self.graph = graph
        self.degrees = self.graph.get_degree_of_nodes()
        self.nodes_infected = []

        super().__init__(adjMatrix, graph)
        self.betaI = 0.05
        self.nodes_infected.append(0)
        self.beta = np.zeros(shape=(self.n,self.n))
        self.delta = np.ones(shape=(self.n))*delta

    def run(self):
        vinit = self.v
        self.calcularBeta(self.t)
        while diff>epsilon:


            u = np.ones(self.n)
            A = np.diag(u-self.delta)
            B = np.diag(u-vinit)

            C = self.matrixMul([A,vinit])
            D = self.matrixMul([B,self.beta,vinit])

            temp = C+D
            vnext=self.checkLimit(temp)
            diff = np.linalg.norm(vnext - vinit)
            vinit = vnext
            self.nodes_infected.append(len(list(filter(lambda x: x >= 0.65, vinit))))

            self.graph.updateValue(vinit)
            self.calcularBeta(self.t)




    def calcularBeta(self,t:int):
        for i in range(self.n):
            if(self.nodes_infected[t] == self.n):
                for j in range(self.n):
                    self.beta[i,j] = self.betaI
            else:
                beta = self.betaI*(1 - (self.nodes_infected[t]/self.n))
                for j in range(self.n):
                    self.beta[i,j] = beta * self.adjMatrix[i,j]

    def matrixMul(self, matrixArray: list) -> np.array:
        """
        Metodo que multiplica las matrices del arreglo
        """
        resultado = matrixArray[0]
        for i in range(1, len(matrixArray)):
            resultado = np.matmul(resultado, matrixArray[i])
        return resultado

    def checkLimit(self, v: np.array) -> np.array:
        for i in range(self.n):
            tao = (np.sum(self.beta[i,:])/self.degrees[i][1])/self.delta[i]
            upperBound = 1 - 1/(1+ (tao*self.degrees[i][1]))
            if v[i]<0:
                v[i]=0
            elif v[i]>upperBound:
                v[i] = upperBound
        return v





















    def plotTime(self):
        """
        Metodo que grafica la evolcion de la infeccion en el tiempo
        """
        plt.figure()
        t = np.linspace(0, self.t, num=len(self.nodes_infected), endpoint=True)
        plt.title('Nodos infectados vs Tiempo')
        plt.xlabel('Instantes de tiempo')
        plt.ylabel('# de nodos infectados')
        plt.plot(t, self.nodes_infected)
        plt.show()













    def setRates(self, delta, beta):
        """
        Funcion para definir las tasas de infeccion del modelo
        """
        self.beta = beta
        self.delta = delta









if __name__=='__main__':
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'JSON/Test10Nodos.json')
    g = Graph(1,path)
    model = NIMFA_Fixed(g.adjM,g,0.25)
    model.run()
    model.plotTime()