__author__ = 'jrootham'

import math

def wrap(angle1, angle2):
    return math.fabs(angle1 - angle2)

class Location:
    def __init__(self, lat, long, level):
        self.lat = lat
        self.long = long
        self.level = level
        self.neighbours = []
        visited = False

    def distance(self, other):
        return self.dist(other.lat, other.long)

    def dist(self, lat, long):
        return math.sqrt(wrap(self.lat, lat) ** 2 + wrap(self.long, long) ** 2)

    def connect(self, other):
        if not other in self.neighbours:
            self.neighbours.append(other)
            other.neighbours.append(self)

