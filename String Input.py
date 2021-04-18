from tkinter import *
from PIL import Image, ImageTk
from functools import partial

### GUI Window Functions ###

# Define function to bring pop up windows to forefront
def window_tofront(window):
    window.lift()
    window.attributes('-topmost', True)
    window.after_idle(window.attributes, '-topmost', False)

# import modules for mathematical operation

import matplotlib.pyplot as plt
import numpy as np
import cmath as cm
import pandas as pd

###### Introduction screen and number/type of elements are obtained in this block##################
###################################################################################################
print(30 * '-')
print("WELCOME TO EIS SIMULATOR")
print(30 * '-')
print("Ciruit element codes: ")
print("R: Resistance")
print("C: Capacitance")
print("CPE: Constant Phase Element")
print("W: Warburg Impedance")
print(30 * '-')
###########################
## Robust error handling ##
## only accept int 1-4   ##
###########################

## Wait for valid input in while...not ###
is_valid = 0
# obtain number of elements user wishes to simulate. keep asking for a number until user inputs integer from 1-4
# try/except for error handling of float and string inputs, while loop to ensure value 1-4
while not is_valid:
    n_elements_str = input('How many elements would you like to simulate? Enter an integer value (1-4) : ')
    try:
        n_elements = int(n_elements_str)
        if n_elements >= 1 and n_elements <= 4:
            is_valid = 1  ## set it to 1 to validate input and to terminate the while..not loop
        else:
            print(str(n_elements) + " is not a valid integer. \nPlease enter an integer value from 1-4.")
    except ValueError:
        print(str(n_elements_str) + " is not a valid integer. \nPlease enter an integer value from 1-4.")

# Run user picture selection window to determine circuit config


# define variable to determine when user is done with data inputs to close reference picture window
user_inputs_done = False



### obtain type of elements and parameters
# elements types are stored in list
# parameters are stored in params list, with corresponding index as element_types list.
# if more than one parameter is needed to describe and element ie. CPE or W, the value stored in params is a nested list with multiple parameters.

#####object element_types specifies the user defined elements, object params has the corresponding parameters in the same index############
###### For example if element_types[1] is a Warburg impedance, params[1] will be a tuple with (A, D_O, D_R, c_0_bulk, c_R_bulk, n_el)######

element_types = []
params = []


def check_neg_error(a):  # function designed to produce valueerror if given a negative or 0 as an argument
    if a <= 0:
        cause_error = int("str")
        pass
    else:
        pass


