# -------------------------------------------------------------------------------------------------------------
# Modelo epidemiologico SIRS implementado con un modelo NIMFA
# Realizado por: Juan Diego Gonzalez Gomez
# Basado en el modelo SIS de: https://github.com/MartinGalvanCastro/NimdaModel
# -------------------------------------------------------------------------------------------------------------

# -------------------- Imports -----------------------
import random
import os, time
import numpy as np

from random import seed

from Modelo.utils.Grafo import Grafo

# -------------------- Variables globales -----------------------
rngSeed = 32
np.random.seed(rngSeed)
seed(rngSeed)

# -------------------- Clase que representa el modelo --------------------
class Modelo:
    # Funcion que declara e inicializa las variables del modelo
    def __init__(self, adjMatrix: np.array, graph: Grafo, parametros):
        self.adjMatrix = adjMatrix
        self.n = len(self.adjMatrix)

        self.graph = graph
        self.nodes_infected = []
        self.nodes_infected.append(graph.initialInfected)

        self.parametros = parametros

        self.v = [0.5 for _ in range(self.n)]
        self.v[graph.initialInfected] = 1

        self.iterations = parametros[3]
        self.history = [[i for i in self.v]]
        self.actualIteration = self.iterations

        # self.m = 10
        # self.v = np.zeros(self.n)
        # self.colors = mpl.colors.Normalize(vmin=0, vmax=1, clip=True)
        # self.v[:] = [uniform(0, 0.05) for _ in range(self.n)]

        # self.degrees = self.graph.get_degree_of_nodes()

        # self.alfa = np.zeros(shape=(self.n, self.n))
        # self.beta = np.ones(shape=(self.n)) * betaI

        # -- Control --
        self.control = 0

    def back(self):
        self.control = 1

    # Funcion que ejecuta la simulacion del modelo
    def run(self):
        self.t = 0
        while self.t < self.iterations:

            for i in range(self.n):
                # Nodos susceptibles
                if self.graph.nodes[i]["value"] == 0.5:
                    for j in self.graph.get_infected_neigboors(i):
                        if random.randint(1, 100) <= self.parametros[0] * 100:
                            self.graph.nodes[i]["value"] = 1
                            self.v[i] = 1

                elif self.graph.nodes[i]["value"] == 1:
                    if random.randint(1, 100) <= self.parametros[1] * 100:
                        self.graph.nodes[i]["value"] = 0
                        self.v[i] = 0

                else:
                    if random.randint(1, 100) <= self.parametros[2] * 100:
                        self.graph.nodes[i]["value"] = 0.5
                        self.v[i] = 0.5

            self.t += 1
            self.graph.updateValue(self.v)
            self.history.append([i for i in self.v])
            time.sleep(0.25)

        self.exportarDatos()

    # Funcion que exporta lso resultados del modelo (la variable self.history)
    def exportarDatos(self):
        with open("Modelos Guardados/{}nodos.txt".format(self.n), 'w', encoding='utf-8') as f:
            for i in self.history:
                f.write(str(i) + "\n")

# Funcion que ejecuta un modelo de prueba en caso de que este archivo sea ejecutado
if __name__ == '__main__':
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Grafos Guardados/6Nodos.json')

    # Se elimina el virus (ver nodo #3)
    g = Grafo(1, path)
    model = Modelo(g.adjM, g, 0.33, 0.16, 0.08)

    # El virus infecta la red completa
    #g = Grafo(2, str(30))
    #model = Modelo(g.adjM, g, 0.5, 0.05, 0.06)

    # SIR model
    # g = Grafo(2, str(30))
    # model = Modelo(g.adjM, g, 0.5, 0.25, 0.00)

    model.run()

    print("\nEsta fue una ejecucion de prueba para el modelo.\n")
    print("Para ejecutar la aplicacion completa debe ejecutar el archivo \"main.py\".")

    model.plotTime()

