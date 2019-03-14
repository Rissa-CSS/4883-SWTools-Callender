"""
Course: CMPS 4883
Assignemt: A05
Date: 3/07/19
Github username: Rissa-CSS
Repo url: https://github.com/Rissa-CSS/4883-SWTools-Callender/tree/master/Assignments/A05
Name: Clorissa Callender
Description: 
    To convert an image to ascii art.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def img_to_ascii(**kwargs):
    """ 
    The ascii character set we use to replace pixels.
    0 - 17 = 'W' (darkest character)
    238-255 = '.' (lightest character)
    """
    
    ascii_chars = [ "W", 'M', 'B', 'R', 'A', '1','f','j','q','n','u', 'a', 'c', ',', '.']
  
    
    width = kwargs.get('width',200)
    height = kwargs.get('height',200)
    FontName=kwargs.get('FontName')
    FontSize=kwargs.get('FontSize')
    path = kwargs.get('path',None)
    SavedImage = kwargs.get('SavedImage')
    
    #Opens the image
    im = Image.open(path)
    #Resizes the Image
    im = resize(im,width)
    #Loads the image into a new variable
    test =im.load()
    #gets the width and height of the new variable
    w,h = im.size
    #Creates a new blank image
    newImg = Image.new('RGBA',(w,h),(255,255,255,255))
    #Sets the font
    fnt = ImageFont.truetype(FontName,FontSize)
    #Draws on new image
    drawOnMe = ImageDraw.Draw(newImg)
    imlist = list(im.getdata())
    i = 1
    
    counter =0
    #Loops through the values for the width
    for x in range(w): 
        #Loops through the values for the height
        for y in range(h):
            #Gets the RBGA/RBG value of the pixel
            val = test[x,y]
            #Shifts the width and height by 10
            wid = x +10
            y += 10
            #Calculates which ascii char to replace a pixel with based on color
            avg = sum(val)//4
            uni = ascii_chars[avg//25]
            #Draws the char on the new image
            drawOnMe.text((wid,y),uni,font = fnt, fill=val)
            counter +=1
    
    #Shows and saves the new image
    
    newImg.show()
    newImg.save(SavedImage)

    
    
def resize(img,width):
    """
    This resizes the img while maintining aspect ratio. Keep in 
    mind that not all images scale to ascii perfectly because of the
    large discrepancy between line height line width (characters are 
    closer together horizontally then vertically)
    """
    
    wpercent = float(width / float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((width ,hsize), Image.ANTIALIAS)

    return img


if __name__=='__main__':
    #Gets the path of the new image
    #path = 'C:/Users/Chloe/Documents/Users/Clorissa/Computer Science/Software/4883-SWTools-Callender/Assignments/A05/me.jpg'
    #Checks if 4 values have been entered: path, output image name, font name and font size

    if(len(sys.argv) ==5):
        # Gets the values from command line and stores them in the respective variables
        path = sys.argv[1]
        SavedImage = sys.argv[2]
        FontName =sys.argv[3]
        FontSize = int(sys.argv[4])
    
    else:
        #Default values incase the user did not input any
        path='4883-SWTools-Callender/Assignments/A05/Images/me.jpg'
        SavedImage ='4883-SWTools-Callender/Assignments/A05/output_images/output.png'
        FontName = '4883-SWTools-Callender/Assignments/A05/Fonts/Shailena.ttf'
        FontSize = 12

     #Calls the function convert the image to ascii    
    img_to_ascii(path=path,SavedImage=SavedImage,FontName=FontName, FontSize=FontSize)
