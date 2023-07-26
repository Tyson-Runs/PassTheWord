'''
This program develops easy to remember passwords and saves their hash values
It also uses facial recognition to verify user during password reset
By Tyson Shannon

Needed libraries:
pip install numpy
pip install opencv-python
pip install dlib
https://code.visualstudio.com/docs/cpp/config-msvc - for dlib install error
pip install face_recognition
'''

import random
import tkinter as tk
from tkinter import messagebox
import cv2 as cv
import numpy as np
import face_recognition as fr
import os

#----Password Variables----

symbols = ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "=", "{", "[", "}", "]", ";", ":", "'", "<", ">", ",", ".", "?", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
adjectiveFile = open("Adjectives.txt")
nounFile = open("Nouns.txt")
adjectiveContent = adjectiveFile.readlines()
nounContent = nounFile.readlines()
#List of passwords and the accounts they're associated to
passwordHash = []
accounts = {}
#Encryption/decryption keys
key1 = random.randrange(1, 200)
key2 = random.randrange(1, 115792089237316195423570985008687907852837564279074904382605163141518161494335)
#Change working directory for image saving
directory = r"C:\Users\tysha\OneDrive\Desktop\Code\Password System\Pictures"
os.chdir(directory)

#----Encryption/Decryption Code----

#Image encryption/decryption
def secureImg(name):
    try:
        #Path to image
        path = name+".jpg"    
        #Open file to read
        file = open(path, "rb")          
        #Storing image data
        image = file.read()
        file.close()       
        #Converting image into byte array to perform encryption on numeric data
        image = bytearray(image)     
        #Performing XOR operation on each value of bytearray
        for index, values in enumerate(image):
            image[index] = values ^ key1    
        #Opening file to write
        file = open(path, "wb")          
        #Writing encrypted data in image
        file.write(image)
        file.close()            
    except Exception:
        print("Error caught: ", Exception.__name__)

#Password encryption
def encryptPass(password): 
    try:  
        charAr = []
        #Turn string into ASCII array
        for i in password:
            charAr.append(ord(i)) 
        #Performing XOR operation on each value of ASCII array
        for index, values in enumerate(charAr):
            charAr[index] = values ^ key2     
        return charAr
    except Exception:
        print("Error caught: ", Exception.__name__)

#Password decryption
def decryptPass(charAr):
    try:
        output = ""
        #Decrypt ASCII values using XOR and convert back to chars
        for index, values in enumerate(charAr):
            charAr[index] = chr(values ^ key2)
        #Join chars together to return password
        for i in charAr:
            output = output+i
        return output
    except Exception:
        print("Error caught: ", Exception.__name__)

#----Camera Code----

#Initialize the camera
cam_port = 0
cam = cv.VideoCapture(cam_port)
#Take picture
def takePic(email):
    #Reading the input using the camera
    result, image = cam.read()
    #If image will detected without any error, 
    #Show result
    if result:
        #Showing result, it take frame name and image 
        #Output
        cv.imshow(email, image)
        #Saving image in folder and encrypt it
        cv.imwrite(email+".jpg", image)
        secureImg(email) 
        #If keyboard interrupt occurs, destroy image 
        #Window
        cv.waitKey(0)
        cv.destroyWindow(email)

#----Facial Recognition Code----

def accessCheck(email, type):
    result, image = cam.read()
    if result:
        #Take new picture
        name= email+"_"+type+"_"
        cv.imshow(email, image)
        cv.imwrite(name+".jpg", image)
        #Encrypt image
        secureImg(name) 
        cv.waitKey(0)
        cv.destroyWindow(email)
        #First image (Original)
        #Decrypt
        secureImg(email) 
        imageArchived = fr.load_image_file(email+".jpg") 
        imageArchived = cv.cvtColor(imageArchived, cv.COLOR_BGR2RGB)
        origEncode = fr.face_encodings(imageArchived)[0]
        #Encrypt again
        secureImg(email) 
        #Second image (Taken at reset)
        #Decrypt
        secureImg(name) 
        imageNew = fr.load_image_file(name+".jpg")
        imageNew = cv.cvtColor(imageNew, cv.COLOR_BGR2RGB)
        newEncode = fr.face_encodings(imageNew)[0]
        #Encrypt again
        secureImg(name) 
        #Compare both pictures returns [True] or [False]
        return fr.compare_faces([origEncode], newEncode)

