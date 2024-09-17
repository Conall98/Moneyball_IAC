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

# mpl  = 2000 #kg of payload to be delivered
# dvt = 5800 #total dv of the mission
# destination_type = "orbit"
# data = 1e12 # quantity of data to be returned

# #%%
# mpls = np.random.uniform(1000,2000,20)
# dvls = np.random.uniform(1900, 5800, 20)
# dvtv = 5800 - dvls
# Isps = np.random.uniform(300, 460, 20)


#%% MA space constructor ## lunar lander test case
# costs = []
# MAs = []
# for mpl in mpls:
#     for dvl in dvls:
#         for Isp in Isps:
#             ME2_test = SM.ME(name="lander1", mp=mpl, dv=dvl, Isp=Isp, vehicle_type="lander")
#             mpTV = ME2_test.mtotal_calc()
#             ME1_test = SM.ME(name="TV1", mp=mpTV, dv=5800-dvl, Isp=Isp, vehicle_type="TV", vehicle_ref = SM.TV_Cent)
#             Ma_test = SM.MA(mpl=ME2_test.mp, dv=dvt, destination="surface", data=1e12, ME1=ME1_test, ME2=ME2_test)
            
#             ddte = SM.AMCM(Ma_test)
#             launch = SM.Launchcosts(Ma_test)
#             Aq_cost = ddte + launch
            
#             MAs.append(Ma_test)
#             costs.append(Aq_cost/1000) # in billions
   
            
#%% More comprehensive MA space constructor

### The set-what ###
mp_test = 2000
mpr_test = 2000
dvt_test = 5800
dvl_test = 2000
dvtv_test = dvt_test - dvl_test
dest_test = "surface"
### How-Space ###
LOA = [1, 2, 3, 4] # Level of Autonomy E1, E2, E3, E4
LS = [1, 2] #1 = single launch, 2 = rideshare
RO = [1, 2, 3, 4] #Hohmann, Gravity assist, Low thrust, Lowthrust + grav.assist
COMM = [1, 2, 3] #[DSN, dedicated GS, Leased GS]
DISP = [1, 2, 3] #1 leave in place 2 passive 2nd mission, active 2nd mission
DRS1 = SM.Lrefs # Design Reference Spacecraft 1 = LM style lander, 2, Hydrogen lander 3, Methalox lander
DRS2 = SM.TVrefs # Design Reference Spacecraft #1 = TV_Cent, Ariane, Falcon, DCSS
LRS = SM.Lchrefs # launcher reference
EOL = [1, 2, 3] #1=leave in place, 2=passive 2nd mission, 3=active 2nd mission

# single instance test

# ME2 = SM.ME(name="lander1", mp=mp_test, dv=dvl_test,  vehicle_type="lander", vehicle_ref = DRS1[0])
# ME1 = SM.ME(name="TV1",     mp=ME2.mtotal_calc(),    dv=dvtv_test, vehicle_type="TV",     vehicle_ref = DRS2[0])
# MA_star = SM.MA(mp_test, dvt_test, dest_test, ME1, ME2, traj=RO[0], comms=COMM[0], aut=LOA[0], launcher=LRS[0], EOL=None, ME3=None, ME4=None, data=None)

# ddte = SM.AMCM(MA_star) #millions
# launch = SM.Launchcosts(MA_star) #millions
# Aq_cost = ddte + launch #millions

#combination space

MAs = []
ddte_costs = []
Launch_costs = []
Aq_costs = []
total_masses = []
propellent_masses = []
dry_masses = []
counter = 0
for reference_vehicle_2 in DRS1:
    for reference_vehicle_1 in DRS2:
        ME2 = SM.ME(name="lander1", mp=mp_test, dv=dvl_test,  vehicle_type="lander", vehicle_ref = reference_vehicle_2)
        ME1 = SM.ME(name="TV1",     mp=ME2.mtotal_calc(),    dv=dvtv_test, vehicle_type="TV",     vehicle_ref = reference_vehicle_1)
        print(counter)
        for launcher_choice in LRS:
            for trajectory_choice in RO: #meaningless right now
                for communications_choice in COMM:
                    for autonomy_choice in LOA:
                    
                        MA_star = SM.MA(mp_test, dvt_test, dest_test, ME1, ME2, 
                                traj=RO[0], comms=communications_choice, 
                                aut=autonomy_choice, launcher=launcher_choice, EOL=None, 
                                ME3=None, ME4=None, data=None)
                        MAs.append(MA_star)
                        ddte = SM.AMCM(MA_star) #millions
                        launch = SM.Launchcosts(MA_star) #millions
                        Aq = ddte + launch #millions 
                        # print(launch)
                        # np.append(costs, [[ddte, launch, Aq_cost]], axis = 0)
                        ddte_costs.append(ddte)
                        Launch_costs.append(launch)
                        Aq_costs.append(Aq)
                        
                        total_masses.append(MA_star.mt_imLEO_calc())
                        counter += 1
    
    



#%%
plt.figure()
x = range(0, counter)
plt.plot(x, Launch_costs)
plt.title("launch cost")

plt.figure()
x = range(0, counter)
plt.plot(x, Aq_costs)
plt.title("total cost")

plt.figure()
x = range(0, counter)
plt.plot(x, total_masses)
plt.title("total imLEO")

#%%
plt.figure()
x = range(0, counter)
plt.hist(Aq_costs, bins = 10)
plt.xlabel("system aquisition cost (millions)")
plt.ylabel("# solutions")
plt.title("Space Missions Total Cost")

#%% Intermediate evaluation criteria
# a = Ma_test.md_mission_calc()
# b = Ma_test.mprop_mission_calc()
# c = Ma_test.mt_imLEO_calc()

# interesults = {"Total Mission Dry Mass": a,
#                 "Total mission propellant mass": b,
#                 "total initial mass to LEO": c }

# interesults 


# #%% Cost
# #ddte and launch costs
# ddte = SM.AMCM(Ma_test)
# launch = SM.Launchcosts(Ma_test)
# Aq_cost = ddte + launch
# Aq_cost #in millions