# for loop through element number, this loop addresses and collects parameters for each element 1-4 one at a time
for i in range(1, n_elements + 1):
    valid = 0
    while not valid:  # ensure user input is only allowed element types R, C, CPE, or W
        ith_element = input('What is element #' + str(i) + '? ')
        if ith_element in ['R', 'C', 'CPE', 'W']:
            valid = 1
        else:
            print(str(
                ith_element) + " is not a valid input. \nPlease choose from R. Resistor, C. Capacitance, CPE. Constant Phase Element, W. Warburg Impedance")
    element_types.append(ith_element)
    valid_values = 0
    while not valid_values: ## while loop prompts user for values dependant on element identity, checks those values for errors, and if valid appends them to a list of parameters and breaks loop
        try:
            if ith_element == 'R':
                r = float(input("Please specify the resitance in Ohms : "))
                check_neg_error(r)
                params.append(r)
            elif ith_element == 'C':
                c = float(input("Please specify the capacitance in F : "))
                check_neg_error(c)
                params.append(c)
            elif ith_element == 'CPE':
                ntrue = 0
                q = float(input("Please specify the Q parameter in F : "))
                check_neg_error(q)
                while not ntrue:
                    n = float(input(
                        "Please specify the ideality factor n between 0 and 1 : "))  # ensure that the ideality factor is indeed between 0 and 1 or continue asking for it until it is.
                    if n >= 0 and n <= 1:
                        ntrue = 1
                    else:
                        print(str(n) + " is not between 0 and 1.")
                params.append([q, n])
            else:
                choose_sigma = False
                choose_param = False
                print(
                    "Would you like to provide the general Warburg coefficent \u03C3 or more specific parameters (ie. species concentrations, diffusion coefficients etc.)?")
                ## determine whether user wants to enter warburg coefficient or individual concentration/diffusion parameters
                while not choose_param and not choose_sigma:
                    sigma_or_param = str(input("Enter \'sigma\' or \'parameters\' : "))
                    if sigma_or_param == "sigma":
                        choose_sigma = True
                    elif sigma_or_param == "parameters":
                        choose_param = True
                    else:
                        print("Please enter one of the provided responses.")

                if choose_sigma:
                    sigma_val = float(
                        input("Please specify the value of the Warburg coefficient \u03C3 in Ohms/\u221asec : "))
                    check_neg_error(sigma_val)
                    params.append([sigma_val])
                else:
                    A = float(input("Please specify the area A in cm^2 : "))
                    check_neg_error(A)

                    D_O = float(input("Please specify the diffusion coefficient of the oxidized species in cm^2/s : "))
                    check_neg_error(D_O)

                    D_R = float(input("Please specify the diffusion coefficient of the reduced species in cm^2/s : "))
                    check_neg_error(D_R)

                    c_O_bulk = float(
                        input("Please specify the bulk concentration of oxidized species in mol/L : ")) / 1000
                    check_neg_error(c_O_bulk)

                    c_R_bulk = float(
                        input("Please specify the bulk concentration of reduced species in mol/L : ")) / 1000
                    check_neg_error(c_R_bulk)

                    n_el = int(input("Please specify the number of electrons in the redox reaction: "))
                    check_neg_error(n_el)

                    params.append([A, D_O, D_R, c_O_bulk, c_R_bulk, n_el])
            valid_values = 1
        except ValueError:  #if Valueerror occurs, code skips changing the validvalues variable to one, prints invalid value statement, and restarts the current while loop
            print("You have entered an invalid value. Please ensure entered values are positive and numerical.")

### Circuit Configuration Based on User Input String ###

#Function for extracting text inside of a parenthesis
def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])

#Error handling for the user input string
def verify_configuration(circuit_string):
    string_check = []
    
    #Check for balanced parenthesese
    stack = []
    for i in circuit_string:
        if i == "(":
            stack.append(i)
        elif i == ")":
            if ((len(stack) > 0) and
                ("(" == stack[len(stack)-1])):
                stack.pop()
            else:
                string_check.append(False)
                print("Please make sure parentheses within the circuit configuration are matching.")
    if len(stack) != 0:
        string_check.append(False)
        print("Please make sure parentheses within the circuit configuration are matching.")
        
    #Check for valid brackets
    invalid_brackets = ["{","}","[","]"]
    valid_brackets = []
    for i in invalid_brackets:
        valid_brackets.append(i not in circuit_string)
    string_check.append(all(valid_brackets))
    if not all(valid_brackets):
        ("Please make sure you are only using parentheses and not square or curly brackets.")
        
    #Check that paranthesis are only used to group parallel elements
    valid_parentheses = []
    for i in list(parenthetic_contents(circuit_string)):
        if "/" not in i[1]:
            valid_parentheses.append(False)
    string_check.append(all(valid_parentheses))
    if not all(valid_parentheses):
        print("Please make sure you use parentheses only to group objects in parallel.")
        
    #Check that parallel elements are enclosed with paranthesis
    if "/" in circuit_string and "(" not in circuit_string:
        string_check.append(False)
        print("Please make sure parallel groupings are contained in parentheses.")
    
    return all(string_check)

valid = False

while not valid:
    print("When entering a circuit configuration, please follow the following formatting guidelines:" )
    print("- Use E1, E2, E3, and E4 to represent the corresponding elements")
    print("- Use + to delimit elements or groups of elements in series. E.g E1+E2 shows that element 1 and 2 are in series")
    print("- Use / to delimit elements or groups of elements in parallel. E.g. (E1/E2) shows that element 1 and 2 are in parallel")
    print("- Enclose all elements in parallel in parentheses. E.g. (E1/E2/E3) or (E1+E2/E3)")
    print("- Do not use parentheses to enclose elements in series. E.g. ((E1+E2)/E3) is an invalid input")
    circuit_string = input('What is the circuit configuration you would like to simulate? ')
    circuit_string = circuit_string.replace(" ","")
    valid = verify_configuration(circuit_string)
    if valid:
        print(circuit_string)   

