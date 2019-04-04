#!/usr/local/bin/python3
import sys
sys.path.append('/Users/griffin/Dropbox/Scripts-random/image_projects/image_package')

from PIL import Image
import google_images_download #importing the library
#from image_package.color_functions import color_distance
import glob
import random


"""
"""

def pasteInOrder():
    files = glob.glob('./emojis/**/*.png', recursive=True)

    print(len(files))
    
    im = Image.new("RGBA", (1924, 1924), "white")

    x = 0
    y = 0
    #for f in files:
    #print(f)
    tmp = Image.open('./emojis/two_hearts.png').convert("RGBA")
    im.paste(tmp, (x,y),tmp)
    tmp.close()
    #x += 64
    #if x > 1924:
    #x = 0
    #y += 64
    im.show()

pasteInOrder()