# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:53:39 2018

@author: William Keilsohn
"""

'''
I'm not gonna lie, I got about 75% of the way through this project and found it a little boring. 
I mean, I make charts for all my other classes, my research, and even a few side projects.
I just really wanted to have more fun with the programing or problem solving part of this project, and worry less about the problem itself.
So I thought I could spice it up a bit by having the suprise be that statistics would print out on memes.
This files handles those images
'''

# Import packages
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import imread, imsave, imresize
from PIL import Image, ImageDraw, ImageFont


# Save all the data I care about 

### Sources for all the signs
### I cleaned a few of them up in FireAlpaca so that python could write on a blank canvas
### Also it should go without saying, that I don't own any of these images nor any part(s) of the properties the girl(s) belong to.
g1 = 'https://imgflip.com/memetemplate/106117641/girl-anime'
g2 = 'https://imgflip.com/memetemplate/124725559/Caption-Neos-Sign'
g3 = 'https://vignette.wikia.nocookie.net/epicrapbattlesofhistory/images/b/b0/Mugi_holding_a_sign_meme_3.png/revision/latest?cb=20161226225349'
g4 = 'https://twitter.com/LitAnimemes/status/1015030153242693632'
g5 = 'https://steamcommunity.com/sharedfiles/filedetails/?l=russian&id=1260045708'
g6 = 'https://me.me/i/where-my-memes-komi-san-say-224cc8eb2aeb42a6a3cb6dc1afa6a120'

sourceLis = [g1, g2, g3, g4, g5, g6]


# Image handeling

# Load in the images
programLoc = 'C://Users//kingw//Documents//CISC8000_Projects_2018'
folderLoc = programLoc + '//FBIdata'
signFolder = folderLoc + '//signs//' #Directs to the folder with the images

imageLis = ['g1', 'g2', 'g3', 'g4', 'g5', 'g6'] #Image names

def textWritter(text, num): #https://stackoverflow.com/questions/16373425/add-text-on-image-using-pil
    image = imageLis[num]
    imValue = signFolder + image + '.jpg'
    tempPic = Image.open(imValue)
    newTempPic = ImageDraw.Draw(tempPic)
    if num >= 3: ### Function determines the placement of text on the images.
        if num == 3: #Fits
            x = 450
            y = 200
        elif num == 4: # Fits.
            x = 100
            y = 100
        else:
            x = 75
            y = 75
    elif num == 1: # Fits, but could always look a little nicer.
        x = 350
        y = 590
    else:
        if num == 0: #Fits
            x = 200
            y = 370
        else: # Fits.
            x = 75
            y = 210
    newTempPic.text((x , y), text, (0, 0, 0)) #https://www.rapidtables.com/web/color/black-color.html
    tempPic.save(signFolder + 'temp_pic.jpg')
    displayImg = plt.imread(signFolder + 'temp_pic.jpg') # Array lab/lecture
    plt.imshow(displayImg) # Array lab/lecture
    
