#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from solver import Node, ThermalModel, FDMExplicit
#from matplotlib import pyplot
import datetime

inicio = datetime.datetime.now()		# Tiempo de Compilación


# CONSTANTES

EMLI = 0.05     		# Emisividad efectiva MLI
FA_RAD_PL = 1.0       	# Factor de area afectiva del radiador de la plataforma
POT_PLAT = 2000.0		# Pot interna de la plataforma (W)
POT_CTR = 37.0       	# Pot disipada sobre CTR (W)
POT_MTR = 1.0       	# Pot disipada sobre MTR (W)
POT_TIERRA = 900.0    	# Pot incidente sobre cada Panel
T0=-273.15


		
model = ThermalModel()

model.addNode(Node(1, 1.0*1.0, T0, lambda x: POT_PLAT, 'Plataforma'))

model.addNode(Node(2, 1.0*1.0, T0, lambda x: 0.0, 'Panel X4'))
model.addNode(Node(3, 1.0*1.0, T0, lambda x: POT_CTR, 'Estructura CTR'))
model.addNode(Node(4, 1.0*1.0, T0, lambda x: POT_MTR, 'MTR'))	#VARIACION DE POTENCIA

model.addNode(Node(5, 1.0*1.0, T0, lambda x: 0.0, 'MLI'))
model.addNode(Node(6, 1.0*1.0, T0, lambda x: POT_TIERRA, 'Modulos Radiantes'))
model.addNode(Node(-7, 1.0,    0.0, lambda x: 0.0, 'Espacio'))

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

solver = FDMExplicit(model,0.01)

Temp=solver.solve_stationary()
print("Temperaturas Estado Estacionario:\n")
print(Temp-273)

# Calculo del Tiempo  

final = datetime.datetime.now()

Diferencia = final - inicio

#print("\n Tiempo de Cálculo:")
#print Diferencia.total_seconds()





