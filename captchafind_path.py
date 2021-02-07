import cv2
import os
from PIL import Image
import numpy as np
import sys
import pytesseract
from PIL import  ImageFilter

def bw(im):
    originalImage = cv2.imread(im)
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 180, 255, cv2.THRESH_BINARY)
    #cv2.imshow('Black white image', blackAndWhiteImage)
    cv2.imwrite('blackwhite.jpeg', blackAndWhiteImage)
    return blackAndWhiteImage
def lineremove(img):
    img = Image.open(img) # get image
    pixels = img.load() # create the pixel map
    rgb_im = img.convert('RGB')
    r, g, b = rgb_im.getpixel((1, 1))
    pixels = rgb_im.load() # create the pixel map
    width, height = img.size 
    iar = np.asarray(rgb_im)
    print("Image size=",img.size)
    n=0
    for i in range(img.size[0]): # for every pixel:
        for j in range(img.size[1]):
            if ((i>15 and i<120)and j==21 ): # if not white:
                pixels[i,j] = (255,255,255)
    rgb_im.save('lineremoved.jpeg', format='JPEG')

def fill(imag):
    img = Image.open(imag) # get image
    pixels = img.load() # create the pixel map
    rgb_im = img.convert('RGB')
    r, g, b = rgb_im.getpixel((1, 1))
    pixels = rgb_im.load() # create the pixel map
    width, height = img.size 
    iar = np.asarray(rgb_im)
    n=0
    #print(np.asarray(rgb_im))
    for i in range(img.size[0]): 
        for j in range(img.size[1]):
            if (j==21 ):
                ui=pixels[i,j-1][0]
                uj=pixels[i,j-1][1]
                di=pixels[i,j+1][0]
                dj=pixels[i,j+1][1]

                
                try:
                    ui1=pixels[i+1,j-1][0]
                    uj1=pixels[i+1,j-1][1]
                    di1=pixels[i-1,j+1][0]
                    dj1=pixels[i-1,j+1][1]
                    ni=30
                    nj=30
                    if((ui<=ni and uj<nj and di<=ni and dj<nj)or (ui1<=ni and uj1<nj and di1<=ni and dj1<nj)):
                        pixels[i,j]=(0,0,0)
                except:
                    pass

               
    #rgb_im.show()
    rgb_im.save('final.jpeg', format='JPEG')
     
def textconvert(im):
      # Read image path from command line
      imPath = im 
      # Uncomment the line below to provide path to tesseract manually
      #pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
      # Define config parameters.
      # '-l eng'  for using the English language
      # '--oem 1' for using LSTM OCR Engine
      config = ('-l eng  --psm 3 --oem 1')
      # Read image from disk
      im = cv2.imread(imPath, cv2.IMREAD_COLOR)
      # Run tesseract OCR on image
      text = pytesseract.image_to_string(im, config=config)
      # Print recognized text
      final_text = text.lower()
      return final_text
def mainpage(file):
    file=str(file)
    try:
        bw(file+'.jpg')
    
    except:
        try:
            bw(file+'.jpeg')
        except:
            bw(file+'.png')
    lineremove('blackwhite.jpeg')
    fill('lineremoved.jpeg')
    textf=textconvert('final.jpeg')
    return textf
#mainpage('imahe name') 
