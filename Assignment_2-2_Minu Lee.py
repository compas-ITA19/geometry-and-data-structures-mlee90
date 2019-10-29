from random import random
from random import shuffle
from math import floor
from math import atan2
from numpy import add
from numpy import subtract
from numpy import argsort
from numpy import array
from compas_plotters import Plotter
from compas.geometry import Polygon

# First, a random convex polygon in 2D has to be created. The Valtr's proof is used for that.
# This function sorts the x and y components to create random vectors within 2D-space
def rand_coord_sort(x):
    x.sort()
    x_iso = x[1:n-1]
    shuffle(x_iso)

    x_sub_1 = x_iso[:floor((n-2)/2)]
    x_sub_2 = x_iso[floor((n-2)/2):]

    x_sub_1.sort(reverse=True)
    x_sub_2.sort()

    x_sub = []
    x_sub.append(x[-1])
    x_sub.extend(x_sub_1)
    x_sub.append(x[0])
    x_sub.extend(x_sub_2)
    x_sub.append(x[-1])

    x_vec = subtract(x_sub[1:], x_sub[:-1])
    
    return x_vec
# Cross product for two given vectors
def cross(a,b):
    c = [
        a[1]*b[2]-a[2]*b[1],
        a[2]*b[0]-a[0]*b[2],
        a[0]*b[1]-a[1]*b[0]
        ]
    return c
# This function creates a convex 2D-polygon with a given number of vertices using the Valtr's proof
def Valtr(n):
    # create random components for x and y
    x = [random() for i in range(0,n)]
    y = [random() for i in range(0,n)]

    # sort x and y components
    x_vec = rand_coord_sort(x)
    y_vec = rand_coord_sort(x)

    # randomly combine x and y to create vectors
    shuffle(x_vec)
    shuffle(y_vec)
    vectors = [[x_vec[i], y_vec[i], 0] for i in range(n)]

    # sort vectors according to ascending angle
    atan_vec = [atan2(y_vec[i],x_vec[i]) for i in range(n)]
    id_order = argsort(atan_vec)
    vectors_sort = [[x_vec[i], y_vec[i], 0] for i in id_order]

    point_coord = []
    point_coord.append([0,0,0])

    # create polygon from vector addition (according to Valtr's proof, the polygon should close itself)
    for i in range(1,n):
        new_point = add(point_coord[i-1], vectors_sort[i-1])
        point_coord.append([new_point[0], new_point[1], 0])

    # define Polygon 
    polygon = Polygon(point_coord)
    # check if polygon is really convex
    if polygon.is_convex() == False:
        print('This polygon is NOT convex!')

    return polygon

# number of points in polygon
n = 6

# create polygon using Valtr's proof
polygon = Valtr(n)

area = 0
lines_out = []
lines_in = []
points = []

# defining the "pizza slices" in the polygon
for i in range(n):
    # define points for plotter
    points.append({
        'pos': polygon.points[i],
        'radius': 0.005,
    })

    # define vectors to centroid and outer lines of polygon
    a = polygon.points[i]-polygon.centroid
    if i == n-1:
        b = polygon.points[0]-polygon.centroid
        lines_out.append({
            'start': polygon.points[i],
            'end': polygon.points[0],
            'width': 1.0
        })
    else:
        b = polygon.points[i+1]-polygon.centroid
        lines_out.append({
            'start': polygon.points[i],
            'end': polygon.points[i+1],
            'width': 1.0
        })
    # draw lines from polygon vertices to centroid
    lines_in.append({
        'start': polygon.points[i],
        'end': polygon.centroid,
        'width': 1.0,
        'color': (130, 130, 130)
    })
    # cross product
    c = cross(a,b)
    area = area+c[2]/2 # since polygon is in xy-plane, length of resulting vector from cross product is just the z-component
   
points.append({
    'pos': polygon.centroid,
    'radius': 0.005,
})

plotter = Plotter(figsize=(8, 5))
plotter.draw_points(points)
plotter.draw_lines(lines_out)
plotter.draw_lines(lines_in)
plotter.show()