lo_hi = 0  # check that the frequency range is correctly specified, low to high, positive, and numerical
pos_freq = 0
nonstr_freq = 0
while not nonstr_freq:
    try:
        while not lo_hi or not pos_freq:
            lo_hi = 0
            pos_freq = 0
            low_f = float(input("What is the lowest frequency f (in Hz) that you would like to simulate? : "))
            high_f = float(input("What is the highest frequency f (in Hz) that you would like to simulate? : "))
            if high_f > low_f:
                lo_hi = 1
            else:
                print(
                    "Your upper frequency is lower than your lowest frequency, please ensure a proper frequency range.")
            if low_f > 0 and high_f > 0:
                pos_freq = 1
            else:
                print("Please ensure a proper frequency range with positive values above 0 Hz.")
        nonstr_freq = 1
    except ValueError:
        print("Please ensure you have entered positive numerical values for your frequency range.")

# Alter variable to indicate user is done with data input to close reference picture window
user_inputs_done = True

# create range of frequencies for calculation in increments in logspace
w_input = np.logspace(np.log10(low_f), np.log10(high_f), num=1000)

# multiply each element in the f range by 2pi and append to new list to give list of angular frequencies
w_range = []
for w in w_input:
    x = round(2 * np.pi * w, 4)
    w_range.append(x)

print(element_types)
print(params)


### Calculating Individual Element Impedances ###

# Able to take a frequency range, and relevant parameters from user input
# Returns an np.array of impedances for each frequency value

# Resistor
# w is array of angular frequencies in rad/s
# R is resistance in ohms

def Z_R(w, R):
    Re_Z = np.full(len(w), R)
    Im_Z = np.zeros(len(w))
    return Re_Z + Im_Z


# Capacitor
# w is array of angular frequencies in rad/s
# C is capacitance in farads

def Z_C(w, C):
    x = np.array(w)
    Re_Z = np.zeros(len(w))
    Im_Z = -1 / (x * C) * 1j
    return Re_Z + Im_Z


# Constant phase element
# w is array of angular frequencies in rad/s
# n is a number between 0 and 1

def Z_CPE(w, params):
    x = np.array(w)
    Q = params[0]
    n = params[1]
    Re_Z = (1 / (Q * (x ** n))) * cm.cos(cm.pi * n / 2)
    Im_Z = (-1 / (Q * (x ** n))) * cm.sin(cm.pi * n / 2) * 1j
    return Re_Z + Im_Z


# Warburg impedance
# w is array of angular frequencies in rad/s
# A is electrode area in A/cm^2
# D_O and D_R are diffusion coefficients for oxidized and reduced species in cm^2/s
# c_O_bulk and c_R_bulk are bulk concentrations for oxidized and reduced species in mol/cm^3

def Z_W(w, params):
    x = np.array(w)
    if len(params) == 6:
        A = params[0]
        D_O = params[1]
        D_R = params[2]
        c_O_bulk = params[3]
        c_R_bulk = params[4]
        n = params[5]
        R = 8.314  # J/K•mol
        F = 96485  # C/mol
        T = 298  # K
        sigma = (R * T / ((n * F) ** 2 * A * 2 ** 0.5) * ((1 / D_O ** 0.5 / c_O_bulk) + (1 / D_R ** 0.5 / c_R_bulk)))
        Re_Z = sigma / x ** 0.5
        Im_Z = -sigma / x ** 0.5 * 1j
        return Re_Z + Im_Z
    else:
        Re_Z = params[0] / x ** 0.5
        Im_Z = -params[0] / x ** 0.5 * 1j
        return Re_Z + Im_Z


### Handling User Input of Element Parameters ###

# Input/circuit dictionary
circuits_dict = {}

# Convert user input parameters into impedance arrays
el_impedance = []
# take inputs and calculate Z for element type.
for i in range(n_elements):
    if element_types[i] == 'R':
        zi = Z_R(w_range, params[i])
    elif element_types[i] == 'C':
        zi = Z_C(w_range, params[i])

    elif element_types[i] == 'CPE':
        zi = Z_CPE(w_range, params[i])
    else:
        zi = Z_W(w_range, params[i])
    el_impedance.append(zi)



