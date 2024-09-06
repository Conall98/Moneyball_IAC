# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 18:27:58 2024

@author: cdepaor
"""

import numpy as np
import matplotlib.pyplot as plt
import Lander_Sizing_V2 as L
import TV_Sizer as T

#%%
class Mission_Architecture():
    def __init__(self, imLEO, mprop_lander, mprop_TV, md_lander, md_TV, md_lander_bkdn, mp_surface):
        self.imLEO = imLEO
        self.mprop_lander = mprop_lander
        self.mprop_TV = mprop_TV
        self.md_lander = md_lander
        self.md_TV = md_TV
        self.md_lander_bkdn = md_lander_bkdn
        self.mp_surface = mp_surface
#%%
### Lander Architecture definition ###
Rho_f = 903 # density of fuel
Rho_lox = 1450 # density of ox
MR = 1.6 # mass of ox/f
Isp = 311 # of the main engine
# sigma_max = 165e+6 # # of the material used for the propellant tanks
# Rho_tank_f = 4540 # of the material used for the propellant tanks
# Rho_tank_lox = 4540 # of the material used for the propellant tanks
# d = 4 # major diameter of the spacecraft
# q = 17*100000 # in the fuel tanks
TW = 31 # of the main engine
Type = 0 # 0 for Hypergolic, 1 for Cryo
### ###
LM = L.lander_arch(Rho_f, Rho_lox, MR, Isp, TW, Type) # Lunar module equivalent
L_Hy = L.lander_arch(70.9, 1141, 6, 450, 50, 1) # LOX/LH2 lander, TW from scaled RL-10C
L_Me = L.lander_arch(422.4, 1141, 3.5, 350, 140, 0) #LOX/LCH4 ladnder, TW from Raptor 2
### ###
#%% MA 5
#Single TV and lander. one way, not reusable
mpL = 2000
dvL = 2500 # from lunar dv chart

Lander = L.Lander_sizer(2000, 2500, L_Hy)
mpTV = Lander.mt
dvT = 4000 # from lunar dv chart
TV = T.Centaur_scaler(Lander.mt, dvT)

mpLauncher = Lander.mt + TV.md + TV.m_prop

#%%
dvL = 2500
dvT = 4000
y1 = []
y2 = []
y3 = []
refs = []
mps = np.linspace(100, 10000, 100)
for mpL in mps:
    Lander_test = L.Lander_sizer(mpL, dvL, LM)
    # TV_test = T.TV_chooser(Lander_test.mt, dvT)
    TV_test = T.Centaur_scaler(Lander_test.mt, dvT)
    refs.append(TV_test.ref)
    # print(TV.md)
    y1.append(Lander_test.mt + TV_test.md + TV_test.m_prop)
    y2.append(Lander_test.mt)
    y3.append(TV_test.md + TV_test.m_prop + mpL)

y1 = np.array(y1)
y2 = np.array(y2)
y3 = np.array(y3)
    
plt.figure()
plt.plot(mps/1000, y1/1000, label = "Initial mass to LEO")
plt.plot(mps/1000, y2/1000, label = "Total Lander Mass (LM)")
plt.plot(mps/1000, y3/1000, label = "Total Transfer Vechicle Mass")
plt.hlines(63.800, 0, 10, linestyles = "--", color = "red", label = "Falcon Heavy mp to LEO")
plt.ylim(0, 70)
plt.xlabel("Lander payload mass [t]")
plt.ylabel("System Total Masses [t]")
plt.title("Lunar Lander Mass Estimations [t]")
plt.grid(which='major', linestyle='-', linewidth='0.5', color='grey')
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='grey')

# Set minor ticks
plt.minorticks_on()

plt.legend()
    
    

