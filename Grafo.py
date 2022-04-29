# ----------------------------------------------------
# Generador de grafos
# Realizado por: Juan Diego Gonzalez Gomez - 201911031
# Adaptado y modificado de: https://github.com/MartinGalvanCastro/NimdaModel
# ----------------------------------------------------

# -------------------- Imports -----------------------
import os, json, random
import networkx as nx
import numpy as np
import matplotlib as mpl

from math import dist, inf
from random import uniform, seed
from matplotlib import pyplot as plt

# -------------------- Variables globales -----------------------
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    def __init__(self, mode: int, init: str, ventana) -> None:
        # ---------- Declaracion de atributos ----------
        self.ventana = ventana
        self.G = nx.Graph()
        self.graph_data = None
        self.nodes = []
        self.name = ""
        self.colors = mpl.colors.Normalize(vmin=0, vmax=1, clip=True)
        self.n = 0

        # ---------- Creacion del grafo ----------
        # Si se carga el grafo desde un archivo JSON
        if mode == 1:
            self.pos = {}
            with open(init) as json_file:
                self.graph_data = json.load(json_file)
                self.n = len(self.graph_data)
                self.adjM = np.zeros((self.n, self.n), int)
                self.nodes = self.graph_data
                for i in range(self.n):
                    self.pos[i] = self.graph_data[i]['pos']
                    self.adjM[i, :] = self.graph_data[i]["adjList"]
                    if self.graph_data[i]["value"] == 1:
                        self.initialInfected = i
                self.name = init

        # O si se genera un grafo nuevo (aleatorio)
        else:
            # Inicializacion de atributos
            self.n = int(init)
            RC = 45
            self.pos = {i: (inf, inf) for i in range(self.n)}
            self.pos[0] = (uniform(0, 100), uniform(0, 100))
            self.adjM = np.zeros((self.n, self.n), int)
            self.nodes = [{"value": 0.5, "adjList": [0 for _ in range(self.n)]}
                          for _ in range(self.n)]
            # Se asigna al azar el nodo donde inicia la infeccion
            self.initialInfected = random.randint(0, self.n-1)
            self.nodes[self.initialInfected]["value"] = 1

            # Ubicacion de nodos
            for i in range(1, self.n):
                flag = True
                while flag:
                    self.pos[i] = (uniform(0, 100), uniform(0, 100))

                    # Se revisa que el nodo este cerca de al menos otro nodo (para que luego el grafo sea conexo)
                    for j in range(self.n):
                        if self.pos[j] != (inf, inf) and j != i:
                            dij = dist(self.pos[i], self.pos[j])
                            if dij <= RC:
                                flag = False
                                break

            # Creacion de la lista de adjacencia
            for i in range(self.n):
                self.nodes[i]["pos"] = self.pos[i]
                for j in range(self.n):
                    dij = dist(self.pos[i], self.pos[j])
                    if dij <= RC and i != j:
                        self.adjM[i, j] = 1
                        self.nodes[i]["adjList"][j] = 1

        # Se agregan los arcos al grafo
        self.graph_data = self.nodes
        for i in range(self.n):
            for j in range(i+1, self.n):
                if self.adjM[i, j] == 1:
                    self.G.add_edge(i, j)

        # Se asignan los valores de infeccion de cada nodo
        nx.set_node_attributes(
            self.G, {i: self.nodes[i]['value'] for i in range(self.n)}, name='value')






    # -------------------- Otras funciones de la clase --------------------





    # Funcion que guarda el grafo en un archivo JSON
    def save_graph(self, file) -> None:
        json.dump(self.graph_data, file)

    # Funcion que actualiza el valor de infección de cada nodo
    # v : np.array
    #     Valores para la iteración i
    def updateValue(self, v: np.array) -> None:
        nx.set_node_attributes(
            self.G, {i: v[i] for i in range(len(v))}, name='value')
        self.ventana.grafica()

    # Funcion que devuelve el grado de todos los nodos
    def get_degree_of_nodes(self) -> list:
        return sorted(list(self.G.degree()), key=lambda x: x[0])

    # Funcion que devuelve, para el nodo que recibe por parametro, sus nodos vecinos infectados
    def get_infected_neigboors(self, root) -> list:
        neighboors = []
        for i in range(self.n):
            if self.adjM[root][i]:
                neighboors.append(i)

        resp = []
        for i in neighboors:
            if self.G.nodes[i]['value'] == 1:
                resp.append(i)

        return resp

# Funcion que genera un grafo de prueba en caso de que este archivo sea ejecutado
if __name__=='__main__':
    print("\nEsta es una ejecucion de prueba para el grafo.\n")
    print("Para ejecutar la aplicacion completa debe ejecutar el archivo \"main.py\".")

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Grafos Guardados')
    g = Grafo(2, str(10))
    h = Grafo(2, str(10))
