## Assignment 8 - Image Mosaic
### Date: Monday, April 1<sup>st</sup>

## Background

### Assignment A08 contains the following file/folders:

- domcol.py: This file contains the code which processes the folder of subimages 
              to be used for the mosaic.

- mosaic: This file contains code that uses the JSON file created by the previous 
          program to create the a mosaic.

- emojis: This foolder contains the 64 x 64 emoji images from thr scrapping assignment.

- subimages: This folder contains more emojis that are 16 x 16.

- Images.json: This is a JSON file with the color data results after running domcol.py using
               emojis folder.

- ImagesTest.json: This is a JSON file with the color data results after running domcol.py using
                   subimages folder.
        
- output.png: This is the mosaic image produced using the emojis from the subimages folder.

- output2.png: This is the mosaic image produced using the emojis from the emojis folder.

### How to run program:

1) Run domcol.py first. The user is able to give a folder for the subimages and an output filename 
    for the json results.

    Example Prompt:

        python domcol.py folder=emojis outfile=Images


2) Next run mosaic.py. This produces the mosaic.Data refers to the json file produced in step 1 so make       sure you enter the same file name.

    Example Prompt:

        python mosaic.py original=./emojis/8ball.png subwid=64 subhei=64 outputimage=Mosaic data=Images.json
