import os
import compas

from compas.datastructures import Mesh
from compas_plotters import MeshPlotter
from compas.utilities import i_to_red

from random import random
from math import floor
from numpy import subtract
from numpy import add
from numpy.linalg import norm
from numpy import array
from numpy import cross

# function to draw arrowheads
def arrowhead(xy_0, xy_1):
    arrow = []
    unit_n = array(subtract(xy_1, xy_0))/norm(subtract(xy_1, xy_0))
    unit_t = cross(unit_n, [0,0,1])
    pt_0 = subtract(xy_1, array(unit_n)*0.2)
    pt_1 = add(subtract(xy_1, array(unit_n)*0.4), array(unit_t)*0.1)
    pt_2 = add(subtract(xy_1, array(unit_n)*0.4), array(unit_t)*(-0.1))
    arrow.append({
        'start': pt_0,
        'end': pt_1,
        'width': 2.0,
        'color': (255,0,0)
    })
    arrow.append({
        'start': pt_1,
        'end': pt_2,
        'width': 2.0,
        'color': (255,0,0)
    })
    arrow.append({
        'start': pt_2,
        'end': pt_0,
        'width': 2.0,
        'color': (255,0,0)
    })
    return arrow


HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, 'data')
FILE = os.path.join(DATA, 'faces.obj')

mesh = Mesh.from_obj(FILE)

boundary_vertices = mesh.vertices_on_boundaries()[0]
bc_pt = []

# find all boundary vertices which are not in a corner
for i in boundary_vertices:
    boundary_faces = mesh.vertex_faces(i)
    if len(boundary_faces) > 1:
        bc_pt.append(i)

# choose a random starting point; alternatively, user could give a specific starting point
st_pt = [bc_pt[floor(random()*len(bc_pt))]]

print(st_pt[0])
st_faces = mesh.vertex_faces(st_pt[0]) # faces around vertex (starting point always has 2 vertices)

faces_old = []
faces_old.extend(st_faces)

while len(st_faces) > 0:
    next_pt = [i for i in mesh.face_adjacency_vertices(st_faces[0], st_faces[1]) if i not in st_pt] # vertices which are touched by the two next faces; next vertex is the one which has not already been stored in the path
    st_pt.append(next_pt[0]) # add next vertex to the path
    st_faces = [i for i in mesh.vertex_faces(next_pt[0]) if i not in faces_old] # faces around next vertex; the next two faces are the ones which are not already in the path
    faces_old.extend(st_faces) # add next faces to the path

path = []

# print(mesh.vertex_coordinates(st_pt[0]))
arrow = []
for i in range(len(st_pt)-1):
    path.append({
        'start': mesh.vertex_coordinates(st_pt[i]),
        'end': mesh.vertex_coordinates(st_pt[i+1]),
        'width': 2.0,
        'color': (255,0,0)
    })
    arrow.extend(arrowhead(mesh.vertex_coordinates(st_pt[i]), mesh.vertex_coordinates(st_pt[i+1])))

print(st_pt)

plotter = MeshPlotter(mesh, figsize=(16, 10))
plotter.draw_vertices(
    text={key: key for key in mesh.vertices()},
    radius=0.2,
    facecolor=(255, 255, 255))
plotter.draw_edges()
plotter.draw_lines(path)
plotter.draw_lines(arrow)
plotter.show()