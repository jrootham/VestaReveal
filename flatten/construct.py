__author__ = 'jrootham'

# read lat, long, elevation list from file and build a mesh for a sphere
# with a given radius
# to a given resolution

def construct(infile, radius, resolution):

    map = []
    for line in infile:
        text = line.split()
