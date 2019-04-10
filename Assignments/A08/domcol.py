"""
Course: CMPS 4883
Assignemt: A08
Date: 4/1/19
Github username: Rissa-CSS
Repo url: https://github.com/Rissa-CSS/4883-SWTools-Callender/tree/master/Assignments/A08
Name: Clorissa Callender
Description: 
    Accepts a folder of images and processes it and saves the results in a JSON file.
    
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import Image
import sys,os
import pprint
import requests
from math import sqrt
import glob
import json

def brightness(r,g,b):
    """A function to return the calculated "brightness" of a color.
    http://www.nbdtech.com/Blog/archive/2008/04/27/Calculating-the-Perceived-Brightness-of-a-Color.aspx
    Arguments:
        r: [int]
        g: [int]
        b: [int]
    Returns:
        Values between 0-1 (percent of 0-255)
    Used By:
        get_dominant_colors
    """
    return sqrt(pow(r,2) * .241  + pow(g,2) * .691 + pow(b,2) * .068 ) / 255

def find_histogram(clt):
    """ Create a histogram with k clusters
    Arguments:
        :param: clt
        :return:hist
    Used By:
        get_dominant_colors
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist


def get_color_data(r,g,b,d=3):
    """Get color name and hsv from color api.
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


def extract_cluster_color_values(hist, centroids,ignore_background=False):
    """Get the dominant colors of an image.
    Arguments:
        hist        -- [numpy.ndarray]
        centroids   -- [numpy.ndarray] 
    Returns:
        dictionary of color values
    Used By:
        get_dominant_colors
    """

    colors = []
    
    for (percent, color) in zip(hist, centroids):
        rgb = []
        total = 0
        for c in color:
            c = round(float(c))
            total += c
            rgb.append(c)
        if ignore_background:
            if total > 15 and total < 750:
                colors.append({'percent':round(float(percent),2),'rgb':rgb})
        else:
            colors.append({'percent':round(float(percent),2),'rgb':rgb})

    return colors

def plot_colors(hist, centroids):
    """Get the dominant colors of an image.
    Arguments:
        hist        -- [numpy.ndarray]
        centroids   -- [numpy.ndarray] 
    Returns:
        plot image
    """
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar


def get_dominant_colors(img,save_path=None,n=3):
    """Get the dominant colors of an image.
    Arguments:
        img         -- the image [string, numpy.ndarray]
        save_path   -- out path for saving [string] (default None)
        n           -- number of clusters [int] (default 3)
    Returns:
        dictionary of colors
        load_subimages_data
    Requres:
        extract_cluster_color_values
        query_color
        brightness
    """

    #bg,_ = determine_background(img_path)

    # if its string open it
    if isinstance(img,str):
        print(img)
        if os.path.isfile(img):
            img = cv2.imread(img)
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            usage("Error: image path not valid")

    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number

    clt = KMeans(n_clusters=n) #cluster number
    clt.fit(img)

    hist = find_histogram(clt)
    colors = extract_cluster_color_values(hist, clt.cluster_centers_,True)

    if save_path != None:
        bar = plot_colors(hist, clt.cluster_centers_)
        cv2.imwrite(save_path,bar)
        # plt.axis("off")
        #plt.imshow(bar)
        #plt.show()

    start_delta = 3

    # loop through each cluster
    for i in range(len(colors)):
        c = []
        d = start_delta
        # while we haven't found a named color match (increment delta)
        while len(c) < 1:
            #c = query_color(colors[i]['rgb'][0],colors[i]['rgb'][1],colors[i]['rgb'][2],d)
            c = get_color_data(colors[i]['rgb'][0],colors[i]['rgb'][1],colors[i]['rgb'][2],d)
            d += 3
        colors[i]['named_data'] = c
        colors[i]['brightness'] = brightness(colors[i]['rgb'][0],colors[i]['rgb'][1],colors[i]['rgb'][2])

    return colors



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
    #Searches the dictionary to see if a folder was entered
    if 'folder' in args:
        #If the key exists then the folder is set to what the user entered
        folder = args["folder"]
    else: 
        folder = './emojis'
    #Searches the dictionary to see if a folder was entered
    if 'outfile' in args:
        #If the key exists then the folder is set to what the user entered
        outfile = args["outfile"]
    else: 
        outfile = 'Images'

    files = glob.glob('./'+folder+'/**/*.png', recursive=True)
    #Dictionary that stores the color data for each sub image
    allColors = {}

    #Loops through the images in the folder
    for file in files:
        img = file
       
        # gets a json of dominant colors
        colors = get_dominant_colors(img)
        # Creates a dictionarty for each image
        allColors[img] = {}
        
        x=0
        #Loops through json of color data that is returned
        for info in colors:
            #Creates a dictionary for all of the colors that are in the image
            allColors[img][x] = {}
            
            #Loops through the dictionary
            for k,v in info.items(): 
                #Adds the Percentage, RGB, Brightness, and the colors close to the dominant colors
                allColors[img][x]["Percent"] = info["percent"]
                allColors[img][x]["RGB"] = info["rgb"]
                allColors[img][x]["Brightness"] = info["brightness"]
                allColors[img][x]["Colors"] = {}
                
                #Loops through the dominant colors 
                for result in info["named_data"]["result"]:
                    # Gets the results of the dominnat colors
                    for named,nameinfo in result.items():
                        #Checks to see if the color is already in the image's dictionary
                        if result["name"] not in allColors[img][x]["Colors"].keys():
                            #Creates a dictionary if the color has not been added as yet
                            allColors[img][x]["Colors"][result["name"]] = {}
                        # Adds the R G B values of the color and the distant from the dominant colors
                        allColors[img][x]["Colors"][result["name"]]["R"] = result["r"]
                        allColors[img][x]["Colors"][result["name"]]["G"] = result["g"]
                        allColors[img][x]["Colors"][result["name"]]["B"] = result["b"]
                        allColors[img][x]["Colors"][result["name"]]["Distance"] = result["dist"]
                    

            x=x+1
    #Opens a JSON file to save the images' color data
    f = open( outfile + ".json","w")
    #Dumps the dictionary into the file
    f.write(json.dumps(allColors))
    # Closes dictionary
    f.close()

