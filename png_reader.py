#!/usr/bin/python
from PIL import Image
from random import uniform

def print_file():
    im = Image.open("vesta_medium.png") #Can be many different formats.
    pix = im.load()
    dimensions = im.size #Get the width and hight of the image for iterating over
    width = dimensions[0]
    height = dimensions[1]
    # print "Width: %s, Height:%s" %(width,height)
    for i in range(0,width):
        x = []
        for j in range(0, height):
            x.append(pix[i,j][0])
        print str(x).strip('[]')


def trace_point(input, output, x,y,max_x,max_y):
    output[x,y] = ((output[x,y][0]+1)%256, (output[x,y][1]+1)%256, (output[x,y][2]+1)%256,output[x,y][3])
    min_y = y
    min_x = x
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i<max_x and y+j<max_y and x+i>=0 and y+j>=0:
                if input[x+i,y+j][0]<input[x,y][0]:
                    min_y = y+j
                    min_x = x+i
    if min_x !=x or min_y !=y:
        trace_point(input,output,min_x,min_y,max_x,max_y)
    else:
        return

def process_file():
    im = Image.open("vesta_medium.png") #Can be many different formats.
    output = Image.new('RGBA',im.size)
    pix = im.load()
    dimensions = im.size #Get the width and hight of the image for iterating over
    width = dimensions[0]
    height = dimensions[1]
    # print "Width: %s, Height:%s" %(width,height)
    out = output.load()
    # clear file
    for i in range(0,width):
        for j in range(0, height):
            out[i,j]=(0,0,0,255)
    for i in range(0,4000000):
        rand_x = int(uniform(0, width))
        rand_y = int(uniform(0, height))
        trace_point(pix,out,rand_x, rand_y,width,height)
        # trace drop
        # check neighbor
        # add the paths until not longer possib
        # track point relief

        #value = (111,111,111,255)
        #out[rand_x, rand_y] = pix[rand_x,rand_y];
    output.save('output.png')

    # print pix[x,y] #Get the RGBA Value of the a pixel of an image
    # pix[x,y] = value

def main():
    process_file()
main()
