# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 17:51:03 2024

@author: cdepaor
"""

import numpy as np
import matplotlib.pyplot as plt
import math as m
import pandas as pd

#%%

class TV_arch:
    def __init__(self, ek, Isp, md, m_prop, ref):
        self.ek = ek
        self.Isp = Isp
        self.md = md
        self.ref = ref
        self.m_prop = m_prop
        
#%%
def TV_chooser(mp, dv):
    TVDB = pd.read_excel(r"TV DB 242.xlsx")
    Ek = 0.5*mp*(dv**2)
    can_ek = []
    can_name = []
    can_md = []
    can_Isp = []
    
    for i in range(0, len(TVDB["Characteristic Energy"])):

        if max(TVDB["Characteristic Energy"]) < Ek:            
            ek = Ek
            ref = TVDB["Stage name"][np.argmax(np.array(TVDB["Characteristic Energy"]))] + "(scaled)"
            md = TVDB["Dry mass"][np.argmax(np.array(TVDB["Characteristic Energy"]))]*(ek/max(TVDB["Characteristic Energy"]))
            # print(md)
            Isp = TVDB["Isp"][np.argmax(np.array(TVDB["Characteristic Energy"]))]
            
        elif Ek - TVDB["Characteristic Energy"][i] < 0 :            
            ek = (TVDB["Characteristic Energy"][i])
            ref_name = (TVDB["Stage name"][i])
            md = (TVDB["Dry mass"][i])
            Isp = (TVDB["Isp"][i])
            ref = TVDB["Stage name"][i] 
            break
            
    # TV = "test"
    m_inert = md + mp
    m_prop = (np.exp(dv/(Isp*9.81)) - 1)*(m_inert)
    
    TV = TV_arch(int(ek), int(Isp), int(md), int(m_prop), ref)
    # return TVDB
    return TV

#%%
def Tsiol_check(mf, mi, dv, Isp): 
    print("Tsiolkovsky Test Result: ",  "Given dV", np.round(dv, 1),  "## dV by Tsiol_check", np.round(Isp*9.81*np.log(mi/mf), 1))

#%%Test1
Test_TV = TV_chooser(15600, 5973)

mf = 15600 + 3900
mi = 15600 + 3900 + 92670
dv = 5973

Tsiol_check(mf, mi, dv, Test_TV.Isp)
Test_TV.m_prop
#%%Test
test_mps = np.linspace(0, 16000, 100)
test_dvs = np.linspace(5972, 5972, 100)
for i in test_dvs:
    Test_TV = TV_chooser(15600, i) # generates a test dv based on mp and dv
    mf = Test_TV.md + 15600# mf for Tsiolkovsky
    mi = Test_TV.md + 15600 + Test_TV.m_prop # mi for Tsiolkovsky
    Isp = Test_TV.Isp
    print("dv: ", np.round(i), "Propellant: ", Test_TV.m_prop)
    # Tsiol_check(mf, mi, i, Isp)

# test_dv = 5973
# test_mp = 15600
# Test_TV = TV_chooser(test_mp, test_dv)
# mf = Test_TV.md + test_mp# mf for Tsiolkovsky
# print(mf)
# mi = Test_TV.md + test_mp + Test_TV.m_prop # mi for Tsiolkovsky
# print(mi)
# Isp = Test_TV.Isp
# print(Isp)
# # print(Test_TV.m_prop)
# print(test_dv)
# Tsiol_check(mf, mi, test_dv, Isp)




        