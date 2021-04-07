import matplotlib.pyplot as plt
import numpy as np
import cmath as cm



print(30 * '-')
print("WELCOME TO EIS SIMULATOR")
print(30 * '-')
print("Ciruit element codes: ")
print("R. Resistor")
print("C. capacitor")
print("CPE. Constant Phase Element")
print("W. Warburg impedance")
print(30 * '-')
###########################
## Robust error handling ##
## only accept int 1-4   ##
###########################
## Wait for valid input in while...not ###
is_valid=0
#obtain number of elements user wishes to simulate.
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
  while not valid:
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
      c = int(input("Please specify the capacitance in uF: "))
      params.append(c)
  elif ith_element == 'CPE':
      ntrue = 0
      q = int(input("Please specify the Q parameter: "))
      n = float(input("Please specify the ideality factor n between 0 and 1: "))
      while not ntrue:
          if n >= 0 and n<=1:
              ntrue = 1
          else:
              print(str(n) + "is not between 0 and 1")
      params.append((q,n))
  else:
    A = int(input("Please specify the area A in cm^2: "))
    D_O = float(input("Please specify the diffusion coefficient of the oxidized species in cm^2/s: "))
    D_R = float(input("Please specify the diffusion coefficient of the reduced species in cm^2/s: "))
    c_O_bulk = float(input("Please specify the bulk concentration of oxidized species in mol/cm^3: "))
    c_R_bulk = float(input("Please specify the bulk concentration of oxidized species in mol/cm^3: "))
    n_el = int(input("Please specify the number of electrons in the redox reaction: "))
    params.append((A,D_O,D_R,c_O_bulk,c_R_bulk,n_el))

print(params)

  # if i > 1:
  #   serf = 0
  #   while not serf:
  #       try:
  #           s_p = input('Will it be in series or in parallel to the previous element (s/p)? ')
  #           if s_p in ['s','p']:
  #               serf = 1
  #       except ValueError as e:
  #           print(" '%s' is not series or parallel. Please enter s for a series connection or p for a parallel connection")
  #   connector.append(s_p)




#obtain the required parameters from user. store in dictionary or list?
