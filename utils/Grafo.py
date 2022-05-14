# ----------------------------------------------------
# Generador de grafos
# Realizado por: Juan Diego González Gómez
# Adaptado y modificado de: https://github.com/MartinGalvanCastro/NimdaModel
# ----------------------------------------------------

# -------------------- Imports -----------------------
import numpy as np
import networkx as nx
import os, json, random
import matplotlib as mpl

from math import dist, inf
from tkinter import messagebox
from random import uniform, seed

# -------------------- Variables globales -----------------------
rngSeed = 32
np.random.seed(rngSeed)
seed(rngSeed)

# -------------------- Clase que representa un grafo --------------------
class Grafo:
    # Función que crea un grafo y lo grafica
    # mode : int
    #     Modo de creación:
    #         1 -> Grafo cargado desde un archivo JSON
    #         2 -> Grafo nuevo (aleatorio)
    # init : String
    #     Puede ser la ruta al json (modo 1) o la cantidad de nodos que tiene el grafo (modo 2)
    def __init__(self, mode: int, init: str, ventana) -> None:
        # ---------- Declaración de atributos ----------
        self.ventana = ventana
        self.G = nx.Graph()
        self.graph_data = None
        self.nodes = []
        self.name = ""
        self.n = 0

        # ---------- Creación del grafo ----------
        # Si se carga el grafo desde un archivo JSON
        if mode == 1:
            self.pos = {}
            try:
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
            except Exception:
                messagebox.showerror('Error', "El archivo seleccionado no tiene un formato valido")
                return

        # O si se genera un grafo nuevo (aleatorio)
        else:
            # Inicialización de atributos
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

            # Ubicación de nodos
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

            # Creación de la lista de adjacencia
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

        # Se asignan los valores de infección de cada nodo
        nx.set_node_attributes(
            self.G, {i: self.nodes[i]['value'] for i in range(self.n)}, name='value')






    # -------------------- Otras funciones de la clase --------------------





    # Función que guarda el grafo en un archivo JSON
    def save_graph(self, file) -> None:
        json.dump(self.graph_data, file)

    # Función que actualiza el valor de infección de cada nodo
    # v : np.array
    #     Valores para la iteración i
    def updateValue(self, v: np.array) -> None:
        nx.set_node_attributes(
            self.G, {i: v[i] for i in range(len(v))}, name='value')
        self.ventana.grafica()

    # Función que devuelve el grado de todos los nodos
    def get_degree_of_nodes(self) -> list:
        return sorted(list(self.G.degree()), key=lambda x: x[0])

    # Función que devuelve, para el nodo que recibe por parámetro, sus nodos vecinos infectados
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

# Función que genera un grafo de prueba en caso de que este archivo sea ejecutado
if __name__=='__main__':
    print("\nEsta es una ejecución de prueba para el grafo.\n")
    print("Para ejecutar la aplicación completa debe ejecutar el archivo \"main.py\".")

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Grafos Guardados')
    g = Grafo(2, str(10))
    h = Grafo(2, str(10))