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

        top = self.top = tk.Toplevel(parent)

        self.myLabel = tk.Label(top, text='Ingrese el numero de nodos (entre 2 y 100):')
        self.myLabel.pack()

        vldt_ifnum_cmd = (self.top.register(self.validate), '%S')
        self.entry = tk.Entry(top, validate='all', validatecommand=vldt_ifnum_cmd)
        self.entry.pack()

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
            if 2 <= int(self.entry.get()) <= 100:
                self.val = self.entry.get()
                self.top.destroy()
            else:
                messagebox.showerror('Error', "El valor ingresado está fuera de rango (entre 2 y 100)")
        else:
            self.top.bell()
