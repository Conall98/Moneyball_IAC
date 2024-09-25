# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 13:35:01 2024

@author: cdepaor
"""



import numpy as np
import Lander_Sizing_V2 as L
import TV_Sizer as T
import cost_functions as c


#%% reference vehicles
LM = L.lander_arch(903, 1450, 1.6, 311, 31, 0, "LM") # Lunar module equivalent
L_Hy = L.lander_arch(70.9, 1141, 6, 450, 50, 0, "LOX/LH2") # LOX/LH2 lander, TW from scaled RL-10C
L_Me = L.lander_arch(422.4, 1141, 3.5, 350, 140, 0, "LOX/CH4") #LOX/LCH4 ladnder, TW from Raptor 2

Lrefs = [LM, L_Hy, L_Me]

#TV_arch = TV.arch(ek, Isp, md, m_prop, ref)
TV_Cent = T.TV_arch(9.7e+10, 451, 2462, 20830, "Centaur")
TV_Aria = T.TV_arch(6.62e+10, 446, 4540, 14700, "Ariane 5 2S")
TV_Falc = T.TV_arch(3.48e+11, 348, 3900, 92670, "Falcon 9 2S")
TV_DCSS = T.TV_arch(1.36e+11, 462, 3490, 27200, "DCSS")

TVrefs = [TV_Cent, TV_Aria, TV_Falc, TV_DCSS]

FH = T.Launcher(63800, 97, "Falcon Heavy") #payload to leo, name
# SLS = T.Launcher(95000, 2500, "Space Launch System")
#Vega C
Vega = T.Launcher(2500, 37, "Vega") #payload to leo, name
#Ariane 6
Ariane62 = T.Launcher(10350, 70, "Ariane A62")
Ariane64 = T.Launcher(21650, 115, "Ariane A64")
#Falcon 9
Falcon9 = T.Launcher(22800, 70, "Falcon 9")
#Electron
Electron = T.Launcher(320, 7.5, "Electron")
#Atlas V 551
AltasV = T.Launcher(18850, 153, "AtlasV")
#firefly alpha
Firefly = T.Launcher(1030, 17.6, "Firefly")
#Vulcan
Vulcan = T.Launcher(21650, 150, "Vulcan")
#angara
Angara = T.Launcher(24500, 100, "Angara")
#soyuz 2
Soyuz = T.Launcher(8200, 80, "Soyuz 2b")

Lchrefs = [FH, Vega, Ariane62, Ariane64, Falcon9, Electron, AltasV, Firefly, Vulcan, Angara, Soyuz]
#%% 
class wspace():
    def __init__(self, mp, destination, data, mission_life):
        self.mp = mp
        self.dest = destination #just a dv for now. should eventually be an object with destinations each with a possible trajectory below certain TOF
        self.data = data
        self.time = mission_life

#%%

class ME(): #spacecrafts
    def __init__(self, name, mp, dv, power=None, comms=None, aut=None, vehicle_type=None, vehicle_ref = None):
        self.name = name
        self.mp = mp
        self.dv = dv
        # self.Isp = Isp
        self.power = power
        self.comm = comms
        self.type = vehicle_type
        self.ref = vehicle_ref
    
    # method to compute the dry mass of the mission element
    def dry_mass_calc(self): 
        if self.type == "lander": #for landers
            Lander_star = L.Lander_sizer(self.mp, self.dv, self.ref)
            md = Lander_star.md
            

        elif self.type == "TV":#for transfer vehicles
            md = self.ref.md #use ref for simplicity
            

        elif self.type == "orbiter":
            md = self.ref.md #use ref for simplicity
        
        else:
            raise ValueError("No vehicle_type given for Mission element")
        
        return md
    
    # retrieving Isp from design reference
    

    def mprop_calc(self):
        dry_mass = self.dry_mass_calc()
        Isp = self.ref.Isp
        mprop = L.prop(self.mp, dry_mass, Isp, self.dv)
        return mprop
    
    def mtotal_calc(self):
        dry_mass = self.dry_mass_calc()
        prop_mass = self.mprop_calc()
        return dry_mass+prop_mass+self.mp
    
    def dmb(self):
        Lander_star = L.Lander_sizer(self.mp, self.dv, self.ref)
        return Lander_star.dry_mass_breakdown
    
#%% System of systems
class MA():
    def __init__(self, mpl, dv, destination, ME1, ME2=None, ME3=None, ME4=None, traj=None, comms=None, aut=None, launcher=None, EOL=None, data=None):
        self.mpl = mpl            # payload mass
        self.dv = dv            # mission delta-v 
        self.dest = destination # surface or orbit
        self.traj = traj        # trajectory
        self.data = data        # data handling system
        self.comms = comms      # optional communications system
        self.aut = aut          # optional autonomy system
        self.launcher = launcher # optional launcher information
        self.EOL = EOL          # optional end of life information
        self.ME1 = ME1          # transfer vehicle
        self.ME2 = ME2          # probe reference vehicle
        self.ME3 = ME3          # additional transfer vehicle
        self.ME4 = ME4          # additional transfer vehicle
    
    def md_mission_calc(self):
        #assuming always having at least a TV and a probe or lander
        md_mission_result = self.ME1.dry_mass_calc()
        #additional vehicles
        if self.ME2 is not None:
            md_mission_result = md_mission_result + self.ME2.dry_mass_calc()    
            if self.ME3 is not None:
                md_mission_result = md_mission_result + self.ME3.dry_mass_calc()
                if self.ME4 is not None:
                    md_mission_result = md_mission_result + self.ME4.dry_mass_calc()
        
        return int(md_mission_result)
    
    
    def mprop_mission_calc(self):
        #assuming always having at least a TV and a probe or lander
        mprop_mission_result = self.ME1.mprop_calc()
        #additional vehicles
        if self.ME2 is not None:
            mprop_mission_result = mprop_mission_result + self.ME2.mprop_calc()
            if self.ME3 is not None:
                mprop_mission_result = mprop_mission_result + self.ME3.mprop_calc()
                if self.ME4 is not None:
                    mprop_mission_result = mprop_mission_result + self.ME4.mprop_calc()        
        
        return int(mprop_mission_result)
    
    
    def mt_imLEO_calc(self):
        #assuming always having at least a TV and a probe or lander
        mt_imLEO_result = self.ME1.mtotal_calc()
        #additional vehicles
        if self.ME2 is not None:
            mt_imLEO_result = mt_imLEO_result + self.ME2.mtotal_calc()
            if self.ME3 is not None:
                mt_imLEO_result = mt_imLEO_result + self.ME3.mtotal_calc()
                if self.ME4 is not None:
                    mt_imLEO_result = mt_imLEO_result + self.ME4.mtotal_calc()        
        
        return int(mt_imLEO_result)
    



#%%
def link(d, R, Gt, Pt, f):
    # gain of reciever --> dia of dish --> cost of ground station equipment + lease / building purcahse
    EbNo = 12.6 #dB
    T = 135 #K
   
    lam = 299792458/f #in meters
    
    Ls = 20*np.log10(4*np.pi*d/lam)
    
    Pt = 10*np.log10(Pt)
    Gr = EbNo - Pt + Ls - Gt - 228.6 + 10*np.log10(T) + 10*np.log10(R)
    # print(Ls)
    # print(10*np.log10(T))
    D = (((10**(Gr/10))/(6))*lam**2)**0.5
    
    return D

#%% AMCM
def AMCM(MA):
    a = MA.md_mission_calc()
    # print(a)
    
    #AMCM coefficients
    A = 5.65*10e-4
    B = 0.5941
    C = 0.6604
    D = 80.599
    E = 3.8085*10e-55
    F = -0.3553
    G = 1.5691
    #specification value for AMCM
    S = 2.39  #planetary
    
    Q = 1 #quantity 
    M = a*2.2 #dry mass in pounds
    IOC = 2024 #initial year of operation
    Bl = 2 #iteration of the design
    Di = 0
    
    
    AD_C = A*(Q**B)*(M**C)*(D**S)*(E**(1/(IOC-1900)))*(Bl**F)*(G**Di)
    
    ### dedicated GroundSegment ###
    d = 385000000 # should be a param of MA in the destination object
    R = 10e6 # should be a param of MA in the data object
    Gt = 24 #dB typical (high)
    Pt = 300 #W
    f = 3e9 #s-band
    
    D = link(d, R, Gt, Pt, f)
    GS_equip = (650*D + 350*20 + 1550)/1000 #SMAD pg 730 FY92 in M€
    GS_equip = GS_equip*1.84 # FY2020
    GS_FAC = (18/81)*GS_equip # from table 20.3 in SMAD sized FAC from equip
    
    GS_C = GS_FAC + GS_equip
    
    ### wrap up ###
    
    # print("acquisition (M$)", int(AD_C))
    # print("ground station (M$)", int(GS_C))
    # print("ground station dish diameter (m)", int(D))
    # print("ground station equipment (M$)", int(GS_equip))
    # print("ground station facility (M$)", int(GS_FAC))
    C = AD_C+GS_C
    
    
    return int(C) #returns k$
    
#%% 
def Launchcosts(MA):

    c = MA.mt_imLEO_calc()
    Launcher = MA.launcher
    
    #should have a launcher in the MA
    
    SLC = Launcher.slc() #specific launch cost
    # print(SLC, c)
    # return SLC*c
    return Launcher.cost

#%% TP derived Cost function
def TP(MA):
    a = MA.ME1.dmb()
    str_c = c.structure(a["Str"])
    prpl_c = c.motor((a["Propulsion"])*(77/313))+c.tanks((a["Propulsion"])*(236/313))
    power_c = c.power(a["Power"])
    avio_c = c.avionics(a["Avionics"])
    therm_c = c.thermal(a["Thermal"])
    ADCS_c = c.other(a["Other"])
    
    acq_cost = str_c + prpl_c + power_c + avio_c + therm_c + ADCS_c
    acq_cost = acq_cost/0.69 # the system integration factor present in TP
    
    return acq_cost

# %%
# i = 4250
# # MA_dict(MAs[i], i)

# TP(MAs[i])
#%%
# i = 152
# Ma_test = MAs[i]
# #%% Cost
# # ddte and launch costs
# ddte = AMCM(Ma_test)
# launch = Launchcosts(Ma_test)
# Aq_cost = ddte + launch
# Aq_cost #in millions
    
    
    
    
    
    
    
    
    
    
    

