import matplotlib.pyplot as plt
import numpy as np
import cmath as cm
import 



print (30 * '-')
print ("WELCOME TO EIS SIMULATOR")
print (30 * '-')
print("Ciruit element codes: ")
print ("R. Resistor")
print ("C. capacitor")
print ("CPE. Constant Phase Element")
print("W. Warburg impedance) 
print (30 * '-')
###########################
## Robust error handling ##
## only accept int 1-4   ##
###########################
## Wait for valid input in while...not ###
is_valid=0
#obtain number of elements user wishes to simulate.
while not is_valid :
        try :
                n_elements = int ( raw_input('How many elements would you like to simulate? : ') )
                if n_elements >= 1 and <= 4:
                  is_valid = 1 ## set it to 1 to validate input and to terminate the while..not loop
        except ValueError, e :
                print ("'%s' is not a valid integer. Please enter an interger value from 1-4" % e.args[0].split(": ")[1])
 
### obtain type of elements and their relation to the next element in line
element_types = []
connector = []
for i in range(1:n_elements+1): 
  valid =0 
  ith_element = raw_input('What is element #' + str(i) + '? ')
  while not valid:
      try :
            if ith_element in ['R','C','CPE','W']:
                valid = 1
      except ValueError, e:
            print("'%s' is not a valid input. Please choose from R. Resistor, C. Capacitance, CPE. Constant Phase Element, W. Warburg Impedance" % e.args[0].split(": ")[1])
  series_parallell = raw_input('Will it be in series or in parallel to the following element (s/p)? ')
  element_types.append(ith_element) 
  connector.append(series_parallel)

#obtain the required parameters from user. store in dictionary or list?
for el in element_types:
      if el == 'R':
          
