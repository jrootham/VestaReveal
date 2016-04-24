__author__ = 'jrootham'

import sys
import math

infile = open(sys.argv[1], 'r')
outfile = open(sys.argv[2], 'w')

for line in infile:
    text = line.split()
    pos=[]
    for i in range(len(text)):
        pos.append(float(text[i]))

    outfile.write(str(math.radians(pos[0] / 2)) + ' ' + str(math.radians(pos[1] / 2)) + ' ' + str(pos[2]) + '\n')
