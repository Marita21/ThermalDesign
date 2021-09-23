#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from solver import Node, ThermalModel, FDMExplicit
from matplotlib.figure import Figure
import datetime

inicio = datetime.datetime.now()		# Tiempo de Compilación


# CONSTANTES

EMLI = 0.95     		# 
E1 = 1       	        # 
m_Al=0.56               # kg [V=0.25m*0.25m*0.003 y Densidad=2700Kg/m^2]
C_AL=880               # 880 J/kg*K                 
F=0.2

# Tiempo de Simulación

t_start = 0.0
t_end = 10000.0   # 

# VARIACION DE POTENCIA

def power_PHEATER(time):     # Variación  de Potencia en heater
    if time == 0.0:
        return 0.0
    elif time >= 1.0 and time <=150.0:
        return 100.0
    else:
        return 100.0
		
model = ThermalModel()



model.addNode(Node(1, 1.0*1.0, 4, lambda x: 100.0, 'P1'))

model.addNode(Node(2, 1.0*1.0, 4, lambda x: 0.0, 'P2'))

model.addNode(Node(-7, 1.0,    4, lambda x: 0.0, 'Espacio'))


#HEADER CONDUCTOR DATA

model.addAdmittance(1, 2, 2500*F)                #Placa 1
model.addAdmittance(1, -7, 2500.0*(1-F))          #Placa 2
model.addAdmittance(2, -7, 2500.0*(1-F))          #Espacio


solver = FDMExplicit(model,0.01)

#solver.solve(t_start, t_end)

Temp=solver.solve_stationary()
print("Temperaturas Estado Estacionario [°C]:")
print(Temp-273.15)



# Calculo del Tiempo  

final = datetime.datetime.now()

Diferencia = final - inicio

print("\n Tiempo de Cálculo:")
print (Diferencia.total_seconds())



