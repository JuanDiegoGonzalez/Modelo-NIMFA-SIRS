# ----------------------------------------------------
# Generador de grafos
# Realizado por: Juan Diego Gonzalez Gomez - 201911031
# Adaptado y modificado de: https://github.com/MartinGalvanCastro/NimdaModel
# ----------------------------------------------------

# -------------------- Imports -----------------------
import os, json
import networkx as nx
import numpy as np
import matplotlib as mpl

from math import dist, inf
from random import uniform, seed
from matplotlib import pyplot as plt

# -------------------- Variables globales -----------------------
rngSeed = 32
np.random.seed(rngSeed)
seed(rngSeed)

# -------------------- Clase que representa un grafo --------------------
class Grafo:
    # Funcion que crea un grafo y lo grafica
    # mode : int
    #     Modo de creacion:
    #         1 -> Grafo cargado desde un archivo json
    #         2 -> Grafo nuevo (aleatorio)
    # init : String
    #     Puede ser la ruta al json (modo 1) o la canitdad de nodos que tiene el grafo (modo 2)
    def __init__(self, mode: int, init: str) -> None:
        # ---------- Declaracion de atributos ----------
        plt.show()
        self.G = nx.Graph()
        self.graph_data = None
        self.nodes = []
        self.name = ""
        self.colors = mpl.colors.Normalize(vmin=0, vmax=1, clip=True)
        n = 0

        # ---------- Creacion del grafo ----------
        # Si se carga el grafo desde un archivo JSON
        if mode == 1:
            self.pos = {}
            with open(init) as json_file:
                self.graph_data = json.load(json_file)
                n = len(self.graph_data)
                self.adjM = np.zeros((n, n), int)
                self.nodes = self.graph_data
                for i in range(n):
                    self.pos[i] = self.graph_data[i]['pos']
                    self.adjM[i, :] = self.graph_data[i]["adjList"]
                self.name = init

        # O si se genera un grafo nuevo (aleatorio)
        else:
            # Inicializacion de atributos
            n = int(init)
            RC = 45
            self.pos = {i: (inf, inf) for i in range(n)}
            self.pos[0] = (uniform(0, 100), uniform(0, 100))
            self.adjM = np.zeros((n, n), int)
            self.nodes = [{"value": uniform(0, 0.1), "adjList": [0 for _ in range(n)]}
                          for _ in range(n)]

            # Ubicacion de nodos
            for i in range(1, n):
                flag = True
                while flag:
                    self.pos[i] = (uniform(0, 100), uniform(0, 100))

                    # Se revisa que el nodo este cerca de al menos otro nodo (para que luego el grafo sea conexo)
                    for j in range(n):
                        if self.pos[j] != (inf, inf) and j != i:
                            dij = dist(self.pos[i], self.pos[j])
                            if dij <= RC:
                                flag = False
                                break

            # Creacion de la lista de adjacencia
            for i in range(n):
                self.nodes[i]["pos"] = self.pos[i]
                for j in range(n):
                    dij = dist(self.pos[i], self.pos[j])
                    if dij <= RC and i != j:
                        self.adjM[i, j] = 1
                        self.nodes[i]["adjList"][j] = 1

        # Se agregan los arcos al grafo
        self.graph_data = self.nodes
        for i in range(n):
            for j in range(i+1, n):
                if self.adjM[i, j] == 1:
                    self.G.add_edge(i, j)

        # Se asignan los valores de infeccion de cada nodo
        nx.set_node_attributes(
            self.G, {i: self.nodes[i]['value'] for i in range(n)}, name='value')

        # ---------- Grafica del grafo ----------
        self.plot()

    # -------------------- Otras funciones de la clase --------------------
    # Funcion para graficar el grafo
    def plot(self) -> None:
        plt.clf()
        mapper = mpl.cm.ScalarMappable(norm=self.colors, cmap=mpl.cm.coolwarm)
        nx.draw(self.G,
                self.pos,
                node_color=[mapper.to_rgba(self.G.nodes[i]['value'])
                            for i in self.G.nodes],
                with_labels=True,
                font_color='black',
                edge_cmap=mpl.cm.coolwarm,
                vmin=0, vmax=1)
        plt.colorbar(mapper, shrink=0.75)
        plt.pause(0.1)
        plt.draw()

    # Funcion que guarda el grafo en un archivo JSON
    def save_graph(self,nombre) -> None:
        if self.name == '':
            self.name = f"{nombre}.json"
        print("Saving graph as: " + self.name)
        with open(f"{self.name}", "w") as outfile:
            json.dump(self.graph_data, outfile)

    # Funcion que actualiza el valor de infección de cada nodo
    # v : np.array
    #     Valores para la iteración i
    def updateValue(self, v: np.array) -> None:
        nx.set_node_attributes(
            self.G, {i: v[i] for i in range(len(v))}, name='value')
        self.plot()

    # Funcion que devuelve el grado de todos los nodos
    def get_degree_of_nodes(self) -> list:
        return sorted(list(self.G.degree()), key=lambda x: x[0])

    # Funcion que devuelve, para cada nodo, sus nodos vecinos infectados
    def get_infected_neigboors(self) -> list:
        resp = []
        for node in self.G.nodes():
            adjList = self.graph_data[node]['adjList']
            infected = 0
            for i,neighboor in enumerate(adjList):
                if neighboor == 1:
                    infected += 1 if self.G.nodes[i]['value'] >= 0.65 else 0
            resp.append((node, infected))
        return resp

# Funcion que genera un grafo de prueba en caso de que este archivo sea ejecutado
if __name__=='__main__':
    print("\nEsta es una ejecucion de prueba para el grafo.\n")
    print("Para ejecutar la aplicacion completa debe ejecutar el archivo \"main.py\".")

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Grafos Guardados')
    g = Grafo(2, str(10))
    h = Grafo(2, str(10))
