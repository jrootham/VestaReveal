__author__ = 'jrootham'

import sys
import math
import location

infile = open(sys.argv[1])
width = int(sys.argv[3])
height = int(sys.argv[4])

map = []
locations = []

for line in infile:
    text = line.split()
    pos=[]
    for i in range(len(text)):
        pos.append(float(text[i]))

    map.append(pos[:])
    locations.append(location.Location(pos[0], pos[1], pos[2]))

byLat = sorted(map, key=lambda pos: pos[0])
byLong = sorted(map, key=lambda pos: pos[1])

minLat = byLat[0][0];
maxLat = byLat[len(byLat)-1][1];
minLong = byLong[0][1];
maxLong = byLong[len(byLong)-1][1];

midLat = minLat + (maxLat - minLat) / 2
midLong = minLong + (maxLong - minLong) / 2

print minLat, maxLat, minLong, maxLong, midLat, midLong

def search(lat, long):
    loc = locations[0]

    for l in locations:
        if loc.dist(lat, long) > l.dist(lat, long):
            loc = l

    return loc

def value(x, y):
    midWidth = width / 2
    midHeight = height / 2

    halfLat = midLat - minLat
    halfLong = midLong - minLong

    latR = midWidth / math.sin(halfLat)
    longR = midHeight / math.sin(halfLong)

    latBase = latR * math.cos(halfLat)
    longBase = longR * math.cos(halfLong)

    xDelta = midWidth - x
    yDelta = midHeight - y

    xDir = midLat - math.atan(xDelta / latBase)
    yDir = midLong - math.atan(yDelta / longBase)

    return int(search(xDir, yDir).level)

outfile = open(sys.argv[2], 'w')

maxLevel = 0

for x in range(0, width):
    print x
    for y in range(0, height):
        v = value(x,y)
        maxLevel = max(maxLevel,v)
        outfile.write(str(v) + ' ')
    outfile.write('\n')


print maxLevel
