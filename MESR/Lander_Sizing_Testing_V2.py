# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 18:04:46 2024

@author: cdepaor
"""

import numpy as np
import matplotlib.pyplot as plt
import math as m


#%% Landers under test
import Recursive_Sizing_V2 as R
#               (self, Rho_f, Rho_lox, MR, Isp, sigma_max, Rho_tank_f, Rho_tank_Lox, d, q):
L1 = R.lander_arch(422.4, 1141.2, 3.5, 350, 165e+6, 4540, 4540, 4, 100000, 143, 0)



#%%
LM = R.lander_arch(903, 1450, 1.6, 311, 165e+6, 4540, 4540, 4, 17*100000, 31, 0) #https://en.wikipedia.org/wiki/Descent_propulsion_system
#%% Mission paramters
mp = 4821
dv = 2500

#%% Test 1
import Recursive_Sizing_V2 as R
L_arch = LM
A, B, C, D, E = R.Looper(mp, dv, L_arch)
md = C["md"]
mprop = C["mprop"]
mt = C["mt"]
#%% Test 2
import Recursive_Sizing_V2 as R
md = R.p2d(mp)
md_init = md
L_arch = LM
m_prop = R.prop(mp, md, L_arch.Isp, dv)
R.ss_masses(mp, md, md_init, m_prop, L_arch, dv)


#%%
tin1 = []
tin2 = []
tin3 = []

for mp in np.linspace(100, 5000, 1899):
    A, B, C, D, E = R.Looper(mp, dv, L_arch)
    tin1.append(C["mp"])
    tin2.append(C["md"])
    tin3.append(R.p2d(C["mp"]))

plt.figure()
plt.plot(tin1, tin2, linestyle = "--", label = "after it.")
plt.plot(tin1, tin3, linestyle = "--", label = "before it.")
plt.scatter(4821, 2034)
plt.xlabel("mp [kg]")
plt.ylabel("md [kg]")
plt.title("Statistical VS. Sizing Algorithm")
plt.legend()
    
#%%

tin1 = []
tin2 = []
tin3 = []

plt.figure()
for mp in np.linspace(100, 5000, 100):
    tin3.append(R.p2d(mp))
    tin1.append(mp)
plt.plot(tin1, tin3, linestyle = "--", color = "red", label = "Statistical relation.")

for dv in np.linspace(1000, 5000, 5):
    #print(dv)
    for mp in np.linspace(100, 5000, 100):
        A, B, C, D, E = R.Looper(mp, dv, L_arch)        
        tin2.append(C["md"])
    
    plt.plot(tin1, tin2, label = "{} m/s".format(int(dv)))
    tin2 = []

plt.scatter(4821, 2034)
plt.xlabel("mp [kg]")
plt.ylabel("md [kg]")
plt.title("mp to md with different dVs")
plt.legend()
#%%
mdDB = [770,
626,
340,
190,
847,
273,
271,
267,
266,
262,
800,
1200,
1200,
1365,
1360,
1360,
1144,
1200,
1000,
2626,
2626,
2626,
2109,
2134,
2034,
2034]

mpDB = [30,
27,
30,
20,
99.8,
33,
33,
33,
33,
33,
112,
170,
170,
515,
520,
520,
756,
800,
836,
4795,
4795,
4795,
4489,
4700,
4819,
4821]
#%%
tin1 = []
tin2 = []
tin3 = []
dv1 = []
dv2 = []
dv3 = []
dv4 = []
dv5 = []

plt.figure()
for mp in np.linspace(100, 5000, 100):
    tin3.append(R.p2d(mp))
    tin1.append(mp)
plt.plot(tin1, tin3, linestyle = "--", color = "red", label = "Statistical relation.")


for mp in np.linspace(100, 5000, 100):
    A, B, C, D, E = R.Looper(mp, 1000, L_arch)        
    dv1.append(C["md"])
    A, B, C, D, E = R.Looper(mp, 2000, L_arch)        
    dv2.append(C["md"])
    A, B, C, D, E = R.Looper(mp, 3000, L_arch)        
    dv3.append(C["md"])
    A, B, C, D, E = R.Looper(mp, 4000, L_arch)        
    dv4.append(C["md"])
    A, B, C, D, E = R.Looper(mp, 5000, L_arch)        
    dv5.append(C["md"])
    

plt.plot(tin1, dv1, label = "Algorithm. dV = 1 km/s")
plt.plot(tin1, dv2, label = "Algorithm. dV = 2 km/s")
plt.plot(tin1, dv3, label = "Algorithm. dV = 3 km/s")
plt.plot(tin1, dv4, label = "Algorithm. dV = 4 km/s")
plt.plot(tin1, dv5, label = "Algorithm. dV = 5 km/s")


plt.scatter(mpDB, mdDB)
plt.xlabel("mp [kg]")
plt.ylabel("md [kg]")
plt.title("Payload Mass to Dry Mass relations")
plt.legend()

