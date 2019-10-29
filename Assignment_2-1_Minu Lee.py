from random import random

# create two random vectors
a = [random(), random(), random()]
b = [random(), random(), random()]

# return cross product of two given vectors
def cross(a,b):
    c = [
        a[1]*b[2]-a[2]*b[1],
        a[2]*b[0]-a[0]*b[2],
        a[0]*b[1]-a[1]*b[0]
        ]
    return c

# return the normalised vector
def norm(a):
    length = (a[0]**2+a[1]**2+a[2]**2)**(1/2)
    a_norm = [i/length for i in a]
    return a_norm

# create normal vector (corresponding to z) for "base" plane (corresponding to xy)
c = cross(a,b)

# normalise first and third vector (corresponding to x and z)
a_norm = norm(a)
c_norm = norm(c)

# create second vector (corresponding to y) to create orthonormal base coordinate system
b_norm = cross(c_norm, a_norm)
