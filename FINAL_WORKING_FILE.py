from tkinter import *
from PIL import Image, ImageTk
from functools import partial

# pathway to image folder (note:change to your device path, if on Windows change backslashes to forward)

imgfolder_4e = "F:/Python images for EIS/4element/"
imgfolder_3e = "F:/Python images for EIS/3element/"
imgfolder_2e = "F:/Python images for EIS/2element/"
imgfolder_1e = "F:/Python images for EIS/1element/"

# define dictionaries for storing images

img_dict_4e = {}
img_dict_3e = {}
img_dict_2e = {}
img_dict_1e = {}

# for loops to fill process/resize images with Pillow and fill image Dictionaries
for x in range(1, 11):
    full_img_path = imgfolder_4e + f'pic4_{x}.png'
    img_processed = Image.open(full_img_path)
    img_processed = img_processed.resize((145, 125), Image.ANTIALIAS)
    img_dict_4e[f'img4_{x}'] = img_processed
for x in range(1, 5):
    full_img_path = imgfolder_3e + f'pic3_{x}.png'
    img_processed = Image.open(full_img_path)
    img_processed = img_processed.resize((145, 125), Image.ANTIALIAS)
    img_dict_3e[f'img3_{x}'] = img_processed
for x in range(1, 3):
    full_img_path = imgfolder_2e + f'pic2_{x}.png'
    img_processed = Image.open(full_img_path)
    img_processed = img_processed.resize((145, 125), Image.ANTIALIAS)
    img_dict_2e[f'img2_{x}'] = img_processed
for x in range(1, 2):
    full_img_path = imgfolder_1e + f'pic1_{x}.png'
    img_processed = Image.open(full_img_path)
    img_processed = img_processed.resize((145, 125), Image.ANTIALIAS)
    img_dict_1e[f'img1_{x}'] = img_processed

# Construct combined image dictionary out of seperate dictionaries

master_img_dict = {}
for key in img_dict_4e:
    master_img_dict[key] = img_dict_4e[key]
for key in img_dict_3e:
    master_img_dict[key] = img_dict_3e[key]
for key in img_dict_2e:
    master_img_dict[key] = img_dict_2e[key]
for key in img_dict_1e:
    master_img_dict[key] = img_dict_1e[key]

# Establish default string variable for Circuit Choice
chosen_circuit = "None"


# function to open picture/button window of 4 element choices

def four_element_choice():
    four_window = Tk()
    four_window.geometry("1000x450")
    four_window.title("Circuit configuration Options")
    frame = LabelFrame(four_window,
                       text="Choose from the possible circuit configurations.You will be able to specify the identity of each element afterwards:",
                       padx=50, pady=50)
    frame.pack()

    def buttonpush(a):
        global chosen_circuit
        chosen_circuit = a
        four_window.destroy()

    b_img_dict = {}
    buttonnum = 1
    for key in img_dict_4e:
        b_img_dict[key] = ImageTk.PhotoImage(img_dict_4e[key])
    for key in b_img_dict:
        if buttonnum < 3:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=1, row=buttonnum, padx=10, pady=10)
            buttonnum = buttonnum + 1
        elif buttonnum < 5:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=2, row=buttonnum - 2, padx=10, pady=10)
            buttonnum = buttonnum + 1
        elif buttonnum < 7:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=3, row=buttonnum - 4, padx=10, pady=10)
            buttonnum = buttonnum + 1
        elif buttonnum < 9:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=4, row=buttonnum - 6, padx=10, pady=10)
            buttonnum = buttonnum + 1
        elif buttonnum < 11:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=5, row=buttonnum - 8, padx=10, pady=10)
            buttonnum = buttonnum + 1
    four_window.lift()
    four_window.attributes('-topmost', True)
    four_window.after_idle(four_window.attributes, '-topmost', False)
    four_window.mainloop()
    return chosen_circuit


# Function to open window for 3 element choices

def three_element_choice():
    three_window = Tk()
    three_window.geometry("1000x450")
    three_window.title("Circuit configuration Options")
    frame = LabelFrame(three_window,
                       text="Choose from the possible circuit configurations. You will be able to specify the identity of each element afterwards:",
                       padx=50, pady=50)
    frame.pack()

    def buttonpush(a):
        global chosen_circuit
        chosen_circuit = a
        three_window.destroy()

    b_img_dict = {}
    buttonnum = 1
    for key in img_dict_3e:
        b_img_dict[key] = ImageTk.PhotoImage(img_dict_3e[key])
    for key in b_img_dict:
        if buttonnum < 3:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=1, row=buttonnum, padx=10, pady=10)
            buttonnum = buttonnum + 1
        else:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=2, row=buttonnum - 2, padx=10, pady=10)
            buttonnum = buttonnum + 1
    three_window.lift()
    three_window.attributes('-topmost', True)
    three_window.after_idle(three_window.attributes, '-topmost', False)
    three_window.mainloop()
    return chosen_circuit


