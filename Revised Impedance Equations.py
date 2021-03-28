#!/usr/bin/env python
# coding: utf-8

# In[154]:


import numpy as np
import cmath as cm
import matplotlib.pyplot as plt


# In[155]:


#Resistor
#w is array of rotationalfrequencies
#R is resistance

def Z_R(w, R):
    Re_Z = np.full(len(w), R)  
    Im_Z = np.zeros(len(w))
    return Re_Z+Im_Z


# In[156]:


#Capacitor
#w is array of rotational frequencies
#C is capacitance

def Z_C(w, C):
    Re_Z = np.zeros(len(w))
    Im_Z = -1/(w*C)*1j 
    return Re_Z+Im_Z


# In[157]:


#Constant phase element
#w is array of rotational frequencies
#n is a number between 0 and 1 (Simplifies to an ideal capacitor when n=1)

def Z_CPE(w, Q, n):
    Re_Z = (1/(Q*w**n))*cm.cos(cm.pi*n/2)  
    Im_Z = (-1/(Q*w**n))*cm.sin(cm.pi*n/2)*1j
    return Re_Z+Im_Z


# In[158]:


#Warburg impedance
#w is array of rotational frequencies
#A is electrode area
#D_O and D_R are diffusion coefficients for oxidized and reduced species
#c_O_bulk and c_R_bulk are bulk concentrations for oxidized and reduced species

def Z_W(w, A, D_O, D_R, c_O_bulk, c_R_bulk, n):
    R = 8.314 #J/K•mol
    F = 96485 #C/mol
    T = 298 #K
    sigma = (R*T/((n*F)**2*A*2**0.5)*((1/D_O**0.5/c_O_bulk)+(1/D_R**0.5/c_R_bulk)))
    Re_Z = sigma/w**0.5
    Im_Z = -sigma/w**0.5
    return Re_Z+Im_Z


# ### Adding Impedances

# In[181]:


def add_two_impedances(E1, E2, config):
    if config == "parallel":
        return 1/((1/E1)+(1/E2))
    elif config == "series":
        return E1+E2


# ### Plotting to Verify Results

# In[182]:


#Frequency array
w = np.logspace(.5,10,1000)


# In[183]:


#Testing ideal capacitor in parallel with resistor (semicircle)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = total_Z.real
y = -total_Z.imag
ax.scatter(x, y)
plt.show()


# In[184]:


total_Z = add_two_impedances2(Z_CPE(w, 2e-6, .8), Z_R(w, 2),"parallel")


# In[185]:


#testing CPE in parallel with resistor (depressed semicircle)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = total_Z.real
y = -total_Z.imag
ax.scatter(x, y)
plt.show()

