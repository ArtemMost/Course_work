import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import random
from statistics import mean
from dataclasses import dataclass
import new_kursach

r_centre=np.array([0,1000,0])

V_theor=[]
R=[]
V=[]
r_stat=[]
v_stat=[]
for k in range(0,50): #расчет наблюдаемых величин
    file = f'/home/mostovski/Загрузки/StarSampler-master/StarSampler/elip/elips{k}.csv'
    data = pd.read_csv(file)
    for i in range(int(8*len(data['t'])/10),int(9*len(data['t'])/10)):
        read_r=np.array(list(map(float,data['r'][i][1:-1].split())))
        read_v=np.array(list(map(float,data['v'][i][1:-1].split())))
        r = abs(read_r[0])*r_centre[1]/(read_r[1]+r_centre[1])
        if r<1:
            v_obs=recovered_velocity(los_velocity(read_v,read_r,r_centre),read_r,r_centre)
            v_theor=circ_velocity('NFW',r)
            R.append(r)
            V.append(v_obs)

data_obs = pd.DataFrame({'R':np.array(R),'v_obs':np.array(V),'V':np.array(V_theor)})

for i in range(0,100): #выбор случайных звёзд для последующего анализа
    for c in range(i):
        j = random.choice(data_obs.index)
        r_stat.append(data_obs['R'][j])
        v_stat.append(data_obs['v_obs'][j])
        
    data_stat = pd.DataFrame({'R':np.array(r_stat),'v_obs':np.array(v_stat)})
    data_stat.to_csv(f'/home/mostovski/Загрузки/StarSampler-master/StarSampler/random_orbit/semicircular/random_orbit_elips{i}.csv')
    r_stat=[]
    v_stat=[]

 
ax=data_obs.plot(x = 'R',y = 'v_obs',color='Green', kind='scatter')
data_obs.plot(x='R',y='V',color='Red',kind='scatter',ax=ax)

