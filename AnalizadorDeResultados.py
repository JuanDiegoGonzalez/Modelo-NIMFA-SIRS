import numpy as np
import tkinter as tk

from tkinter.filedialog import askopenfilename

window = tk.Tk()
filename = askopenfilename(initialdir='./Datos de Prueba', filetypes=(('Archivos de texto', '*.txt'),))

try:
    file = open(filename)
    file.readline()
    file.readline()
    file.readline()
    file.readline()
    file.readline()
    iter = int(file.readline()[:-1])

    S_historico = []
    I_historico = []
    R_historico = []

    for i in range(iter):
        line = file.readline()
        vals = line.replace("[", "").replace("]", "").replace(" ", "").split(",")
        datos = [float(j) for j in vals]

        S = 0
        I = 0
        R = 0
        for j in datos:
            if j == 0.5:
                S += 1
            elif j == 1:
                I += 1
            else:
                R += 1

        S_historico.append(S)
        I_historico.append(I)
        R_historico.append(R)

    print("Susceptibles:\navg:{}\nmax:{}\nmin:{}\n".format(np.average(S_historico), np.max(S_historico),
                                                           np.min(S_historico)))
    print("Infectados:\navg:{}\nmax:{}\nmin:{}\n".format(np.average(I_historico), np.max(I_historico),
                                                         np.min(I_historico)))
    print("Recuperados:\navg:{}\nmax:{}\nmin:{}\n".format(np.average(R_historico), np.max(R_historico),
                                                          np.min(R_historico)))

except Exception as e:
    print(e)
    print("Debe seleccionar un archivo con un modelo de la carpeta /Datos de Prueba")
