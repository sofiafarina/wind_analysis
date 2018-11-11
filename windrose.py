from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

# reading data from dext3r
"""
wd = pd.read_csv("springd.csv", header = None, names = ["uno", "due", "direzioni"])
direzioni = wd["direzioni"]

ws = pd.read_csv("springv.csv", header = None, names = ["uno", "due", "velocità"])
velocità = ws["velocità"]
"""

#%%
# reading data from UniBo stations 

wd = pd.read_table("primavera01.txt", header = None, delim_whitespace=True, names = ["0", "1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19"], dtype = float)
direzioni = wd["9"]
velocità = wd["8"]
total_data = pd.concat([velocità, direzioni], axis=1, names = ["velocità", "direzioni"])
data_cdd = total_data[(total_data["9"] > 0.) & (total_data["9"] < 360.)]
data_cdv = total_data[(total_data["8"] > 0.) & (total_data["8"] < 25.)]

print("************* statistica dati filtrati *************")
print("primavera 01")
print("initial data:", len(total_data))
print("without non physical directions:", len(data_cdd))
print("without non physical velocities:", len(data_cdv))

total_data= total_data[(total_data["9"] > 0.) & (total_data["9"] < 360.) & (total_data["8"] > 0.) & (total_data["8"] < 25.)]
total_data = total_data.reset_index(drop=True)


h = 24 
m = 6
hh = h - 1
hhh = h - 2
mm = m - 1

# filtraggio velocità che non variano 

print("len(velocità)", len(total_data["8"]))
ll = 0
kk = 0 

for i in range(0,len(total_data)):
    if(i>= hh):
        i = i - ll 
    if(len(total_data) < i+h+1): 
        break
    ll = 0
    err = 0
    for j in range(h-1):
        if(np.abs(total_data["8"][i+j]-total_data["8"][i+j+1]) < 0.477): 
            err = err + 1  
    if(err > hhh):
        total_data = total_data.drop(total_data.index[i:i+h])
        total_data = total_data.reset_index(drop=True)
        kk = kk+1
        ll = h

print("without non varying values of velocity", len(total_data))
     

#%%

# filtraggio direzioni costanti 

a = 0
b = 0 
total_data = total_data.reset_index(drop=True)

for i in range(0,len(total_data["9"])):
    if(i >= m):
        i = i - a
    if(len(total_data) < i+m+1):
        break
    a = 0
    er = 0
    for j in range(m):
        if(np.abs(total_data["9"][i+j]-total_data["9"][i+j+1]) < 22.5): 
            er = er + 1         
    if(er >= m):
        #print("sono nell'if", i)
        total_data = total_data.drop(total_data.index[i:i+m])
        total_data = total_data.reset_index(drop=True)
        b = b+1
        a = mm

total_data_filtered = total_data
print("without non varying values of directions", len(total_data["9"]))
        
        
#%%

#production of a txt file 
total_data_filtered.to_csv(r'spring18_2c.txt', header=None, index=None, sep=' ', mode='a')



#%%

ax = WindroseAxes.from_ax()
#ax.contourf(total_data_filtered["9"], total_data_filtered["8"], bins=np.arange(0, 6, 0.5), cmap=cm.BuPu)
ax.contourf(total_data_filtered["9"], total_data_filtered["8"], normed = True, bins=np.arange(0, 6, 0.5), cmap=cm.BuPu)


#ax.contourf(direzioni, velocità, bins=np.arange(0, 6, 0.5), cmap=cm.BuPu) # per farlo con quelli dell'arpae
#ax.contour(direzioni, velocità, bins=np.arange(0, 6, 0.5), colors='black') per avere anche i contorni neri delle varie zone
ax.set_legend()
ax.set_title("spring 2018, 2c")

#%%
# this is to produce the PDF 
from windrose import plot_windrose
df = pd.DataFrame({'speed': total_data_filtered["8"], 'direction': total_data_filtered["9"]})
plot_windrose(df, kind='pdf', bins=np.arange(0.01,8,1), cmap=cm.hot, lw=3, color = "crimson")


#%%

























