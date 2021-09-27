#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------

#Global mathematical model of SAC-A with 31 nodes and according to design
# status of March 3, 1997. Orbit of 51.6 degrees of inclination in winter
# solstice (beta=15), at 205 mn (380 km). Attitude: panels always deployed
# and directed towards the sun, satellite main axis perpendicular to the
# ecliptic plane.

#                                NOMINAL HOT CASE WITH 23W (INTERNAL)

#----------------------------------------------------------------------------

from solver import Node, ThermalModel, FDMExplicit
#from matplotlib import pyplot
import datetime



inicio = datetime.datetime.now()		# Tiempo de Compilación

#HEADER CONTROL DATA


EMLI  = 0.03     # MLI effective emissivity
PINF  = 7.0      # Internal power dissipated at lower platform
PSUP  = 12.00    # Internal power dissipated at upper platform
F_AREA = 0.31    # Area correction for radiator



model = ThermalModel()


#HEADER NODE DATA


     
              
           
model.addNode(Node(1, 14400.0, 297.98277018,  lambda x:PINF, 'Lower platform'))
model.addNode(Node(2, 22400.0, 298.24525503, lambda x: PSUP, 'Upper platform'))
model.addNode(Node(3, 1600.0, 296.06883956,  lambda x: 4.73, 'Interface ring'))
model.addNode(Node(4, 400.0,329.76981036, lambda x: 6.45, 'Front panel radiator'))
model.addNode(Node(5, 450.0,352.92355844, lambda x: 39.43, 'Front solar panel'))
model.addNode(Node(6, 450.0,287.98149354, lambda x: 7.51, 'Rear solar panel'))
model.addNode(Node(7, 450.0,326.16023767, lambda x: 44.97, 'Lateral solar panel _1'))
model.addNode(Node(8, 450.0,326.16113637, lambda x: 44.97, 'Lateral solar panel _2'))
model.addNode(Node(9, 150.0,334.52013919, lambda x: 2.79, 'Silicon cell SiCELL_2'))
model.addNode(Node(10, 150.0,334.28346766,lambda x: 2.79, 'Silicon cell SiCELL_1'))
model.addNode(Node(11, 200.0,272.24511844, lambda x: 1.04, 'RF antena'))
model.addNode(Node(12, 300.0,278.89073804, lambda x: 1.53, 'Upper microSwitch'))
model.addNode(Node(13, 300.0, 289.79374615, lambda x: 0.25, 'Lower microSwitch'))
model.addNode(Node(14, 3.0,230.57181926, lambda x: 6.55, 'MLI-Upper platform'))
model.addNode(Node(15, 3.0,231.29593541, lambda x: 3.02, 'MLI-lateral_2'))
model.addNode(Node(16, 3.0, 230.27827859, lambda x: 7.84, 'MLI-Lower platform'))
model.addNode(Node(17, 3.0,246.37801687, lambda x: 2.23, 'Shunt_2'))
model.addNode(Node(18, 3.0,246.37762173, lambda x: 2.23, 'Shunt_1'))
model.addNode(Node(19, 3.0,231.29564763, lambda x: 3.02, 'MLI-lateral_1'))
model.addNode(Node(20, 100.0, 238.06403638, lambda x: 1.49, 'GPS_1 Antenna'))
model.addNode(Node(21, 100.0,240.55841625, lambda x: 1.05, 'GPS_2 Antenna'))
model.addNode(Node(22, 100.0, 238.06404797, lambda x: 1.50, 'GPS_3 Antenna'))
model.addNode(Node(23, 100.0,240.5584162, lambda x: 1.05, 'GPS_4 Antenna'))
model.addNode(Node(24, 250.0, 299.55312394, lambda x: 0.0, 'Structure - lateral_1'))
model.addNode(Node(25, 250.0, 296.43180947, lambda x: 0.0, 'Structure - rear'))
model.addNode(Node(26, 450.0,295.62728453,  lambda x: 2.68*F_AREA, 'Radiator_2'))
model.addNode(Node(27, 450.0,295.62727054, lambda x: 2.68*F_AREA, 'Radiator_1'))
model.addNode(Node(28, 250.0, 299.55318916, lambda x: 0.0, 'Structure - lateral_2'))
model.addNode(Node(29, 3.0, 231.75567726, lambda x: 1.73, 'MLI - magnetometer'))
model.addNode(Node(30, 300.0, 287.14924544, lambda x: 0.0,'Magnetometer'))
model.addNode(Node(31, 1100.0,301.97360573, lambda x: 0.0, 'Structure - front'))
model.addNode(Node(32, 3.0,339.90875354, lambda x: 0.0, 'Mathematical node'))
model.addNode(Node(-99, 0.10, 0.0, lambda x: 0.0, 'Space'))



