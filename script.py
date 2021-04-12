from numpy import array
from scipy.spatial import HalfspaceIntersection
from scipy.spatial import ConvexHull

from itertools import combinations

from compas.geometry import Plane, Vector
from compas.datastructures import Mesh

from compas_view2.app import App


left = Plane([-1, 0, 0], [-1, 0, 0])
right = Plane([+1, 0, 0], [+1, 0, 0])
top = Plane([0, 0, +1], [0, 0, +1])
bottom = Plane([0, 0, -1], [0, 0, -1])
front = Plane([0, -1, 0], [0, -1, 0])
back = Plane([0, +1, 0], [0, +1, 0])

halfspaces = array([
    left.abcd,
    right.abcd,
    top.abcd,
    bottom.abcd,
    front.abcd,
    back.abcd], dtype=float)

interior = array([0, 0, 0], dtype=float)

hsi = HalfspaceIntersection(halfspaces, interior)
hull = ConvexHull(hsi.intersections)

mesh = Mesh.from_vertices_and_faces([hsi.intersections[i] for i in hull.vertices], hull.simplices)
mesh.unify_cycles()

to_merge = []
for a, b in combinations(mesh.faces(), 2):
    na = Vector(* mesh.face_normal(a))
    nb = Vector(* mesh.face_normal(b))
    if na.dot(nb) >= 1:
        if na.cross(nb).length < 1e-6:
            to_merge.append([a, b])

for faces in to_merge:
    mesh.merge_faces(faces)

viewer = App()
viewer.add(mesh, show_vertices=True, pointsize=10)
viewer.run()
