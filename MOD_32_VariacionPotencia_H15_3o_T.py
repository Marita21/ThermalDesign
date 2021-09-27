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
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from solver import Node, ThermalModel, FDMExplicit
from matplotlib.figure import Figure
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


# Tiempos en los que cambia las potencias

power_times1 = [ 0.0, 16580.0, 16580.0, 17300.0, 17300.0, 55266.0,] 
                

power_Low= [1.0, 1.0,  1.0,  1.0,  1.0, 1.0,]
            

power_Upp= [1.0, 1.0,  4.429,  4.429,  1.0, 1.0,]
            

for index in range(len(power_Low)):
   power_Low[index] = power_Low[index]*PINF
   

for index in range(len(power_Upp)):
    power_Upp[index]=power_Upp[index]*PSUP
    
    
def generate_power_function(time, power):
    from bisect import bisect
    power_array = power
    power_times1 = time

    def get_power_X(time):
        return power_array[bisect(power_times1, time)-1]
    return get_power_X

power_L= generate_power_function(power_times1, power_Low)
    
power_U = generate_power_function(power_times1, power_Upp)

    

power_times = [    0.0,  230.4,  460.8,  690.6,  921.0,
                1151.4, 1381.8, 1611.6, 1842.0, 2072.4,
                2302.8, 2532.6, 2763.0, 2993.4, 3223.8,
                3454.2, 3684.0, 3914.4, 4144.8, 4375.2,
                4605.0, 4835.0, 5065.8, 5296.2, 5526.6,   
                5526.6, 5757.0, 5987.4, 6217.2, 6447.6,  # 2da orbita
                6678.0, 6908.4, 7138.2, 7368.6, 7599.0, 
                7829.4, 8059.2, 8289.6, 8520.0, 8750.4, 
                8980.8, 9210.6, 9441.0, 9671.4, 9901.8, 
               10131.6,10361.6,10592.4,10822.8,11053.2,
               11053.2,11283.6,11514.0,11743.8,11974.2,  # 3ra orbita
               12204.6,12435.0,12664.8,12895.2,13125.6,
               13356.0,13585.8,13816.2,14046.6,14277.0, 
               14507.4,14737.2,14967.6,15198.0,15428.4, 
               15658.2,15888.2,16119.0,16349.4,16579.8,] 


power_node_103 = [ 7.64,  7.30,  6.92,  6.52,  6.17,
                   5.96,  5.89,  5.96,  6.17,  6.52,
                   6.92,  7.30,  7.64,  8.03,  8.46,
                   8.88,  9.25,  9.51,  9.60,  9.51,
                   9.25,  8.88,  8.46,  8.03,  7.64,]

power_node_103 = power_node_103*3



power_node_104 = [14.16, 13.95, 13.68, 13.41, 13.17,
                  13.02, 12.97, 13.02, 13.17, 13.41,
                  13.68, 13.95, 14.16, 14.34, 14.49,
                  14.60, 14.69, 14.75, 14.77, 14.75,
                  14.69, 14.60, 14.48, 14.34, 14.16,]

power_node_104 = power_node_104*3
                  
power_node_105 = [73.27, 73.22, 73.11, 72.96, 72.81,
                  72.70, 72.67, 72.70, 72.81, 72.96,
                  73.11, 73.22, 73.27, 73.36, 73.64,
                  73.96, 74.25, 74.43, 74.49, 74.43,
                  74.25, 73.96, 73.64, 73.36, 73.27,]

power_node_105 = power_node_105*3

                   
power_node_106 = [ 4.31,  4.87,  5.69,  6.55,  7.29,
                   7.78,  7.95,  7.78,  7.28,  6.54,
                   5.69,  4.87,  4.31,  3.88,  3.49,
                   3.17,  2.93,  2.78,  2.73,  2.78,
                   2.93,  3.17,  3.50,  3.88,  4.31,]
                   
