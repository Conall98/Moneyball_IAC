# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 19:02:33 2024

@author: cdepaor
"""

import numpy as np
import matplotlib.pyplot as plt
import math as m

#%% Functions
class lander_arch:
    # def __init__(self, Rho_f, Rho_lox, MR, Isp, sigma_max, Rho_tank_f, Rho_tank_Lox, d, q, TW, Type):
    def __init__(self, Rho_f, Rho_lox, MR, Isp, TW, Fuel_Type, ref):
        self.Rho_f = Rho_f
        self.Rho_lox = Rho_lox 
        self.MR = MR 
        self.Isp = Isp 
        # self.sigma_max = sigma_max 
        # self.Rho_tank_f = Rho_tank_f
        # self.Rho_tank_Lox = Rho_tank_Lox
        # self.d = d
        # self.q = q
        self.TW = TW
        self.Fuel_Type = Fuel_Type
        self.ref = ref
        
class lander:
    def __init__(self, mp, md, mprop, mt, dry_mass_breakdown):
        self.mp = mp
        self.md = md
        self.mprop = mprop
        self.mt = mt
        self.dry_mass_breakdown = dry_mass_breakdown
        
#%%
def p2d(mp):
    a = 367.29
    b = -904.17
    return a*m.log(mp) + b

def prop(mp, md, Isp, dv):

    return (mp+md)*(np.exp(dv/(Isp*9.81)) - 1)
#%%
def S_Taurus(V_lox, d):
    b_range = np.linspace(0.01, d/2, 2000)
    roots = np.zeros([3, 2])
    root_count = 0
    ys = [0]
    for b in b_range:
        y = b**3 - (d/2)*b**2 + V_lox/(2*np.pi**2)
        if y*ys[len(ys)-1] < 0:
            a = d/2 - b
            roots[root_count, 1] = b
            roots[root_count, 0] = a
            root_count = root_count+1
        ys.append(y)
    for i in range(0,len(roots[:, 0]))    :
        if roots[i, 0] > roots[i, 1]:
            a = roots[i, 0]
            b = roots[i, 1]
    S = (4*np.pi**2)*a*b
    return S, a, b
#%%
def m_propulsion_taurus(m_prop, mp, md, Lander_architecture):
    
    d = Lander_architecture.d
    Rho_f = Lander_architecture.Rho_f
    Rho_lox = Lander_architecture.Rho_lox
    MR = Lander_architecture.MR
    q = Lander_architecture.q
    Rho_F_tank = Lander_architecture.Rho_tank_f
    Rho_lox_tank = Lander_architecture.Rho_tank_Lox
    sigma_max = Lander_architecture.sigma_max
    
    #Fuel and Lox properties
    m_f = m_prop/(MR + 1)
    m_Lox = (m_prop/4.5)*MR
    
    ############### Ss
    # F
    V_f = m_f/Rho_f
    r = (V_f/(0.75*np.pi))**(1/3)
    S_F = (3/4)*(np.pi*(r)**3)
    V_ball = 0.75*np.pi*r**3
    d_ball = 2*r
    
    # Lox
    V_lox = m_Lox/Rho_lox
    S_Lox, a, b = S_Taurus(V_lox, d)  
    V_donut = 2*(np.pi**2)*a*(b**2)
    
    ############### ts

    
    # F
    t_F = (q*(d/2))/(2*sigma_max)
    
    # Lox
    t_Lox = (q*b)/(2*sigma_max) * (2*a - b)/(a - b)

    
    
    m_F_tank = S_F * t_F * Rho_F_tank
    m_Lox_tank = S_Lox * t_Lox * Rho_lox_tank
    
    
    
    tanks_dict = {"Lox mass": m_Lox, 
                  "Lox volume": V_lox,
                  "Donut Volume": V_donut,
                  "Donut Surface": S_Lox,
                  "fuel mass": m_f , 
                  "fuel volume": V_f, 
                  "Ball volume": V_ball,
                  "Ball diameter": d_ball,
                  "Lox donut radius (a)": a,
                  "Lox donut radius (b)": b,
                  "outer diameter (d)": d, 
                  "Lox tank mass": m_Lox_tank,
                  "Fuel tank mass": m_F_tank,
                  "Lox tank thickness": t_Lox,
                  "fuel tank thickness": t_F,}
    # Engine_mass = 0.048*(mp+md+m_prop) # factor from scaled space X raptor 2 Lox LCH4 engine
    m_propulsion = m_Lox_tank + m_F_tank
    
    return m_propulsion

#%% Isaji propellant subsystem sizing
def Isaji_prop(mp, md, dv, LA):
    Cryo = LA.Fuel_Type
    Rho_mix = LA.MR*(LA.Rho_lox*LA.Rho_f)/(LA.MR*LA.Rho_f+LA.Rho_lox)
    dv_scaler = (np.exp(dv/(LA.Isp*9.81)))/(np.exp(2500/(311*9.81))) #isajii is using Apollo as his benchmark
    if Cryo == 1: # that is if LOX/LH2
        mpss = ((2.702*((mp+md)/(1000))**2.785) - (0.01813*((mp+md)/(1000))**4.348))*dv_scaler
    elif Cryo == 0: # That is if propellant is not LOX/LH2 0 for storable
        mpss = (((mp+md)**1.811)*(Rho_mix**(-0.4262))*(LA.Isp**(-1.201))+245.3)*dv_scaler
    return mpss    
#%%
#L1 = lander_arch(422.4, 1141.2, 3.5, 350, 143, 0)
            #   Rho_f, Rho_lox, MR, Isp, TW, Fuel_Type
#print(Isaji_prop(1, 5000, 2671, L1)/2671)
#%%
def m_propulsion_spheres(m_prop, mp, md, Lander_architecture):
    d = Lander_architecture.d
    Rho_f = Lander_architecture.Rho_f
    Rho_lox = Lander_architecture.Rho_lox
    MR = Lander_architecture.MR
    q = Lander_architecture.q
    Rho_F_tank = Lander_architecture.Rho_tank_f
    Rho_lox_tank = Lander_architecture.Rho_tank_Lox
    sigma_max = Lander_architecture.sigma_max
    
    m_f = m_prop/(MR + 1)
    m_Lox = (m_prop/(MR + 1))*MR
    
    ############### Ss
    # F
    V_f = m_f/Rho_f
    r = (3*V_f/(4*np.pi))**(1/3)
    S_F = (4)*(np.pi*(r)**2)
    V_ball = (4/3)*np.pi*r**3
    d_ball = 2*r
    
    # Lox
    V_lox = m_Lox/Rho_lox
    rl = (3*V_lox/(4*np.pi))**(1/3)
    S_Lox = (4)*(np.pi*(rl)**2)
    V_Lox_ball = (4/3)*np.pi*rl**3
    d_Lox_ball = 2*rl
    
    # S_Lox, a, b = S_Taurus(V_lox, d)  
    # V_donut = 2*(np.pi**2)*a*(b**2)
    
    ############### ts
    # F
    t_F = (q*(d_ball/2))/(2*sigma_max)
    
    # Lox
    t_Lox = (q*(d_Lox_ball/2))/(2*sigma_max)

    
    
    m_F_tank = S_F * t_F * Rho_F_tank
    m_Lox_tank = S_Lox * t_Lox * Rho_lox_tank
    
    
    
    tanks_dict = {"Lox mass": m_Lox, 
                  "Lox volume": V_lox,                  
                  "Lox Ball volume": V_Lox_ball,
                  "Lox Ball diameter": d_Lox_ball,
                  "Lox Ball surface": S_Lox,
                  "fuel mass": m_f , 
                  "fuel volume": V_f, 
                  "Fuel Ball volume": V_ball,
                  "Fuel Ball diameter": d_ball,
                  "Lox tank mass": m_Lox_tank,
                  "Fuel tank mass": m_F_tank,
                  "Lox tank thickness": t_Lox,
                  "fuel tank thickness": t_F,}
    

    # m_propulsion = Engine_mass + m_Lox_tank + m_F_tank
    m_tanks = m_Lox_tank + m_F_tank
    
    return m_tanks
    # return tanks_dict
#%%
# L1 = lander_arch(422.4, 1141.2, 3.5, 350, 143, 0)
# m_propulsion_spheres(18000, 2000, 2671, L1)
#%%
def engine_size(TW, mt):
     #from Apollo LM. Thrust was 1.7 times mt
    T_req = 9.81*mt*1.7
    return T_req/(TW*9.81)
    
#%%
# engine_size(140, 20000)

#%%m_propulsion_spheres_test
# m_prop = 12789.31
# mp = 2000
# md = p2d(mp)

# m_propulsion_ss = m_propulsion_spheres(m_prop, mp, md, L1)
# print(m_propulsion_ss)
# print(m_propulsion_ss/md)

#%%
def ss_masses(mp, md, md_init, m_prop, Lander_architecture, dv):
   
    # d = Lander_architecture.d
    Rho_f = Lander_architecture.Rho_f
    Rho_lox = Lander_architecture.Rho_lox
    MR = Lander_architecture.MR
    # q = Lander_architecture.q
    # Rho_F_tank = Lander_architecture.Rho_tank_f
    # Rho_lox_tank = Lander_architecture.Rho_tank_Lox
    # sigma_max = Lander_architecture.sigma_max
    mt = mp + md + m_prop
    Cryo = Lander_architecture.Fuel_Type

    a = 0.276*md_init # Structure
    # b = m_propulsion_spheres(m_prop, mp, md, Lander_architecture) + engine_size(Lander_architecture.TW, mt) # Propulsion
    #b = 0.337*md
    b = Isaji_prop(mp, md, dv, Lander_architecture)
    c = 0.076*md_init # power
    d = 0.088*md_init # avionics
    e = 0.133*md_init # thermal
    f = 0.094*md_init # other
    ss_masses =  np.array([a, b, c, d, e, f])
    m_dry_total = sum(ss_masses)
    
    ss_dict = {"payload": np.round(mp, 2),
               "Str": np.round(a, 2),
               "Propulsion": np.round(b, 2), 
               "prop fraction": np.round(b/m_dry_total, 2),
               "Power": np.round(c, 2), 
               "Avionics": np.round(d, 2), 
               "Thermal": np.round(e, 2), 
               "Other": np.round(f, 2), 
               "md_init": np.round(md_init, 2), 
               "md_final": np.round(m_dry_total, 2)}
    
    return ss_dict
# #%%
# LM = lander_arch(422.4, 1141.2, 3.5, 350, 143, 1)
# ss_masses(4821, 1600, 2200, 18000, LM, 2500)
#%%
def Tsiolkovsky_check(mf, mi, dv, Isp): 
    print("Tsiolkovsky Test Result: ",  np.round(dv, 1),  np.round(Isp*9.81*np.log(mi/mf), 1))
    # print("Tsiolkovsky Test Result: ",  np.round(dv, 1) ==  np.round(Isp*9.81*np.log(mi/mf), 1))
    # print("Tsiolkovsky Test Result: ",  abs(np.round(dv, 1) -  np.round(Isp*9.81*np.log(mi/mf), 1)))
    return

#%%
def convergence(x, y, xtitle, ytitle, title):
    plt.figure()
    plt.scatter(x, y, marker="x")
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.title(title)
    

#%%
def Looper(mp, dv, Lander_architecture):
    
    Isp = Lander_architecture.Isp
    Rho_f = Lander_architecture.Rho_f
    Rho_lox = Lander_architecture.Rho_lox
    MR = Lander_architecture.MR
    # q = Lander_architecture.q
    # Rho_tank_f = Lander_architecture.Rho_tank_f
    # Rho_tank_Lox = Lander_architecture.Rho_tank_Lox
    # sigma_max = Lander_architecture.sigma_max
    
    
    md_init = p2d(mp)
    m_prop_init = prop(mp, md_init, Isp, dv)
    # print(m_prop_init)
    mt_init = mp + m_prop_init + md_init
    mpss_init = ss_masses(mp, md_init, md_init, m_prop_init, Lander_architecture, dv)["Propulsion"]
    
    mds = [md_init]
    mprops = [m_prop_init]
    mts = [mt_init]
    mpsss = [mpss_init]
    
    md = md_init
    m_prop = m_prop_init
    mt = mt_init
    # Tsiolkovsky_check(mp+md , mp+md+m_prop, dv, Lander_architecture.Isp) #Tsiolkovsky is fine but md is not
    for i in range(0, 100):
       
        md = ss_masses(mp, md, md_init, m_prop, Lander_architecture, dv)["md_final"] #adjust md
        mpss = ss_masses(mp, md, md_init, m_prop, Lander_architecture, dv)["Propulsion"] 
        m_prop = prop(mp, md, Isp, dv) #adjust m_prop for that md
        mt = mp + m_prop + md #adjust mt
        
        mds.append(md)
        mprops.append(m_prop)
        mts.append(mt)
        mpsss.append(mpss)
        # print(i)
        
        if abs(md - mds[i]) < 1:
            # print(len(mds))
            break
    md_final = mds[len(mds)-1]
    m_prop_final = mprops[len(mprops)-1]
    
    ###
    # convergence(range(0, len(mds)), mds, "iterations", "mds", "convergence check")
    ###
    
    mbm = {"mp":np.round(mp, 2), 
           "md":np.round(md_final, 2), 
           "mprop":np.round(m_prop_final, 2),
           "mt": np.round(mp + md_final + m_prop_final)}
    
    mb_raw = ss_masses(mp, md_final, md_init, m_prop_final, Lander_architecture, dv)
    mb_percent = {"Str          ": np.round((mb_raw["Str"]/mb_raw["md_final"])*100, 2),
                  "Propulsion   ": np.round((mb_raw["Propulsion"]/mb_raw["md_final"])*100, 2), 
                  "Power        ": np.round(( mb_raw["Power"]/mb_raw["md_final"])*100, 2), 
                  "Avionics     ": np.round((mb_raw["Avionics"]/mb_raw["md_final"])*100, 2),
                  "Thermal      ": np.round((mb_raw["Thermal"]/mb_raw["md_final"])*100, 2), 
                  "Other        ": np.round((mb_raw["Other"]/mb_raw["md_final"])*100, 2), 
                  "md_final     ": np.round((mb_raw["md_final"]/mb_raw["md_final"])*100, 2)}
    
    # {"md_init": md_init, "md_final": md_final}, mb_percent, mb_raw, mbm
    
    return mb_percent, mb_raw, mbm, mds, mpsss
    # return mb_raw
 
# #%%
# LM = lander_arch(903, 1450, 1.6, 311, 31, 0)
# Looper(4700, 2500, LM)
#%%
def Lander_sizer(mp, dv, Lander_architecture):
    A, B, C, D, E = Looper(mp, dv, Lander_architecture)
    dry_mass_breakdown = B
    major_mass_breakdown = C
    return lander(C["mp"], C["md"], C["mprop"], C["mt"], B)

#%%
# L_Hy = lander_arch(70.9, 1141, 6, 450, 50, 0)
# test = Lander_sizer(20000, 5000, L_Hy)


