#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------

#Global mathematical model of SAC-A with 31 nodes and according to design
# status of March 3, 1997. Equatorial Orbit without inclination in vernal
# equinox (beta=90), at 205 mn (380 km). Attitude: panels always deployed
# and directed towards the sun, satellite main axis perpendicular to the
# ecliptic plane.


#                                 HOT CASE WITH 23W (INTERNAL)

#----------------------------------------------------------------------------

from solver import Node, ThermalModel, FDMExplicit
#from matplotlib import pyplot
import datetime



inicio = datetime.datetime.now()		# Tiempo de Compilación

#HEADER CONTROL DATA


EMLI  = 0.01     # MLI effective emissivity
PINF  = 9.0      # Internal power dissipated at lower platform
PSUP  = 14.00    # Internal power dissipated at upper platform
F_AREA = 0.31    # Area correction for radiator


# Tiempo de Simulación
t_start = 0.0
t_end = 16579.8 #12000 #55266.0      






def power_mtr(time):     # Variación  de Potencia en MTR
    if time == 0.0:
        return 0.0
    elif time >= 100.0 and time <= 600.0:
        return 200.0
	#elif time >= 700.0 and time =< 899.0:
	#	return 0.0
    elif time >= 900.0 and time <= 1400.0:
        return 200.0
    else:
        return 0.0


model = ThermalModel()


#HEADER NODE DATA


              
           
model.addNode(Node(1, 14400.0, -273.0,  lambda x: PINF, 'Lower platform'))
model.addNode(Node(2, 22400.0, -273.0, lambda x: PSUP, 'Upper platform'))
model.addNode(Node(3, 1600.0, -273.0, lambda x: 6.00, 'Interface ring'))
model.addNode(Node(4, 400.0,-273.0, lambda x: 10.85, 'Front panel radiator'))
model.addNode(Node(5, 450.0,-273.0, lambda x: 51.74, 'Front solar panel'))
model.addNode(Node(6, 450.0,-273.0, lambda x: 6.81, 'Rear solar panel'))
model.addNode(Node(7, 450.0,-273.0, lambda x: 56.86, 'Lateral solar panel _1'))
model.addNode(Node(8, 450.0,-273.0, lambda x: 56.86, 'Lateral solar panel _2'))
model.addNode(Node(9, 150.0,-273.0, lambda x: 4.47, 'Silicon cell SiCELL_2'))
model.addNode(Node(10, 150.0,-273.0, lambda x: 4.47, 'Silicon cell SiCELL_1'))
model.addNode(Node(11, 200.0,-273.0, lambda x: 1.46, 'RF antena'))
model.addNode(Node(12, 300.0,-273.0, lambda x: 2.17, 'Upper microSwitch'))
model.addNode(Node(13, 300.0, -273.0, lambda x: 0.25, 'Lower microSwitch'))
model.addNode(Node(14, 3.0,-273.0, lambda x: 10.48, 'MLI-Upper platform'))
model.addNode(Node(15, 3.0,-273.0, lambda x: 3.72, 'MLI-lateral_2'))
model.addNode(Node(16, 3.0, -273.0, lambda x: 8.96, 'MLI-Lower platform'))
model.addNode(Node(17, 3.0,-273.0, lambda x: 3.01, 'Shunt_2'))
model.addNode(Node(18, 3.0,-273.0, lambda x: 3.01, 'Shunt_1'))
model.addNode(Node(19, 3.0,-273.0, lambda x: 3.72, 'MLI-lateral_1'))
model.addNode(Node(20, 100.0, -273.0, lambda x: 1.89, 'GPS_1 Antenna'))
model.addNode(Node(21, 100.0,-273.0, lambda x: 1.46, 'GPS_2 Antenna'))
model.addNode(Node(22, 100.0, -273.0, lambda x: 1.89, 'GPS_3 Antenna'))
model.addNode(Node(23, 100.0,-273.0, lambda x: 1.46, 'GPS_4 Antenna'))
model.addNode(Node(24, 250.0, -273.0, lambda x: 0.0, 'Structure - lateral_1'))
model.addNode(Node(25, 250.0, -273.0, lambda x: 0.0, 'Structure - rear'))
model.addNode(Node(26, 450.0,-273.0,  lambda x: 2.60*F_AREA, 'Radiator_2'))
model.addNode(Node(27, 450.0,-273.0,  lambda x: 2.60*F_AREA, 'Radiator_1'))
model.addNode(Node(28, 250.0, -273.0, lambda x: 0.0, 'Structure - lateral_2'))
model.addNode(Node(29, 3.0, -273.0, lambda x: 2.14, 'MLI - magnetometer'))
model.addNode(Node(30, 300.0, -273.0, lambda x: 0.0,'Magnetometer'))
model.addNode(Node(31, 1100.0,-273.0, lambda x: 0.0, 'Structure - front'))
model.addNode(Node(32, 3.0,-273.0, lambda x: 0.0, 'Mathematical node'))
model.addNode(Node(-99, 0.10, 0.0, lambda x: 0.0, 'Space'))



