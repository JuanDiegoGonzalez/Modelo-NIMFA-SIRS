# ----------------------------------------------------
# Diálogo mostrado para generar un nuevo grafo
# Realizado por: Juan Diego González Gómez
# ----------------------------------------------------

# -------------------- Imports -----------------------
import tkinter as tk

from tkinter import messagebox


class DialogoCrearGrafo:
    def __init__(self, parent):
        self.val = None
        self.val2 = None

        top = self.top = tk.Toplevel(parent)

        self.myLabel = tk.Label(top, text='Ingrese el numero de nodos (entre 2 y 100):')
        self.myLabel.pack()

        vldt_ifnum_cmd = (self.top.register(self.validate), '%S')
        self.entry = tk.Entry(top, validate='all', validatecommand=vldt_ifnum_cmd)
        self.entry.pack()

        self.myLabel2 = tk.Label(top, text='Ingrese el nivel de densidad (entre 0 y 40):')
        self.myLabel2.pack()

        vldt_ifnum_cmd = (self.top.register(self.validate), '%S')
        self.entry2 = tk.Entry(top, validate='all', validatecommand=vldt_ifnum_cmd)
        self.entry2.pack()

        self.submitButton = tk.Button(top, text='Submit', command=self.send)
        self.submitButton.pack()

        self.cancelButton = tk.Button(top, text='Cancel', command=self.top.destroy)
        self.cancelButton.pack()

    def validate(self, S):
        valid = S == '' or S.isdigit()
        if not valid:
            self.top.bell()
        return valid

    def send(self):
        if self.entry.get() != "":
            if (2 <= int(self.entry.get()) <= 100) and (0 <= int(self.entry2.get()) <= 40):
                self.val = self.entry.get()
                self.val2 = self.entry2.get()
                self.top.destroy()
            else:
                messagebox.showerror('Error', "Al menos un valor ingresado está fuera de rango.")
        else:
            self.top.bell()