# Function to open window for 2 element choices

def two_element_choice():
    two_window = Tk()
    two_window.geometry("1000x450")
    two_window.title("Circuit configuration Options")
    frame = LabelFrame(two_window,
                       text="Choose from the possible circuit configurations. You will be able to specify the identity of each element afterwards:",
                       padx=50, pady=50)
    frame.pack()

    def buttonpush(a):
        global chosen_circuit
        chosen_circuit = a
        two_window.destroy()

    b_img_dict = {}
    buttonnum = 1
    for key in img_dict_2e:
        b_img_dict[key] = ImageTk.PhotoImage(img_dict_2e[key])
    for key in b_img_dict:
        if buttonnum < 2:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=1, row=buttonnum, padx=10, pady=10)
            buttonnum = buttonnum + 1
        else:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=2, row=buttonnum - 1, padx=10, pady=10)
            buttonnum = buttonnum + 1
    two_window.lift()
    two_window.attributes('-topmost', True)
    two_window.after_idle(two_window.attributes, '-topmost', False)
    two_window.mainloop()
    return chosen_circuit


# function to prompt user to enter number of circuit elements and return circuit element image key

def determine_circuit_config(n):
    if n == 4:
        return four_element_choice()
    elif n == 3:
        return three_element_choice()
    elif n == 2:
        return two_element_choice()
    elif n == 1:
        return "img1_1"


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
print("W: Warburg impedance")
print(30 * '-')
###########################
## Robust error handling ##
## only accept int 1-4   ##
###########################

## Wait for valid input in while...not ###
is_valid = 0
# obtain number of elements user wishes to simulate. keep asking for a number until user inputs interger from 1-4
while not is_valid:
    n_elements_str = input('How many elements would you like to simulate? : ')
    try:
        n_elements = int(n_elements_str)
        if n_elements >= 1 and n_elements <= 4:
            is_valid = 1  ## set it to 1 to validate input and to terminate the while..not loop
        else:
            print(str(n_elements) + " is not a valid integer. \n Please enter an integer value from 1-4")
    except ValueError:
        print(str(n_elements_str) + " is not a valid integer. \n Please enter an integer value from 1-4")

# Run user picture selection window to determine circuit congfig

user_choice_img_key = determine_circuit_config(n_elements)

# convert image dictionary key string to be used for circuits dictionary

user_choice_circuits_key = user_choice_img_key.lstrip("img")

# Use Pillow to resize users chosen circuit image for reference display

user_choice_img = master_img_dict[user_choice_img_key].resize((290, 250), Image.ANTIALIAS)

# define variable to determine when user is done with data inputs to close reference picture window
user_inputs_done = False


# Open window with circuit reference picture to assist in element assignment

def open_reference_window():
    global user_inputs_done
    global user_choice_img
    reference_window = Tk()
    reference_window.geometry("500x450")
    reference_window.title("Simulated Circuit Configuration")
    frame = LabelFrame(reference_window,
                       text="Below is your chosen circuit for reference as you specify element identities:", padx=50,
                       pady=50)
    frame.pack()
    reference_img = ImageTk.PhotoImage(user_choice_img)
    label = Label(frame, image=reference_img)
    label.pack()

    def do_nothing():  # disabling closewindow button
        pass

    reference_window.protocol('WM_DELETE_WINDOW', do_nothing)

    reference_window.lift()
    reference_window.attributes('-topmost', True)
    reference_window.after_idle(reference_window.attributes, '-topmost', False)

    while not user_inputs_done:
        reference_window.update()

    reference_window.destroy()


# Import threading, create separate thread for pulling up circuit reference window, and start thread
import threading

thread_1 = threading.Thread(target=open_reference_window)
thread_1.start()