#HEADER CONDUCTOR DATA




# CONDUCTANCIAS

model.addConductance(1, 31, 1.10) 			# Lower_plat - Front_estr
model.addConductance(1, 24, 0.22) 			# Lower_plat - Latestr_1
model.addConductance(1, 28, 0.22)             # Lower_plat - Latestr_2
model.addConductance(1, 25, 0.22)             # Lower_plat - Rear_estr.
model.addConductance(1, 27, 0.44)             # Lower_plat - Radiator_1
model.addConductance(1, 26, 0.44)             # Lower_plat - Radiator_2
model.addConductance(2, 31, 1.10)             # Upper_plat - Front_estr
model.addConductance(2, 24, 0.22)             # Upper_plat - Latestr_1
model.addConductance(2, 28, 0.22)             # Upper_plat - Latestr_2
model.addConductance(2, 25, 0.22)             # Upper_plat - Rear_estr
model.addConductance(2, 27, 0.44)             # Upper_plat - Radiator_1
model.addConductance(2, 26, 0.44)             # Upper_plat - Radiator_2
model.addConductance(25, 26, 0.46)            # Rear_estr  - Radiator_2
model.addConductance(26, 28, 0.46)            # Radiator_2 - Latestr_2
model.addConductance(28, 31, 0.23)            # Latestr_2  - Front_estr
model.addConductance(31, 24, 0.23)            # Front_estr - Latestr_1
model.addConductance(24, 27, 0.46)            # Latestr_1  - Radiator_1
model.addConductance(27, 25, 0.46)            # Radiator_1 - Rear_estr
model.addConductance(31,  4, 0.25)            # Front_estr - Rad_panel
model.addConductance(31, 32, 0.07)            # Front_estr - Arith_node
model.addConductance(32, 5, 1.84)             # Arith_node - Panel_front
model.addConductance(4, 32, 2.10)             # Rad_panel  - Arith_node
model.addConductance(4, 10, 0.109)            # Rad_panel  - SiCELL_1
model.addConductance(4,  9, 0.10)             # Rad_panel  - SiCELL_2
model.addConductance(24, 7, 0.08)             # Latestr_1  - Panel_lat1
model.addConductance(28, 8, 0.08)             # Latestr_2  - Panel_lat2
model.addConductance(27, 6, 0.31)             # Radiator_1 - Panel_rear
model.addConductance(26, 6, 0.31)             # Radiator_2 - Panel_rear
model.addConductance(2,  6, 0.61)             # Upper_plat - Panel_rear
model.addConductance(1,  6, 0.61)             # Lower_plat - Panel_rear
model.addConductance(2, 20, 0.025)            # Upper_plat - DGPS_1
model.addConductance(2, 21, 0.025)            # Upper_plat - DGPS_2
model.addConductance(2, 22, 0.025)            # Upper_plat - DGPS_3
model.addConductance(2, 23, 0.025)            # Upper_plat - DGPS_4
model.addConductance(2, 11, 0.06)             # Upper_plat - RF_antenna
model.addConductance(2, 12, 0.06)             # Upper_plat - Up_switch
model.addConductance(2, 30, 0.06)             # Upper_plat - Magnetomet
model.addConductance(1,  3, 2.30)             # Lower_plat - Interf_ring
model.addConductance(1, 13, 0.10)             # Lower_plat - Low_switch

# ADMITANCIAS

