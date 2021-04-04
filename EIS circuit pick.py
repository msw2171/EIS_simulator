from tkinter import *
from PIL import Image, ImageTk
from functools import partial

# pathway to image folder (note:change to your device path, if on Windows change backslashes to forward)

imgfolder_4e="F:/Python images for EIS/4element/"
imgfolder_3e="F:/Python images for EIS/3element/"
imgfolder_2e="F:/Python images for EIS/2element/"
imgfolder_1e="F:/Python images for EIS/1element/"

# define dictionaries for storing images

img_dict_4e={}
img_dict_3e={}
img_dict_2e={}
img_dict_1e={}

# for loops to fill process/resize images with Pillow and fill image Dictionaries
for x in range(1,11):
    full_img_path=imgfolder_4e + f'pic4_{x}.png'
    img_processed = Image.open(full_img_path)
    img_processed = img_processed.resize((145, 125), Image.ANTIALIAS)
    img_dict_4e[f'img4_{x}']=img_processed
for x in range(1,5):
    full_img_path = imgfolder_3e + f'pic3_{x}.png'
    img_processed = Image.open(full_img_path)
    img_processed = img_processed.resize((145, 125), Image.ANTIALIAS)
    img_dict_3e[f'img3_{x}'] = img_processed
for x in range(1,3):
    full_img_path = imgfolder_2e + f'pic2_{x}.png'
    img_processed = Image.open(full_img_path)
    img_processed = img_processed.resize((145, 125), Image.ANTIALIAS)
    img_dict_2e[f'img2_{x}'] = img_processed
for x in range(1,2):
    full_img_path = imgfolder_1e + f'pic1_{x}.png'
    img_processed = Image.open(full_img_path)
    img_processed = img_processed.resize((145, 125), Image.ANTIALIAS)
    img_dict_1e[f'img1_{x}'] = img_processed



#Establish default string variable for Circuit Choice
chosen_circuit="None"

#function to open picture/button window of 4 element choices

def four_element_choice():
    four_window = Tk()
    four_window.geometry("1000x450")
    four_window.title("Circuit configuration Options")
    frame = LabelFrame(four_window, text="Choose from the possible circuit configurations. You will be able to specify the identity of each element afterwards:", padx=50, pady=50)
    frame.pack()
    def buttonpush(a):
        global chosen_circuit
        chosen_circuit=a
        four_window.destroy()
    b_img_dict={}
    buttonnum=1
    for key in img_dict_4e:
        b_img_dict[key]= ImageTk.PhotoImage(img_dict_4e[key])
    for key in b_img_dict:
        if buttonnum<3:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=1, row=buttonnum, padx=10, pady=10)
            buttonnum=buttonnum+1
        elif buttonnum<5:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=2, row=buttonnum-2, padx=10, pady=10)
            buttonnum = buttonnum + 1
        elif buttonnum<7:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=3, row=buttonnum-4, padx=10, pady=10)
            buttonnum = buttonnum + 1
        elif buttonnum<9:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=4, row=buttonnum - 6, padx=10, pady=10)
            buttonnum = buttonnum + 1
        elif buttonnum<11:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=5, row=buttonnum - 8, padx=10, pady=10)
            buttonnum = buttonnum + 1
    four_window.mainloop()
    return chosen_circuit

# Function to open window for 3 element choices

def three_element_choice():
    three_window = Tk()
    three_window.geometry("1000x450")
    three_window.title("Circuit configuration Options")
    frame = LabelFrame(three_window, text="Choose from the possible circuit configurations. You will be able to specify the identity of each element afterwards:", padx=50, pady=50)
    frame.pack()
    def buttonpush(a):
        global chosen_circuit
        chosen_circuit=a
        three_window.destroy()
    b_img_dict={}
    buttonnum=1
    for key in img_dict_3e:
        b_img_dict[key]= ImageTk.PhotoImage(img_dict_3e[key])
    for key in b_img_dict:
        if buttonnum<3:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=1, row=buttonnum, padx=10, pady=10)
            buttonnum=buttonnum+1
        else:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=2, row=buttonnum-2, padx=10, pady=10)
            buttonnum = buttonnum + 1

    three_window.mainloop()
    return chosen_circuit

#Function to open window for 2 element choices

def two_element_choice():
    two_window = Tk()
    two_window.geometry("1000x450")
    two_window.title("Circuit configuration Options")
    frame = LabelFrame(two_window, text="Choose from the possible circuit configurations. You will be able to specify the identity of each element afterwards:", padx=50, pady=50)
    frame.pack()
    def buttonpush(a):
        global chosen_circuit
        chosen_circuit=a
        two_window.destroy()
    b_img_dict={}
    buttonnum=1
    for key in img_dict_2e:
        b_img_dict[key]= ImageTk.PhotoImage(img_dict_2e[key])
    for key in b_img_dict:
        if buttonnum<2:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=1, row=buttonnum, padx=10, pady=10)
            buttonnum=buttonnum+1
        else:
            buttontest = Button(frame, image=b_img_dict[key], command=partial(buttonpush, key))
            buttontest.grid(column=2, row=buttonnum-1, padx=10, pady=10)
            buttonnum = buttonnum + 1

    two_window.mainloop()
    return chosen_circuit

#function to prompt user to enter number of circuit elements and return circuit element image key

def determine_circuit_config():
    num_elements=input("How many elements would you like to simulate? Enter a number (1-4): ")
    if num_elements=="4":
        return four_element_choice()
    elif num_elements=="3":
        return three_element_choice()
    elif num_elements=="2":
        return two_element_choice()
    elif num_elements=="1":
        return "img1_1"
    else:
        print("Invalid Input")
        return determine_circuit_config()

final_config=determine_circuit_config()
print(final_config)