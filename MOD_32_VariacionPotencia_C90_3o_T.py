#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------

# Global mathematical model of SAC-A with 31 nodes and according to design
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


EMLI  = 0.03     # MLI effective emissivity
PINF  = 7.0      # Internal power dissipated at lower platform
PSUP  = 12.00    # Internal power dissipated at upper platform
F_AREA = 0.31    # Area correction for radiator


# Tiempo de Simulación
t_start = 0.0
t_end = 16579.8 #12000 #55266.0      


# Tiempos en los que cambia las potencias

power_times1 = [ 0.0,19343.,19343.,20063.,20063., 55266.0,] 
                

power_Low= [1.0, 1.0,  1.0,  1.0,  1.0, 1.0,]
            

power_Upp= [1.0, 1.000, 5.000, 5.000, 1.000,  1.000, ]
            

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


power_node_103 = [ 5.04,  5.31,  5.68,  6.13,  6.62,
                   7.11,  7.56,  7.88,  8.02,  7.93,
                   7.60,  7.07,  6.46,  6.37,  6.35,
                   2.38,  2.32,  2.21,  2.06,  1.89,
                   1.71,  1.54,  1.38,  1.24,  1.13,
                   1.08,  5.05,  5.04,  5.04, ]

power_node_103 = power_node_103*3



power_node_104 = [8.14,   7.37,   6.67,   6.06,   5.55,
                  5.20,   5.12,   5.19,   5.54,   6.06,
                  6.67,   7.37,   8.13,   9.03,   9.30,
                  4.26,   4.94,   5.84,   6.58,   7.00,
                  7.12,   7.00,   6.59,   5.85,   4.95,
                  4.27,   9.31,   9.04,   8.14, ]

power_node_104 = power_node_104*3
                  
power_node_105 = [61.31,  60.59,  59.44,  58.30,  57.57,
                  57.44,  57.44,  57.44,  57.57,  58.30,
                  59.44,  60.59,  61.31,  62.45,  62.88,
                   5.45,   6.54,   8.02,   9.34,  10.34,
                  10.71,  10.34,   9.34,   8.02,   6.54,
                   5.45,  62.88,  62.45,  61.31, ]

power_node_105 = power_node_105*3

                   
power_node_106 = [ 3.55,   6.15,   9.99,  14.35,  18.61,
                  21.95,  23.20,  21.95,  18.61,  14.35,
                   9.99,   6.15,   3.54,   2.24,   1.91,
                   1.91,   1.19,   0.45,   0.06,   0.00,
                   0.00,   0.00,   0.06,   0.45,   1.19,
                   1.91,   1.91,   2.24,   3.55, ]
                   
power_node_106 = power_node_106*3

power_node_107 = [62.92,  63.82,  65.13,  67.00,  69.48,
                  71.85,  73.32,  73.58,  72.69,  71.39,
                  69.77,  67.94,  66.16,  65.65,  65.67,
                   8.02,   8.19,   8.71,   9.49,  10.32,
                  10.50,   9.92,   8.88,   7.65,   6.42,
                   5.66,  63.31,  63.07,  62.92, ]
                  
power_node_107 = power_node_107*3

power_node_108 = [66.16,  67.94,  69.77,  71.38,  72.68,
                  73.57,  73.32,  71.85,  69.48,  67.02,
                  65.14,  63.83,  62.94,  63.10,  63.34,
                   5.69,   6.45,   7.67,   8.89,   9.93,
                  10.50,  10.32,   9.49,   8.71,   8.19,
                   8.02,  65.67,  65.65,  66.16, ]
                  
power_node_108 = power_node_108*3

power_node_109 = [ 4.60,   4.50,   4.31,   4.06,   3.79,
                   3.58,   3.53,   3.53,   3.53,   3.53,
                   3.54,   3.58,   3.65,   3.77,   3.82,
                   0.29,   0.41,   0.62,   0.85,   1.08,
                   1.29,   1.47,   1.58,   1.54,   1.42,
                   1.30,   4.83,   4.77,   4.60, ]
                   
power_node_109 = power_node_109*3

power_node_110 = [ 3.65,   3.58,   3.54,   3.53,   3.53,
                   3.53,   3.53,   3.58,   3.79,   4.06,
                   4.31,   4.50,   4.60,   4.77,   4.83,
                   1.30,   1.42,   1.54,   1.58,   1.47,
                   1.29,   1.08,   0.85,   0.62,   0.41,
                   0.29,   3.82,   3.77,   3.65, ]
                   
