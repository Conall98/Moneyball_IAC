# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 18:27:58 2024

@author: cdepaor
"""

import numpy as np
import matplotlib.pyplot as plt
import math as m
import Lander_Sizing_V2 as L
import TV_Sizer as T

#%%
class Mission_Architecture3():
    def __init__(self, imLEO, mprop_lander, mprop_TV1, md_TV1, mprop_TV2, md_TV2, md_lander, md_lander_bkdn, mp_surface, mprop_cycle):
        self.imLEO = imLEO
        self.mprop_lander = mprop_lander
        self.mprop_TV1 = mprop_TV1
        self.md_TV1 = md_TV1
        self.mprop_TV2 = mprop_TV2
        self.md_TV2 = md_TV2
        self.md_lander = md_lander
        self.md_lander_bkdn = md_lander_bkdn
        self.mp_surface = mp_surface
        self.mprop_cycle = mprop_cycle

class Construction_Architecture():
    def __init__(self, launcher, n_laun, imLEO, init_md_LEO, init_mprop_LEO):
        self.Laun = launcher
        self.n_laun = n_laun
        self.imLEO = imLEO
        self.init_md_LEO = init_md_LEO
        self.init_mprop_LEO = init_mprop_LEO
#%%
### Lander Architecture definition ###
# Rho_f = density of fuel
# Rho_lox = density of ox
# MR =  mass of ox/f
# Isp = of the main engine
# TW = of the main engine
# Type = 0 for Hypergolic, 1 for Cryo
### ###

#L_arch = Lander_arch(Rho_f, Rho_lox, MR, Isp, TW, Fuel_Type)
LM = L.lander_arch(903, 1450, 1.6, 311, 31, 0, "LM") # Lunar module equivalent
L_Hy = L.lander_arch(70.9, 1141, 6, 450, 50, 0, "LOX/LH2") # LOX/LH2 lander, TW from scaled RL-10C
L_Me = L.lander_arch(422.4, 1141, 3.5, 350, 140, 0, "LOX/CH4") #LOX/LCH4 ladnder, TW from Raptor 2

#TV_arch = TV.arch(ek, Isp, md, m_prop, ref)
TV_Cent = T.TV_arch(9.7e+10, 451, 2462, 20830, "Centaur")
TV_Aria = T.TV_arch(6.62e+10, 446, 4540, 14700, "Ariane 5 2S")
TV_Falc = T.TV_arch(3.48e+11, 348, 3900, 92670, "Falcon 9 2S")
TV_DCSS = T.TV_arch(1.36e+11, 462, 3490, 27200, "DCSS")

FH = T.Launcher(63800, "Falcon Heavy") #payload to leo, name
SLS = T.Launcher(95000, "Space Launch System") #payload to leo, name
#%% 2t case
def ARCH_Sizer_MA3(mpL, dvL, dvT1, dvT2, LUT, TUT1, TUT2):
    Lander = L.Lander_sizer(mpL, dvL, LUT)
    mp_TV = Lander.mt
    TV1 = T.TV_scaler(mp_TV, dvT1, TUT1)
    TV2 = T.TV_scaler(mp_TV, dvT2, TUT2)
    
    imLEO = Lander.md + TV1.md + TV1.m_prop + TV2.md
    mprop_lander = int(Lander.mprop)
    mprop_TV1 = TV1.m_prop
    md_TV1 = TV1.md
    mprop_TV2 = TV2.m_prop
    md_TV2 = TV2.md
    md_lander = Lander.md
    md_lander_bkdn = Lander.dry_mass_breakdown
    mp_surface = mpL
    mprop_cycle = int(Lander.mprop + TV1.m_prop*2)
    MA = Mission_Architecture3(imLEO, mprop_lander, mprop_TV1, md_TV1, mprop_TV2, md_TV2, md_lander, md_lander_bkdn, mp_surface, mprop_cycle)
                            
    return MA
#%%
def ARCH_Construction_Sizer_MA3(max_pl_LEO, mpL, dvL, dvT, LUT, TUT, LaUT):
    Lander = L.Lander_sizer(mpL, dvL, LUT)
    mp_TV = max(Lander.md, mpL)
    
    TV1 = T.TV_scaler(mp_TV, dvT, TUT)
    TV2 = T.TV_scaler(mp_TV, dvT, TUT)
    imLEO = Lander.md + TV1.md + TV1.m_prop + TV2.md
    if Lander.md + TV1.md + TV1.m_prop < max_pl_LEO:
        constr_launches = 1
    else:
        constr_launches = m.cieil(imLEO/max_pl_LEO)
    
    
    launcher = LaUT.ref
    n_laun = constr_launches
    init_md_LEO = Lander.md + TV1.md + TV2.m
    init_mprop_LEO = TV1.m_prop

    CA = Construction_Architecture(launcher, n_laun, imLEO, init_md_LEO, init_mprop_LEO)
    return CA
#%% test CA


#%%
#MA% Max mpL case
def Max_ARCH_Sizer_MA3(Max_pl_LEO, dvL, dvT, LUT, TUT):
    y1 = [] #total mass
    y2 = [] #lander total mass
    y3 = [] # TV total mass
    refs = []
    mps = np.linspace(100, 10000, 100)
    for mpL in mps:
        Lander_test = L.Lander_sizer(mpL, dvL, LM)
        mp_TV = Lander_test.md
        # print(Lander_test.md)
        # print(mpL)
        # print(dvT)
        # print(TUT)
        TV_test = T.TV_scaler(mp_TV, dvT, TUT)
        refs.append(TV_test.ref)
        y1.append(mpL)
        y2.append(Lander_test.md)
        y3.append(TV_test.md)
        if y1[len(y1)-1] < Max_pl_LEO or y2[len(y2)-1] < Max_pl_LEO or y3[len(y3)-1] < Max_pl_LEO:
            mpL_max = mpL
            
        
    # y1 = np.array(y1)
    # y2 = np.array(y2)
    # y3 = np.array(y3)
        
    # plt.figure()
    # plt.plot(mps/1000, y1/1000, label = "Payload Mass")
    # plt.plot(mps/1000, y2/1000, label = "Lander Dry Mass (LM)")
    # plt.plot(mps/1000, y3/1000, label = "Transfer Vechicle Dry Mass")
    # plt.hlines(Max_pl_LEO/1000, 0, 10, linestyles = "--", color = "red", label = "Max mp to LEO")
    # # plt.ylim(0, 70)
    # plt.xlabel("Lander payload mass [t]")
    # plt.ylabel("System Total Masses [t]")
    # plt.title("Lunar Lander Mass Estimations [t]\n mpl_max = {}t".format(mpL_max/1000))
    # plt.grid(which='major', linestyle='-', linewidth='0.5', color='grey')
    # plt.grid(which='minor', linestyle=':', linewidth='0.5', color='grey')
    
    # # Set minor ticks
    # plt.minorticks_on()
    
    # plt.legend()
    imLEO = Lander_test.md + TV_test.md + TV_test.m_prop
    mprop_cycle = Lander_test.mprop + TV_test.m_prop
    return Mission_Architecture3(imLEO, Lander_test.mprop, TV_test.m_prop, Lander_test.md, TV_test.md, Lander_test.dry_mass_breakdown, mpL_max, mprop_cycle)

#%%
mpL = 2000
dvL = 4000
dvT1 = 3800
dvT2 = 1300
LaUT = FH
TUT1 = TV_Falc
TUT2 = TV_Falc
LUT = LM

MA3 = ARCH_Sizer_MA3(mpL, dvL, dvT1, dvT2, LUT, TUT1, TUT2)
# CA3 = ARCH_Construction_Sizer_MA3(LaUT.mp, mpL, dvL, dvT, LUT, TUT, LaUT)


# Max_MA3 = Max_ARCH_Sizer_MA3(LaUT.mp, dvL, dvT, L_Me, TUT)
# Max_CA3 = 

#%%
MAUT = MA3
Results = {"imleo": MAUT.imLEO, 
           "Payload to surface": MAUT.mp_surface,
           "md_lander": MAUT.md_lander, 
           "mprop_lander": MAUT.mprop_lander,
           "md_TV1": MAUT.md_TV1, 
           "mprop_TV1" :MAUT.mprop_TV1, 
           "md_TV2": MAUT.md_TV2, 
           "mprop_TV2" :MAUT.mprop_TV2, 
           "md_lander_bkdn": MAUT.md_lander_bkdn, 
           "propellant per cycle": MAUT.mprop_cycle,
           "Lander Architecture":LUT.ref, 
           "Launcher": LaUT.ref}
        





































