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

#----Password Variables----

symbols = ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "=", "{", "[", "}", "]", ";", ":", "'", "<", ">", ",", ".", "?", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
adjectiveFile = open('Adjectives.txt')
nounFile = open('Nouns.txt')
adjectiveContent = adjectiveFile.readlines()
nounContent = nounFile.readlines()
#List of passwords and the accounts they're associated to
passwordHash = []
accounts = {}


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
        #Saving image in local storage
        cv.imwrite(email+".jpg", image)
        #If keyboard interrupt occurs, destroy image 
        #Window
        cv.waitKey(0)
        cv.destroyWindow(email)

#----Facial Recognition Code----

def accessCheck(email):
    result, image = cam.read()
    if result:
        #Take new picture
        cv.imshow(email, image)
        cv.imwrite(email+"_reset_"+".jpg", image)
        cv.waitKey(0)
        cv.destroyWindow(email)
        #First image (Original)
        imageArchived = fr.load_image_file(email+".jpg")
        imageArchived = cv.cvtColor(imageArchived, cv.COLOR_BGR2RGB)
        origEncode = fr.face_encodings(imageArchived)[0]
        #Second image (Taken at reset)
        imageNew = fr.load_image_file(email+"_reset_"+".jpg")
        imageNew = cv.cvtColor(imageNew, cv.COLOR_BGR2RGB)
        newEncode = fr.face_encodings(imageNew)[0]
        #Compare both pictures returns [True] or [False]
        return fr.compare_faces([origEncode], newEncode)

#----Password Generation Code----

#New password generation
def passwordGenerator(email):
#Picks random items from above list & files to create password and hash
    randAdjective = random.choice(adjectiveContent)
    randNoun = random.choice(nounContent)
    currentPassword = randAdjective.strip()+random.choice(symbols)+randNoun.strip()+random.choice(symbols)
    currentHash = hash(currentPassword)
    #Checks if password hash already exists and creates new one if yes or saves hash if no
    if currentHash in passwordHash:
        passwordGenerator(email)
    else:
        passwordHash.append(currentHash)
        accounts[email] = currentHash
        #Display new password for user
        tk.messagebox.showinfo("Sssshhhh...", "Your password is: "+currentPassword)

#----Main Code----

def main():
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
    existingEmail = emailEntryReset.get()
    #Runs face recognition
    accessGrant = accessCheck(existingEmail)
    displayReset.config(text="")
    if accessGrant != [True]:
        displayReset.config(text="Access denied.")
    elif existingEmail == "":
        displayReset.config(text="Please enter an email.")
    elif existingEmail in accounts:
        passwordGenerator(existingEmail)
    else:
        displayReset.config(text="Email account not found.")


#----GUI----

def reset():
    label3.pack()
    emailEntryReset.pack()
    enterResetBut.pack()

window = tk.Tk()
window.geometry("700x350")
window.title("PassTheWord")
label1 = tk.Label(text="Enter Email Below", fg="red")
emailEntry = tk.Entry()
enterButton = tk.Button(window, text="Enter", command=main)
display = tk.Label()
space1 = tk.Label()

label3 = tk.Label(text="Enter Existing Email", fg="red")
emailEntryReset = tk.Entry()
enterResetBut = tk.Button(window, text="Enter", command=resetMain)
forgotPass = tk.Button(window, text="Reset Password", fg="red", bg="yellow", command=reset)
displayReset = tk.Label()

label1.pack()
emailEntry.pack()
enterButton.pack()
display.pack()
space1.pack()
forgotPass.pack()
displayReset.pack()

window.mainloop()
