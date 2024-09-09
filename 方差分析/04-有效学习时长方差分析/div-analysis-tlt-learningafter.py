# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
from scipy.stats import f

# data = pd.DataFrame(pd.read_excel("D:/匹配/learningtimeafter.xlsx"))
data = pd.DataFrame(pd.read_excel("learningtimeafter.xlsx"))
print(len(data.columns))
print(len(data.index))

r = 2

data0=data[data['D']==0]
Sd0=data0.iloc[:,3]
n0 = len(Sd0)

data1=data[data['D']==1]
Sd1=data1.iloc[:,2]
n1 = len(Sd1)

X_mean = []

Sd0_mean = sum(Sd0)/len(Sd0)
X_mean.append(Sd0_mean)

Sd1_mean = sum(Sd1)/len(Sd1)
X_mean.append(Sd1_mean)

Xm = sum(X_mean)/len(X_mean)

Sb2=0
Sb2=n0*(X_mean[0]-Xm)**2+n1*(X_mean[1]-Xm)**2

Sw2 = 0
for i in range(n0):
    Sw2 = Sw2 + (data0.iloc[i][3]-Sd0_mean)**2
        
for i in range(n1):
    Sw2 = Sw2 + (data1.iloc[i][2]-Sd1_mean)**2
    
F = (Sb2/(r-1))/(Sw2/(n0+n1-r))
print(F)

fenwei = f.isf(q=0.05, dfn=r-1, dfd=n0+n1-r)
print(fenwei)

if F>fenwei:
    print("There is a significant difference")
    ATE=Sd1_mean-Sd0_mean
    print("ATE=",ATE)
else:
    print("There is no significant difference")
    
