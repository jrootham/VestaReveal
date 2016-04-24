__author__ = 'jrootham'

import random
import math

SIZE = 100

out = open('test.txt', 'w')

def distance(lat, long):
    mid = SIZE / 2
    dist_squared = (lat - mid) ** 2 + (long - mid) ** 2
    return math.sqrt(dist_squared)

levelList = []

for lat in range(0, SIZE):
    row = []

    for long in range(0, SIZE):
        dist = distance(lat, long)
        edge = SIZE / 2.2
        level = 0
        if dist < edge:
#            level = max(0, 50 * (math.sqrt(edge - dist) - random.random()))
            level = max(0, 35 * (math.sqrt(edge - dist)))
        row.append(level)

    levelList.append(row)

for lat in range(1, SIZE-1):
    for long in range(1, SIZE-1):
        sum = 0

        for i in range(-1, 1):
            for j in range(-1, 1):
                sum += levelList[lat + i][long + j]

        if sum > 0:
            average = sum / 9
            levelList[lat][long] = max(0, average + random.uniform(-2, 2))

for lat in range(0, SIZE):
    for long in range(0, SIZE):
        out.write(str(math.radians(lat)) + ' '
                  +  str(math.radians(long)) + ' '
                  + str(levelList[lat][long]) + '\n')
