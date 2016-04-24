#!/usr/bin/python
from PIL import Image
from random import uniform
from Queue import PriorityQueue
from math import sqrt
def print_file():
    im = Image.open("vesta_medium.tiff") #Can be many different formats.
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

xx = 0

def trace_point(input, output, x,y,max_x,max_y):
    # spill the water
    global xx
    xx +=1
    if output[x,y][0] == 255:
        pass
        # for i in range(1,-2,-1):
        #    for j in range(1,-2,-1):
        #        if x+i<max_x and y+j<max_y and x+i>=0 and y+j>=0 and x+i!=x and y+j!=y:
        #            if output[x+i,y+j][0]<255:
        #                output[x+i,y+j] = output[x+i,y+j]+1
    else:
        output[x,y] = (output[x,y][0]+1,output[x,y][1]+1,output[x,y][2]+1,255)

    min_y = y
    min_x = x
    for i in range(1,-2,-1):
        for j in range(1,-2,-1):
            if x+i<max_x and y+j<max_y and x+i>=0 and y+j>=0 and x+i!=x and y+j!=y:
                if input[x+i,y+j][0]<input[x,y][0]:
                    min_y =y+j
                    min_x =x+i
    if min_y!=y and min_x!=x:
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
    for i in range(0,10000000):
        rand_x = int(uniform(0, width))
        rand_y = int(uniform(0, height))
        trace_point(pix,out,rand_x, rand_y,width,height)
        # trace drop
        # check neighbor
        # add the paths until not longer possib
        # track point relief

        #value = (111,111,111,255)
        #out[rand_x, rand_y] = pix[rand_x,rand_y];
    #for i in range(0,width):
    #    for j in range(0, height):
    #        if (out[i,j][0]<255):
    #            out[i,j] = (0,0,0,255)
    output.save('output.png')

def flatten_file():
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
            if pix[i,j][0]<127:
                out[i,j]=pix[i,j]
            else:
                out[i,j]=0
    #for i in range(0,10000000):
    #    rand_x = int(uniform(0, width))
    #    rand_y = int(uniform(0, height))
    #    trace_point(pix,out,rand_x, rand_y,width,height)
        # trace drop
        # check neighbor
        # add the paths until not longer possib
        # track point relief

        #value = (111,111,111,255)
        #out[rand_x, rand_y] = pix[rand_x,rand_y];
    #for i in range(0,width):
    #    for j in range(0, height):
    #        if (out[i,j][0]<255):
    #            out[i,j] = (0,0,0,255)
    output.save('output.png')
    # print pix[x,y] #Get the RGBA Value of the a pixel of an image
    # pix[x,y] = value

def heuristic(a, b):
    x= abs(a[0] - b[0])+ abs(a[1] - b[1])
    print x
    return x

def find_path(start, goal):
    global xx
    im = Image.open("output.png") #Can be many different formats.
    output = Image.new('RGBA',im.size)
    pix = im.load()
    dimensions = im.size #Get the width and hight of the image for iterating over
    width = dimensions[0]
    height = dimensions[1]
    # initial parameters
    frontier = PriorityQueue()
    frontier.put(start,0)
    closed_set = []
    costs_so_far ={}
    came_from = {}
    open_set=[start]
    costs_so_far[start] = 0
    came_from[start] = None
    max_y = height
    max_x = width
    while not frontier.empty():
        xx = xx+1
        current = frontier.get()
        if current[0] == goal[0] and current[1] == goal[1]:
            break;
        x = current[0]
        y = current[1]
        for i in range(-1,2):
            for j in range(-1,2):
                if x+i<max_x and y+j<max_y and x+i>=0 and y+j>=0 and x+i!=x and y+j!=y:
                    new_cost = costs_so_far[current] + pix[x+i,y+j][0]
                    if (x+i,y+j) not in costs_so_far or new_cost < costs_so_far[(x+i,y+j)]:
                        costs_so_far[(x+i,y+j)] = new_cost
                        priority = new_cost + heuristic(goal, (x+i,y+j))
                        frontier.put((x+i,y+j), priority)
                        came_from[(x+i,y+j)] = current
        if xx>1000:
            break
            #print current
    return (came_from, costs_so_far)

def read_data():
    f = open("vesta_data_dump.txt","r")
    line="s2"
    str_arra =[2,3]
    height = 500
    width = 1000
    output = Image.new('I',(width,height))
    out = output.load()
    y = -1
    while(len(line)>0):
        line = f.readline().strip()
        str_arra = line.split(' ')
        if len(str_arra)>1:
            width= len(str_arra)
            y=y+1
            for x in range(0, width):
                print "%s:%s" % (x,y)
                out[x,y] = int(str_arra[x])

    output.save('output2.png')

def main():
    # read_data()
    #process_file()
    results= find_path((400,240),(500,250))
    #print results[0]
    #print "%s points processed" % xx
    # flatten_file()
main()