power_node_106 = power_node_106*3

power_node_107 = [74.76, 75.19, 75.83, 76.65, 77.60,
                  78.59, 79.50, 80.20, 80.57, 80.55,
                  80.19, 79.62, 79.05, 78.59, 78.35,
                  78.19, 78.01, 77.73, 77.34, 76.82,
                  76.21, 75.54, 74.96, 74.64, 74.76,]
                  
power_node_107 = power_node_107*3

power_node_108 = [79.05, 79.63, 80.20, 80.55, 80.57,
                  80.20, 79.50, 78.58, 77.60, 76.65,
                  75.83, 75.18, 74.76, 74.64, 74.96,
                  75.54, 76.21, 76.82, 77.34, 77.73,
                  78.01, 78.19, 78.35, 78.59, 79.05,]
                  
power_node_108 = power_node_108*3

power_node_109 = [ 6.82,  6.81,  6.73,  6.60,  6.42,
                   6.23,  6.04,  5.87,  5.74,  5.64,
                   5.58,  5.56,  5.57,  5.60,  5.68,
                   5.79,  5.94,  6.10,  6.27,  6.43,
                   6.58,  6.69,  6.76,  6.80,  6.82,]
                   
power_node_109 = power_node_109*3

power_node_110 = [ 5.57,  5.56,  5.58,  5.64,  5.74,
                   5.87,  6.04,  6.23,  6.42,  6.60,
                   6.73,  6.81,  6.82,  6.80,  6.76,
                   6.69,  6.58,  6.43,  6.27,  6.10,
                   5.94,  5.79,  5.68,  5.60,  5.57,]
                   
power_node_110 = power_node_110*3
#
power_node_111= [ 1.58,  1.71,  1.83,  1.91,  1.95,
                  1.96,  1.96,  1.96,  1.95,  1.91,
                  1.83,  1.71,  1.58,  1.46,  1.34,
                  1.20,  1.06,  0.95,  0.90,  0.95,
                  1.06,  1.20,  1.34,  1.46,  1.58,]
                  
power_node_111 = power_node_111*3
#
power_node_112= [2.47,  2.61,  2.75,  2.85,  2.92,
                 2.96,  2.98,  2.96,  2.92,  2.85,
                 2.75,  2.61,  2.47,  2.34,  2.21,
                 2.10,  1.99,  1.91,  1.88,  1.91,
                 1.99,  2.10,  2.21,  2.34,  2.47,]
                 
power_node_112 = power_node_112*3
                 
power_node_113=  [0.21,  0.15,  0.09,  0.04,  0.01,
                  0.00,  0.00,  0.00,  0.01,  0.04,
                  0.09,  0.15,  0.21,  0.29,  0.37,
                  0.45,  0.52,  0.58,  0.60,  0.58,
                  0.52,  0.45,  0.37,  0.29,  0.21, ]
                  
power_node_113 = power_node_113*3
#
power_node_114=  [ 7.43, 10.01, 13.15, 16.40, 19.29,
                  21.34, 22.10, 21.33, 19.29, 16.40,
                  13.15, 10.00,  7.43,  5.56,  4.16,
                   3.18,  2.63,  2.39,  2.32,  2.39,
                   2.63,  3.18,  4.16,  5.56,  7.43,]
                   
power_node_114 = power_node_114*3
#
power_node_115=  [ 7.43, 10.01, 13.15, 16.40, 19.29,
                  21.34, 22.10, 21.33, 19.29, 16.40,
                  13.15, 10.00,  7.43,  5.56,  4.16,
                   3.18,  2.63,  2.39,  2.32,  2.39,
                   2.63,  3.18,  4.16,  5.56,  7.43,]
                   
power_node_115 = power_node_115*3
#
power_node_116=  [ 8.64,  6.56,  4.74,  3.36,  2.55,
                   2.27,  2.24,  2.27,  2.55,  3.36,
                   4.74,  6.56,  8.64, 11.08, 13.72,
                  16.27, 18.47, 20.02, 20.60, 20.02,
                  18.47, 16.27, 13.72, 11.08,  8.64,]
                  
