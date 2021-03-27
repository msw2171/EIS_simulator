#!/usr/bin/env python
# coding: utf-8

# First draft of code for the impedance of each of the individual elements. Each function takes in an array of rotational frequencies and relevant parameters, then returns a 2D array with a column for both the real and imaginary impedances

# In[149]:


import numpy as np
import math
import matplotlib.pyplot as plt


# In[150]:


#Resistor
#w is array of rotationalfrequencies
#R is resistance

def Z_R (w, R):
    Re_Z = R + w*0  
    Im_Z = 0*w
    return np.vstack([Re_Z, Im_Z])


# In[151]:


#Capacitor
#w is array of rotational frequencies
#C is capacitance

def Z_C (w, C):
    Re_Z = 0*w 
    Im_Z = -1/(w*C)
    return np.vstack([Re_Z, Im_Z])


# In[152]:


#Constant phase element
#w is array of rotational frequencies
#n is a number between 0 and 1 (Simplifies to an ideal capacitor when n=1)

def Z_CPE(w, Q, n):
    Re_Z = (1/(Q*w**n))*math.cos(math.pi*n/2)  
    Im_Z = (-1/(Q*w**n))*math.sin(math.pi*n/2)
    return np.vstack([Re_Z, Im_Z])


# In[153]:


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
    return np.vstack([Re_Z, Im_Z])


# Plotting each of the functions just to verify they produce the expected graphs

# In[154]:


#Frequency array
w = np.logspace(.5,10,1000)


# In[155]:


#Testing resistance
R_impedance = Z_R(w,10)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = Z_R(w,10)[0,:]
y = Z_R(w,10)[1,:]
ax.scatter(x, y)
plt.show()

R_impedance


# In[174]:


# Testing Capacitance
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = Z_C(w,20e-6)[0,:]
y = -Z_C(w,20e-6)[1,:]
ax.scatter(x, y)
plt.show()


# In[183]:


#Testing CPE
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = Z_CPE(w, 20e-6, 0.8)[0,:]
y = -Z_CPE(w, 20e-6, 0.8)[1,:]
ax.scatter(x, y)
plt.show()


# In[180]:


#Testing warburg impedance
warburg = Z_W(w, 2, .0005, 0.0005, 1, 1, 1)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = warburg[0,:]
y = -warburg[1,:]
ax.scatter(x, y)
plt.show()


# In[ ]:




