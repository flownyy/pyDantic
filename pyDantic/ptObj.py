from .ptTypes import Position3D, MeshInfo

def parse_obj(file_path: str) -> MeshInfo:
    meshinfo = MeshInfo()

    with open(file_path, "r") as obj_file:
        for line in obj_file.readlines():
            command, *args = line.split(" ")
            match command:
                case "v":
                    vertex: Position3D = tuple((float(arg) for arg in args))
                    meshinfo.verticies.append(vertex)
                case "f":
                    face: list[int] = []

                    for arg in args:
                        idx = int(arg.split("/")[0]) - 1
                        face.append(idx)

                    meshinfo.faces.append(face)
                case _:
                    pass
    
    return meshinfo