power_node_116 = power_node_116*3
#
power_node_117=  [ 5.76,  5.95,  5.85,  5.47,  4.82,
                   3.94,  2.94,  1.95,  1.09,  0.47,
                   0.14,  0.07,  0.05,  0.05,  0.08,
                   0.27,  0.63,  1.12,  1.74,  2.48,
                   3.27,  4.07,  4.82,  5.43,  5.76,]
                   
power_node_117 = power_node_117*3
#
power_node_118=  [ 0.05,  0.07,  0.14,  0.47,  1.10,
                   1.95,  2.94,  3.94,  4.82,  5.47,
                   5.85,  5.95,  5.76,  5.43,  4.82,
                   4.07,  3.27,  2.48,  1.74,  1.12,
                   0.63,  0.27,  0.08,  0.05,  0.05,]
                   
power_node_118 = power_node_118*3
#
power_node_119=  [ 0.04,  0.05,  0.13,  0.51,  1.23,
                   2.27,  3.51,  4.81,  5.92,  6.73,
                   7.17,  7.22,  6.93,  6.55,  5.86,
                   4.98,  4.01,  3.06,  2.17,  1.40,
                   0.77,  0.33,  0.08,  0.03,  0.04,]
                   
power_node_119 = power_node_119*3
#
power_node_120=  [ 1.13,  1.55,  2.03,  2.54,  3.02,
                   3.40,  3.60,  3.60,  3.45,  3.15,
                   2.74,  2.29,  1.87,  1.50,  1.16,
                   0.87,  0.62,  0.43,  0.29,  0.21,
                   0.23,  0.36,  0.55,  0.80,  1.13,]
                   
power_node_120 = power_node_120*3
#
power_node_121=  [1.27,  1.68,  2.15,  2.60,  2.94,
                  3.13,  3.17,  3.02,  2.66,  2.22,
                  1.74,  1.29,  0.89,  0.59,  0.37,
                  0.20,  0.07,  0.04,  0.07,  0.12,
                  0.22,  0.39,  0.63,  0.93,  1.27,]
                  
power_node_121 = power_node_121*3
#
power_node_122=  [ 1.87,  2.30,  2.75,  3.15,  3.45,
                   3.60,  3.60,  3.40,  3.02,  2.54,
                   2.03,  1.55,  1.13,  0.80,  0.55,
                   0.36,  0.23,  0.21,  0.29,  0.43,
                   0.62,  0.87,  1.16,  1.50,  1.87,]
                   
power_node_122 = power_node_122*3
#
power_node_123=  [ 0.89,  1.29,  1.74,  2.22,  2.66,
                   3.02,  3.17,  3.13,  2.94,  2.60,
                   2.15,  1.68,  1.27,  0.93,  0.63,
                   0.39,  0.22,  0.12,  0.07,  0.04,
                   0.07,  0.20,  0.37,  0.59,  0.89,]
                   
power_node_123 = power_node_123*3
#
power_node_126=  [ 3.33,  3.67,  3.97,  4.04,  3.83,
                   3.37,  2.74,  2.05,  1.40,  0.86,
                   0.49,  0.28,  0.18,  0.16,  0.19,
                   0.29,  0.47,  0.74,  1.08,  1.48,
                   1.91,  2.35,  2.75,  3.08,  3.33,]
                   
power_node_126 = power_node_126*3
                   
for index in range(len(power_node_126)):
   power_node_126[index] = power_node_126[index]*F_AREA
#
power_node_127=  [ 0.18,  0.28,  0.49,  0.86,  1.40,
                   2.05,  2.74,  3.37,  3.83,  4.04,
                   3.97,  3.67,  3.33,  3.08,  2.75,
                   2.35,  1.91,  1.48,  1.08,  0.74,
                   0.47,  0.29,  0.19,  0.16,  0.18,]
                   