# Assigns the calculated impedance to specific elements
if n_elements == 1:
    E1 = el_impedance[0]
    E2 = 0
    E3 = 0
    E4 = 0
    elements = [E1]
elif n_elements == 2:
    E1 = el_impedance[0]
    E2 = el_impedance[1]
    E3 = 0
    E4 = 0
    elements = [E1, E2]
elif n_elements == 3:
    E1 = el_impedance[0]
    E2 = el_impedance[1]
    E3 = el_impedance[2]
    E4 = 0
    elements = [E1, E2, E3]
else:
    E1 = el_impedance[0]
    E2 = el_impedance[1]
    E3 = el_impedance[2]
    E4 = el_impedance[3]
    elements = [E1, E2, E3, E4]
    
element_dict = {}
for count, element in enumerate(elements):
    element_dict["E"+str(count+1)]=element

### Parse Circuit Input String to Convert into a List of Elements ###

def parse_input(input_string):
    
    grouped_elem_dict = {}
    
    #If the circuit contains parallel elements
    if "(" in input_string:
        para_contents = list(parenthetic_contents(input_string))
        #Handle elements in parallel first
        for count, i in enumerate(para_contents):
            #This is currently only able to subsitute one P equivalency, not all
            for key in grouped_elem_dict:
                i=(i[0],i[1].replace(grouped_elem_dict[key][1],key))
            para_tuple=[]
            para_elems = i[1].split("/")
            for p in para_elems:
                if "+" in p:
                    series_list = []
                    series_elems = p.split("+")
                    for s in series_elems:
                        if s[0]=="P":
                            series_list.append(grouped_elem_dict[s][0])
                        else:
                            series_list.append(element_dict[s])
                    para_tuple.append(series_list)
                else:
                    if p[0]=="P":
                        para_tuple.append(grouped_elem_dict[p][0])
                    else:
                        para_tuple.append(element_dict[p])
            grouped_elem_dict["P"+str(count+1)]=[tuple(para_tuple),"("+i[1]+")"]
        
        simplified_circ = input_string
        for key in grouped_elem_dict:
            simplified_circ = simplified_circ.replace(grouped_elem_dict[key][1],key)
        series_list = []
        series_elems = simplified_circ.split("+")
        for s in series_elems:
            if s[0]=="P":
                series_list.append(grouped_elem_dict[s][0])
            else:
                series_list.append(element_dict[s])
    
    #If the circuit has no parallel elements
    else:
        series_list = []
        series_elems = input_string.split("+")
        for s in series_elems:
            series_list.append(element_dict[s])
        
    return [series_list]

### Functions for Calculating Impedance ###

# Function for adding impedances in series
def add_series_Z(elements):
    return np.sum(elements, axis=0)


# Function for adding impedances in parallel
def add_parallel_Z(elements):
    inv_elements = []
    for i in elements:
        inv_elements.append(1 / i)
    return 1 / (np.sum(inv_elements, axis=0))


# Logic Loop for calculating total impedance
def calc_Z(input_circuit, config):
    circuit = input_circuit
    # Tuple can't be modified so create a dummy list to store calculations
    dummy_circuit = []
    # while not all(isinstance(x, np.ndarray) for x in dummy_circuit):
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


### Plotting the Calculated Impedances ###

# Construct Frequency list from angular frequency list
f_range = []
two_pi = round(2 * np.pi, 4)
for _ in range(len(w_range)):
    f_range.append(w_range[_] / two_pi)

# Convert w and f lists into arrays
w_array = np.array(w_range)
f_array = np.array(f_range)

# Set Parameters for Nyquist Plot

circuit = parse_input(circuit_string)
impedance_array = calc_Z(circuit, "series")
x = impedance_array.real
y = -1 * impedance_array.imag

fig, ax = plt.subplots()
ax.set_title('Simulated Nyquist Plot')
ax.set_ylabel('-Z\" (Ohms)')
ax.set_xlabel('Z\' (Ohms)')