model.addAdmittance(1, 16, 1200.*EMLI)                      # Lower_plat - Lower_MLI
model.addAdmittance(2, 14, 1500.*EMLI)                      # Upper_plat - Upper_MLI
model.addAdmittance(24, 19, 500.*EMLI)                      # Latestr_1  - MLI_Later1
model.addAdmittance(24, 18, 400.*EMLI)                      # Latestr_1  - Shunt_1
model.addAdmittance(28, 15, 500.*EMLI)                      # Latestr_2  - MLI_Later2
model.addAdmittance(28, 17, 400.*EMLI)                      # Latestr_2  - Shunt_2
model.addAdmittance(30, 29, 3000.*EMLI)                     # Magnetomet - Magn_MLI
model.addAdmittance(3, 16,  106.424)                        #  from SSPTA
model.addAdmittance(3, -99, 210.306)                        #  from SSPTA
model.addAdmittance(4,  7,    8.474)                        #  from SSPTA
model.addAdmittance(4,  8,    8.474)                        #  from SSPTA
model.addAdmittance(4, -99, 436.524)                        #  from SSPTA
model.addAdmittance(5, -99, 562.647)                        #  from SSPTA
model.addAdmittance(6, -99, 562.647)                        #  from SSPTA
model.addAdmittance(7, 10,    4.582)                        #  from SSPTA
model.addAdmittance(7, 18,   59.946)                        #  from SSPTA
model.addAdmittance(7, 19,   42.879)                        #  from SSPTA
model.addAdmittance(7, 20,    1.538)                        #  from SSPTA
model.addAdmittance(7, -99,1105.034)                        #  from SSPTA
model.addAdmittance(8,  9,    4.582)                        #  from SSPTA
model.addAdmittance(8, 15,   42.879)                        #  from SSPTA
model.addAdmittance(8, 17,   59.946)                        #  from SSPTA
model.addAdmittance(8, 22,    1.538)                        #  from SSPTA
model.addAdmittance(8, -99,1105.034)                        #  from SSPTA
model.addAdmittance(9, -99,  79.908)                        #  from SSPTA
model.addAdmittance(10,-99,  79.908)                        #  from SSPTA
model.addAdmittance(11, 12,   1.701)                        #  from SSPTA
model.addAdmittance(11, 14,  15.962)                        #  from SSPTA
model.addAdmittance(11, 20,   2.145)                        #  from SSPTA
model.addAdmittance(11, 21,   2.142)                        #  from SSPTA
model.addAdmittance(11, 22,   2.145)                        #  from SSPTA
model.addAdmittance(11, 23,   2.142)                        #  from SSPTA
model.addAdmittance(11, 29,   3.711)                        #  from SSPTA
model.addAdmittance(11, -99, 86.412)                        #  from SSPTA
model.addAdmittance(12, 14,   9.881)                        #  from SSPTA
model.addAdmittance(12, 21,   2.745)                        #  from SSPTA
model.addAdmittance(12, 23,   2.745)                        #  from SSPTA
model.addAdmittance(12, -99, 97.698)                        #  from SSPTA
model.addAdmittance(13, -99, 26.730)                        #  from SSPTA
model.addAdmittance(14, 20,  32.392)                        #  from SSPTA
model.addAdmittance(14, 21,  36.769)                        #  from SSPTA
model.addAdmittance(14, 22,  32.392)                        #  from SSPTA
model.addAdmittance(14, 23,  36.769)                        #  from SSPTA
model.addAdmittance(14, 29,  30.516)                        #  from SSPTA
model.addAdmittance(14, -99,688.541)                        #  from SSPTA
model.addAdmittance(15, 17,   1.128)                        #  from SSPTA
model.addAdmittance(15, -99,330.793)                        #  from SSPTA
model.addAdmittance(16, -99,828.833)                        #  from SSPTA
model.addAdmittance(17, -99,253.101)                        #  from SSPTA
model.addAdmittance(18, 19,   1.128)                        #  from SSPTA
model.addAdmittance(18, -99,253.101)                        #  from SSPTA
model.addAdmittance(19, -99,330.793)                        #  from SSPTA
model.addAdmittance(20, 22,   1.014)                        #  from SSPTA
model.addAdmittance(20, 23,   1.289)                        #  from SSPTA
model.addAdmittance(20, 29,   6.992)                        #  from SSPTA
model.addAdmittance(20, -99,178.462)                        #  from SSPTA
model.addAdmittance(21, 22,   1.289)                        #  from SSPTA
model.addAdmittance(21, 23,   1.014)                        #  from SSPTA
model.addAdmittance(21, 29,   1.113)                        #  from SSPTA
model.addAdmittance(21, -99,144.697)                        #  from SSPTA
model.addAdmittance(22, 29,   6.992)                        #  from SSPTA
model.addAdmittance(22, -99,178.462)                        #  from SSPTA
model.addAdmittance(23, 29,   1.113)                        #  from SSPTA
model.addAdmittance(23, -99,144.697)                        #  from SSPTA
model.addAdmittance(26, -99,191.484*F_AREA)                 #  from SSPTA
model.addAdmittance(27, -99,191.484*F_AREA)                 #  from SSPTA
model.addAdmittance(29, -99,160.929)                        #  from SSPTA

solver = FDMExplicit(model,0.1)	
Temp = solver.solve_stationary()
print("Temperaturas Estado Estacionario:")
print(Temp)

final = datetime.datetime.now()
Diferencia= final -inicio
print Diferencia.total_seconds()
