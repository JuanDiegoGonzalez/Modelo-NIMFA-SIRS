# -*- coding: utf-8 -*-

# ----------------------------------------------------
# Interfaz principal de la aplicacion
# Realizado por: Juan Diego Gonzalez Gomez - 201911031
# Adaptado y modificado de: https://github.com/MartinGalvanCastro/NimdaModel
# ----------------------------------------------------

# -------------------- Imports -----------------------
import sys
from Modelotemp import Graph
from Modelo import Modelo

from PySide2.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import *

# -------------------- Variables globales -----------------------
ratio_ventana = 1

# -------------------- Clase ventana principal --------------------
class Ui_MainWindow(object):
    # Funcion que declara y configura los elementos de la interfaz principal
    def setupUi(self, MainWindow):
        global ratio_ventana

        # ---------- Declaracion de atributos ----------
        self.Graph = None
        self.Model = None

        ratio_ventana = 0.7 if MainWindow.screen().geometry().height() < 1000 else 1

        # Parametro 1: Punto de inicio en X (esquina superior izquierda)
        # Parametro 2: Punto de inicio en Y (esquina superior izquierda)
        # Parametro 3: Longitud en X
        # Parametro 4: Longitud en Y
        self.posElementos = [
            QRect(240, 0*ratio_ventana, 20, 521*ratio_ventana),  # Linea de separacion - Barra de menu
            QRect(0, 0*ratio_ventana, 801, 21*ratio_ventana),  # Barra de menu
            QRect(30, 30*ratio_ventana, 181, 31*ratio_ventana),  # "Parametros"
            QRect(20, 80*ratio_ventana, 201, 31*ratio_ventana),  # Boton "Cargar Simulacion"
            QRect(20, 130*ratio_ventana, 201, 31*ratio_ventana),  # Boton "Guardar Simulacion"
            QRect(20, 180*ratio_ventana, 201, 31*ratio_ventana),  # Boton "Generar un Nuevo Grafo"

            QRect(25, 240*ratio_ventana, 181, 31*ratio_ventana),  # Titulo "Tasa de Infeccion"
            QRect(20, 280*ratio_ventana, 191, 22*ratio_ventana),  # Slider Tasa de Infeccion
            QRect(10, 220*ratio_ventana, 221, 16*ratio_ventana),  # Separador Botones con Tasas
            QRect(163, 310*ratio_ventana, 47, 13*ratio_ventana),  # Numero "1" de la tasa de Infeccion
            QRect(80, 310*ratio_ventana, 47, 13*ratio_ventana),  # Numero "0.5" de la tasa de Infeccion
            QRect(-20, 310*ratio_ventana, 51, 16*ratio_ventana),  # Numero "0" de la tasa de Infeccion

            QRect(25, 340*ratio_ventana, 181, 31*ratio_ventana),  # Titulo "Tasa de Cura"
            QRect(20, 380*ratio_ventana, 191, 22*ratio_ventana),  # Slider Tasa de Cura
            QRect(10, 540*ratio_ventana, 221, 16*ratio_ventana),  # Separador "Tasas con Correr simulacion"
            QRect(-20, 410*ratio_ventana, 51, 16*ratio_ventana),  # Numero "0" de la tasa de Infeccion
            QRect(80, 410*ratio_ventana, 47, 13*ratio_ventana),  # Numero "0.5" de la tasa de Infeccion
            QRect(163, 410*ratio_ventana, 47, 13*ratio_ventana),  # Numero "1" de la tasa de Infeccion

            QRect(25, 440*ratio_ventana, 181, 31*ratio_ventana),  # Titulo "Tasa de Resusceptibilidad"
            QRect(20, 480*ratio_ventana, 191, 22*ratio_ventana),  # Slider Tasa de Resusceptibilidad
            QRect(10, 540*ratio_ventana, 221, 16*ratio_ventana),  # Separador
            QRect(-20, 510*ratio_ventana, 51, 16*ratio_ventana),  # Numero "0" de la tasa de Infeccion
            QRect(80, 510*ratio_ventana, 47, 13*ratio_ventana),  # Numero "0.5" de la tasa de Infeccion
            QRect(163, 510*ratio_ventana, 47, 13*ratio_ventana),  # Numero "1" de la tasa de Infeccion

            QRect(20, 570*ratio_ventana, 201, 31*ratio_ventana),  # Boton "Correr Simulacion"
        ]

        # ---------- Configuracion de la pantalla ----------
        MainWindow.setFixedSize(242, 670*ratio_ventana)

        # ---------- Fuentes ----------
        # Tamanio slider de las tasas
        font = QFont()
        font.setPointSize(7*ratio_ventana)
        font.setBold(False)
        font.setWeight(50)

        # "Tasa de..."
        font1 = QFont()
        font1.setPointSize(12*ratio_ventana)

        # "0", "0.5" y "1"
        font2 = QFont()
        font2.setPointSize(11*ratio_ventana)

        # "Parametros"
        font3 = QFont()
        font3.setPointSize(22*ratio_ventana)
        font3.setBold(True)
        font3.setWeight(75)

        # ---------- Barra de menu ----------
        # Subelementos de la barra de menu
        self.actionNuevo = QAction(MainWindow)
        self.actionNuevo.setObjectName(u"actionNuevo")
        self.actionCargar = QAction(MainWindow)
        self.actionCargar.setObjectName(u"actionCargar")
        self.actionGuardar = QAction(MainWindow)
        self.actionGuardar.setObjectName(u"actionGuardar")
        self.actionCerrar = QAction(MainWindow)
        self.actionCerrar.setObjectName(u"actionCerrar")
        self.actionAyuda_sobre_el_uso_del_app = QAction(MainWindow)
        self.actionAyuda_sobre_el_uso_del_app.setObjectName(u"actionAyuda_sobre_el_uso_del_app")
        self.actionAcerca_de_la_App = QAction(MainWindow)
        self.actionAcerca_de_la_App.setObjectName(u"actionAcerca_de_ka_Aoo")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        # Configuracion de la barra de menu
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(self.posElementos[0])
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(self.posElementos[1])

        # Elementos de la barra de menu
        self.menuArchivo = QMenu(self.menubar)
        self.menuArchivo.setObjectName(u"menuArchivo")
        self.menuAyuda = QMenu(self.menubar)
        self.menuAyuda.setObjectName(u"menuAyuda")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Adicion de elementos a la barra de menu
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())
        self.menuArchivo.addAction(self.actionNuevo)
        self.menuArchivo.addAction(self.actionCargar)
        self.menuArchivo.addAction(self.actionGuardar)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.actionCerrar)
        self.menuAyuda.addAction(self.actionAyuda_sobre_el_uso_del_app)
        self.menuAyuda.addSeparator()
        self.menuAyuda.addAction(self.actionAcerca_de_la_App)

        # ---------- Interfaz principal ----------
        # Titulo "Parametros"
        self.TituloParametros = QLabel(self.centralwidget)
        self.TituloParametros.setObjectName(u"TituloParametros")
        self.TituloParametros.setGeometry(self.posElementos[2])
        self.TituloParametros.setFont(font3)
        self.TituloParametros.setAlignment(Qt.AlignCenter)

        # Botones "Cargar Simulacion", "Guardar Simulacion" y "Generar un Nuevo Grafo"
        self.Cargar = QPushButton(self.centralwidget)
        self.Cargar.setObjectName(u"Cargar")
        self.Cargar.setGeometry(self.posElementos[3])
        self.Guardar = QPushButton(self.centralwidget)
        self.Guardar.setObjectName(u"Guardar")
        self.Guardar.setGeometry(self.posElementos[4])
        self.NuevoGrafo = QPushButton(self.centralwidget)
        self.NuevoGrafo.setObjectName(u"NuevoGrafo")
        self.NuevoGrafo.setGeometry(self.posElementos[5])

        # Separador (entre los botones y las tasas)
        self.Separador1 = QFrame(self.centralwidget)
        self.Separador1.setObjectName(u"Separador1")
        self.Separador1.setGeometry(self.posElementos[8])
        self.Separador1.setFrameShape(QFrame.HLine)
        self.Separador1.setFrameShadow(QFrame.Sunken)

        # ----- Tasa de infeccion -----
        # Titulo
        self.TituloTasaInf = QLabel(self.centralwidget)
        self.TituloTasaInf.setObjectName(u"TituloTasaInf")
        self.TituloTasaInf.setGeometry(self.posElementos[6])
        self.TituloTasaInf.setFont(font1)
        self.TituloTasaInf.setAlignment(Qt.AlignCenter)

        # Slider
        self.TasaInfeccionSlider = QSlider(self.centralwidget)
        self.TasaInfeccionSlider.setObjectName(u"TasaInfeccionSlider")
        self.TasaInfeccionSlider.setGeometry(self.posElementos[7])
        self.TasaInfeccionSlider.setFont(font)
        self.TasaInfeccionSlider.setFocusPolicy(Qt.StrongFocus)
        self.TasaInfeccionSlider.setMaximum(12)
        self.TasaInfeccionSlider.setSingleStep(1)
        self.TasaInfeccionSlider.setPageStep(2)
        self.TasaInfeccionSlider.setValue(0)
        self.TasaInfeccionSlider.setSliderPosition(0)
        self.TasaInfeccionSlider.setTracking(True)
        self.TasaInfeccionSlider.setOrientation(Qt.Horizontal)
        self.TasaInfeccionSlider.setInvertedAppearance(False)
        self.TasaInfeccionSlider.setInvertedControls(False)
        self.TasaInfeccionSlider.setTickPosition(QSlider.TicksBelow)
        self.TasaInfeccionSlider.setTickInterval(2)

        # Numeros "0", "0.5" y "1"
        self.Num0TInf = QLabel(self.centralwidget)
        self.Num0TInf.setObjectName(u"Num0TInf")
        self.Num0TInf.setGeometry(self.posElementos[11])
        self.Num0TInf.setFont(font2)
        self.Num0TInf.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.Num1TInf = QLabel(self.centralwidget)
        self.Num1TInf.setObjectName(u"Num1TInf")
        self.Num1TInf.setGeometry(self.posElementos[10])
        self.Num1TInf.setFont(font2)
        self.Num1TInf.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.Num2TInf = QLabel(self.centralwidget)
        self.Num2TInf.setObjectName(u"Num2TInf")
        self.Num2TInf.setGeometry(self.posElementos[9])
        self.Num2TInf.setFont(font2)
        self.Num2TInf.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        # ----- Tasa de cura -----
        # Titulo
        self.TituloTasaCur = QLabel(self.centralwidget)
        self.TituloTasaCur.setObjectName(u"TituloTasaCur")
        self.TituloTasaCur.setGeometry(self.posElementos[12])
        self.TituloTasaCur.setFont(font1)
        self.TituloTasaCur.setAlignment(Qt.AlignCenter)

        # Slider
        self.TasaCuraSlider = QSlider(self.centralwidget)
        self.TasaCuraSlider.setObjectName(u"TasaCuraSlider")
        self.TasaCuraSlider.setGeometry(self.posElementos[13])
        self.TasaCuraSlider.setFont(font)
        self.TasaCuraSlider.setFocusPolicy(Qt.StrongFocus)
        self.TasaCuraSlider.setMaximum(12)
        self.TasaCuraSlider.setSingleStep(1)
        self.TasaCuraSlider.setPageStep(2)
        self.TasaCuraSlider.setValue(0)
        self.TasaCuraSlider.setSliderPosition(0)
        self.TasaCuraSlider.setTracking(True)
        self.TasaCuraSlider.setOrientation(Qt.Horizontal)
        self.TasaCuraSlider.setInvertedAppearance(False)
        self.TasaCuraSlider.setInvertedControls(False)
        self.TasaCuraSlider.setTickPosition(QSlider.TicksBelow)
        self.TasaCuraSlider.setTickInterval(2)

        # Numeros "0", "0.5" y "1"
        self.Num0TCon_2 = QLabel(self.centralwidget)
        self.Num0TCon_2.setObjectName(u"Num0TCon_2")
        self.Num0TCon_2.setGeometry(self.posElementos[15])
        self.Num0TCon_2.setFont(font2)
        self.Num0TCon_2.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.Num1TCur = QLabel(self.centralwidget)
        self.Num1TCur.setObjectName(u"Num1TCur")
        self.Num1TCur.setGeometry(self.posElementos[16])
        self.Num1TCur.setFont(font2)
        self.Num1TCur.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.Num2TCura = QLabel(self.centralwidget)
        self.Num2TCura.setObjectName(u"Num2TCura")
        self.Num2TCura.setGeometry(self.posElementos[17])
        self.Num2TCura.setFont(font2)
        self.Num2TCura.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        # ----- Tasa de resusceptibilidad -----
        # Titulo
        self.TituloTasaRes = QLabel(self.centralwidget)
        self.TituloTasaRes.setObjectName(u"TituloTasaRes")
        self.TituloTasaRes.setGeometry(self.posElementos[18])
        self.TituloTasaRes.setFont(font1)
        self.TituloTasaRes.setAlignment(Qt.AlignCenter)

        # Slider
        self.TasaResSlider = QSlider(self.centralwidget)
        self.TasaResSlider.setObjectName(u"TasaResSlider")
        self.TasaResSlider.setGeometry(self.posElementos[19])
        self.TasaResSlider.setFont(font)
        self.TasaResSlider.setFocusPolicy(Qt.StrongFocus)
        self.TasaResSlider.setMaximum(12)
        self.TasaResSlider.setSingleStep(1)
        self.TasaResSlider.setPageStep(2)
        self.TasaResSlider.setValue(0)
        self.TasaResSlider.setSliderPosition(0)
        self.TasaResSlider.setTracking(True)
        self.TasaResSlider.setOrientation(Qt.Horizontal)
        self.TasaResSlider.setInvertedAppearance(False)
        self.TasaResSlider.setInvertedControls(False)
        self.TasaResSlider.setTickPosition(QSlider.TicksBelow)
        self.TasaResSlider.setTickInterval(2)

        # Numeros "0", "0.5" y "1"
        self.Num0TRes = QLabel(self.centralwidget)
        self.Num0TRes.setObjectName(u"Num0TRes")
        self.Num0TRes.setGeometry(self.posElementos[21])
        self.Num0TRes.setFont(font2)
        self.Num0TRes.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.Num1TRes = QLabel(self.centralwidget)
        self.Num1TRes.setObjectName(u"Num1TRes")
        self.Num1TRes.setGeometry(self.posElementos[22])
        self.Num1TRes.setFont(font2)
        self.Num1TRes.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.Num2TRes = QLabel(self.centralwidget)
        self.Num2TRes.setObjectName(u"Num2TRes")
        self.Num2TRes.setGeometry(self.posElementos[23])
        self.Num2TRes.setFont(font2)
        self.Num2TRes.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        # Separador (entre las tasas y "Correr simulacion")
        self.Separador2 = QFrame(self.centralwidget)
        self.Separador2.setObjectName(u"Separador2")
        self.Separador2.setGeometry(self.posElementos[14])
        self.Separador2.setFrameShape(QFrame.HLine)
        self.Separador2.setFrameShadow(QFrame.Sunken)

        # ---------- Boton "Correr simulacion" ----------
        self.Correr = QPushButton(self.centralwidget)
        self.Correr.setObjectName(u"Correr")
        self.Correr.setGeometry(self.posElementos[24])

        # ---------- Traducir interfaz a palabras ----------
        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # -------------------- Otras funciones de la clase --------------------

    # Funcion que traduce la interfaz principal a palabras
    def retranslateUi(self, MainWindow):
        # Titulo de la pantalla
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"Modelo SIRS", None))

        # Elementos del menu
        self.menuArchivo.setTitle(
            QCoreApplication.translate("MainWindow", u"Archivo", None))
        self.actionNuevo.setText(
            QCoreApplication.translate("MainWindow", u"Nuevo", None))
        self.actionCargar.setText(
            QCoreApplication.translate("MainWindow", u"Cargar", None))
        self.actionGuardar.setText(
            QCoreApplication.translate("MainWindow", u"Guardar", None))
        self.actionCerrar.setText(
            QCoreApplication.translate("MainWindow", u"Cerrar", None))

        self.menuAyuda.setTitle(
            QCoreApplication.translate("MainWindow", u"Ayuda", None))
        self.actionAyuda_sobre_el_uso_del_app.setText(
            QCoreApplication.translate("MainWindow", u"Ayuda sobre el uso del app", None))
        self.actionAcerca_de_la_App.setText(
            QCoreApplication.translate("MainWindow", u"Acerca de la App", None))

        self.TituloParametros.setText(
            QCoreApplication.translate("MainWindow", u"Parametros", None))

        # Botones superiores
        self.Cargar.setText(QCoreApplication.translate(
            "MainWindow", u"Cargar Simulaci\u00f3n", None))
        self.Cargar.clicked.connect(self.loadGraph)
        self.Guardar.setText(QCoreApplication.translate(
            "MainWindow", u"Guardar Simulaci\u00f3n", None))
        self.Guardar.clicked.connect(self.saveGraph)
        self.NuevoGrafo.setText(QCoreApplication.translate(
            "MainWindow", u"Generar un Nuevo Grafo", None))
        self.NuevoGrafo.clicked.connect(self.newGraph)

        # Elementos tasa de infeccion
        self.TituloTasaInf.setText(QCoreApplication.translate(
            "MainWindow", u"Tasa de Infeccion", None))
        self.Num0TInf.setText(
            QCoreApplication.translate("MainWindow", u"0", None))
        self.Num1TInf.setText(
            QCoreApplication.translate("MainWindow", u"0.5", None))
        self.Num2TInf.setText(
            QCoreApplication.translate("MainWindow", u"1", None))

        # Elementos tasa de cura
        self.TituloTasaCur.setText(QCoreApplication.translate(
            "MainWindow", u"Tasa de Cura", None))
        self.Num0TCon_2.setText(
            QCoreApplication.translate("MainWindow", u"0", None))
        self.Num1TCur.setText(
            QCoreApplication.translate("MainWindow", u"0.5", None))
        self.Num2TCura.setText(
            QCoreApplication.translate("MainWindow", u"1", None))

        # Elementos tasa de resusceptibilidad
        self.TituloTasaRes.setText(QCoreApplication.translate(
            "MainWindow", u"Tasa de Resusceptibilidad", None))
        self.Num0TRes.setText(
            QCoreApplication.translate("MainWindow", u"0", None))
        self.Num1TRes.setText(
            QCoreApplication.translate("MainWindow", u"0.5", None))
        self.Num2TRes.setText(
            QCoreApplication.translate("MainWindow", u"1", None))

        # Boton final
        self.Correr.setText(QCoreApplication.translate(
            'MainWindow', u"Correr Simulaci\u00f3n", None))
        self.Correr.clicked.connect(self.runModel)

    # Funcion que carga una simulacion guardada
    def loadGraph(self):
        dialog = QDialog()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(dialog, "Cargar Grafo", "", "All Files (*);;JSON files (*.json)",
                                                  options=options)
        if fileName:
            self.Graph = Graph(1, fileName)
            self.Graph.plot()

    # Funcion que guarda la simulacion actual
    def saveGraph(self):
        dialog = QDialog()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(dialog, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
            self.Graph.save_graph(fileName)

    # Funcion que genera un nuevo grafo
    def newGraph(self):
        dialog = QDialog()
        ui = Ui_NuevoGrafo()
        ui.setupUi(dialog)
        dialog.show()
        resp = dialog.exec_()
        val = ui.spinBox.value()

        if resp:
            self.Graph = Graph(2, str(val))
            self.Graph.plot()

    # Funcion que ejecuta el modelo
    def runModel(self):
        print("\nLa simulacion iniciara\n")
        alfaI = self.TasaInfeccionSlider.value() / 12
        deltaI = self.TasaCuraSlider.value() / 12
        self.Model = Modelo(self.Graph.adjM, self.Graph, alfaI, deltaI)
        self.Model.run()
        self.Model.plotTime()

# -------------------- Clase ventana nuevo grafo --------------------
class Ui_NuevoGrafo(object):
    # Funcion que declara y configura los elementos de la ventana
    def setupUi(self, NuevoGrafo):
        global ratio_ventana

        # ---------- Declaracion de atributos ----------
        # Parametro 1: Punto de inicio en X (esquina superior izquierda)
        # Parametro 2: Punto de inicio en Y (esquina superior izquierda)
        # Parametro 3: Longitud en X
        # Parametro 4: Longitud en Y
        self.posElementos = [
            QRect(30, 10*ratio_ventana, 241, 51*ratio_ventana),  # Texto "Ingrese el numero de nodos"
            QRect(30, 70*ratio_ventana, 71, 31*ratio_ventana),  # Selector del numero de nodos
            QRect(110, 70*ratio_ventana, 161, 32*ratio_ventana),  # Botones "OK" y "Cancel"
        ]

        # ---------- Fuentes ----------
        # Texto "Ingrese el numero de nodos"
        font = QFont()
        font.setPointSize(12*ratio_ventana)

        # ---------- Ventana ----------
        # Texto "Ingrese el numero de nodos"
        self.label = QLabel(NuevoGrafo)
        self.label.setObjectName(u"label")
        self.label.setGeometry(self.posElementos[0])
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        # Selector del numero de nodos
        self.spinBox = QSpinBox(NuevoGrafo)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(self.posElementos[1])
        self.spinBox.setAlignment(Qt.AlignCenter)
        self.spinBox.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.spinBox.setMinimum(2)

        # Botones "OK" y "Cancel"
        self.buttonBox = QDialogButtonBox(NuevoGrafo)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(self.posElementos[2])
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        # ---------- Traducir interfaz a palabras ----------
        self.retranslateUi(NuevoGrafo)

        # ---------- Ajustar opciones del boton ----------
        self.buttonBox.accepted.connect(NuevoGrafo.accept)
        self.buttonBox.rejected.connect(NuevoGrafo.reject)

        QMetaObject.connectSlotsByName(NuevoGrafo)

    # Funcion que traduce la ventana "Nuevo Grafo" a palabras
    def retranslateUi(self, NuevoGrafo):
        NuevoGrafo.setWindowTitle(QCoreApplication.translate("NuevoGrafo", u"Nuevo Grafo", None))
        self.label.setText(QCoreApplication.translate("NuevoGrafo", u"Ingrese el numero de nodos", None))

# -------------------- Clase App --------------------
class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

# -------------------- Funcion principal (main) --------------------
if __name__ == "__main__":
    app = QApplication()
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())