### obtain type of elements and parameters
element_types = []
params = []
for i in range(1, n_elements + 1):
    valid = 0
    while not valid:  # ensure user input is only allowed element types R, C, CPE, or W
        ith_element = input('What is element #' + str(i) + '? ')
        if ith_element in ['R', 'C', 'CPE', 'W']:
            valid = 1
        else:
            print(str(
                ith_element) + " is not a valid input. \n Please choose from R. Resistor, C. Capacitance, CPE. Constant Phase Element, W. Warburg Impedance")
    element_types.append(ith_element)
    valid_values = 0
    while not valid_values:
        try:
            if ith_element == 'R':
                r = float(input("Please specify the resitance in Ohms: "))
                params.append(r)
            elif ith_element == 'C':
                c = float(input("Please specify the capacitance in F: "))
                params.append(c)
            elif ith_element == 'CPE':
                ntrue = 0
                q = float(input("Please specify the Q parameter in F: "))
                while not ntrue:
                    n = float(input(
                        "Please specify the ideality factor n between 0 and 1: "))  # ensure that the ideality factor is indeed between 0 and 1 or continue asking for it until it is.
                    if n >= 0 and n <= 1:
                        ntrue = 1
                    else:
                        print(str(n) + "is not between 0 and 1")
                params.append([q, n])
            else:
                A = float(input("Please specify the area A in cm^2: "))
                D_O = float(input("Please specify the diffusion coefficient of the oxidized species in cm^2/s: "))
                D_R = float(input("Please specify the diffusion coefficient of the reduced species in cm^2/s: "))
                c_O_bulk = float(input("Please specify the bulk concentration of oxidized species in mol/cm^3: "))
                c_R_bulk = float(input("Please specify the bulk concentration of reduced species in mol/cm^3: "))
                n_el = int(input("Please specify the number of electrons in the redox reaction: "))
                params.append([A, D_O, D_R, c_O_bulk, c_R_bulk, n_el])
            valid_values = 1
        except ValueError:
            print("You have entered an invalid value. Please ensure entered values are numerical.")

lo_hi = 0  # check that the frequency range is correctly specified
pos_freq = 0
nonstr_freq = 0
while not nonstr_freq:
    try:
        while not lo_hi or not pos_freq:
            lo_hi = 0
            pos_freq = 0
            low_f = float(input("What is the lowest frequency (in Hz) that you'd like to simulate? "))
            high_f = float(input("What is the highest frequency (in Hz) that you'd like to simulate? "))
            if high_f > low_f:
                lo_hi = 1
            else:
                print("Your upper frequency is lower than your lowest frequency, please ensure a proper frequency range.")
            if low_f > 0 and high_f > 0:
                pos_freq = 1
            else:
                print("Please ensure a proper frequency range with positive values above 0 Hz")
        nonstr_freq=1
    except ValueError:
        print("Please enter  positive numerical values for your frequency range.")


# Alter variable to indicate user is done with data input to close reference picture window
user_inputs_done = True

w_input = np.logspace(np.log10(low_f), np.log10(high_f), num=100)
# print(w_input)
w_range = []
for w in w_input:
    x = round(2 * np.pi * w, 4)
    w_range.append(x)
#####object element_types specifies the user defined elements, object params has the corresponding parameters in the same index############
###### For example if element_types[1] is a Warburg impedance, params[1] will be a tuple with (A, D_O, D_R, c_0_bulk, c_R_bulk, n_el)######


print(element_types)
print(params)


# ## Calculating Individual Element Impedances
# Able to take a frequency range, element type, and relevant parameters from user input and create an array of impedances for each frequency value

# Resistor
# w is array of rotationalfrequencies
# R is resistance

def Z_R(w, R):
    Re_Z = np.full(len(w), R)
    Im_Z = np.zeros(len(w))
    return Re_Z + Im_Z


# Capacitor
# w is array of rotational frequencies
# C is capacitance

def Z_C(w, C):
    x = np.array(w)
    Re_Z = np.zeros(len(w))
    Im_Z = -1 / (x * C) * 1j
    return Re_Z + Im_Z


# Constant phase element
# w is array of rotational frequencies
# n is a number between 0 and 1 (Simplifies to an ideal capacitor when n=1)

def Z_CPE(w, params):
    x = np.array(w)
    Q = params[0]
    n = params[1]
    Re_Z = (1 / (Q * (x ** n))) * cm.cos(cm.pi * n / 2)
    Im_Z = (-1 / (Q * (x ** n))) * cm.sin(cm.pi * n / 2) * 1j
    return Re_Z + Im_Z


# Warburg impedance
# w is array of rotational frequencies
# A is electrode area
# D_O and D_R are diffusion coefficients for oxidized and reduced species
# c_O_bulk and c_R_bulk are bulk concentrations for oxidized and reduced species

def Z_W(w, params):
    x = np.array(w)
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


# Input/circuit dictionary
circuits_dict = {}

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
# print(el_impedance)
# Sample frequency space
# w = np.logspace(.5,10,100)

# Sample input - two equivalent electrodes and solution resistance
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

# Possible circuits for 4 elements

circuits_4 = [[[E1, E2, E3, E4]],
              [[E1, E2, (E3, E4)]],
              [[E1, ([E2, E3], E4)]],
              [(E4, [E2, E3, E1])],
              [([E1, E3], [E2, E4])],
              [[(E1, E2), (E3, E4)]],
              [([E1, (E2, E3)], E4)],
              [[E1, (E2, E3, E4)]],
              [([E1, E2], E3, E4)],
              [(E1, E2, E3, E4)]]

