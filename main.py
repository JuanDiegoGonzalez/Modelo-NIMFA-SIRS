# ----------------------------------------------------
# Interfaz principal de la aplicación
# Realizado por: Juan Diego González Gómez
# ----------------------------------------------------

# -------------------- Imports -----------------------
import os
import time
import numpy as np
import tkinter as tk
import networkx as nx
import matplotlib as mpl

from PIL import Image, ImageTk
from tkinter import messagebox
from matplotlib.lines import Line2D
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline
from tkinter.filedialog import askopenfilename, asksaveasfile
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

from utils.Grafo import Grafo
from utils.ModeloNimfaSirs import Modelo
from utils.DialogoCrearGrafo import DialogoCrearGrafo


# -------------------- Clase ventana principal --------------------
class Ventana:
    # Función que declara y configura los elementos de la ventana principal
    def __init__(self):
        # ---------- Declaración de la ventana principal ----------
        self.window = tk.Tk()

        # ---------- Parámetros de la ventana ----------
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        self.ajuste_ventana = 100 if hs < 1000 else 0

        w = 1100
        h = 750 - self.ajuste_ventana

        x = (ws / 2 - w / 2)
        y = (hs / 2 - h / 2) if self.ajuste_ventana == 0 else 0

        # ---------- Configuración de la ventana ----------
        self.window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.window.title('Modelo NIMFA - SIRS')
        self.window.config(bg='white')
        self.window.resizable(False, False)

        # ---------- Configuración de atributos de las gráficas ----------
        self.colors = mpl.colors.Normalize(vmin=0, vmax=1, clip=True)
        self.cmap = plt.cm.coolwarm
        self.custom_lines = [Line2D([0], [0], marker='o', color=self.cmap(.5), markerfacecolor=self.cmap(.5),
                                    markersize=15, label='Susceptible'),
                             Line2D([0], [0], marker='o', color=self.cmap(1.), markerfacecolor=self.cmap(1.),
                                    markersize=15, label='Infectado'),
                             Line2D([0], [0], marker='o', color=self.cmap(0.), markerfacecolor=self.cmap(0.),
                                    markersize=15, label='Recuperado')]

        # ---------- Declaración de objetos (grafo y modelo) ----------
        self.Graph = None
        self.Model = None

        # ---------- Configuración de los elementos de la ventana principal ----------
        self.configurarVentana()

        # ---------- Ejecución del programa ----------
        self.window.mainloop()

    # Función que configura los frames de la ventana principal y sus elementos
    def configurarVentana(self):
        # ---------- Frame superior izquierdo ----------
        self.frame1 = tk.Frame(master=self.window)
        self.frame1.place(x=0, y=0)
        self.frame1.config(bg="#A9CCE3", width=300, height=250, relief=tk.RIDGE, bd=8)

        # Boton cargar modelo
        self.cargar_modelo = tk.Button(master=self.frame1, text='Cargar modelo', command=self.cargarModelo,
                                       bg='#A9CCE3', font=('math', 15, 'bold italic'), width=20)
        self.cargar_modelo.grid(pady=(11, 9), row=1, column=1, padx=(17, 17))

        # Boton guardar modelo
        self.guardar_modelo = tk.Button(master=self.frame1, text='Guardar modelo', command=self.guardarModelo,
                                        bg='#A9CCE3', font=('math', 15, 'bold italic'), width=20)
        self.guardar_modelo.grid(pady=9, row=2, column=1, padx=(17, 17))

        # Boton cargar datos de prueba
        self.ejecutar_datos_prueba = tk.Button(master=self.frame1, text='Ejecutar datos de prueba',
                                               command=self.ejecutarConjuntoDatosPrueba, bg='#A9CCE3',
                                               font=('math', 15, 'bold italic'), width=20)
        self.ejecutar_datos_prueba.grid(pady=(9, 11), row=3, column=1, padx=(17, 17))

        # ---------- Frame izquierdo centro ----------
        self.frame2 = tk.Frame(master=self.window)
        self.frame2.place(x=0, y=200)
        self.frame2.config(bg="#A9CCE3", width=300, height=300-self.ajuste_ventana, relief=tk.RIDGE, bd=8)

        # Boton mostrar modelo
        self.mostrar_modelo = tk.Button(master=self.frame2, text='Mostrar modelo', command=self.mostrarModelo,
                                        bg='#A9CCE3', font=('math', 15, 'bold italic'), width=20)
        self.mostrar_modelo.grid(pady=9, row=1, column=1, padx=(17, 17))

        # Boton mostrar ecuaciones del modelo
        self.mostrar_ecuaciones_modelo = tk.Button(master=self.frame2, text='Ecuaciones del modelo',
                                                   command=self.mostrarEcuacionesModelo, bg='#A9CCE3',
                                                   font=('math', 15, 'bold italic'), width=20)
        self.mostrar_ecuaciones_modelo.grid(pady=(9, 172-self.ajuste_ventana), row=2, column=1, padx=(17, 17))

        # Boton mostrar gráfica de evolución
        self.mostrar_grafica_evolucion = tk.Button(master=self.frame2, text='Gráfica de evolución',
                                                   command=self.conInterpolacion, bg='#A9CCE3',
                                                   font=('math', 15, 'bold italic'), width=20)

        # Boton volver al modelo
        self.volver_modelo = tk.Button(master=self.frame2, text='Volver al modelo', command=self.volverModelo,
                                       bg='#A9CCE3', font=('math', 15, 'bold italic'), width=20)

        # Boton nueva ejecución
        self.nueva_ejecucion = tk.Button(master=self.frame2, text='Nueva ejecución', command=self.nuevaEjecucion,
                                         bg='#A9CCE3', font=('math', 15, 'bold italic'), width=20)

        # ---------- Frame inferior izquierdo ----------
        self.frame3 = tk.Frame(master=self.window)
        self.frame3.place(x=0, y=500-self.ajuste_ventana)
        self.frame3.config(bg="#A9CCE3", width=300, height=250, relief=tk.RIDGE, bd=8)

        # Boton crear nuevo grafo
        self.crear_nuevo_grafo = tk.Button(master=self.frame3, text='Crear nuevo grafo', command=self.crearNuevoGrafo,
                                           bg='#A9CCE3', font=('math', 15, 'bold italic'), width=20)
        self.crear_nuevo_grafo.grid(pady=9, row=1, column=1, padx=(17, 17))

        # Boton cargar grafo
        self.cargar_grafo = tk.Button(master=self.frame3, text='Cargar grafo', command=self.cargarGrafo,
                                      bg='#A9CCE3', font=('math', 15, 'bold italic'), width=20)
        self.cargar_grafo.grid(pady=8, row=2, column=1, padx=(17, 17))

        # Boton guardar grafo
        self.guardar_grafo = tk.Button(master=self.frame3, text='Guardar grafo', command=self.guardarGrafo,
                                       bg='#A9CCE3', font=('math', 15, 'bold italic'), width=20)
        self.guardar_grafo.grid(pady=8, row=3, column=1, padx=(17, 17))

        # Boton ejecutar modelo
        self.ejecutar_grafo = tk.Button(master=self.frame3, text='Ejecutar modelo', command=self.ejecutarModelo,
                                        bg='#F4D03F', font=('math', 15, 'bold italic'), width=20)
        self.ejecutar_grafo.grid(pady=8, row=4, column=1, padx=(17, 17))

        # ---------- Frame inferior centro ----------
        self.frame4 = tk.Frame(master=self.window)
        self.frame4.place(x=300, y=500-self.ajuste_ventana)
        self.frame4.config(bg="#A9CCE3", width=500, height=250, relief=tk.RIDGE, bd=8)

        # Label iteración actual
        self.iteracion_actual = tk.Label(master=self.frame4, bg='#A9CCE3', font=('math', 18, 'bold italic'), text="",
                                         width=31)
        # Boton first
        self.boton_first = tk.Button(master=self.frame4, text='<<', command=self.goFirst, bg='#F4D03F',
                                     font=('math', 15, 'bold italic'), width=7)
        # Boton back
        self.boton_back = tk.Button(master=self.frame4, text='<', command=self.goBack, bg='#F4D03F',
                                    font=('math', 15, 'bold italic'), width=7)
        # Boton forward
        self.boton_forward = tk.Button(master=self.frame4, text='>', command=self.goForward, bg='#F4D03F',
                                       font=('math', 15, 'bold italic'), width=7)
        # Boton last
        self.boton_last = tk.Button(master=self.frame4, text='>>', command=self.goLast, bg='#F4D03F',
                                    font=('math', 15, 'bold italic'), width=7)

        # Label modo de gráfica
        self.modo_grafica = tk.Label(master=self.frame4, bg='#A9CCE3', font=('math', 18, 'bold italic'),
                                     text="Modo de gráfica", width=31)
        # Boton first
        self.con_interpolacion = tk.Button(master=self.frame4, text='Con interpolación', command=self.conInterpolacion,
                                           bg='#A9CCE3', font=('math', 15, 'bold italic'), width=15)
        # Boton back
        self.sin_interpolacion = tk.Button(master=self.frame4, text='Sin interpolación', command=self.sinInterpolacion,
                                           bg='#A9CCE3', font=('math', 15, 'bold italic'), width=15)

        # ---------- Frame inferior derecho ----------
        self.frame5 = tk.Frame(master=self.window)
        self.frame5.place(x=800, y=500-self.ajuste_ventana)
        self.frame5.config(bg="#A9CCE3", width=300, height=250,
                           relief=tk.RIDGE, bd=8)

        nombreParametros = ["α", "β", "γ", "# iter"]
        defaultParametros = [0.40, 0.10, 0.18, 20]
        self.parametros = []
        for i in range(4):
            # Label parámetro
            lbl = tk.Label(master=self.frame5, bg='#A9CCE3', font=('math', 18, 'bold italic'), text=nombreParametros[i])
            lbl.grid(pady=5, row=i, column=1, padx=(20, 0))

            # Display e input del valor del parámetro
            vldt_ifnum_cmd = (self.window.register(self.validate), '%S')
            par = tk.Entry(master=self.frame5, validate='all', validatecommand=vldt_ifnum_cmd)
            par.insert(0, defaultParametros[i])
            par.configure(state='readonly')
            par.grid(pady=5, row=i, column=2, padx=(0, 20))
            self.parametros.append(par)

        self.editar_parametros_button = tk.Button(master=self.frame5, text='Editar parámetros',
                                                  command=self.habilitarParametros, bg='#A9CCE3',
                                                  font=('math', 15, 'bold italic'), width=20)
        self.editar_parametros_button.grid(pady=8, row=8, column=1, columnspan=2, padx=(17, 17))

        self.actualizar_parametros_button = tk.Button(master=self.frame5, text='Actualizar parámetros',
                                                      command=self.actualizarParametros, bg='#A9CCE3',
                                                      font=('math', 15, 'bold italic'), width=20)

    # Función que carga un modelo de un archivo .txt generado previamente
    def cargarModelo(self):
        filename = askopenfilename(initialdir='.', filetypes=(('Archivos de texto', '*.txt'),))
        if filename:
            file = open(filename)

            n = file.readline()
            path = filename.split("/")
            path_grafo = ""
            for i in range(len(path) - 1):
                path_grafo += "{}/".format(path[i])
            print("{}{}nodos.json".format(path_grafo, n[:-1]))
            self.Graph = Grafo(1, ["{}{}nodos.json".format(path_grafo, n[:-1])], self)

            params = [float(file.readline()[:-1]), float(file.readline()[:-1]), float(file.readline()[:-1]),
                      int(file.readline()[:-1].split(".")[0])]
            for i in range(len(self.parametros)):
                self.parametros[i].configure(state='normal')
                self.parametros[i].delete(0, tk.END)
                self.parametros[i].insert(0, params[i])
                self.parametros[i].configure(state='readonly')

            self.Model = Modelo(self.Graph.adjM, self.Graph, params)
            self.Model.t = params[3]
            file.readline()
            for i in range(params[3]):
                self.Model.history.append([float(i) for i in file.readline()[:-1].replace("[", "").replace("]", "")
                                          .replace(" ", "").split(",")])

            height = 5 if self.ajuste_ventana == 0 else 4
            self.fig = plt.figure(figsize=(8, height), dpi=100)
            self.canvas = FigureCanvasTkAgg(self.fig, self.window)
            self.canvas.get_tk_widget().place(x=300, y=0)
            nx.set_node_attributes(self.Graph.G, {i: self.Model.history[self.Model.t][i] for i in
                                                  range(len(self.Model.history[self.Model.t]))},
                                   name='value')
            self.grafica()

            self.quitarBotonesPre()
            self.cargarBotonesPost()

    # Función que guarda el modelo actual en un archivo .txt
    def guardarModelo(self):
        if self.Model:
            self.Model.exportarDatos()
            messagebox.showinfo('Guardar Modelo', "¡El modelo se ha exportado exitosamente!")
        else:
            messagebox.showerror('Error', "No se ha ejecutado ningún modelo.")

    # Función que ejecuta un conjunto de datos de prueba
    def ejecutarConjuntoDatosPrueba(self):
        if self.Graph is None:
            self.crearNuevoGrafo()

        if self.Graph is not None:
            if not os.path.exists("./Datos de Prueba/{}nodos".format(self.Graph.n)):
                os.makedirs("./Datos de Prueba/{}nodos".format(self.Graph.n))

            file = open("./Datos de Prueba/{}nodos/{}nodos.json".format(self.Graph.n, self.Graph.n), "w")
            self.Graph.save_graph(file)
            file.close()

            # alfa = np.arange(0.0, 0.6, 0.1)
            # beta = np.arange(0.0, 0.6, 0.1)
            # gamma = np.arange(0.0, 0.6, 0.1)

            casos_de_prueba = []

            # El virus siempre está presente en la red
            casos_de_prueba.append((0.40, 0.10, 0.18))

            # Se elimina el virus
            casos_de_prueba.append((0.10, 0.50, 0.05))

            # El virus infecta la red completa
            casos_de_prueba.append((0.50, 0.10, 0.18))

            # SIR model
            casos_de_prueba.append((0.50, 0.25, 0.00))

            global_start_time = time.time()
            # for i in alfa:
            #    for j in beta:
            #        for k in gamma:
            for caso in casos_de_prueba:
                i, j, k = caso
                with open("Datos de Prueba/{}nodos/{:.2f}-{:.2f}-{:.2f}.txt".format(self.Graph.n, i, j, k), 'w+',
                          encoding='utf-8') as f:
                    f.write(str(self.Graph.n) + "\n")

                start_time = time.time()
                params = [i, j, k, 50]
                print(params)
                self.Model = Modelo(self.Graph.adjM, self.Graph, params)
                self.Model.run(True)
                print("--- %s seconds ---" % (time.time() - start_time))

                with open("Datos de Prueba/{}nodos/{:.2f}-{:.2f}-{:.2f}.txt".format(self.Graph.n, i, j, k), 'a',
                          encoding='utf-8') as f:
                    f.write("--- %s segundos ---\n" % (time.time() - start_time))
            print("--- %s seconds ---" % (time.time() - global_start_time))
            with open("Datos de Prueba/{}nodos/TiempoTotal.txt".format(self.Graph.n), 'w+', encoding='utf-8') as f:
                f.write("--- %s segundos ---\n" % (time.time() - global_start_time))

            messagebox.showinfo('Ejecutar datos de prueba', "¡Los datos de prueba se han ejecutado satisfactoriamente!")

            plt.clf()
            self.canvas.draw()
            self.window.update()

            self.Graph = None
            self.Model = None

    # Función que muestra la imagen del modelo SIRS
    def mostrarModelo(self):
        root = tk.Toplevel()
        img = ImageTk.PhotoImage(Image.open("./assets/Modelo.png"))
        panel = tk.Label(root, image=img)
        panel.pack(side="bottom", fill="both", expand="yes")
        root.mainloop()

    # Función que muestra la imagen de las ecuaciones del modelo SIRS
    def mostrarEcuacionesModelo(self):
        root = tk.Toplevel()
        img = ImageTk.PhotoImage(Image.open("./assets/Ecuaciones Modelo.png"))
        panel = tk.Label(root, image=img)
        panel.pack(side="bottom", fill="both", expand="yes")
        root.mainloop()

    # Función que crea la gráfica con interpolación
    def conInterpolacion(self):
        self.graficaEvolucion(True)

    # Función que crea la gráfica sin interpolación
    def sinInterpolacion(self):
        self.graficaEvolucion(False)

    # Función que grafica la evolución de la infección en el tiempo
    def graficaEvolucion(self, interpolacion):
        plt.clf()

        T = np.arange(0, self.Model.iterations + 1, 1)
        S = [sum(map(lambda x: x == 0.5, i)) for i in self.Model.history]
        I = [sum(map(lambda x: x == 1, i)) for i in self.Model.history]
        R = [sum(map(lambda x: x == 0, i)) for i in self.Model.history]

        if interpolacion:
            T_S_Spline = make_interp_spline(T, S)
            T_I_Spline = make_interp_spline(T, I)
            T_R_Spline = make_interp_spline(T, R)

            T_ = np.linspace(T.min(), T.max(), 500)

            S_ = T_S_Spline(T_)
            I_ = T_I_Spline(T_)
            R_ = T_R_Spline(T_)

            plt.plot(T_, S_, "b", label="Susceptibles")
            plt.plot(T_, I_, "c", label="Infectados")
            plt.plot(T_, R_, "g", label="Recuperados")
        else:
            plt.plot(T, S, "b", label="Susceptibles")
            plt.plot(T, I, "c", label="Infectados")
            plt.plot(T, R, "g", label="Recuperados")

        plt.legend(loc='upper right')
        plt.grid(1)
        plt.xlabel('Iteración')
        plt.ylabel('Estado de los nodos')
        plt.xticks(np.arange(min(T), max(T) + 1, (len(T) - 1) / 10))

        self.canvas.draw()
        self.window.update()

        self.cargar_modelo["state"] = "disabled"
        self.guardar_modelo["state"] = "disabled"
        self.ejecutar_datos_prueba["state"] = "disabled"
        self.mostrar_grafica_evolucion.grid_forget()
        self.volver_modelo.grid(pady=9, row=1, column=1, padx=(17, 17))

        self.modo_grafica.grid(pady=(100, 42), row=1, column=1, columnspan=2, padx=(7, 6))
        self.con_interpolacion.grid(pady=8, row=2, column=1)
        self.sin_interpolacion.grid(pady=8, row=2, column=2)

        self.iteracion_actual.grid_forget()
        self.boton_first.grid_forget()
        self.boton_back.grid_forget()
        self.boton_forward.grid_forget()
        self.boton_last.grid_forget()

    # Función que vuelve a mostrar el modelo cuando se está en la gráfica de evolución
    def volverModelo(self):
        self.grafica()
        self.cargar_modelo["state"] = "normal"
        self.guardar_modelo["state"] = "normal"
        self.ejecutar_datos_prueba["state"] = "normal"
        self.mostrar_grafica_evolucion.grid(pady=9, row=1, column=1, padx=(17, 17))
        self.volver_modelo.grid_forget()

        self.iteracion_actual.grid(pady=(100, 42), row=1, column=1, columnspan=4, padx=(7, 6))
        self.boton_first.grid(pady=8, row=2, column=1, padx=(1, 1))
        self.boton_back.grid(pady=8, row=2, column=2, padx=(1, 1))
        self.boton_forward.grid(pady=8, row=2, column=3, padx=(1, 1))
        self.boton_last.grid(pady=8, row=2, column=4, padx=(1, 1))

        self.modo_grafica.grid_forget()
        self.con_interpolacion.grid_forget()
        self.sin_interpolacion.grid_forget()

    # Función que reinicia el grafo y el modelo, volviendo al estado inicial de la aplicación
    def nuevaEjecucion(self):
        self.cargar_modelo["state"] = "normal"
        self.guardar_modelo["state"] = "normal"
        self.ejecutar_datos_prueba["state"] = "normal"
        self.crear_nuevo_grafo["state"] = "normal"
        self.cargar_grafo["state"] = "normal"
        self.guardar_grafo["state"] = "normal"
        self.ejecutar_grafo["state"] = "normal"
        self.editar_parametros_button["state"] = "normal"
        self.mostrar_modelo["state"] = "normal"
        self.mostrar_ecuaciones_modelo["state"] = "normal"

        self.iteracion_actual.grid_forget()
        self.boton_first.grid_forget()
        self.boton_back.grid_forget()
        self.boton_forward.grid_forget()
        self.boton_last.grid_forget()

        self.mostrar_modelo.grid(pady=9, row=1, column=1, padx=(17, 17))
        self.mostrar_ecuaciones_modelo.grid(pady=(9, 172-self.ajuste_ventana), row=2, column=1, padx=(17, 17))
        self.mostrar_grafica_evolucion.grid_forget()
        self.volver_modelo.grid_forget()
        self.nueva_ejecucion.grid_forget()

        self.modo_grafica.grid_forget()
        self.con_interpolacion.grid_forget()
        self.sin_interpolacion.grid_forget()

        self.canvas.get_tk_widget().place_forget()
        self.Graph = None
        self.Model = None

    # Función que crea un nuevo grafo
    def crearNuevoGrafo(self):
        inputDialog = DialogoCrearGrafo(self.window)
        self.window.wait_window(inputDialog.top)

        if inputDialog.val is not None:
            self.Graph = Grafo(2, [str(inputDialog.val), str(inputDialog.val2)], self)

            height = 5 if self.ajuste_ventana == 0 else 4
            self.fig = plt.figure(figsize=(8, height), dpi=100)
            self.canvas = FigureCanvasTkAgg(self.fig, self.window)
            self.canvas.get_tk_widget().place(x=300, y=0)

            self.grafica()

    # Función que carga un grafo existente
    def cargarGrafo(self):
        filename = askopenfilename(initialdir='./Grafos Guardados', filetypes=(('Archivos JSON', '*.json'),))
        if filename:
            self.Graph = Grafo(1, [filename], self)

            if len(self.Graph.nodes) > 0:
                height = 5 if self.ajuste_ventana == 0 else 4
                self.fig = plt.figure(figsize=(8, height), dpi=100)
                self.canvas = FigureCanvasTkAgg(self.fig, self.window)
                self.canvas.get_tk_widget().place(x=300, y=0)

                self.grafica()
            else:
                self.Graph = None

    # Función que guarda/exporta en un archivo el grafo cargado actualmente
    def guardarGrafo(self):
        if self.Graph:
            file = asksaveasfile(initialdir='./Grafos Guardados', mode='w', defaultextension=".json",
                                 filetypes=(('Archivos JSON', '*.json'),))
            if file:
                self.Graph.save_graph(file)
                file.close()
        else:
            messagebox.showerror('Error', "No se ha creado ningun grafo.")

    # Función que ejecuta el modelo
    def ejecutarModelo(self):
        if self.Graph is None:
            self.crearNuevoGrafo()

        if self.Graph is not None and self.actualizarParametros():
            self.Model = Modelo(self.Graph.adjM, self.Graph, [float(i.get()) for i in self.parametros])

            self.quitarBotonesPre()
            self.Model.run(False)
            self.cargarBotonesPost()

    # Función que deshabilita los botones antes de ejecutar un modelo
    def quitarBotonesPre(self):
        self.cargar_modelo["state"] = "disabled"
        self.guardar_modelo["state"] = "disabled"
        self.ejecutar_datos_prueba["state"] = "disabled"
        self.crear_nuevo_grafo["state"] = "disabled"
        self.cargar_grafo["state"] = "disabled"
        self.guardar_grafo["state"] = "disabled"
        self.ejecutar_grafo["state"] = "disabled"
        self.editar_parametros_button["state"] = "disabled"
        self.mostrar_modelo["state"] = "disabled"
        self.mostrar_ecuaciones_modelo["state"] = "disabled"
        self.iteracion_actual.grid(pady=100, row=1, column=1, columnspan=4, padx=(7, 6))

    # Función que habilita los botones después de ejecutar un modelo
    def cargarBotonesPost(self):
        self.cargar_modelo["state"] = "normal"
        self.guardar_modelo["state"] = "normal"
        self.ejecutar_datos_prueba["state"] = "normal"

        self.iteracion_actual.grid(pady=(100, 42), row=1, column=1, columnspan=4, padx=(7, 6))

        self.boton_first.grid(pady=8, row=2, column=1, padx=(1, 1))
        self.boton_back.grid(pady=8, row=2, column=2, padx=(1, 1))
        self.boton_forward.grid(pady=8, row=2, column=3, padx=(1, 1))
        self.boton_last.grid(pady=8, row=2, column=4, padx=(1, 1))

        self.mostrar_modelo.grid_forget()
        self.mostrar_ecuaciones_modelo.grid_forget()
        self.mostrar_grafica_evolucion.grid(pady=9, row=1, column=1, padx=(17, 17))
        self.nueva_ejecucion.grid(pady=(9, 172-self.ajuste_ventana), row=2, column=1, padx=(17, 17))

    # Función que muestra la primera iteración del modelo actual
    def goFirst(self):
        if self.Model.t > 0:
            self.Model.t = 0
            nx.set_node_attributes(self.Graph.G, {i: self.Model.history[self.Model.t][i] for i in
                                                  range(len(self.Model.history[self.Model.t]))},
                                   name='value')
            self.grafica()

    # Función que muestra la anterior iteración del modelo actual
    def goBack(self) -> None:
        if self.Model.t > 0:
            self.Model.t -= 1
            nx.set_node_attributes(self.Graph.G, {i: self.Model.history[self.Model.t][i] for i in
                                                  range(len(self.Model.history[self.Model.t]))},
                                   name='value')
            self.grafica()

    # Función que muestra la siguiente iteración del modelo actual
    def goForward(self) -> None:
        if self.Model.t < self.Model.iterations:
            self.Model.t += 1
            nx.set_node_attributes(self.Graph.G, {i: self.Model.history[self.Model.t][i] for i in
                                                  range(len(self.Model.history[self.Model.t]))},
                                   name='value')
            self.grafica()

    # Función que muestra la última iteración del modelo actual
    def goLast(self) -> None:
        if self.Model.t < self.Model.iterations:
            self.Model.t = int(self.Model.iterations)
            nx.set_node_attributes(self.Graph.G, {i: self.Model.history[self.Model.t][i] for i in
                                                  range(len(self.Model.history[self.Model.t]))},
                                   name='value')
            self.grafica()

    # Función que grafica las funciones seleccionadas utilizando la función plot de matplotlib.pyplot
    def grafica(self):
        plt.clf()

        mapper = mpl.cm.ScalarMappable(norm=self.colors, cmap=self.cmap)
        nx.draw(self.Graph.G, self.Graph.pos, node_color=[mapper.to_rgba(self.Graph.G.nodes[i]['value'])
                                                          for i in self.Graph.G.nodes], with_labels=True,
                font_color='black', edge_cmap=mpl.cm.coolwarm, vmin=0, vmax=1)

        plt.legend(handles=self.custom_lines, labelspacing=1.2)

        if self.Model:
            if self.Model.t > 0:
                self.iteracion_actual['text'] = "Iteración # {}".format(self.Model.t)
            else:
                self.iteracion_actual['text'] = "Estado inicial"

        self.canvas.draw()
        self.window.update()

    # Función que valida si los caracteres ingresados en el campo de los parámetros son válidos
    def validate(self, S):
        valid = S == '' or S == ',' or S == '.' or S.isdigit() or self.is_float(S)
        if not valid:
            self.window.bell()
        return valid

    # Función que evalua si una cadena de texto es un numero real
    def is_float(self, element) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False

    # Función que habilita los parámetros para ser actualizados
    def habilitarParametros(self):
        self.cargar_modelo["state"] = "disabled"
        self.guardar_modelo["state"] = "disabled"
        self.ejecutar_datos_prueba["state"] = "disabled"
        self.crear_nuevo_grafo["state"] = "disabled"
        self.cargar_grafo["state"] = "disabled"
        self.guardar_grafo["state"] = "disabled"
        self.ejecutar_grafo["state"] = "disabled"

        for i in self.parametros:
            i.configure(state='normal')

        self.editar_parametros_button.grid_forget()
        self.actualizar_parametros_button.grid(pady=8, row=8, column=1, columnspan=2, padx=(17, 17))

    # Función que actualiza los parametros con los valores ingresados por el usuario si estos son validos
    def actualizarParametros(self) -> bool:
        try:
            for i in range(4):
                if i < 3:
                    act = float(self.parametros[i].get())
                    if not 0 <= act <= 1:
                        raise ValueError('Parámetros: al menos un valor ingresado está fuera de rango')
                if i == 3:
                    act = int(self.parametros[i].get())
                    if not 1 <= act <= 100:
                        raise ValueError('Parámetros: al menos un valor ingresado está fuera de rango')

            for i in self.parametros:
                i.configure(state='readonly')

            self.cargar_modelo["state"] = "normal"
            self.guardar_modelo["state"] = "normal"
            self.ejecutar_datos_prueba["state"] = "normal"
            self.crear_nuevo_grafo["state"] = "normal"
            self.cargar_grafo["state"] = "normal"
            self.guardar_grafo["state"] = "normal"
            self.ejecutar_grafo["state"] = "normal"
            self.editar_parametros_button.grid(pady=8, row=8, column=1, columnspan=2, padx=(17, 17))
            self.actualizar_parametros_button.grid_forget()
            return True

        except ValueError as e:
            if str(e).startswith('invalid') or str(e).startswith('could'):
                messagebox.showerror('Error', "Parámetros: al menos un valor ingresado no es válido.")
            else:
                messagebox.showerror('Error', str(e) + ".")
            return False


# Función principal de la aplicación. Crea la interfaz gráfica
if __name__ == '__main__':
    ventana = Ventana()
