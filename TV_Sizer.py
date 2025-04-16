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
        
class Launcher:
    def __init__(self, mp_LEO, cost, ref):
        self.mp = mp_LEO
        self.cost = cost
        self.ref = ref
    def slc(self):
        return self.cost/self.mp
    def Ekc(self):
        return 0.5*self.mp_LEO*(8000**2)
        
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

def Centaur_scaler(mp, dv):
    Ek = 0.5*mp*(dv**2)
    ek = 9.7e10
    if Ek > ek:
        md = 2462*(Ek/ek)    
    else:
        md = 2462
    ref = "Centaur"
    Isp = 451
    m_inert = md + mp
    m_prop = (np.exp(dv/(Isp*9.81)) - 1)*(m_inert)
    
    TV = TV_arch(int(Ek), int(Isp), int(md), int(m_prop), ref)
    return TV
    
# def 2stage_TV_chooser():
#     #Assuming LEO to LOPG for stage 1
#     #Assuming LOPG to LLO for stage 2
#     # mp1
#     # dv1
#     # mp2
#     # dv2
#     # TV1 = 

def TV_scaler(mp, dv, TUT):
    Ek = 0.5*mp*(dv**2)
    ek = TUT.ek
    if Ek > ek:
        md = TUT.md*(Ek/ek)    
    else:
        md = TUT.md
    ref = TUT.ref
    Isp = TUT.Isp
    m_inert = md + mp
    m_prop = (np.exp(dv/(Isp*9.81)) - 1)*(m_inert)
    
    scaled_TV = TV_arch(int(Ek), int(Isp), int(md), int(m_prop), ref)
    return scaled_TV
    
#%%
def Tsiol_check(mf, mi, dv, Isp): 
    print("Tsiolkovsky Test Result: ",  "Given dV", np.round(dv, 1),  "## dV by Tsiol_check", np.round(Isp*9.81*np.log(mi/mf), 1))

#%%
TUT = TV_arch(3.48e+11, 348, 3900, 92670, "Falcon 9 2S")
testtv = TV_scaler(20000, 4000, TUT)

        