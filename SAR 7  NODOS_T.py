#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from solver import Node, ThermalModel, FDMExplicit
from matplotlib.figure import Figure
import datetime

inicio = datetime.datetime.now()		# Tiempo de Compilación


# CONSTANTES

EMLI = 0.05     		# Emisividad efectiva MLI
FA_RAD_PL = 1.0       	# Factor de area afectiva del radiador de la plataforma
POT_PLAT = 2000.0		# Pot interna de la plataforma (W)
POT_CTR = 37.0       	# Pot disipada sobre CTR (W)
POT_MTR = 1.0       	# Pot disipada sobre MTR (W)
POT_TIERRA = 900.0    	# Pot incidente sobre cada Panel
T=273.15

# Tiempo de Simulación

t_start = 0.0
t_end = 1200.0   # 1 horas

# VARIACION DE POTENCIA

def power_mtr(time):     # Variación  de Potencia en MTR
    if time == 0.0:
        return 0.0
    elif time >= 100.0 and time <=600.0:
        return 200.0
    elif time >=600.0 and time <= 1000.0:
        return 0.0
    elif time >= 8200.0 and time <= 1000.0:
        return 100.0
    else:
        return 0.0
		
model = ThermalModel()

model.addNode(Node(1, 1700.*879., 32.851+T, lambda x: POT_PLAT, 'Plataforma'))

model.addNode(Node(2, 1280.*400., 28.59+T, lambda x: 0.0, 'Panel X4'))
model.addNode(Node(3, 42.*879., 28.92+T, lambda x: POT_CTR, 'Estructura CTR'))
model.addNode(Node(4, 17.*879., 28.92+T, power_mtr, 'MTR'))	#VARIACION DE POTENCIA

model.addNode(Node(5, 2.5*250., -77.10+T, lambda x: 0.0, 'MLI'))
model.addNode(Node(6, 17.86*879., 42.87+T, lambda x: POT_TIERRA, 'Modulos Radiantes'))
model.addNode(Node(-7, 1.0, 0.0, lambda x: 0.0, 'Espacio'))

#HEADER CONDUCTOR DATA

# CONDUCTANCIAS

model.addConductance(1, 2, 5.0) 			# 'Plataforma - Panel X4' 

model.addConductance(2, 3, 61.2) 			#'Panel X4 - CTR_4'
model.addConductance(3, 4, 117.0) 			#CTR _MTR

# ADMITANCIAS

model.addConductance(1, 2, 2.0)                 #Plataforma - Panel X4
model.addConductance(2, 3, 61.2)                #Panel X4 - Estructura CTR
model.addConductance(3, 4, 117.0)               #Estructura CTR - MTR

model.addAdmittance(1, -7, 40000.0*FA_RAD_PL)   #Plataforma - Espacio
model.addAdmittance(1, 2, 1080.0)               #Plataforma - Panel X4
model.addAdmittance(2, -7, 7650.0)              #Panel X4 - Espacio
model.addAdmittance(2, 5, 49500.0*EMLI)         #Panel X4 - MLI
model.addAdmittance(4, -7, 377.0)               #MTR - espacio
model.addAdmittance(2, 6, 44550.0)              #Panel X4 - modulo Radiante
model.addAdmittance(6, -7, 7650.0)              #Modulo Radiante - Espacio

solver = FDMExplicit(model,0.1)
solver.solve(t_start, t_end)	



#------------------------------CREAR VENTANA---------------------------------
root = tkinter.Tk()
root.wm_title("Outgassing - PROTOTIPO")


#------------------------------CREAR GRAFICA---------------------------------
fig = Figure(figsize=(5, 5), dpi=100)



#fig.add_subplot(111).plot((solver.t)/3600,solver.T[0]-273, linestyle='--', color='cyan', label="SP")
fig.add_subplot(111).plot((solver.t)/3600,solver.T[1]-273, linestyle='--', color='blue', label="Panel X4")
fig.add_subplot(111).plot((solver.t)/3600,solver.T[2]-273, linestyle='-', color='green', label="Estructura CTR")
fig.add_subplot(111).plot((solver.t)/3600,solver.T[3]-273, linestyle='-', color='red', label="MTR")

#fig.add_subplot(111).plot((solver.t)/3600,solver.T[4]-273, linestyle='--', color='blue', label="MLI")
#fig.add_subplot(111).plot((solver.t)/3600,solver.T[5]-273, linestyle='-', color='green', label="Modulos Radiantes")
#fig.add_subplot(111).plot((solver.t)/3600,solver.T[6]-273, linestyle='-', color='red', label="Espacio")

#fig.add_subplot(111).plot((solver.t)/3600,solver.T[7]-273, linestyle='--', color='blue', label="Panel X5")


# 
# #GRAFICA IMAGENES
# 
fig.suptitle("MODELO 16 NODOS", fontsize=14)
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

#*******************************************************************************
# Calculo del Tiempo  

final = datetime.datetime.now()

Diferencia = final - inicio
print(" ")
print("Tiempo de Procesamiento:")
print Diferencia.total_seconds()


