#!/usr/bin/env python
# coding: utf-8

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
inputs_dict = {}
circuits_dict = {}

E1 = "E1"
E2 = "E2"
E3 = "E3"
E4 = "E4"


# In[7]:


#Possible inputs for 4 elements
inputs_4 =[["E1+E2+E3+E4"],
          ["E1+E2+para(E3,E4)", "E1+para(E2,E3)+E4", "para(E1,E2)+E3+E4"],
          ["E1+para(E2,E3,E4)", "para(E1,E2,E3)+E4"],
          ["E1+para(para(E2,E3),E4)", "E1+para(E2,para(E3,E4))", "para(para(E1,E2),E3)+E4", "para(E1,para(E2,E3))+E4"],
          ["E1+para(E2+E3,E4)", "E1+para(E2,E3+E4)","para(E1+E2,E3)+E4", "para(E1,E2+E3)+E4"],
          ["para((E1+E2),(E3+E4))"],
          ["para((E1+E2+E3),E4)", "para(E1,(E2+E3+E4))"],
          ["para(E1,E2)+para(E3,E4)"],
          ["para(para(E1,E2),para(E3,E4))"],
          ["para(E1,E2,E3,E4)"],
          ["para(E1,E2,(E3+E4))","para(E1,(E2+E3),E4)", "para((E1+E2),E3,E4)"],
          ["para((E1+E2),para(E3,E4))","para(para(E1,E2)(E3+E4),)"]]


#Corresponding circuit array
#First value in each array is 0(series) or 1(parallel)
circuits_4 = [[0, [E1,E2,E3,E4]],
            [0,[E1,E2,[1,[E3,E4]]]],
            [0, [E1,[1,[E2,E3,E4]]]],
            [0,[E1,[1,[[1,[E2,E3]],E4]]]],
            [0,[E1,[1,[[0,[E2,E3]],E4]]]],
            [1,[[0,[E1,E2]],[0,[E3,E4]]]],
            [1,[[0,[E1,E2,E3]],E4]],
            [1,[[1,[E1,E2]],[1,[E3,E4]]]],
            [0,[[1,[E1,E2]],[1,[E3,E4]]]],
            [1,[E1,E2,E3,E4]],
            [1,[E1,E2,[0,[E3,E4]]]],
            [1,[[0,[E1,E2]],[1,[E1,E2]]]]]

#Add all to the dictionaries
for count, array in enumerate(circuits_4):
    circuits_dict["4_"+str(count+1)]=circuits_4[count]
    
for count,array in enumerate(inputs_4):
    inputs_dict["4_"+str(count+1)]=inputs_4[count]


# In[8]:


#Possible inputs for 3 elements
inputs_3 = [["E1+E2+E3"],
            ["E1+para(E2,E3)","para(E1,E2)+E3"],
            ["para(para(E1,E2),E3)","para(E1,para(E2,E3))"],
            ["para(E1+E2,E3)","para(E1,E2+E3)"],
            ["para(E1,E2,E3)"]]

#Corresponding circuit array
#First value in each array is 0(series) or 1(parallel)
circuits_3 = [[0,[E1,E2,E3]],
              [0,[E1,[1,[E2,E3]]]],
              [1,[E1,[0,[E2,E3]]]],
              [1,[E1,[1,[E2,E3]]]],
              [1,[E1,E2,E3]]]
              
for count, array in enumerate(circuits_3):
    circuits_dict["3_"+str(count+1)]=circuits_3[count]
    
for count,array in enumerate(inputs_3):
    inputs_dict["3_"+str(count+1)]=inputs_3[count]


# In[9]:


#Possible inputs for 2 elements
inputs_2 = [["E1+E2"],
            ["para(E1,E2)"]]

circuits_2 = [[0,[E1,E2]],
              [1,[E1,E2]]]

for count, array in enumerate(circuits_2):
    circuits_dict["2_"+str(count+1)]=circuits_2[count]
    
for count,array in enumerate(inputs_2):
    inputs_dict["2_"+str(count+1)]=inputs_2[count]


# In[10]:


#Possible inputs for 1 element
inputs_1 = [["E1"]]

circuits_1 = [[1,E1]]

for count, array in enumerate(circuits_1):
    circuits_dict["1_"+str(count+1)]=circuits_1[count]
    
for count,array in enumerate(inputs_1):
    inputs_dict["1_"+str(count+1)]=inputs_1[count]


# ## Logic Loop Functions for Adding Impedances in Element Array

# In[11]:


#Translate the user input string into one of the preset circuit arrays
def input_to_circuit(input_dict, input_string):
    key = 0
    for i in input_dict:
        for j in input_dict[i]:
            if input_string in j:
                key = i
    return circuits_dict[key]


# In[12]:


#Fill the preset circuit arrays with the user input elements
def element_values(circuit, elements):
    circuit_w_values = circuit
    for a,b in enumerate(circuit_w_values):
        if type(b) == str:
            circuit_w_values[a]=elements[int(b[1])-1]
        elif type(b) == list:
            element_values(b, elements)
    return circuit_w_values
            


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


#Count the number of nested elements in the circuit
#Excluding the overall circuit itself

def count(l):
    if isinstance(l, np.float64):
        return 0
    else:
        return sum(1+count(i) for i in l if isinstance(i,list))


# Logic loop for calculating total impedance from array of impedances, not working

# In[33]:


def calc_Z(circuit):
    #Check level 1 (overall circuit)
    for i,element in enumerate(circuit[1]):
        while count(element)!=0:
            if count(element)==1:
                if circuit[0]==0:
                    x = add_series_Z(circuit[1][1])#the second subscribt may need to be i, not 1
                elif circuit[0]==1:
                    x = add_parallel_Z(circuit[1][1])
                element = x
            else:
                calc_Z(circuit[1][i])
                
                
    return circuit


# Step by step logic loop, need to translate this to a function

# ## Testing the Code

# In[18]:


#Sample frequency space
w = np.logspace(.5,10,1000)

#Sample input - two equivalent electrodes and solution resistance
test_input = "E1+para(E2,E3+E4)"
E1 = Z_R(w,20)
E2 = Z_CPE(w,20e-6,0.8)
E3 = Z_R(w,10)
E4 = Z_W(w, .2, 1e-5, 1.5e-5, 1, 2, 1)

elements = [E1,E2,E3,E4]

circuit_config = input_to_circuit(inputs_dict,test_input)
circuit = element_values(input_to_circuit(inputs_dict,test_input),elements)


# In[ ]:




