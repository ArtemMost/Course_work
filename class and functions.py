from dataclasses import dataclass
import numpy as np
import pandas as pd
import math

def derivative_fi_NFW(R):
    return np.log(1+R)/R**2 - 1/(R*(R+1))

def derivative_fi_psis(R):
    return 1/R-math.atan(R)/R**2

def derivative_fi_kepller(R):
    return 1/R**2

@dataclass
class star:
    r: np.ndarray
    v: np.ndarray
    def esc_velocity(self):
        R = np.linalg.norm(self.r)
        return (2*math.log(1+R)/R)**0.5
    def gravitate_cortesian_rk4(self,prof,dt): #метод рунге-кутта 4 порядка
        r = self.r
        v = self.v
        if prof == 'NFW':
            derivative = derivative_fi_NFW
        if prof =='psis':
            derivative = derivative_fi_psis
        if prof == 'kepller':
            derivative = derivative_fi_kepller
        y = np.array([v,r])
        def f(r,v):
            R = np.linalg.norm(r)
            return np.array([r/R*(-derivative(R)),v])
        k1 = dt*f(r,v)
        k2 = dt*(f(r+k1[0]/2,v+k1[1]/2))
        k3 = dt*(f(r+k2[0]/2,v+k2[1]/2))
        k4 = dt*(f(r+k3[0],v+k3[1]))
        
        k = (k1+2*k2+2*k3+k4)/6
        y+=k
        self.v = y[0]
        self.r = y[1]
        return self
    def gravitate_cortesian(self,prof,dt): #метод эйлера
        if prof == 'NFW':
            derivative = derivative_fi_NFW
        if prof =='psis':
            derivative = derivative_fi_psis
        R = np.linalg.norm(self.r)
        self.v += self.r/R*dt*(-derivative(R))
        self.r += self.v*dt
   


def circ_velocity(prof,r): #круговая скорость 
    if prof == 'NFW':
        derivative = derivative_fi_NFW
    if prof =='psis':
        derivative = derivative_fi_psis
    if prof =='kepller':
        derivative = derivative_fi_kepller
    return (r*derivative(r))**0.5

def los_velocity(v,R,r_centre): #проекция скорости на луч зрения
    r=R+r_centre
    return np.dot(r,v)/np.linalg.norm(r)

def recovered_velocity(v,R,r_centre): #востановленная скорость
    r=R+r_centre
    cos = np.dot(R,r)/np.linalg.norm(r)/np.linalg.norm(R)
    a = math.acos(cos)
    return abs(v/math.sin(a))

    
def cord_generation_cortesian_rk4(stars, prof, T, dt, start_time=0): #генерация координат в фазовом пространстве 
        time=[]
        r=[]
        v=[]
        for i in stars:
            t=T/dt
            k=0
            while k<t:
                time.append(k)
                r.append(i.r)
                v.append(i.v)
                i.gravitate_cortesian_rk4(prof,dt)
                k+=1
               
                t=round(t,6)
            
            data  = pd.DataFrame({'t':time,'r':r,'v':v,}) 
        return data

def cord_generation_cortesian(stars, prof, T, dt):
        data  = pd.DataFrame({'t':[],'r':[],'v':[],'R':[]})
        for i in stars:
            t=0
            k=0
            while t<T:
               
                data.loc[len(data.index)] = [k,list(i.r),list(i.v),np.linalg.norm(i.r)]
                k+=1
                i.gravitate_cortesian(prof,dt)
                t += dt
                t=round(t,6)
                
        return data
    