# Add all to the dictionaries
for count, array in enumerate(circuits_4):
    circuits_dict["4_" + str(count + 1)] = circuits_4[count]

# Possible inputs for 3 elements
circuits_3 = [[[E1, E2, E3]],
              [[E1, (E2, E3)]],
              [([E1, E2], E3)],
              [(E1, E2, E3)]]

for count, array in enumerate(circuits_3):
    circuits_dict["3_" + str(count + 1)] = circuits_3[count]

# Possible inputs for 2 elements
circuits_2 = [[[E1, E2]],
              [(E1, E2)]]

for count, array in enumerate(circuits_2):
    circuits_dict["2_" + str(count + 1)] = circuits_2[count]

# In[10]:


# Possible inputs for 1 element
circuits_1 = [[E1]]

for count, array in enumerate(circuits_1):
    circuits_dict["1_" + str(count + 1)] = circuits_1[count]


# ## Logic Loop Functions for Adding Impedances in Element Array

# In[13]:


# Function for adding impedances in series
def add_series_Z(elements):
    return np.sum(elements, axis=0)


# In[14]:


# Function for adding impedances in parallel
def add_parallel_Z(elements):
    inv_elements = []
    for i in elements:
        inv_elements.append(1 / i)
    return 1 / (np.sum(inv_elements, axis=0))


# In[15]:


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


# Construct Frequency list from angular frequency list
f_range = []
two_pi = round(2 * np.pi, 4)
for _ in range(len(w_range)):
    f_range.append(w_range[_] / two_pi)

# Convert w and f lists into arrays
w_array = np.array(w_range)
f_array = np.array(f_range)

# Set Parameters for Nyquist Plot

circuit = circuits_dict[user_choice_circuits_key]
impedance_array = calc_Z(circuit, "series")
x = impedance_array.real
y = -1*impedance_array.imag

fig, ax = plt.subplots()
ax.set_title('Simulated EIS Plot')
ax.set_ylabel('-Z\" (Ohms)')
ax.set_xlabel('Z\' (Ohms)')
line = ax.plot(x, y, picker=True, pickradius=5)
plt.axis("square")

# Set up Plot Annotation Visual
annot = ax.annotate("", xy=(0, 0), xytext=(-40, 40), textcoords="offset points",
                    bbox=dict(boxstyle='round4', fc='linen', ec='k', lw=1),
                    arrowprops=dict(arrowstyle='-|>'))

annot.set_visible(False)


# Pick point/annotate graph function
def onpick(event):
    global w_array
    global f_array
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    xpoints = xdata[ind]
    ypoints = ydata[ind]
    wpoints = w_array[ind]
    fpoints = f_array[ind]
    first_xpoint = xpoints[0]
    first_ypoint = ypoints[0]
    first_wpoint = wpoints[0]
    first_fpoint = fpoints[0]
    annot.xy = (first_xpoint, first_ypoint)
    text = " Z\'={:.3g}\n-Z\"={:.3g}\n \u03c9 ={:.3g}\n f  ={:.3g}".format(first_xpoint, first_ypoint, first_wpoint,
                                                                   first_fpoint)
    annot.set_text(text)
    annot.set_visible(True)
    fig.canvas.draw()

    console_print_text = ' Z\' = {:.3g} Ohms\n-Z\" = {:.3g} Ohms\nAngular Frequency \u03c9 = {:.3g} Hz\nFrequency f = {:.3g} Hz'.format(
        first_xpoint, first_ypoint, first_wpoint, first_fpoint)

    print('-------------------------------')
    print(console_print_text)
    print('-------------------------------')


# Plot Graph

fig.canvas.mpl_connect('pick_event', onpick)

plt.show()

# Convert the numpy data array into a DataFrame and export as a .txt file to the specified location

from tkinter import filedialog
import tkinter.font as font

Z_data = np.column_stack((x, y, f_array))
df = pd.DataFrame(Z_data, columns=["Z' (ohms)", "-Z'' (ohms) ", "f (Hz)"])

def savefile():
    global df
    file_path=filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", ".txt")])
    if file_path == "":
        return
    else:
        df.to_csv(file_path)
        print("File Saved")
def push_close():
    save_window.destroy()

save_window = Tk()
save_window.geometry("500x250")
save_window.title("Save EIS Plot")
frame = LabelFrame(save_window, text="Would you like to save your EIS plot data to a text file?", padx=20, pady=20)
frame.pack()
save_button=Button(frame, text="Save", font=font.Font(size=20), command=savefile)
save_button.pack(padx=10, pady=10)
close_button=Button(frame, text="Close", font=font.Font(size=20), command=push_close)
close_button.pack(padx=10, pady=10)

save_window.lift()
save_window.attributes('-topmost', True)
save_window.after_idle(save_window.attributes, '-topmost', False)

save_window.mainloop()