#HEADER CONDUCTOR DATA



# CONDUCTANCIAS

model.addConductance(1, 31, 1.10) 							# Lower_plat - Front_estr
model.addConductance(1, 24, 0.22) 							# Lower_plat - Latestr_1
model.addConductance(1, 28, 0.22)                           # Lower_plat - Latestr_2
model.addConductance(1, 25, 0.22)                           # Lower_plat - Rear_estr.
model.addConductance(1, 27, 0.44)                           # Lower_plat - Radiator_1
model.addConductance(1, 26, 0.44)                           # Lower_plat - Radiator_2
model.addConductance(2, 31, 1.10)                           # Upper_plat - Front_estr
model.addConductance(2, 24, 0.22)                           # Upper_plat - Latestr_1
model.addConductance(2, 28, 0.22)                           # Upper_plat - Latestr_2
model.addConductance(2, 25, 0.22)                           # Upper_plat - Rear_estr
model.addConductance(2, 27, 0.44)                           # Upper_plat - Radiator_1
model.addConductance(2, 26, 0.44)                           # Upper_plat - Radiator_2
model.addConductance(25, 26, 0.46)                          # Rear_estr  - Radiator_2
model.addConductance(26, 28, 0.46)                          # Radiator_2 - Latestr_2
model.addConductance(28, 31, 0.23)                          # Latestr_2  - Front_estr
model.addConductance(31, 24, 0.23)                          # Front_estr - Latestr_1
model.addConductance(24, 27, 0.46)                          # Latestr_1  - Radiator_1
model.addConductance(27, 25, 0.46)                          # Radiator_1 - Rear_estr
model.addConductance(31,  4, 0.25)                          # Front_estr - Rad_panel
model.addConductance(31, 32, 0.07)                          # Front_estr - Arith_node
model.addConductance(32, 5, 1.84)                           # Arith_node - Panel_front
model.addConductance(4, 32, 2.10)                           # Rad_panel  - Arith_node
model.addConductance(4, 10, 0.109)                          # Rad_panel  - SiCELL_1
model.addConductance(4,  9, 0.10)                           # Rad_panel  - SiCELL_2
model.addConductance(24, 7, 0.08)                           # Latestr_1  - Panel_lat1
model.addConductance(28, 8, 0.08)                           # Latestr_2  - Panel_lat2
model.addConductance(27, 6, 0.31)                           # Radiator_1 - Panel_rear
model.addConductance(26, 6, 0.31)                           # Radiator_2 - Panel_rear
model.addConductance(2,  6, 0.61)                           # Upper_plat - Panel_rear
model.addConductance(1,  6, 0.61)                           # Lower_plat - Panel_rear
model.addConductance(2, 20, 0.025)                          # Upper_plat - DGPS_1
model.addConductance(2, 21, 0.025)                          # Upper_plat - DGPS_2
model.addConductance(2, 22, 0.025)                          # Upper_plat - DGPS_3
model.addConductance(2, 23, 0.025)                          # Upper_plat - DGPS_4
model.addConductance(2, 11, 0.06)                           # Upper_plat - RF_antenna
model.addConductance(2, 12, 0.06)                           # Upper_plat - Up_switch
model.addConductance(2, 30, 0.06)                           # Upper_plat - Magnetomet
model.addConductance(1,  3, 2.30)                           # Lower_plat - Interf_ring
model.addConductance(1, 13, 0.10)                           # Lower_plat - Low_switch

# ADMITANCIAS