power_node_110 = power_node_110*3
#
power_node_111= [ 1.23,   1.32,   1.39,   1.46,   1.50,
                  1.49,   1.45,   1.39,   1.31,   1.22,
                  1.14,   1.07,   1.00,   0.97,   0.97,
                  0.58,   0.58,   0.58,   0.60,   0.62,
                  0.65,   0.68,   0.71,   0.74,   0.77,
                  0.80,   1.18,   1.19,   1.23, ]
                  
power_node_111 = power_node_111*3
#
power_node_112= [1.95,   2.10,   2.20,   2.25,   2.27,
                 2.26,   2.21,   2.12,   2.01,   1.93,
                 1.87,   1.81,   1.72,   1.71,   1.71,
                 0.67,   0.67,   0.68,   0.71,   0.74,
                 0.78,   0.80,   0.81,   0.83,   0.86,
                 0.88,   1.92,   1.93,   1.95, ]
                 
power_node_112 = power_node_112*3
                 
power_node_113=  [0.08,   0.10,   0.15,   0.20,   0.26,
                  0.34,   0.41,   0.47,   0.50,   0.49,
                  0.45,   0.37,   0.28,   0.26,   0.26,
                  0.26,   0.25,   0.23,   0.21,   0.19,
                  0.16,   0.14,   0.11,   0.10,   0.08,
                  0.08,   0.08,   0.08,   0.08,  ]
                  
power_node_113 = power_node_113*3
#
power_node_114=  [ 8.57,  10.14,  11.40,  12.03,  11.96,
                  11.24,  10.09,   8.71,   7.30,   6.07,
                   5.07,   4.28,   3.68,   3.62,   3.63,
                   2.03,   2.11,   2.32,   2.68,   3.16,
                   3.75,   4.40,   5.08,   5.71,   6.25,
                   6.55,   8.15,   8.24,   8.57, ]
                   
power_node_114 = power_node_114*3
#
power_node_115=  [ 5.24,   6.48,   7.51,   7.93,   7.57,
                   6.39,   4.90,   3.34,   1.98,   0.98,
                   0.38,   0.11,   0.03,   0.04,   0.05,
                   0.05,   0.11,   0.23,   0.41,   0.68,
                   1.14,   1.80,   2.66,   3.50,   4.25,
                   4.69,   4.69,   4.84,   5.24, ]
                   
power_node_115 = power_node_115*3
#
power_node_116=  [ 4.14,   4.69,   5.55,   6.70,   8.13,
                   9.77,  11.43,  12.87,  13.83,  14.09,
                  13.54,  12.25,  10.58,  10.28,  10.19,
                   8.37,   8.08,   7.50,   6.76,   5.93,
                   5.09,   4.29,   3.59,   3.02,   2.60,
                   2.40,   4.22,   4.17,   4.14, ]
                  
power_node_116 = power_node_116*3
#
power_node_117=  [ 4.27,   5.04,   5.66,   5.87,   5.50,
                   4.63,   3.56,   2.46,   1.50,   0.78,
                   0.33,   0.11,   0.04,   0.03,   0.03,
                   0.03,   0.03,   0.05,   0.09,   0.20,
                   0.53,   1.12,   1.87,   2.62,   3.30,
                   3.71,   3.71,   3.86,   4.27, ]
                   
power_node_117 = power_node_117*3
#
power_node_118=  [ 0.05,  0.07,  0.14,  0.47,  1.10,
                   1.95,  2.94,  3.94,  4.82,  5.47,
                   5.85,  5.95,  5.76,  5.43,  4.82,
                   4.07,  3.27,  2.48,  1.74,  1.12,
                   0.63,  0.27,  0.08,  0.05,  0.05,]
                   
power_node_118 = power_node_118*3
#
power_node_119=  [ 0.03,   0.11,   0.38,   0.98,   1.98,
                   3.34,   4.90,   6.39,   7.57,   7.93,
                   7.51,   6.48,   5.24,   4.84,   4.69,
                   4.69,   4.25,   3.50,   2.66,   1.80,
                   1.14,   0.68,   0.41,   0.23,   0.11,
                   0.05,   0.05,   0.04,   0.03,  ]
                   
