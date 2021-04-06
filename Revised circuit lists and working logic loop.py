#!/usr/bin/env python
# coding: utf-8

# ### Possible order of steps:
# 1. User picks an configuration input, which returns an image dictionary key
# 2. User inputs parameters for E1-E4, which call those functions and returns numpy arrays stored as variables E1-E4
# 3. Image dictionary key is used with the circuit dictionary to obtain a circuit list, which is already populated with the numpy arrays from step 2
# 4. Use calc_Z logic loop to calculate the impedance from that circuit list, returning a single numpy array with the same length as the frequency list
# 5. Combine the frequency list with the calculated impedance list
# 6. Graph

# In[1]:


import numpy as np
import cmath as cm
import matplotlib.pyplot as plt
import re


# ## Calculating Individual Element Impedances
# Able to take a frequency range, element type, and relevant parameters from user input and create an array of impedances for each frequency value

# In[2]:


#Resistor
#w is array of rotationalfrequencies
#R is resistance

def Z_R(w, R):
    Re_Z = np.full(len(w), R)  
    Im_Z = np.zeros(len(w))
    return Re_Z+Im_Z


# In[3]:


#Capacitor
#w is array of rotational frequencies
#C is capacitance

def Z_C(w, C):
    Re_Z = np.zeros(len(w))
    Im_Z = -1/(w*C)*1j 
    return Re_Z+Im_Z


# In[4]:


#Constant phase element
#w is array of rotational frequencies
#n is a number between 0 and 1 (Simplifies to an ideal capacitor when n=1)

def Z_CPE(w, Q, n):
    Re_Z = (1/(Q*w**n))*cm.cos(cm.pi*n/2)  
    Im_Z = (-1/(Q*w**n))*cm.sin(cm.pi*n/2)*1j
    return Re_Z+Im_Z


# In[5]:


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
    Im_Z = -sigma/w**0.5*1j
    return Re_Z+Im_Z


# ## Converting Input String to Circuit Array
# 
# - Read the user input string using the user friendly format of para()
# - Each possible user input is tied to a preset array using a code friendly format
# - The array is filled with impedance arrays that draw directly from the separately inputed values of E_i
# 
# Rules for user input:
# - The elements should follow numerical order (don't write E2 + E1, write E1 + E2)
# - Only use parenthesis to surround elements in parallel
# - Within para(), the comma separates the parallel elements, taking precedence over other notation like+
# 

# In[6]:


#Input/circuit dictionary
circuits_dict = {}

#Sample frequency space
w = np.logspace(.5,10,100)

#Sample input - two equivalent electrodes and solution resistance
E1 = Z_R(w,20)
E2 = Z_W(w, .2, 1e-5, 1.5e-5, 1, 2, 1)
E3 = Z_R(w,10)
E4 = Z_CPE(w,20e-6,0.8)
elements = [E1,E2,E3,E4]




# In[7]:


#Possible circuits for 4 elements

circuits_4 = [[[E1,E2,E3,E4]],
              [[E1,E2,(E3,E4)]],
              [[E1,([E2,E3],E4)]],
              [(E1,[E2,E3,E4])],
              [([E1,E3],[E2,E4])],
              [[(E1,E2),(E3,E4)]],
              [([E1,(E2,E3)],E4)],
              [[E1,(E2,E3,E4)]],
              [([E1,E2],E3,E4)],
              [(E1,E2,E3,E4)]]

#Add all to the dictionaries
for count, array in enumerate(circuits_4):
    circuits_dict["4_"+str(count+1)]=circuits_4[count]


# In[8]:


#Possible inputs for 3 elements
circuits_3 = [[[E1,E2,E3]],
             [[E1,(E2,E3)]],
             [([E1,E2],E3)],
             [(E1,E2,E3)]]
              
for count, array in enumerate(circuits_3):
    circuits_dict["3_"+str(count+1)]=circuits_3[count]
    


# In[9]:


#Possible inputs for 2 elements
circuits_2 = [[[E1,E2]],
            [(E1,E2)]]

for count, array in enumerate(circuits_2):
    circuits_dict["2_"+str(count+1)]=circuits_2[count]


# In[10]:


#Possible inputs for 1 element
circuits_1 = [[E1]]

for count, array in enumerate(circuits_1):
    circuits_dict["1_"+str(count+1)]=circuits_1[count]


# ## Logic Loop Functions for Adding Impedances in Element Array

# In[13]:


#Function for adding impedances in series
def add_series_Z(elements):
    return np.sum(elements,axis=0)    


# In[14]:


#Function for adding impedances in parallel
def add_parallel_Z(elements):
    inv_elements = []
    for i in elements:
        inv_elements.append(1/i)
    return 1/(np.sum(inv_elements, axis=0))


# In[15]:


def calc_Z(input_circuit, config):
    circuit = input_circuit
    #Tuple can't be modified so create a dummy list to store calculations
    dummy_circuit = []
    #while not all(isinstance(x, np.ndarray) for x in dummy_circuit):
    for i, feature in enumerate(circuit):
        if isinstance(feature, np.ndarray):
            dummy_circuit.append(feature)
        elif isinstance(feature, list):
            if all(isinstance(circuit, np.ndarray) for i in feature):
                dummy_circuit.append(add_series_Z(feature))
            else:
                dummy_circuit.append(calc_Z(feature, "series"))
        elif isinstance(feature, tuple):
            if all(isinstance(circuit, np.ndarray) for i in feature):
                dummy_circuit.append(add_parallel_Z(feature))
            else:
                dummy_circuit.append(calc_Z(feature, "parallel"))
    if config == "parallel":
        return add_parallel_Z(dummy_circuit)
    elif config == "series":
        return add_series_Z(dummy_circuit)
    


# ## Testing the Code

# In[35]:


test_circuit = circuits_dict["4_10"]
calc_Z(test_circuit, "circuit")

test_plot = calc_Z(test_circuit, "series")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = test_plot.real
y = -test_plot.imag
ax.scatter(x, y)
#plt.xlim([0,.01])
#plt.ylim([0,1])


plt.show()


# In[ ]:




