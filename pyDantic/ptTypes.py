from builtins import int, tuple, list, str
from warnings import warn
from enum import Enum

Position2D = tuple[float, float]
Position3D = tuple[float, float, float]

Size2D = tuple[float, float]
Size3D = tuple[float, float, float]

PositionAndSize2D = tuple[float, float, float, float]
PositionAndSize3D = tuple[float, float, float, float, float, float]

class Color:
    def __init__(self, _, g = None, b = None, a = None):
        self.color: tuple[int, int, int, int] = [255, 0, 255, 255]

        if isinstance(_, int):
            self.color[0] = _
            self.color[1] = g
            self.color[2] = b
            self.color[3] = a or 255
        elif isinstance(_, str):
            hex_color: str = _
            hex_color = hex_color.removeprefix("#").lower()

            if len(hex_color) == 3 or len(hex_color) == 4: # something like #F3E or #3dca (i have never seen something like the 4 case though)
                for idx, char in enumerate(hex_color):
                    self.color[idx] = int(char + char, base = 16)
            elif len(hex_color) == 6 or len(hex_color) == 8: # something like #ffaabb(cc)
                byte = ""
                for idx, char in enumerate(hex_color):
                    byte = byte + char
                    if idx % 2 == 0:
                        continue
    
                    self.color[idx] = int(byte, base = 16)
                    byte = ""
            else:
                raise SyntaxError(f"color \"{_}\" is invalid")
        elif isinstance(_, (list, tuple)):
            for idx, byte in enumerate(_):
                if isinstance(byte, float):
                    warn("list or tuple of floats (list[float] or tuple[float]) was given to Color. Normalized RGB(A) arrays are not supported", SyntaxWarning)
                self.color[idx] = _[idx]
        else:
            raise SyntaxError(f"type \"{type(_)}\" is invalid")
        
        for byte in self.color:
            if byte > 0xFF:
                raise SyntaxError(f"color \"{_}\" is invalid")
    
    def __repr__(self):
        return f"Color(#{self.color[0]:02x}{self.color[1]:02x}{self.color[2]:02x}{self.color[3]:02x})"

    def pygame(self):
        return self.color[:3] # :3

class MeshInfo:
    def __init__(self):
        self.verticies: list[Position3D] = []
        self.faces: list[list[int]] = []

class RotationPlane(Enum):
    XY = "XY"
    XZ = "XZ"
    YZ = "YZ"
