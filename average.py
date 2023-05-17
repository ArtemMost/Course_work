import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import random
from statistics import mean
from dataclasses import dataclass
import new_kursach
from scipy.optimize import curve_fit
from lmfit import Parameters, minimize, fit_report
from lmfit.models import ExpressionModel
file =f'/home/mostovski/Загрузки/StarSampler-master/StarSampler/circ_stat/circ_stat{99}.csv'
data = pd.read_csv(file)

for k in range(2,100): #усреднение
    file =f'/home/mostovski/Загрузки/StarSampler-master/StarSampler/random_orbit/semicircular/random_orbit_elips{k}.csv'
    data = pd.read_csv(file)
    data=data.sort_values(by=['R'])
  
    r=[]
    v=[]
    j=data.index[0]
    rr=[]
    vv=[]
    for i in data.index:
        if data['R'][i]<data['R'][j]+0.01:
            rr.append(data['R'][i])
            vv.append(data['v_obs'][i])
           
        else:
            r.append(mean(rr))
            v.append(mean(vv))
            rr=[data['R'][i]]
            vv=[data['v_obs'][i]]
            j=i
    sorted_data=pd.DataFrame({'R':np.array(r),'v_obs':np.array(v)})

    sorted_data.to_csv(f'/home/mostovski/Загрузки/StarSampler-master/StarSampler/random_orbit/semicircular/random_orbit_elips_sorted{i}.csv')