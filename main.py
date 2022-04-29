# ----------------------------------------------------
# Interfaz principal de la aplicacion
# Realizado por: Juan Diego Gonzalez Gomez
# ----------------------------------------------------

# -------------------- Imports -----------------------
import os, json
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile

from DialogoCrearGrafo import DialogoCrearGrafo

import numpy as np
import networkx as nx
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from Grafo import Grafo
from Modelo import Modelo


# -------------------- Clase ventana principal --------------------
class Ventana:
    # Funcion que declara y configura los elementos de la ventana principal
    def __init__(self, modelPath, graphPath):
        # ---------- Declaracion de la ventana principal ----------
        self.window = tk.Tk()

        # ---------- Parametros de la ventana ----------
        w = 1100
        h = 750

        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()

        x = ws / 2 - w / 2
        y = hs / 2 - h / 2

        self.ratio_ventana = 0.7 if hs < 1000 else 1

        # ---------- Configuracion de la ventana ----------
        self.window.geometry('%dx%d+%d+%d' % (
            w * self.ratio_ventana, h * self.ratio_ventana, x * self.ratio_ventana, y * self.ratio_ventana))
        self.window.title('Modelo NIMFA - SIRS')
        self.window.config(bg='white')
        self.window.resizable(False, False)

        # ---------- Declaracion de objetos (grafo y modelo) ----------
        self.Graph = None
        self.Model = None

        # ---------- Configuracion de los elementos de la ventana principal ----------
        self.configurarVentana()

        # ---------- Ejecucion del programa ----------
        self.window.mainloop()

    # Funcion que configura los frames de la ventana principal y sus elementos
    def configurarVentana(self):
        # ---------- Frame superior izquierdo ----------
        self.frame1 = tk.Frame(master=self.window)
        self.frame1.place(x=0, y=0)
        self.frame1.config(bg="#A9CCE3", width=300 * self.ratio_ventana, height=200 * self.ratio_ventana,
                           relief=tk.RIDGE, bd=8)

        # ---------- Frame inferior izquierdo ----------
        self.frame2 = tk.Frame(master=self.window)
        self.frame2.place(x=0, y=500 * self.ratio_ventana)
        self.frame2.config(bg="#A9CCE3", width=300 * self.ratio_ventana, height=250 * self.ratio_ventana,
                           relief=tk.RIDGE, bd=8)

        # Boton crear nuevo grafo
        self.crear_nuevo_grafo = tk.Button(master=self.frame2, text='Crear nuevo grafo', command=self.crearNuevoGrafo,
                  bg='#A9CCE3', font=('math', 15, 'bold italic'), width=20)
        self.crear_nuevo_grafo.grid(pady=9, row=1, column=1, padx=(17, 17))

        # Boton cargar grafo
        self.cargar_grafo = tk.Button(master=self.frame2, text='Cargar grafo', command=self.cargarGrafo,
                  bg='#A9CCE3', font=('math', 15, 'bold italic'), width=20)
        self.cargar_grafo.grid(pady=8, row=2, column=1, padx=(17, 17))

        # Boton guardar grafo
        self.guardar_grafo = tk.Button(master=self.frame2, text='Guardar grafo', command=self.guardarGrafo,
                  bg='#A9CCE3', font=('math', 15, 'bold italic'), width=20)
        self.guardar_grafo.grid(pady=8, row=3, column=1, padx=(17, 17))

        # Boton ejecutar modelo
        self.ejecutar_grafo = tk.Button(master=self.frame2, text='Ejecutar modelo', command=self.ejecutarModelo,
                  bg='#F4D03F', font=('math', 15, 'bold italic'), width=20)
        self.ejecutar_grafo.grid(pady=8, row=4, column=1, padx=(17, 17))

        # ---------- Frame central ----------
        self.frame3 = tk.Frame(master=self.window).pack()

        # ---------- Frame inferior centro ----------
        self.frame4 = tk.Frame(master=self.window)
        self.frame4.place(x=300, y=500 * self.ratio_ventana)
        self.frame4.config(bg="#A9CCE3", width=500 * self.ratio_ventana, height=250 * self.ratio_ventana,
                           relief=tk.RIDGE, bd=8)

        self.actualIteration = tk.Label(master=self.frame4, bg='#A9CCE3', font=('math', 18, 'bold italic'),
                                        text="", width=31)
        self.actualIteration.grid(pady=100, row=1, column=1, columnspan=5, padx=(7, 6))

        # ---------- Frame superior derecho ----------
        self.frame5 = tk.Frame(master=self.window)
        self.frame5.place(x=800 * self.ratio_ventana, y=0)
        self.frame5.config(bg="#A9CCE3", width=300 * self.ratio_ventana, height=200 * self.ratio_ventana,
                           relief=tk.RIDGE, bd=8)

        # ---------- Frame inferior derecho ----------
        self.frame6 = tk.Frame(master=self.window)
        self.frame6.place(x=800 * self.ratio_ventana, y=500 * self.ratio_ventana)
        self.frame6.config(bg="#A9CCE3", width=300 * self.ratio_ventana, height=250 * self.ratio_ventana,
                           relief=tk.RIDGE, bd=8)

        nombreParametros = ["α", "β", "γ", "# iter"]
        defaultParametros = [0.33, 0.16, 0.08, 20]
        self.parametros = []
        for i in range(4):
            # Label parametro
            lbl = tk.Label(master=self.frame6, bg='#A9CCE3', font=('math', 18, 'bold italic'), text=nombreParametros[i])
            lbl.grid(pady=5, row=i, column=1, padx=(20, 0))

            # Display e input del valor del parametro
            vldt_ifnum_cmd = (self.window.register(self.validate), '%S')
            par = tk.Entry(master=self.frame6, validate='all', validatecommand=vldt_ifnum_cmd)
            par.insert(0, defaultParametros[i])
            par.configure(state='readonly')
            par.grid(pady=5, row=i, column=2, padx=(0, 20))
            self.parametros.append(par)

        self.editar_parametros_button = tk.Button(master=self.frame6, text='Editar parametros',
                                                  command=self.habilitarParametros,
                                                  bg='#A9CCE3', font=('math', 15, 'bold italic'), width=20)
        self.editar_parametros_button.grid(pady=8, row=8, column=1, columnspan=2, padx=(17, 17))

        self.actualizar_parametros_button = tk.Button(master=self.frame6, text='Actualizar parametros',
                                                      command=self.actualizarParametros,
                                                      bg='#A9CCE3', font=('math', 15, 'bold italic'), width=20)

    # Funcion que valida si los caracteres ingresados en el campo de los parametros son validos
    def validate(self, S):
        valid = S == '' or S == ',' or S == '.' or S.isdigit() or self.is_float(S)
        if not valid:
            self.window.bell()
        return valid

    # Funcion que evalua si una cadena de texto es un numero real
    def is_float(self, element) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False

    # Funcion que habilita los parametros para ser actualizados
    def habilitarParametros(self):
        for i in self.parametros:
            i.configure(state='normal')

        self.editar_parametros_button.grid_forget()
        self.actualizar_parametros_button.grid(pady=8, row=8, column=1, columnspan=2, padx=(17, 17))

    # Funcion que actualiza los parametros con los valores ingresados por el usuario si estos son validos
    def actualizarParametros(self) -> bool:
        try:
            for i in range(4):
                if i < 3:
                    act = float(self.parametros[i].get())
                    if not 0 <= act <= 1:
                        raise ValueError('Parametros: al menos un valor ingresado esta fuera de rango')
                if i == 3:
                    act = int(self.parametros[i].get())
                    if not 1 <= act <= 100:
                        raise ValueError('Parametros: al menos un valor ingresado esta fuera de rango')

            for i in self.parametros:
                i.configure(state='readonly')

            self.editar_parametros_button.grid(pady=8, row=8, column=1, columnspan=2, padx=(17, 17))
            self.actualizar_parametros_button.grid_forget()
            return True

        except ValueError as e:
            if str(e).startswith('invalid') or str(e).startswith('could'):
                messagebox.showerror('Error', "Parametros: al menos un valor ingresado no es valido")
            else:
                messagebox.showerror('Error', e)
            return False

    # Funcion que crea un nuevo grafo
    def crearNuevoGrafo(self):
        inputDialog = DialogoCrearGrafo(self.window)
        self.window.wait_window(inputDialog.top)

        if inputDialog.val is not None:
            self.Graph = Grafo(2, str(inputDialog.val), self)

            self.fig = plt.figure(figsize=(5, 3.5), dpi=100)
            self.canvas = FigureCanvasTkAgg(self.fig, self.window)
            self.canvas.get_tk_widget().place(x=300 * self.ratio_ventana, y=150 * self.ratio_ventana)

            self.grafica()

    # Funcion que carga un grafo existente
    def cargarGrafo(self):
        filename = askopenfilename(initialdir='./Grafos Guardados', filetypes=(('Archivos JSON', '*.json'),))
        if filename:
            self.Graph = Grafo(1, filename, self)

            self.fig = plt.figure(figsize=(5, 3.5), dpi=100)
            self.canvas = FigureCanvasTkAgg(self.fig, self.window)
            self.canvas.get_tk_widget().place(x=300 * self.ratio_ventana, y=150 * self.ratio_ventana)

            self.grafica()

    # Funcion que guarda/exporta en un archivo el grafo cargado actualmente
    def guardarGrafo(self):
        if self.Graph:
            file = asksaveasfile(initialdir='./Grafos Guardados', mode='w', defaultextension=".json",
                                 filetypes=(('Archivos JSON', '*.json'),))
            if file:
                self.Graph.save_graph(file)
                file.close()
        else:
            messagebox.showerror('Error', "No se ha creado ningun grafo")

    # Funcion que ejecuta el modelo
    def ejecutarModelo(self):
        if self.Graph is None:
            self.crearNuevoGrafo()

        if self.Graph is not None and self.actualizarParametros():
            self.actualizarParametros()
            self.Model = Modelo(self.Graph.adjM, self.Graph, [float(i.get()) for i in self.parametros])

            self.quitarBotonesPre()
            self.Model.run()
            self.cargarBotonesPost()
            # self.Model.plotTime()

    def quitarBotonesPre(self):
        self.crear_nuevo_grafo["state"] = "disabled"
        self.cargar_grafo["state"] = "disabled"
        self.guardar_grafo["state"] = "disabled"
        self.ejecutar_grafo["state"] = "disabled"
        self.editar_parametros_button["state"] = "disabled"
        self.actualIteration.grid(pady=100, row=1, column=1, columnspan=4, padx=(7, 6))

    def cargarBotonesPost(self):
        self.actualIteration.grid(pady=(100, 42), row=1, column=1, columnspan=4, padx=(7, 6))
        tk.Button(master=self.frame4, text='<<', command=self.goFirst,
                  bg='#F4D03F', font=('math', 15, 'bold italic'), width=7).grid(pady=8, row=2, column=1,
                                                                                padx=(1, 1))
        tk.Button(master=self.frame4, text='<', command=self.goBack,
                  bg='#F4D03F', font=('math', 15, 'bold italic'), width=7).grid(pady=8, row=2, column=2,
                                                                                padx=(1, 1))
        tk.Button(master=self.frame4, text='>', command=self.goForward,
                  bg='#F4D03F', font=('math', 15, 'bold italic'), width=7).grid(pady=8, row=2, column=3,
                                                                                padx=(1, 1))
        tk.Button(master=self.frame4, text='>>', command=self.goLast,
                  bg='#F4D03F', font=('math', 15, 'bold italic'), width=7).grid(pady=8, row=2, column=4,
                                                                                padx=(1, 1))

    def goFirst(self):
        if self.Model.t > 0:
            self.Model.t = 0
            nx.set_node_attributes(
                self.Graph.G,
                {i: self.Model.history[self.Model.t][i] for i in range(len(self.Model.history[self.Model.t]))},
                name='value')
            self.grafica()

    def goBack(self) -> None:
        if self.Model.t > 0:
            self.Model.t -= 1
            nx.set_node_attributes(
                self.Graph.G,
                {i: self.Model.history[self.Model.t][i] for i in range(len(self.Model.history[self.Model.t]))},
                name='value')
            self.grafica()

    def goForward(self) -> None:
        if self.Model.t < self.Model.iterations:
            self.Model.t += 1
            nx.set_node_attributes(
                self.Graph.G,
                {i: self.Model.history[self.Model.t][i] for i in range(len(self.Model.history[self.Model.t]))},
                name='value')
            self.grafica()

    def goLast(self) -> None:
        if self.Model.t < self.Model.iterations:
            self.Model.t = int(self.Model.iterations)
            nx.set_node_attributes(
                self.Graph.G,
                {i: self.Model.history[self.Model.t][i] for i in range(len(self.Model.history[self.Model.t]))},
                name='value')
            self.grafica()

    # Funcion que grafica las funciones seleccionadas utilizando la funcion plot de matplotlib.pyplot
    def grafica(self):
        plt.clf()

        mapper = mpl.cm.ScalarMappable(norm=self.Graph.colors, cmap=mpl.cm.coolwarm)
        nx.draw(self.Graph.G,
                self.Graph.pos,
                node_color=[mapper.to_rgba(self.Graph.G.nodes[i]['value'])
                            for i in self.Graph.G.nodes],
                with_labels=True,
                font_color='black',
                edge_cmap=mpl.cm.coolwarm,
                vmin=0, vmax=1)
        plt.colorbar(mapper, shrink=0.75)

        if self.Model:
            if self.Model.t > 0:
                self.actualIteration['text'] = "Iteracion # {}".format(self.Model.t)
            else:
                self.actualIteration['text'] = "Estado inicial"

        self.canvas.draw()
        self.window.update()


if __name__ == '__main__':
    modelPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Modelos Guardados/6Nodos.txt')
    graphPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Grafos Guardados/6Nodos.json')
    controller = Ventana(modelPath, graphPath)
