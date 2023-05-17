import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import random
from dataclasses import dataclass
import new_kursach

k=0
while k<=100:
    x=random.uniform(0,0.71)
    y=random.uniform(0,0.71)
    vx=random.uniform(0,0.6)
    vy=random.uniform(0,0.6)
    t=10
    s=star(np.array([x,y,.0],dtype=np.float64),np.array([vx,vy,.0],dtype=np.float64))
    if np.linalg.norm(s.v) < s.esc_velocity():
        data = cord_generation_cortesian_rk4([s],'NFW',t,0.00001)
        data.to_csv(f"/home/mostovski/Загрузки/StarSampler-master/StarSampler/elip/large_elips{k}.csv")
        k+=1
