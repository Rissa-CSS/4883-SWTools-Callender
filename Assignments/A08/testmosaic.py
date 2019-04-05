#!/usr/local/bin/python3
import sys

from PIL import Image
import google_images_download #importing the library
#from image_package.color_functions import color_distance
import glob
import random
import cv2
import json
import requests

"""
"""
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

"""
Tries to open a file 
"""
def openFileJson(path):
    try:
      f = open(path, "r")
      data = f.read()
      if is_json(data):
          return json.loads(data)
      else:
          print( "Error: Not json.")
          return {}
    except IOError:
        print("Error: Game file doesn't exist.")
        return {}

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



def colorMatch(col,y):
    data = openFileJson('./Images.json')
    rgb = []
    ClosestImg ={}
    highestper = 0
    imgSelection =[]
    repimg = []
    for x in range(3):
        rgb.append(y[x])
    #print(rgb)
    for imgname, imgdata in data.items():
        for index, colinfo in imgdata.items():
            #print(colinfo["RGB"])

            # Checks to see if any image has this exact color
            if set(rgb).issubset(colinfo["RGB"]):
                # Checks the closest colors dictionary and updates the percentage if it as already there
                print("YES")
                if imgname in ClosestImg.keys():
                    if ClosestImg[imgname] > colinfo["Percent"]:
                        ClosestImg[imgname] = colinfo["Percent"]
                else:
                    ClosestImg[imgname] = colinfo["Percent"]
    if not (ClosestImg):
        for imgname, imgdata in data.items():
            for index, colinfo in imgdata.items():
                #print("Col: ",colinfo)
                if col in colinfo["Colors"].keys():
                    #print("Col: ",col)
                    if imgname in ClosestImg.keys():
                        if ClosestImg[imgname] > colinfo["Percent"]:
                            ClosestImg[imgname] = colinfo["Percent"]
                    else:
                        ClosestImg[imgname] = colinfo["Percent"]
    if (ClosestImg):
        for color, percent in ClosestImg.items():
            #print(color, percent)
            if percent > highestper:
                highestper = percent
        for color, percent in ClosestImg.items():
            if percent == highestper:
                imgSelection.append(color)
        
        return (random.choice(imgSelection))

    else:
        return "NULL"
    
    
def pasteInOrder():
        files = glob.glob('./emojis/**/*.png', recursive=True)
        originalimg = Image.open('./Untitled.jpg').convert("RGBA")
        
        img = originalimg.load()
        colindex =0
        w,h = originalimg.size
        #print(w,h)
        im = Image.new("RGBA", (w*64, h*64), "white")
        a=0
        pastey = 0
        pastex = 0
        for x in range(w):
            for y in range(h):
                c = get_color_data(img[x,y][0],img[x,y][1],img[x,y][2])
                #print(c["result"])
                repimg = "NULL"
                domcol = []
                for colors in c["result"]:
                    domcol.append( colors["name"])
                #print(domcol, "  Length: ",len(domcol))
                #print("")
                
                domcolindex  = 0
                
                while repimg == "NULL":
                    
                    repimg =colorMatch(domcol[domcolindex],img[x,y])
                    domcolindex+=1
                    if domcolindex>=len(domcol):
                        repimg = "./emojis/wolf.png"
            
               
                
                '''print("")
                print("")
                '''
                tmp = Image.open(repimg.replace("\\","/")).convert("RGBA")
                im.paste(tmp, (pastex,pastey),tmp)
                tmp.close()
                
                pastex += 64
            
            pastex = 0
            pastey += 64
            
        #col = c["result"][0]["name"]
        #print(col)
        #print(c)
        
        
        
        #x += 64
        #if x > 1924:
        #x = 0
        #y += 64
        im.show()
        im.save("output.png")
        
        
pasteInOrder()
