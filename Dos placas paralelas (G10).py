#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from solver import Node, ThermalModel, FDMExplicit
from matplotlib.figure import Figure
import datetime

inicio = datetime.datetime.now()		# Tiempo de Compilación


# CONSTANTES

EMLI = 0.95     		# 
E1 = 1       	        # 

F=0.2

# Tiempo de Simulación

t_start = 0.0
t_end = 300.0   # 

# VARIACION DE POTENCIA

def power_PHEATER(time):     # Variación  de Potencia en heater
    if time == 0.0:
        return 0.0
    elif time >= 1.0 and time <=150.0:
        return 100.0
    else:
        return 100.0
		
model = ThermalModel()



model.addNode(Node(1, 0.0027*1300, 4, power_PHEATER, 'P1'))


model.addNode(Node(2, 0.0027*1300, 4, lambda x: 0.0, 'P2'))

model.addNode(Node(-7, 1.0,    4, lambda x: 0.0, 'Espacio'))


#HEADER CONDUCTOR DATA

model.addAdmittance(1, 2, 2500*F)                 #Placa 1


model.addAdmittance(1, -7, 2500.0*(1-F))          #Placa 2

model.addAdmittance(2, -7, 2500.0*(1-F))              #Espacio


solver = FDMExplicit(model,0.01)
solver.solve(t_start, t_end)	



#------------------------------CREAR VENTANA---------------------------------
root = tkinter.Tk()
root.wm_title("Análisis y Diseño Térmico")


#------------------------------CREAR GRAFICA---------------------------------
fig = Figure(figsize=(5, 5), dpi=100)




fig.add_subplot(111).plot((solver.t),solver.T[0]-273, linestyle='--', color='blue', label="PLACA 1")
fig.add_subplot(111).plot((solver.t),solver.T[1]-273, linestyle='-', color='green', label="PLACA 2")

#fig.add_subplot(111).plot((solver.t)/3600,solver.T[7]-273, linestyle='--', color='blue', label="ESPACIO")



# 
# #GRAFICA IMAGENES
# 
fig.suptitle("PLACAS PARALELAS (G10) d=9mm", fontsize=14)
fig.add_subplot(111).set_xlabel('Tiempo [s]')
fig.add_subplot(111).set_ylabel('Temperatura [C]')
fig.add_subplot(111).grid(linestyle='--', linewidth=0.9, alpha=0.5)
fig.add_subplot(111).legend(loc=6, bbox_to_anchor=(1.0,0.9))


canvas = FigureCanvasTkAgg(fig, master=root)  # CREAR AREA DE DIBUJO DE TKINTER.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

#-----------------------AÑADIR BARRA DE HERRAMIENTAS--------------------------
toolbar = NavigationToolbar2Tk(canvas, root)# barra de iconos
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

#-----------------------------BOTÓN "cerrar"----------------------------------
def cerrar():
    root.quit()     
    root.destroy()

button = tkinter.Button(master=root, text="cerrar", command=cerrar)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()

#*******************************************************************************
# Calculo del Tiempo  

final = datetime.datetime.now()

Diferencia = final - inicio
print(" ")
print("Tiempo de Procesamiento:")
print Diferencia.total_seconds()


