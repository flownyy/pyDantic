from pyDantic.ptPrimitives import Mesh
from pyDantic.ptDraw import Workspace
from pyDantic.ptObj import parse_obj
from pyDantic.ptTypes import MeshInfo

window = Workspace(1280, 720)

shark_mesh: MeshInfo = parse_obj("SharkBoi.obj")

shark = Mesh((0, 0, 0), (1, 1, -1), shark_mesh.verticies, shark_mesh.faces)

window.add_elem(shark)

while window.active:
    window.draw()