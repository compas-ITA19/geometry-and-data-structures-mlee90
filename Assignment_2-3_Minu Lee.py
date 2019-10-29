from random import random
from numpy import cross

def cross_manual(a,b):
    c = [
        a[1]*b[2]-a[2]*b[1],
        a[2]*b[0]-a[0]*b[2],
        a[0]*b[1]-a[1]*b[0]
        ]
    return c

# number of vectors
n = 10
# create two random arrays of vectors
a = [[random(), random(), random()] for i in range(n)]
b = [[random(), random(), random()] for i in range(n)]

# loop over all entries in the array
c = []
for i in range(n):
    c.append(cross_manual(a[i], b[i]))

# using numpy
c_np = cross(a, b)