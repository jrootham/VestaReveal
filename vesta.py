#!/usr/bin/python
from PIL import Image
from random import uniform
from Queue import PriorityQueue
from math import sqrt
import sys, getopt


def print_file(inputfile):
    im = Image.open(inputfile) #Can be many different formats.
    pix = im.load()
    dimensions = im.size #Get the width and hight of the image for iterating over
    width = dimensions[0]
    height = dimensions[1]
    # print "Width: %s, Height:%s" %(width,height)
    for i in range(0,width):
        x = []
        for j in range(0, height):
            x.append(pix[i,j][0]) #just the first layer
        print str(x).strip('[]')

xx = 0

def trace_point(input, output, x,y,max_x,max_y):
    # spill the water
    global xx
    xx +=1
    if output[x,y][0] == 255:
        pass
        # spill water aroind
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

def trace_map(inputfile, outputfile, iterations):
    im = Image.open(inputfile)
    output = Image.new('RGBA',im.size)
    pix = im.load()
    dimensions = im.size
    width = dimensions[0]
    height = dimensions[1]
    out = output.load()
    for i in range(0,width):
        for j in range(0, height):
            out[i,j]=(0,0,0,255)
    for i in range(0,iterations):
        rand_x = int(uniform(0, width))
        rand_y = int(uniform(0, height))
        trace_point(pix,out,rand_x, rand_y,width,height)
    print "Ran total of %s iterations" % xx
    output.save(outputfile)

### UNFINISHED - A* path finding algorithm on modified map
def heuristic(a, b):
    x= abs(a[0] - b[0])+ abs(a[1] - b[1])
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
# END UNFINISHED

def read_data(filename_in, filename_out, mode=8):
    f = open(filename_in,"r")
    line="xx"
    str_arra =[]
    height = 500
    width = 1000
    print "Converting ASCII input into grayscale PNG"
    if mode==8:
        output = Image.new('RGBA',(width,height))
    elif mode==16:
        output = Image.new('I',(width,height))
    out = output.load()
    y = -1
    while(len(line)>0):
        line = f.readline().strip()
        str_arra = line.split(' ')
        if len(str_arra)>1:
            w= len(str_arra)
            y=y+1
            for x in range(0, w):
                if mode==8:
                    out[x,y] = (int(str_arra[x]),int(str_arra[x]),int(str_arra[x]),255)
                elif mode==16:
                    out[x,y] = int(str_arra[x])
    output.save(filename_out)

def main(argv):
    inputfile = ''
    outputfile = ''
    task = ''
    mode =8
    try:
        opts, args = getopt.getopt(argv,"ht:i:o:m:d:",["task=","ifile=","ofile=","mode=","drops="])
    except getopt.GetoptError:
        print 'vesta.py -t <task> -i <inputfile> -o <outputfile> -m <mode> -d <drops>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'vesta.py -t <task> -i <inputfile> -o <outputfile> -m <mode> -d <drops>'
            sys.exit()
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-t", "--task"):
            task = arg
        elif opt in ("-m", "--mode"):
            mode = int(arg)
        elif opt in ("-d", "--drops"):
            drops = int(arg)
    if task == "ascii_to_png":
        read_data(inputfile,outputfile,mode)
    if task == "trace_map":
        trace_map(inputfile,outputfile,drops)
    if task == "img_to_ascii":
        print_file(inputfile)

main(sys.argv[1:])