model.addAdmittance(1, 16, 1200.*EMLI)                      # Lower_plat - Lower_MLI
model.addAdmittance(2, 14, 1500.*EMLI)                      # Upper_plat - Upper_MLI
model.addAdmittance(24, 19, 500.*EMLI)                      # Latestr_1  - MLI_Later1
model.addAdmittance(24, 18, 400.*EMLI)                      # Latestr_1  - Shunt_1
model.addAdmittance(28, 15, 500.*EMLI)                      # Latestr_2  - MLI_Later2
model.addAdmittance(28, 17, 400.*EMLI)                      # Latestr_2  - Shunt_2
model.addAdmittance(30, 29, 3000.*EMLI)                     # Magnetomet - Magn_MLI
model.addAdmittance(3, 16,  136.178)                        #  from SSPTA
model.addAdmittance(3, -99, 257.228)                        #  from SSPTA
model.addAdmittance(4,  7,    9.625)                        #  from SSPTA
model.addAdmittance(4,  8,    9.625)                        #  from SSPTA
model.addAdmittance(4, -99, 472.481)                        #  from SSPTA
model.addAdmittance(5, -99, 589.440)                        #  from SSPTA
model.addAdmittance(6, -99, 589.440)                        #  from SSPTA
model.addAdmittance(7, 10,    5.190)                        #  from SSPTA
model.addAdmittance(7, 18,   66.225)                        #  from SSPTA
model.addAdmittance(7, 19,   48.031)                        #  from SSPTA
model.addAdmittance(7, 20,    1.705)                        #  from SSPTA
model.addAdmittance(7, -99,1163.069)                        #  from SSPTA
model.addAdmittance(8,  9,    5.190)                        #  from SSPTA
model.addAdmittance(8, 15,   48.031)                        #  from SSPTA
model.addAdmittance(8, 17,   66.225)                        #  from SSPTA
model.addAdmittance(8, 22,    1.705)                        #  from SSPTA
model.addAdmittance(8, -99,1163.069)                        #  from SSPTA
model.addAdmittance(9, -99,  86.153)                        #  from SSPTA
model.addAdmittance(10,-99,  86.153)                        #  from SSPTA
model.addAdmittance(11, 12,   1.983)                        #  from SSPTA
model.addAdmittance(11, 14,  18.462)                        #  from SSPTA
model.addAdmittance(11, 20,   2.479)                        #  from SSPTA
model.addAdmittance(11, 21,   2.476)                        #  from SSPTA
model.addAdmittance(11, 22,   2.479)                        #  from SSPTA
model.addAdmittance(11, 23,   2.476)                        #  from SSPTA
model.addAdmittance(11, 29,   4.317)                        #  from SSPTA
model.addAdmittance(11, -99, 95.537)                        #  from SSPTA
model.addAdmittance(12, 14,  10.766)                        #  from SSPTA
model.addAdmittance(12, 21,   2.985)                        #  from SSPTA
model.addAdmittance(12, 23,   2.985)                        #  from SSPTA
model.addAdmittance(12, -99,102.067)                        #  from SSPTA
model.addAdmittance(13, -99, 26.730)                        #  from SSPTA
model.addAdmittance(14, 20,  35.214)                        #  from SSPTA
model.addAdmittance(14, 21,  39.916)                        #  from SSPTA
model.addAdmittance(14, 22,  35.214)                        #  from SSPTA
model.addAdmittance(14, 23,  39.916)                        #  from SSPTA
model.addAdmittance(14, 29,  33.234)                        #  from SSPTA
model.addAdmittance(14, -99,713.037)                        #  from SSPTA
model.addAdmittance(15, 17,   0.964)                        #  from SSPTA
model.addAdmittance(15, -99,345.665)                        #  from SSPTA
model.addAdmittance(16, -99,858.911)                        #  from SSPTA
model.addAdmittance(17, -99,259.298)                        #  from SSPTA
model.addAdmittance(18, 19,   0.964)                        #  from SSPTA
model.addAdmittance(18, -99,259.298)                        #  from SSPTA
model.addAdmittance(19, -99,345.665)                        #  from SSPTA
model.addAdmittance(20, 22,   1.079)                        #  from SSPTA
model.addAdmittance(20, 23,   1.289)                        #  from SSPTA
model.addAdmittance(20, 29,   7.535)                        #  from SSPTA
model.addAdmittance(20, -99,184.751)                        #  from SSPTA
model.addAdmittance(21, 22,   1.378)                        #  from SSPTA
model.addAdmittance(21, 23,   1.079)                        #  from SSPTA
model.addAdmittance(21, 29,   1.210)                        #  from SSPTA
model.addAdmittance(21, -99,149.509)                        #  from SSPTA
model.addAdmittance(22, 29,   7.535)                        #  from SSPTA
model.addAdmittance(22, -99,184.751)                        #  from SSPTA
model.addAdmittance(23, 29,   1.210)                        #  from SSPTA
model.addAdmittance(23, -99,149.509)                        #  from SSPTA
model.addAdmittance(26, -99,201.741*F_AREA)                 #  from SSPTA
model.addAdmittance(27, -99,201.741*F_AREA)                 #  from SSPTA
model.addAdmittance(29, -99,167.194)                        #  from SSPTA

solver = FDMExplicit(model,0.1)	
Temp = solver.solve_stationary()
print("Temperaturas Estado Estacionario:")
print(Temp-273.15)

final = datetime.datetime.now()
Diferencia= final -inicio
print Diferencia.total_seconds()
