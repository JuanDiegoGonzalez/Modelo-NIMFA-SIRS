# -------------------------------------------------------------------------------------------------------------
# Modelo epidemiológico SIRS implementado con un modelo NIMFA
# Realizado por: Juan Diego González Gómez
# Inspirado en el modelo SIS de: https://github.com/MartinGalvanCastro/NimdaModel
# -------------------------------------------------------------------------------------------------------------

# -------------------- Imports -----------------------
import os
import time
import random
import numpy as np

from random import seed

from utils.Grafo import Grafo

# -------------------- Variables globales -----------------------
rngSeed = 32
np.random.seed(rngSeed)
seed(rngSeed)


# -------------------- Clase que representa el modelo --------------------
class Modelo:
    # Función que declara e inicializa las variables del modelo
    def __init__(self, adjMatrix: np.array, graph: Grafo, parametros):
        self.adjMatrix = adjMatrix
        self.n = len(self.adjMatrix)
        self.parametros = parametros
        self.Graph = graph

        self.v = [0.5 for _ in range(self.n)]
        self.v[self.Graph.initialInfected] = 1

        self.iterations = parametros[3]
        self.history = [[i for i in self.v]]

    # Función que ejecuta la simulación del modelo
    def run(self, test):
        self.t = 0
        temporal_nodes = [a.copy() for a in self.Graph.nodes]
        while self.t < self.iterations:
            for i in range(self.n):
                # Nodos susceptibles
                if self.Graph.nodes[i]["value"] == 0.5:
                    alfa = self.calcularAlfa(len(self.Graph.get_infected_neigboors(i)))
                    if random.randint(1, 100) <= alfa * 100:
                        temporal_nodes[i]["value"] = 1
                        self.v[i] = 1

                # Nodos infectados
                elif self.Graph.nodes[i]["value"] == 1:
                    if random.randint(1, 100) <= self.parametros[1] * 100:
                        temporal_nodes[i]["value"] = 0
                        self.v[i] = 0

                # Nodos recuperados
                else:
                    if random.randint(1, 100) <= self.parametros[2] * 100:
                        temporal_nodes[i]["value"] = 0.5
                        self.v[i] = 0.5

            self.Graph.nodes = [a.copy() for a in temporal_nodes]
            self.t += 1
            if not test:
                self.Graph.updateValue(self.v)
            self.history.append([i for i in self.v])
            if not test:
                time.sleep(0.25)

        if test:
            self.exportarDatosTest()

    # Funcion que calcula la probabilidad de que un nodo susceptible se infecte
    def calcularAlfa(self, d: int):
        return 1 - ((1 - self.parametros[0]) ** d)

    # Función que exporta los resultados del modelo (la variable self.history)
    def exportarDatos(self):
        with open("Modelos Guardados/{}nodos.txt".format(self.n), 'w', encoding='utf-8') as f:
            file = open("./Modelos Guardados/{}nodos.json".format(self.n), "w")
            self.Graph.save_graph(file)
            file.close()
            f.write(str(self.n) + "\n")

            for i in self.parametros:
                f.write(str(i) + "\n")
            for i in self.history:
                f.write(str(i) + "\n")

    # Función que exporta los parametros y resultados del test (la variable self.history)
    def exportarDatosTest(self):
        with open("Datos de Prueba/{}nodos/{:.2f}-{:.2f}-{:.2f}.txt".format(self.Graph.n, self.parametros[0], self.parametros[1], self.parametros[2]), 'a', encoding='utf-8') as f:
            for i in self.parametros:
                f.write(str(i) + "\n")
            for i in self.history:
                f.write(str(i) + "\n")
