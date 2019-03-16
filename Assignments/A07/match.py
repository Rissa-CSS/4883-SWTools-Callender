"""
Course: CMPS 4883
Assignemt: A07
Date: 3/15/19
Github username: Rissa-CSS
Repo url: https://github.com/Rissa-CSS/4883-SWTools-Callender/tree/master/Assignments/A07
Name: Clorissa Callender
Description: 
    Compares an image and determines the closest image in the flder.
"""
# import the necessary packages
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import cv2


def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err
 
def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	
 
	# setup the figure
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f" % (m))
 
	# show first image
	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(imageA, cmap = plt.cm.gray)
	plt.axis("off")
 
	# show the second image
	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(imageB, cmap = plt.cm.gray)
	plt.axis("off")
 
	# show the images
	plt.show()

def resize(img,width,height):
    """
    This resizes the img while maintining aspect ratio. Keep in 
    mind that not all images scale to ascii perfectly because of the
    large discrepancy between line height line width (characters are 
    closer together horizontally then vertically)
    """
    
    wpercent = float(width / float(img.shape[0]))
    hsize = int((float(img.shape[1])*float(wpercent)))
    img = cv2.resize(img, (width ,height))

    return img


if __name__ == '__main__':
    
    #Creates a dictionary for the arguments the users will enter from the command line
    args = {}

    # Creates a list to store all of the Image paths
    allImages = []

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
        #Sets default folder
        folder = "Images"
    
    #Searches the dictionary for the image name
    if 'image' in args:
        image = args["image"]
    else:
        #Sets default image
        image = "original.jpg"
    
    
    #Creates the original photo path
    origimg = folder + '/' + image
    if (os.path.isfile(origimg)):
        
        #Reads the image and converts it to greyscale
        original = cv2.imread(origimg)
        original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        w,h = original.shape
    
    
        #Loops through the files in the give folder
        for filename in os.listdir(folder):
            #Checks to see if it is a picture format of (.jpg,.png,jpeg)
            if filename.endswith(".jpg") or filename.endswith(".jpeg")  or filename.endswith(".png"): 
                #Checks that the original image in not added to the list
                if (os.path.join(folder, filename) != folder + '\\'+ image):
                    
                    #Replaces all \ with / so that the path can be found
                    allImages.append(os.path.join(folder, filename).replace('\\','/'))
        
        
        if (len(allImages)>1):#opens the first image and converts it to greyscale
            im =cv2.imread(allImages[0])
            im =cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        
            #Calculates the mean squared value from the original to the first image
            closest = mse(original,im)
            
            #Loops through the dictionary of image paths
            for images in allImages:
                #opens the image and converts it to greyscale
                im =cv2.imread(images)
                im =cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                #Resize the images to the size of the original
                im=resize(im,w,h)
                
                #Calculates mean squared distance of the image to the original image
                meansqval = mse(original,im)
                
                #Checks to see if the mean squared value is more than 0
                if (meansqval >0):
                    #Checks if the mse is less than the one currently closest
                    if (meansqval < closest):
                        closest = meansqval
                        
            # Loops throguh all the images again
            for images in allImages:
                #Read and convert images to greyscale again
                im =cv2.imread(images)
                im =cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                im=resize(im,w,h)
                #If this is the closest image to the original both are printed
                if ( mse(original,im) == closest):
                    compare_images(original, im, "Original vs Closest Image")
        else:
            #Tells the user the folder has no other images but the original
            print("Your folder is empty")
        
    else:
        #Tells the user they have entered an invalid path
        print("This photo path does not exist!")
