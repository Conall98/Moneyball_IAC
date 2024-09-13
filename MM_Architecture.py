# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 13:58:08 2024

@author: cdepaor
"""

import numpy as np
import Lander_Sizing_V2 as L
import TV_Sizer as T
import SM_Architecture as SM
import matplotlib.pyplot as plt

#%% input sheet

mpl  = 2000 #kg of payload to be delivered
dvt = 5800 #total dv of the mission
destination_type = "orbit"
data = 1e12 # quantity of data to be returned

#%%
mpls = np.random.uniform(1000,2000,20)
dvls = np.random.uniform(1900, 5800, 20)
dvtv = 5800 - dvls
Isps = np.random.uniform(300, 460, 20)


#%% MA space constructor ## lunar lander test case
costs = []
MAs = []
for mpl in mpls:
    for dvl in dvls:
        for Isp in Isps:
            ME2_test = SM.ME(name="lander1", mp=mpl, dv=dvl, Isp=Isp, vehicle_type="lander")
            mpTV = ME2_test.mtotal_calc()
            ME1_test = SM.ME(name="TV1", mp=mpTV, dv=5800-dvl, Isp=Isp, vehicle_type="TV", vehicle_ref = SM.TV_Cent)
            Ma_test = SM.MA(mpl=ME2_test.mp, dv=dvt, destination="surface", data=1e12, ME1=ME1_test, ME2=ME2_test)
            
            ddte = SM.AMCM(Ma_test)
            launch = SM.Launchcosts(Ma_test)
            Aq_cost = ddte + launch
            
            MAs.append(Ma_test)
            costs.append(Aq_cost/1000) # in billions
            
#%%
#plt.figure()
#x = MAs
#plt.plot()

#%% Intermediate evaluation criteria
a = Ma_test.md_mission_calc()
b = Ma_test.mprop_mission_calc()
c = Ma_test.mt_imLEO_calc()

interesults = {"Total Mission Dry Mass": a,
                "Total mission propellant mass": b,
                "total initial mass to LEO": c }

interesults 


#%% Cost
#ddte and launch costs
ddte = SM.AMCM(Ma_test)
launch = SM.Launchcosts(Ma_test)
Aq_cost = ddte + launch
Aq_cost #in millions