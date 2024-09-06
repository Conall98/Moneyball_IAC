# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 13:35:01 2024

@author: cdepaor
"""



import numpy as np
import Lander_Sizing_V2 as L
import TV_Sizer as T


#%% reference vehicles
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

#%% 
class wspace():
    def __init__(self, mp, destination, data, mission_life):
        self.mp = mp
        self.dest = destination #just a dv for now. should eventually be an object with destinations each with a possible trajectory below certain TOF
        self.data = data
        self.time = mission_life

#%%

class ME(): #spacecrafts
    def __init__(self, name, mp, dv, Isp, power=None, comms=None, aut=None, vehicle_type=None, vehicle_ref = None):
        self.name = name
        self.mp = mp
        self.dv = dv
        self.Isp = Isp
        self.power = power
        self.comm = comms
        self.type = vehicle_type
        self.ref = vehicle_ref
    
    # method to compute the dry mass of the mission element
    def dry_mass_calc(self): 
        if self.type == "lander": #for landers
            md = L.p2d(self.mp)
            
        elif self.ref is not None: #for transfer vehicles
            if self.type == "TV":
                md = self.ref.md #use ref for simplicity
            
        elif self.ref is not None: #for orbiter type probes
            if self.type == "orbiter":
                md = self.ref.md #use ref for simplicity
        
        else:
            raise ValueError("No vehicle_ref given for Mission element")
        
        return md

    def mprop_calc(self):
        dry_mass = self.dry_mass_calc()
        mprop = L.prop(self.mp, dry_mass, self.Isp, self.dv)
        return mprop
    
    def mtotal_calc(self):
        dry_mass = self.dry_mass_calc()
        prop_mass = self.mprop_calc()
        return dry_mass+prop_mass+self.mp
    
    
#%% System of systems
class MA():
    def __init__(self, mpl, dv, destination, data, ME1, ME2, traj=None, comms=None, aut=None, launcher=None, EOL=None, ME3=None, ME4=None):
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
        md_mission_result = self.ME1.dry_mass_calc() + self.ME2.dry_mass_calc() 
        #additional vehicles
        if self.ME3 is not None:
            md_mission_result = md_mission_result + self.ME3.dry_mass_calc()
            if self.ME4 is not None:
                md_mission_result = md_mission_result + self.ME4.dry_mass_calc()
        
        return int(md_mission_result)
    
    
    def mprop_mission_calc(self):
        #assuming always having at least a TV and a probe or lander
        mprop_mission_result = self.ME1.mprop_calc() + self.ME2.mprop_calc() 
        #additional vehicles
        if self.ME3 is not None:
            mprop_mission_result = mprop_mission_result + self.ME3.mprop_calc()
            if self.ME4 is not None:
                mprop_mission_result = mprop_mission_result + self.ME4.mprop_calc()        
        
        return int(mprop_mission_result)
    
    
    def mt_imLEO_calc(self):
        #assuming always having at least a TV and a probe or lander
        mt_imLEO_result = self.ME1.mtotal_calc() + self.ME2.mtotal_calc() 
        #additional vehicles
        if self.ME3 is not None:
            mt_imLEO_result = mt_imLEO_result + self.ME3.mtotal_calc()
            if self.ME4 is not None:
                mt_imLEO_result = mt_imLEO_result + self.ME4.mtotal_calc()        
        
        return int(mt_imLEO_result)

#%% test case one way lunar mission 

mpl  = 2000 #kg of payload to be delivered
dvt = 5800 #total dv of the mission
destination_type = "orbit"
data = 1e12 # quantity of data to be returned

ME2_test = ME(name="lander1", mp=mpl, dv=2000, Isp=350, vehicle_type="lander")
mpTV = ME2_test.mtotal_calc()
ME1_test = ME(name="TV1", mp=mpTV, dv=3800, Isp=350, vehicle_type="TV", vehicle_ref = TV_Cent)

Ma_test = MA(mpl=ME2_test.mp, dv=dvt, destination="surface", data=1e12, ME1=ME1_test, ME2=ME2_test)


#%% Intermediate evaluation criteria
a = Ma_test.md_mission_calc()
b = Ma_test.mprop_mission_calc()
c = Ma_test.mt_imLEO_calc()

interesults = {"Total Mission Dry Mass": a,
               "Total mission propellant mass": b,
               "total initial mass to LEO": c }

interesults 
# #%%
# TV.md()





#%%
# Lander = ME( mp=mp, dv=dv, Isp=L_Hy.Isp, vehicle_ref = L_Hy, name="lander",vehicle_type="lander")
        

#%% another class for Op_facs