# if Z imaginary is 0 at all points, The resistance is independant of frequency, all plotted points are the same Z" and Z'
# The plot should be given as scatter instead of line such that the singular point is visible on the graph
# picker property for points on the plot is activated with 5 pixel radius to allow artist elements (points) to be selected on click
Zimag_allzero = True
for _ in range(len(y)):
    if y[_] != 0:
        Zimag_allzero = False
if Zimag_allzero:
    y = np.zeros(len(y))
    line = ax.plot(x, y, "o", picker=True, pickradius=5)
else:
    line = ax.plot(x, y, picker=True, pickradius=5)

# plotting axis scales as equal in a square axis allows graph to be read more easily qualitatively
plt.axis("square")

# Set up Plot Annotation Visual and disable it until onpick click event
annot = ax.annotate("", xy=(0, 0), xytext=(-40, 40), textcoords="offset points",
                    bbox=dict(boxstyle='round4', fc='linen', ec='k', lw=1),
                    arrowprops=dict(arrowstyle='-|>'))

# hide annotation until made visible by click event
annot.set_visible(False)


# define Pick point/annotate graph function
def onpick(event):
    global w_array ## use global values for the frequency lists
    global f_array
    thisline = event.artist
    xdata = thisline.get_xdata()  ##get data x,y from plot
    ydata = thisline.get_ydata()
    ind = event.ind  ## click event establishes index of plotted elements
    xpoints = xdata[ind]
    ypoints = ydata[ind]
    wpoints = w_array[ind]
    fpoints = f_array[ind]  ##index returned from click used to select corressponding x,y, frequency data (there could be multiple points selected from click)
    first_xpoint = xpoints[0]
    first_ypoint = ypoints[0]
    first_wpoint = wpoints[0]
    first_fpoint = fpoints[0]  ##use only the first index returned with each click to annotate the plot, format annotation text
    annot.xy = (first_xpoint, first_ypoint)
    text = " Z\'={:.4g}\n-Z\"={:.4g}\n \u03c9 ={:.4g}\n f  ={:.4g}".format(first_xpoint, first_ypoint, first_wpoint,
                                                                           first_fpoint)
    annot.set_text(text) ## set text for annotation, make annotation visible, and update plot visual
    annot.set_visible(True)
    fig.canvas.draw()

    ## print data to console for additional viewing
    console_print_text = ' Z\' = {:.4g} Ohms\n-Z\" = {:.4g} Ohms\nAngular Frequency \u03c9 = {:.4g} Hz\nFrequency f = {:.4g} Hz'.format(
        first_xpoint, first_ypoint, first_wpoint, first_fpoint)

    print('-------------------------------')
    print(console_print_text)
    print('-------------------------------')


# define a buttonpress event to clear annotation if outside of graph axes
def clear_annot(event):
    if event.inaxes is None:
        annot.set_visible(False)
        event.canvas.draw()


# link defined events to plotting canvas and plot

fig.canvas.mpl_connect('pick_event', onpick)
fig.canvas.mpl_connect('button_press_event', clear_annot)
plt.show()

### Exporting the Data ###

# Convert the numpy data array into a DataFrame and export as a .txt file to the specified location

from tkinter import filedialog
import tkinter.font as font

Z_data = np.column_stack((x, y, w_array, f_array))
df = pd.DataFrame(Z_data, columns=["Z' (ohms)", "-Z'' (ohms)", "Angular frequency (Hz)", "frequency (Hz)"])

#define savefile function for save button. filedialog allows user to set save location and name
def savefile():
    global df
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", ".txt")])
    if file_path == "":
        return
    else:
        df.to_csv(file_path)
        print("File Saved")

#close window function
def push_close():
    save_window.destroy()

# create and format popup save window, assign savefile and close functions to respective buttons
save_window = Tk()
save_window.geometry("500x250")
save_window.title("Save EIS Plot")
frame = LabelFrame(save_window, text="Would you like to save your EIS plot data to a text file?", padx=20, pady=20)
frame.pack()
save_button = Button(frame, text="Save", font=font.Font(size=20), command=savefile)
save_button.pack(padx=10, pady=10)
close_button = Button(frame, text="Close", font=font.Font(size=20), command=push_close)
close_button.pack(padx=10, pady=10)

window_tofront(save_window)

save_window.mainloop()
