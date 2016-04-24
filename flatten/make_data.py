__author__ = 'jrootham'

import random
import math

SIZE = 100

out = open('test.txt', 'w')

def distance(lat, long):
    mid = SIZE / 2
    dist_squared = (lat - mid) ** 2 + (long - mid) ** 2
    return math.sqrt(dist_squared)

for lat in range(0, SIZE):
    for long in range(0, SIZE):
        dist = distance(lat, long)
        edge = SIZE / 4
        level = 0
        if dist < edge:
            level = max(0, 50 * (math.sqrt(edge - dist) - random.random()))
        out.write(str(math.radians(lat + random.random())) + ' '
                  +  str(math.radians(long + random.random())) + ' '
                  + str(level) + '\n')
