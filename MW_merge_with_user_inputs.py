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
import matplotlib.pyplot as plt
import numpy as np
import cmath as cm

###### Introduction screen and number/type of elements are obtained in this block##################
###################################################################################################
print(30 * '-')
print("WELCOME TO EIS SIMULATOR")
print(30 * '-')
print("Ciruit element codes: ")
print("R: Resistance")
print("C: Capacitance")
print("CPE: Constant Phase Element")
print("W: Warburg impedance")
print(30 * '-')
###########################
## Robust error handling ##
## only accept int 1-4   ##
###########################
## Wait for valid input in while...not ###
is_valid=0
#obtain number of elements user wishes to simulate. keep asking for a number until user inputs interger from 1-4
while not is_valid:
    n_elements = int(input('How many elements would you like to simulate? : '))
    if n_elements >=1 and n_elements <= 4:
      is_valid = 1 ## set it to 1 to validate input and to terminate the while..not loop
    else:
        print(str(n_elements) + " is not a valid integer. \n Please enter an interger value from 1-4")

### obtain type of elements and parameters
element_types = []
params = []
for i in range(1,n_elements+1):
  valid = 0
  while not valid: #ensure user input is only allowed element types R, C, CPE, or W
    ith_element = input('What is element #' + str(i) + '? ')
    if ith_element in ['R','C','CPE','W']:
        valid = 1
    else:
        print(str(ith_element) + " is not a valid input. \n Please choose from R. Resistor, C. Capacitance, CPE. Constant Phase Element, W. Warburg Impedance")
  element_types.append(ith_element)
  if ith_element == 'R':
      r = int(input("Please specify the resitance in Ohms: "))
      params.append(r)
  elif ith_element == 'C':
      c = float(input("Please specify the capacitance in F: "))
      params.append(c)
  elif ith_element == 'CPE':
      ntrue = 0
      q = float(input("Please specify the Q parameter in F: "))
      n = float(input("Please specify the ideality factor n between 0 and 1: "))
      while not ntrue: #ensure that the ideality factor is indeed between 0 and 1 or continue asking for it until it is.
          if n >= 0 and n<=1:
              ntrue = 1
          else:
              print(str(n) + "is not between 0 and 1")
      params.append([q,n])
  else:
    A = float(input("Please specify the area A in cm^2: "))
    D_O = float(input("Please specify the diffusion coefficient of the oxidized species in cm^2/s: "))
    D_R = float(input("Please specify the diffusion coefficient of the reduced species in cm^2/s: "))
    c_O_bulk = float(input("Please specify the bulk concentration of oxidized species in mol/cm^3: "))
    c_R_bulk = float(input("Please specify the bulk concentration of oxidized species in mol/cm^3: "))
    n_el = int(input("Please specify the number of electrons in the redox reaction: "))
    params.append([A,D_O,D_R,c_O_bulk,c_R_bulk,n_el])


lo_hi = 0 #check that the frequency range is correctlye specified
while not lo_hi:
    low_w = float(input("What is the lowest frequency (in Hz) that you'd like to simulate? "))
    high_w = float(input("What is the highest frequency (in Hz) that you'd like to simulate? "))
    if high_w > low_w:
         lo_hi = 1
    else:
         print("Your upper frequency is lower than your lowest frequency, please ensure a proper frequency range.")


w_range = np.logspace(low_w,high_w,5000)
#####object element_types specifies the user defined elements, object params has the corresponding parameters in the same index############
###### For example if element_types[1] is a Warburg impedance, params[1] will be a tuple with (A, D_O, D_R, c_0_bulk, c_R_bulk, n_el)######


print(element_types)
print(params)



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

def Z_CPE(w, params):
    Q = params[0]
    n = params[1]
    Re_Z = (1/(Q*(w**n)))*cm.cos(cm.pi*n/2)
    Im_Z = (-1/(Q*(w**n)))*cm.sin(cm.pi*n/2)*1j
    return Re_Z+Im_Z


# In[5]:


#Warburg impedance
#w is array of rotational frequencies
#A is electrode area
#D_O and D_R are diffusion coefficients for oxidized and reduced species
#c_O_bulk and c_R_bulk are bulk concentrations for oxidized and reduced species

def Z_W(w, params):
    A = params[0]
    D_O = params[1]
    D_R = params[2]
    c_O_bulk = params[3]
    c_R_bulk = params[4]
    n = params[5]
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

el_impedance = []
#take inputs and calculate Z for element type.
for i in range(4):
    if element_types[i] == 'R':
              zi = Z_R(w_range, params[i])
    elif element_types[i] == 'C':
               zi = Z_C(w_range, params[i])

    elif element_types[i] == 'CPE':
               zi = Z_CPE(w_range, params[i])
    else:
               zi = Z_W(w_range, params[i])
    el_impedance.append(zi)
print(el_impedance)
#Sample frequency space
# w = np.logspace(.5,10,100)

#Sample input - two equivalent electrodes and solution resistance
E1 = el_impedance[0]
E2 = el_impedance[1]
E3 = el_impedance[2]
E4 = el_impedance[3]
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
#calc_Z(test_circuit, "circuit")

test_plot = calc_Z(test_circuit, "parallel")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = test_plot.real
y = -test_plot.imag
ax.scatter(x, y)


plt.show()


# In[ ]:
