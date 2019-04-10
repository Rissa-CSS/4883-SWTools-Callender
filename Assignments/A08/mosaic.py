"""
Course: CMPS 4883
Assignemt: A08
Date: 4/1/19
Github username: Rissa-CSS
Repo url: https://github.com/Rissa-CSS/4883-SWTools-Callender/tree/master/Assignments/A08
Name: Clorissa Callender
Description: 
    Creates a mosaic of subimages from a folder entered by the user.
"""

import sys
from PIL import Image
import google_images_download #importing the library
#from image_package.color_functions import color_distance
import glob
import random
import cv2
import json
import requests
import os

def is_json(myjson):
    
    """
    Checks to see if a file is a json file.
    """
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


def openFileJson(path):
    """
    Tries to open a file 
    """
    try:
      f = open(path, "r")
      data = f.read()
      if is_json(data):
          return json.loads(data)
      else:
          print( "Error: Not json.")
          return {}
    except IOError:
        print("Error: File doesn't exist.")
        return {}

def get_color_data(r,g,b,d=3):
    """
    Get color name and hsv from color api.
    Arguments:
        r -- red   [int]
        g -- green [int]
        b -- blue  [int]
    Returns:
        json
    """
    payload = {'r':r, 'g':g, 'b':b,'d':d}
    r = requests.get('http://cs.mwsu.edu/~griffin/color-api/', params=payload)
    return r.json()



def colorMatch(col,y,datafile):
    """
    Gets the emoji color to the color of the pixel.
    Arguments:
        col -- name of the color [str]
        y -- tuple of rgba values [int]
    Returns:
        str
    """
    # Opens the file with color data from the subimages
    data = openFileJson('./'+datafile)
    # Creates a list to store the rgb values of the pixel
    rgb = []
    # Creates a dictionar to store data about the closest images
    ClosestImg ={}
    #Value of the highest percentage of color closest to the pixel
    highestper = 0
    # List of Images to select from
    imgSelection =[]
    #
    repimg = []

    # Loops through the color tuple and convert it to a list
    for x in range(3):
        rgb.append(y[x])
    # Loops through the data in the JSON file
    for imgname, imgdata in data.items():
        for index, colinfo in imgdata.items():
            # Checks to see if any image has this exact color
            if set(rgb).issubset(colinfo["RGB"]):
                # Checks the closest colors dictionary and updates the percentage if it as already there
                if imgname in ClosestImg.keys():
                    if ClosestImg[imgname] > colinfo["Percent"]:
                        ClosestImg[imgname] = colinfo["Percent"]
                else:
                    ClosestImg[imgname] = colinfo["Percent"]
    # Checks to see if dictionary is empty(No perfect matches found)
    if not (ClosestImg):
        # Loops through the color data from the JSON file
        for imgname, imgdata in data.items():
            for index, colinfo in imgdata.items():
                # Loops through the colors closest to the emojis to see if the original color is
                # in an emoji
                if col in colinfo["Colors"].keys():
                    # Checks the closest colors dictionary and updates the percentage if it as already there
                    if imgname in ClosestImg.keys():
                        if ClosestImg[imgname] > colinfo["Percent"]:
                            ClosestImg[imgname] = colinfo["Percent"]
                    else:
                        ClosestImg[imgname] = colinfo["Percent"]
    # Makes sure the dictionar is not empty
    if (ClosestImg):
        # Loops through the dictionary of Closest Images to see which Images have the highest 
        # percentage of the desired colors
        for color, percent in ClosestImg.items():
            if percent > highestper:
                highestper = percent
        for color, percent in ClosestImg.items():
            if percent == highestper:
                imgSelection.append(color)
        #Random resturns an image name from the images with the highest percentage
        return (random.choice(imgSelection))

    else:
        #Returns null if the Closest Image dictionary is empty
        return "NULL"
    
    
def pasteInOrder(original,sw,sh, saveImage,data):    
    
    """
    Gets the emoji color to the color of the pixel.
    Arguments:
        orignal -- The name of the image that the mosaic is to be created. [str]
        sw -- width of subimage [int]
        sh -- heigh of subimage [int]
        saveImage -- Name of output image [str]
        data -- name of file for color data [str]
    Returns:
        NONE
    """

    #Opens the orignal Image
    originalimg = Image.open(original).convert("RGBA")
    #Loads the image
    img = originalimg.load()
    # Gets the width and height of the original image
    w,h = originalimg.size
    # Creates a new White image
    im = Image.new("RGBA", (w*sw, h*sh), "white")
    
    # Stores the locations of x,y that an image shoulld be pasted at
    pastey = 0
    pastex = 0
    
    # Loops through the pixels of an image
    for y in range(h):
        for x in range(w):
            # Calls the get_color_data to get dictionary of color data of the current pixel
            c = get_color_data(img[x,y][0],img[x,y][1],img[x,y][2])
            # Stores the name of the replacement image
            repimg = "NULL"
            # List of the colors returned 
            domcol = []
            # Loops through the dictionary returned from get_color_dat
            for colors in c["result"]:
                #aDDS COLORS TO THE list
                domcol.append( colors["name"])
            # Keeps tracks of index of elements in domcol
            domcolindex  = 0
            # Distance from original color
            delta = 0
            # Loops until a replacement image is found
            while repimg == "NULL":
                # Checks to see if the loop had gone through every color in the list
                if domcolindex<=len(domcol):
                    # Calls colorMatch function to get name of image closest to the pixel
                    repimg =colorMatch(domcol[domcolindex],img[x,y],data)
                    #increments index counter by 1
                    domcolindex+=1
                else:
                    #If all the colors of the list has been search the range of color of the pixel is adjusted to + or - delta
                    if img[x,y][0] in range(img[x,y][0]-delta, img[x,y][0]+delta) and img[x,y][1] in range(img[x,y][1]-delta,img[x,y][1]+delta) and img[x,y][2] in range(img[x,y][2]-delta,img[x,y][2]+delta):
                            # Gets the color data for the pixel within the new range delta
                            newcolors = get_color_data(img[x,y][0],img[x,y][1],img[x,y][2],delta)
                            for colors in newcolors["result"]:
                                #Calls color match for the name of the replacemnt image closest to the new pixel color
                                repimg = colorMatch(colors["name"],(colors["r"],colors["g"],colors["b"]),data)
                    #Increments the range by 5
                    delta += 5
            
            # Opens the replacemnet image and converts it to RGBA
            tmp = Image.open(repimg.replace("\\","/")).convert("RGBA")
            tempw, temph = tmp.size
            # Pastes the image and mask it with itself so the background does not show
            im.paste(tmp, (pastex,pastey),tmp)
            # Closes the image
            tmp.close()
            # Increments the x loctaion by the width of the image
            pastex += tempw
        # Resets the x 
        pastex = 0
        # Increments locations of y by height of image
        pastey += temph
        
    #Shows the mosaic image and saves it with the file name entered
    im.show()
    im.save(saveImage)


if __name__=='__main__':
    #Creates a dictionary for the arguments the users will enter from the command line
    args = {}
    files = []
    #Checks to see if the user enters arguments besides the file name
    if (len(sys.argv)>1):
        #Loops through the list of arguments entered after the file name
        for arg in sys.argv[1:]:
            #Splits the arguments on the = into a key value pair
            k,v = arg.split('=')
            args[k] = v
    #Searches the dictionary to see if a the original path was entered was entered
    if 'original' in args:
        #If the key exists then the original path is set to what the user entered
        original = args["original"]
    else: 
        original = './emojis/8ball.png'
    #Searches the dictionary to see if a width was entered
    if 'subwid' in args:
        #If the key exists then the width is set to what the user entered
        sw = args["subwid"]
    else: 
        sw = 64
    #Searches the dictionary to see if a height was entered
    if 'subhei' in args:
        #If the key exists then the height is set to what the user entered
        sh = args["subhei"]
    else: 
        sh = 64
    filename = os.path.basename(original) # get only filename if image is read with a path. 
    name,ext = filename.split('.')
    
    #Searches the dictionary to see if a save image name was entered
    if 'outputimage' in args:
        #If the key exists then the folder is set to what the user entered
        outimg = './'+args["outputimage"]+'./' + name+'_mosaic'+'.'+ext 
    else: 
        outimg = name+'_mosaic'+'.'+ext       
    # Calls the mosaic function
    if 'data' in args:
        #If the key exists then the height is set to what the user entered
        datafile = args["data"]
    else: 
        datafile = './Images.json'
    pasteInOrder(original,int(sw),int(sh),outimg,datafile)