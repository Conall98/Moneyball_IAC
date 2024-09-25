# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 16:13:45 2024

@author: cdepaor
"""
### TP_cost_functions ###
# reverse engineered CERs from TP. acquisition costs only

def structure(m): #unmanned space planetary structures and mech primary
    return 0.0565*m + 6.796

def avionics(m): # assumed it was a programmable information processer from computer in legacy unmanned space
    return 0.2366*m + 10.15

def other(m): # assumed it was ADCS subsytem from legacy unmanned space
    return 0.2972*m + 6.958

def power(m): #EPS Legacy unmanned psace power
    return 0.2452*m + 7.93

def thermal(m): # unmanned spac planetary, thermal control, miscellaneous
    return 0.0447*m + 3.062

def motor(m): #unmanned space - earth orbiting, propulsion, thruster, liquid
    return 0.3181*m + 4.128

def tanks(m): #Unamanned space planetary, propulsion, tank, 
    return 0.0843*m + 4.572
    