power_node_127 = power_node_127*3

for index in range(len(power_node_127)):
   power_node_127[index] = power_node_127[index]*F_AREA
#
power_node_129=  [ 1.86,  2.14,  2.42,  2.67,  2.87,
                   2.99,  3.04,  2.99,  2.87,  2.67,
                   2.42,  2.14,  1.86,  1.61,  1.38,
                   1.15,  0.93,  0.78,  0.73,  0.78,
                   0.93,  1.15,  1.38,  1.61,  1.86,]
                   
power_node_129 = power_node_129*3

    

def generate_power_function(time, power):
    from bisect import bisect
    power_array = power
    power_times = time

    def get_power_X(time):
        return power_array[bisect(power_times, time)-1]
    return get_power_X

power_103 = generate_power_function(power_times, power_node_103)
power_104 = generate_power_function(power_times, power_node_104)
power_105 = generate_power_function(power_times, power_node_105)
power_106 = generate_power_function(power_times, power_node_106)
power_107 = generate_power_function(power_times, power_node_107)
power_108 = generate_power_function(power_times, power_node_108)
power_109 = generate_power_function(power_times, power_node_109)
power_110 = generate_power_function(power_times, power_node_110)
power_111 = generate_power_function(power_times, power_node_111)
power_112 = generate_power_function(power_times, power_node_112)
power_113 = generate_power_function(power_times, power_node_113)
power_114 = generate_power_function(power_times, power_node_114)
power_115 = generate_power_function(power_times, power_node_115)
power_116 = generate_power_function(power_times, power_node_116)
power_117 = generate_power_function(power_times, power_node_117)
power_118 = generate_power_function(power_times, power_node_118)
power_119 = generate_power_function(power_times, power_node_119)
power_120 = generate_power_function(power_times, power_node_120)
power_121 = generate_power_function(power_times, power_node_121)
power_122 = generate_power_function(power_times, power_node_122)
power_123 = generate_power_function(power_times, power_node_123)
power_126 = generate_power_function(power_times, power_node_126)
power_127 = generate_power_function(power_times, power_node_127)
power_129 = generate_power_function(power_times, power_node_129)




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

  
              
           
model.addNode(Node(1, 14400.0, 297.98277018,  power_L, 'Lower platform'))
model.addNode(Node(2, 22400.0, 298.24525503, power_U, 'Upper platform'))
model.addNode(Node(3, 1600.0, 296.06883956,  power_103, 'Interface ring'))
model.addNode(Node(4, 400.0,329.76981036, power_104, 'Front panel radiator'))
model.addNode(Node(5, 450.0,352.92355844, power_105, 'Front solar panel'))
model.addNode(Node(6, 450.0,287.98149354, power_106, 'Rear solar panel'))
model.addNode(Node(7, 450.0,326.16023767, power_107, 'Lateral solar panel _1'))
model.addNode(Node(8, 450.0,326.16113637, power_108, 'Lateral solar panel _2'))
model.addNode(Node(9, 150.0,334.52013919, power_109, 'Silicon cell SiCELL_2'))
model.addNode(Node(10, 150.0,334.28346766, power_110, 'Silicon cell SiCELL_1'))
model.addNode(Node(11, 200.0,272.24511844, power_111, 'RF antena'))
model.addNode(Node(12, 300.0,278.89073804, power_112, 'Upper microSwitch'))
model.addNode(Node(13, 300.0, 289.79374615, power_113, 'Lower microSwitch'))
model.addNode(Node(14, 0.1,230.57181926, power_114, 'MLI-Upper platform'))
model.addNode(Node(15, 0.1,231.29593541, power_115, 'MLI-lateral_2'))
model.addNode(Node(16, 0.1, 230.27827859, power_116, 'MLI-Lower platform'))
model.addNode(Node(17, 0.1,246.37801687,power_117, 'Shunt_2'))
model.addNode(Node(18, 0.1,246.37762173, power_118, 'Shunt_1'))
model.addNode(Node(19, 0.1,231.29564763, power_119, 'MLI-lateral_1'))
model.addNode(Node(20, 100.0, 238.06403638, power_120, 'GPS_1 Antenna'))
model.addNode(Node(21, 100.0,240.55841625, power_121, 'GPS_2 Antenna'))
model.addNode(Node(22, 100.0, 238.06404797, power_122, 'GPS_3 Antenna'))
model.addNode(Node(23, 100.0,240.5584162, power_123, 'GPS_4 Antenna'))
model.addNode(Node(24, 250.0, 299.55312394, lambda x: 0.0, 'Structure - lateral_1'))
model.addNode(Node(25, 250.0, 296.43180947, lambda x: 0.0, 'Structure - rear'))
model.addNode(Node(26, 450.0,295.62728453,  power_126, 'Radiator_2'))
model.addNode(Node(27, 450.0,295.62727054,  power_127, 'Radiator_1'))
model.addNode(Node(28, 250.0, 299.55318916, lambda x: 0.0, 'Structure - lateral_2'))
model.addNode(Node(29, 3.0, 231.75567726, power_129, 'MLI - magnetometer'))
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
solver.solve(t_start, t_end)		