#----Password Generation Code----

#New password generation
def passwordGenerator(email):
#Picks random items from above list & files to create password and hash
    randAdjective = random.choice(adjectiveContent)
    randNoun = random.choice(nounContent)
    currentPassword = randAdjective.strip()+random.choice(symbols)+randNoun.strip()+random.choice(symbols)
    currentHash = encryptPass(currentPassword)
    #Checks if password hash already exists and creates new one if yes or saves hash if no
    if currentHash in passwordHash:
        passwordGenerator(email)
    else:
        passwordHash.append(currentHash)
        accounts[email] = currentHash
        #Display new password for user
        tk.messagebox.showinfo("Sssshhhh...", "Your password is: "+currentPassword)

#Password retrieval
def getPassword(email): 
    #Decrypt and return
    return decryptPass(accounts[email])

#----Main Code----

def registerMain():
    email = emailEntry.get()
    display.config(text="")
    if email in accounts:
        display.config(text="Account already has password.")
    elif email != "":
        takePic(email)
        passwordGenerator(email)
    else:
        display.config(text="Please enter an email.")

def resetMain():
    existingEmail = emailEntry.get()
    #Runs face recognition
    accessGrant = accessCheck(existingEmail, "reset")
    display.config(text="")
    if accessGrant != [True]:
        display.config(text="Access denied.")
    elif existingEmail == "":
        display.config(text="Please enter an email.")
    elif existingEmail in accounts:
        passwordGenerator(existingEmail)
    else:
        display.config(text="Email account not found.")

def retrieveMain():
    existingEmail = emailEntry.get()
    #Runs face recognition
    accessGrant = accessCheck(existingEmail, "retrieval")
    display.config(text="")
    if accessGrant != [True]:
        display.config(text="Access denied.")
    elif existingEmail == "":
        display.config(text="Please enter an email.")
    elif existingEmail in accounts:
        currentPassword = getPassword(existingEmail)
        tk.messagebox.showinfo("Sssshhhh...", "Your password is: "+currentPassword)
    else:
        display.config(text="Email account not found.")

#----GUI----

def register():
    label1.config(text="Enter Email Below to Recieve Password")
    enterButton.config(command=registerMain)
    display.config(text="")
def reset():
    label1.config(text="Enter Existing Email Below to Reset Password")
    enterButton.config(command=resetMain)
    display.config(text="")
def retrieve():
    label1.config(text="Enter Existing Email Below to Retrieve Password")
    enterButton.config(command=retrieveMain)
    display.config(text="")
def default():
    label1.config(text="Select an Option Below")
    enterButton.config(command=default)
    display.config(text="")


#Window
window = tk.Tk()
window.geometry("700x390")
window.title("PassTheWord")
#Entry form
logoPhoto = tk.PhotoImage(file="Logo.png")
logo = tk.Button(window, image=logoPhoto, command=default)
label1 = tk.Label(text="Select an Option Below")
emailEntry = tk.Entry()
enterButton = tk.Button(window, text="Enter", bg="light gray", command=default)
display = tk.Label(fg="red")
space1 = tk.Label()
logo.pack()
label1.pack()
emailEntry.pack()
enterButton.pack()
display.pack()
space1.pack()
#Register
registerPass = tk.Button(window, text="Register for Password", fg="snow3", bg="maroon", width=24, command=register)
space2 = tk.Label()
registerPass.pack()
space2.pack()
#Reset
forgotPass = tk.Button(window, text="Reset Password", fg="snow3", bg="maroon", width=24, command=reset)
space3 = tk.Label()
forgotPass.pack()
space3.pack()
#Retrieve
getPass = tk.Button(window, text="Retrieve Password", fg="snow3", bg="maroon", width=24, command=retrieve)
space4 = tk.Label()
getPass.pack()
space4.pack()
#Pembina Logo
logoPhotoPem = tk.PhotoImage(file="images.png")
logoPhotoPem = logoPhotoPem.subsample(3, 3)
logoPembina = tk.Button(window, image=logoPhotoPem, command=default)
logoPembina.pack()

window.mainloop()