power_node_119 = power_node_119*3
#
power_node_120=  [ 1.39,   1.64,   1.91,   2.13,   2.27,
                   2.34,   2.33,   2.22,   2.05,   1.83,
                   1.56,   1.29,   1.08,   1.02,   1.01,
                   1.01,   1.00,   0.99,   0.97,   0.96,
                   0.99,   1.02,   1.08,   1.15,   1.23,
                   1.28,   1.29,   1.31,   1.39, ]
                   
power_node_120 = power_node_120*3
#
power_node_121=  [1.48,   1.72,   1.92,   1.99,   1.94,
                  1.79,   1.56,   1.29,   1.00,   0.74,
                  0.53,   0.41,   0.37,   0.39,   0.40,
                  0.37,   0.40,   0.46,   0.53,   0.61,
                  0.71,   0.83,   0.96,   1.10,   1.23,
                  1.31,   1.33,   1.37,   1.48, ]
                  
power_node_121 = power_node_121*3
#
power_node_122=  [ 1.94,   2.23,   2.48,   2.64,   2.66,
                   2.55,   2.33,   2.03,   1.70,   1.36,
                   1.04,   0.77,   0.56,   0.48,   0.47,
                   0.47,   0.47,   0.54,   0.66,   0.81,
                   0.99,   1.18,   1.38,   1.57,   1.74,
                   1.82,   1.82,   1.85,   1.94, ]
                   
power_node_122 = power_node_122*3
#
power_node_123=  [1.19,   1.36,   1.49,   1.58,   1.63,
                  1.62,   1.56,   1.45,   1.32,   1.15,
                  0.96,   0.78,   0.63,   0.57,   0.56,
                  0.54,   0.53,   0.53,   0.56,   0.62,
                  0.71,   0.80,   0.90,   1.00,   1.07,
                  1.11,   1.13,   1.14,   1.19, ]
                   
power_node_123 = power_node_123*3
#
power_node_126=  [ 2.60,   4.12,   5.94,   7.46,   8.20,
                   8.02,   7.11,   5.72,   4.13,   2.63,
                   1.42,   0.61,   0.22,   0.06,   0.03,
                   0.03,   0.00,   0.00,   0.00,   0.02,
                   0.14,   0.38,   0.71,   1.13,   1.60,
                   1.96,   1.96,   2.10,   2.60, ]
                   
power_node_126 = power_node_126*3
                   
for index in range(len(power_node_126)):
   power_node_126[index] = power_node_126[index]*F_AREA
#
power_node_127=  [ 0.22,   0.61,   1.42,   2.63,   4.13,
                   5.72,   7.11,   8.03,   8.20,   7.46,
                   5.94,   4.12,   2.60,   2.10,   1.96,
                   1.96,   1.60,   1.13,   0.71,   0.38,
                   0.14,   0.02,   0.00,   0.00,   0.00,
                   0.03,   0.03,   0.06,   0.22, ]
                   
power_node_127 = power_node_127*3

for index in range(len(power_node_127)):
   power_node_127[index] = power_node_127[index]*F_AREA
#
power_node_129=  [ 1.65,   2.01,   2.37,   2.69,   2.95,
                   3.14,   3.14,   2.93,   2.58,   2.20,
                   1.83,   1.50,   1.22,   1.12,   1.10,
                   0.89,   0.84,   0.80,   0.84,   0.92,
                   0.98,   1.04,   1.08,   1.13,   1.21,
                   1.28,   1.49,   1.52,   1.65, ]
                   
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