#------------------------------CREAR VENTANA---------------------------------
root = tkinter.Tk()
root.wm_title("Outgassing - PROTOTIPO")


#------------------------------CREAR GRAFICA---------------------------------
fig = Figure(figsize=(5, 5), dpi=100)

# GRAFICA 1	
  
#fig.add_subplot(111).plot((solver.t)/3600,solver.T[0]-273, linestyle='--', color='yellow', label="Lower platform")
#fig.add_subplot(111).plot((solver.t)/3600,solver.T[1]-273, linestyle='--', color='blue', label="Upper platform")
#fig.add_subplot(111).plot((solver.t)/3600,solver.T[2]-273, linestyle='-', color='green', label="Interface ring")
  
# GRAFICA 2
  
#fig.add_subplot(111).plot((solver.t)/3600,solver.T[4]-273, linestyle='--', color='blue', label="Front solar panel")
#fig.add_subplot(111).plot((solver.t)/3600,solver.T[5]-273, linestyle='-.', color='magenta', label="Rear solar panel")
#fig.add_subplot(111).plot((solver.t)/3600,solver.T[6]-273, linestyle='-', color='red', label="Lateral solar panel _1")
#fig.add_subplot(111).plot((solver.t)/3600,solver.T[8]-273, linestyle='-', color='green', label="Silicon cell SiCELL_2")
       
# GRAFICA 3
       
fig.add_subplot(111).plot((solver.t)/3600,solver.T[10]-273, linestyle='--', color='blue', label="RF antena")
fig.add_subplot(111).plot((solver.t)/3600,solver.T[11]-273, linestyle='-', color='green', label="Upper microSwitch")
fig.add_subplot(111).plot((solver.t)/3600,solver.T[12]-273, linestyle='-', color='red', label="Lower microSwitch")	
fig.add_subplot(111).plot((solver.t)/3600,solver.T[13]-273, linestyle='-.', color='cyan', label="GPS_1 Antenna")
fig.add_subplot(111).plot((solver.t)/3600,solver.T[14]-273, linestyle='-', color='purple', label="Magnetometer")

#*******************************************************************************
# Calculo del Tiempo  

final = datetime.datetime.now()

#********************************************************************************

Diferencia = final - inicio
print(" ")
print("Tiempo de Procesamiento:")
print Diferencia.total_seconds()

# #GRAFICA IMAGENES
# 
fig.suptitle("MOD_32_VariacionPotencia_H15_3o", fontsize=14)
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


