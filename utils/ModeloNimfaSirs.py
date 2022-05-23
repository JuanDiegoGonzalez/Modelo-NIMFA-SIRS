# -------------------------------------------------------------------------------------------------------------
# Modelo epidemiológico SIRS implementado con un modelo NIMFA
# Realizado por: Juan Diego González Gómez
# Inspirado en el modelo SIS de: https://github.com/MartinGalvanCastro/NimdaModel
# -------------------------------------------------------------------------------------------------------------

# -------------------- Imports -----------------------
import random
import os, time
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
        self.graph = graph

        self.v = [0.5 for _ in range(self.n)]
        self.v[graph.initialInfected] = 1

        self.iterations = parametros[3]
        self.history = [[i for i in self.v]]

    # Función que ejecuta la simulación del modelo
    def run(self, test):
        self.t = 0
        temporal_nodes = [a.copy() for a in self.graph.nodes]
        while self.t < self.iterations:
            for i in range(self.n):
                # Nodos susceptibles
                if self.graph.nodes[i]["value"] == 0.5:
                    alfa = self.calcularAlfa(len(self.graph.get_infected_neigboors(i)))
                    if random.randint(1, 100) <= alfa * 100:
                        temporal_nodes[i]["value"] = 1
                        self.v[i] = 1

                # Nodos infectados
                elif self.graph.nodes[i]["value"] == 1:
                    if random.randint(1, 100) <= self.parametros[1] * 100:
                        temporal_nodes[i]["value"] = 0
                        self.v[i] = 0

                # Nodos recuperados
                else:
                    if random.randint(1, 100) <= self.parametros[2] * 100:
                        temporal_nodes[i]["value"] = 0.5
                        self.v[i] = 0.5

            self.graph.nodes = [a.copy() for a in temporal_nodes]
            self.t += 1
            if not test:
                self.graph.updateValue(self.v)
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
            for i in self.parametros:
                f.write(str(i) + "\n")
            for i in self.history:
                f.write(str(i) + "\n")

    # Función que exporta los parametros y resultados del test (la variable self.history)
    def exportarDatosTest(self):
        with open("Datos de Prueba/Caso{}Nodos.txt".format(self.n), 'a', encoding='utf-8') as f:
            for i in self.parametros:
                f.write(str(i) + "\n")
            for i in self.history:
                f.write(str(i) + "\n")


# Función que ejecuta un modelo de prueba en caso de que este archivo sea ejecutado
if __name__ == '__main__':
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Grafos Guardados/6Nodos.json')

    # Se elimina el virus (ver nodo #3)
    g = Grafo(1, path)
    model = Modelo(g.adjM, g, 0.33, 0.16, 0.08)

    # El virus infecta la red completa
    # g = Grafo(2, str(30))
    # model = Modelo(g.adjM, g, 0.5, 0.05, 0.06)

    # SIR model
    # g = Grafo(2, str(30))
    # model = Modelo(g.adjM, g, 0.5, 0.25, 0.00)

    model.run()

    print("\nEsta fue una ejecución de prueba para el modelo.\n")
    print("Para ejecutar la aplicación completa debe ejecutar el archivo \"main.py\".")

    model.plotTime()