model = ThermalModel()


  
              
           
model.addNode(Node(1, 14400.0, 267.20680393,  power_L, 'Lower platform'))
model.addNode(Node(2, 22400.0, 267.93588684, power_U, 'Upper platform'))
model.addNode(Node(3, 1600.0, 265.19565877,  power_103, 'Interface ring'))
model.addNode(Node(4, 400.0,280.23769264, power_104, 'Front panel radiator'))
model.addNode(Node(5, 450.0,294.29978828, power_105, 'Front solar panel'))
model.addNode(Node(6, 450.0,262.58166698, power_106, 'Rear solar panel'))
model.addNode(Node(7, 450.0,281.40890725, power_107, 'Lateral solar panel _1'))
model.addNode(Node(8, 450.0,281.40866422, power_108, 'Lateral solar panel _2'))
model.addNode(Node(9, 150.0,278.72505086, power_109, 'Silicon cell SiCELL_2'))
model.addNode(Node(10, 150.0,278.81352507,power_110, 'Silicon cell SiCELL_1'))
model.addNode(Node(11, 200.0,247.06674956, power_111, 'RF antena'))
model.addNode(Node(12, 300.0,251.74321647, power_112, 'Upper microSwitch'))
model.addNode(Node(13, 300.0, 262.50961538, power_113, 'Lower microSwitch'))
model.addNode(Node(14, 0.010,211.90748089, power_114, 'MLI-Upper platform'))
model.addNode(Node(15, 0.010,217.31389554, power_115, 'MLI-lateral_2'))
model.addNode(Node(16, 0.010, 215.88774433, power_116, 'MLI-Lower platform'))
model.addNode(Node(17, 0.010,225.33009722, power_117, 'Shunt_2'))
model.addNode(Node(18, 0.010,225.33019106, power_118, 'Shunt_1'))
model.addNode(Node(19, 0.010,217.31395888, power_119, 'MLI-lateral_1'))
model.addNode(Node(20, 100.0, 222.89324573, power_120, 'GPS_1 Antenna'))
model.addNode(Node(21, 100.0,223.24352468, power_121, 'GPS_2 Antenna'))
model.addNode(Node(22, 100.0, 223.01221204, power_122, 'GPS_3 Antenna'))
model.addNode(Node(23, 100.0,223.01221204, power_123, 'GPS_4 Antenna'))
model.addNode(Node(24, 250.0, 267.94104343, lambda x: 0.0, 'Structure - lateral_1'))
model.addNode(Node(25, 250.0, 266.69563838, lambda x: 0.0, 'Structure - rear'))
model.addNode(Node(26, 450.0,266.27682007,  power_126, 'Radiator_2'))
model.addNode(Node(27, 450.0,266.2768239 , power_127, 'Radiator_1'))
model.addNode(Node(28, 250.0, 267.94102566, lambda x: 0.0, 'Structure - lateral_2'))
model.addNode(Node(29, 0.010, 225.55513943, power_129, 'MLI - magnetometer'))
model.addNode(Node(30, 300.0, 254.35204102, lambda x: 0.0,'Magnetometer'))
model.addNode(Node(31, 1100.0,269.13557097, lambda x: 0.0, 'Structure - front'))
model.addNode(Node(32, 1.0,286.49632293, lambda x: 0.0, 'Mathematical node'))
model.addNode(Node(-99, 1.0, 0.0, lambda x: 0.0, 'Space'))



#HEADER CONDUCTOR DATA

# CONDUCTANCIAS

model.addConductance(1, 31, 1.10) 					   # Lower_plat - Front_estr
model.addConductance(1, 24, 0.22) 					   # Lower_plat - Latestr_1
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
  
fig.add_subplot(111).plot((solver.t)/3600,solver.T[4]-273, linestyle='--', color='blue', label="Front solar panel")
fig.add_subplot(111).plot((solver.t)/3600,solver.T[5]-273, linestyle='-.', color='magenta', label="Rear solar panel")
fig.add_subplot(111).plot((solver.t)/3600,solver.T[6]-273, linestyle='-', color='red', label="Lateral solar panel _1")
fig.add_subplot(111).plot((solver.t)/3600,solver.T[8]-273, linestyle='-', color='green', label="Silicon cell SiCELL_2")
       
# GRAFICA 3
       
#fig.add_subplot(111).plot((solver.t)/3600,solver.T[10]-273, linestyle='--', color='blue', label="RF antena")
#fig.add_subplot(111).plot((solver.t)/3600,solver.T[11]-273, linestyle='-', color='green', label="Upper microSwitch")
#fig.add_subplot(111).plot((solver.t)/3600,solver.T[12]-273, linestyle='-', color='red', label="Lower microSwitch")	
#fig.add_subplot(111).plot((solver.t)/3600,solver.T[13]-273, linestyle='--', color='blue', label="GPS_1 Antenna")
#fig.add_subplot(111).plot((solver.t)/3600,solver.T[14]-273, linestyle='-', color='green', label="Magnetometer")


#*******************************************************************************
# Calculo del Tiempo  

final = datetime.datetime.now()

Diferencia = final - inicio
print(" ")
print("Tiempo de Procesamiento:")
print Diferencia.total_seconds()

# #GRAFICA IMAGENES
# 
fig.suptitle("MOD_32_VariacionPotencia_C90_3o", fontsize=14)
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






