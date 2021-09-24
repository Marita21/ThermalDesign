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
m_Al= 0.506             # kg [V=0.25m*0.25m*0.003 y Densidad=2700Kg/m^2]
C_AL=880                # 880 J/kg*K                 
F=0.2

mdisco=0.429
C_TFL=1000

# Tiempo de Simulación

t_start = 0.0
t_end = 25000.0   # 

# VARIACION DE POTENCIA

def power_PHEATER(time):     # Variación  de Potencia en heater
    if time == 0.0:
        return 0.0
    elif time >= 1.0 and time <=150.0:
        return 100.0
    else:
        return 100.0
		

model = ThermalModel()



model.addNode(Node(1, m_Al*C_AL, 4, power_PHEATER, 'Placa 1'))

model.addNode(Node(2, m_Al*C_AL, 4, lambda x: 0.0, 'Placa 2'))

model.addNode(Node(3,mdisco*C_TFL,4,lambda x: 0.0, 'Disco'))

model.addNode(Node(-4, 1.0,    4, lambda x: 0.0, 'Espacio'))


#HEADER CONDUCTOR DATA

model.addConductance(2, 3, 5.41)

model.addAdmittance(1, 2, 650*F)                #Placa 1 [cm^2]  SIGMA = 5.67e-12 Stefan-Boltzmann constant in w/cm^2xK^4
model.addAdmittance(1, -4, 650.0*(1-F))          #Placa 2[cm^2]
model.addAdmittance(2, -4, (650.0-50)*(1-F))          #Espacio [cm^2]


solver = FDMExplicit(model,0.01)
solver.solve(t_start, t_end)	

#*******************************************************************************
# Calculo del Tiempo  

final = datetime.datetime.now()

Diferencia = final - inicio
print(" ")
print("Tiempo de Procesamiento:")
print (Diferencia.total_seconds())


#------------------------------CREAR VENTANA---------------------------------
root = tkinter.Tk()
root.wm_title("Análisis y Diseño Térmico")


#------------------------------CREAR GRAFICA---------------------------------
fig = Figure(figsize=(5, 5), dpi=100)




fig.add_subplot(111).plot((solver.t)/3600,solver.T[0]-273, linestyle='--', color='blue', label="PLACA 1")
fig.add_subplot(111).plot((solver.t)/3600,solver.T[1]-273, linestyle='-', color='green', label="PLACA 2")

fig.add_subplot(111).plot((solver.t)/3600,solver.T[2]-273, linestyle='--', color='RED', label="DISCO")



# 
# #GRAFICA IMAGENES
# 
fig.suptitle("PLACAS PARALELAS (Al) disco(TFL)=3mm", fontsize=14)
fig.add_subplot(111).set_xlabel('Tiempo [h]')
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



