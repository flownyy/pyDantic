from .ptDraw import *
import pygame

class Rectangle(Element2D):
    def draw(this: 'Rectangle', args: tuple[pygame.Surface]):
        workspace: pygame.Surface = args[0]

        pygame.draw.rect(workspace, this.color.pygame(), this.posize)

    def __init__(self, position: Position2D, size: Size2D, color = Color("f0f")):
        super().__init__(TypeIdentifier("ptPrimitives.Rectangle"), position, size, dict())

        self.behaviors["draw"] = self.draw
        self.color = color

class Mesh(Element3D):
    def normalize_point(p: Position2D, screen_width: int, screen_height: int) -> Position2D:
        min_dim = min(screen_height, screen_width)
        max_dim = max(screen_height, screen_width)

        offset_x = 0
        offset_y = 0

        if max_dim == screen_width:
            offset_x += (screen_width - screen_height) / 2.0
        else:
            offset_y += (screen_height - screen_width) / 2.0
        return (
            (p[0] + 1) / 2.0 * min_dim + offset_x,
            (1 - (p[1] + 1) / 2.0) * min_dim + offset_y
        )

    def project_point(p: Position3D) -> Position2D:
        try:
            return (
                p[0] / p[2],
                p[1] / p[2]
            )
        except ZeroDivisionError:
            return (-1, -1)

    def draw_point(ws: pygame.Surface, p: Position2D):
        return
        pygame.draw.rect(ws, Color("#1e1").pygame(), (p[0] - 5, p[1] - 5, 10, 10))

    def draw(this: 'Mesh', args: tuple[pygame.Surface]):
        workspace: pygame.Surface = args[0]

        verticies = list([(vertex[0] * this.size[0] + this.position[0], vertex[1] * this.size[1] + this.position[1], vertex[2] * this.size[2] + this.position[2]) for vertex in this.verticies])

        # TODO: LEFTOVER DEBUG CODE
        if not pygame.key.get_pressed()[pygame.K_LSHIFT]:
            if pygame.key.get_pressed()[pygame.K_UP]:
                this.set_position((this.position[0], this.position[1], this.position[2] + 0.1))
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                this.set_position((this.position[0], this.position[1], this.position[2] - 0.1))
        else:
            if pygame.key.get_pressed()[pygame.K_UP]:
                this.set_position((this.position[0], this.position[1] + 0.1, this.position[2]))
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                this.set_position((this.position[0], this.position[1] - 0.1, this.position[2]))

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            this.set_position((this.position[0] - 0.1, this.position[1], this.position[2]))
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            this.set_position((this.position[0] + 0.1, this.position[1], this.position[2]))

        for face in this.faces:
            prev_vertex: Position3D = None
            for idx, vertex_idx in enumerate(face):
                vertex = list(verticies[vertex_idx])

                Mesh.draw_point(workspace, Mesh.normalize_point(Mesh.project_point(vertex), workspace.get_width(), workspace.get_height()))
                
                if idx == 0:
                    prev_vertex = vertex
                    continue

                pygame.draw.line(
                    workspace, 
                    Color("#1e1").pygame(),            
                    Mesh.normalize_point(Mesh.project_point(vertex), workspace.get_width(), workspace.get_height()), 
                    Mesh.normalize_point(Mesh.project_point(prev_vertex), workspace.get_width(), workspace.get_height())
                )

                prev_vertex = vertex

            pygame.draw.line(
                workspace, 
                Color("#1e1").pygame(), 
                Mesh.normalize_point(Mesh.project_point(vertex), workspace.get_width(), workspace.get_height()), 
                Mesh.normalize_point(Mesh.project_point(verticies[face[0]]), workspace.get_width(), workspace.get_height())
            )

    def __init__(self, position: Position3D, size: Size3D, verticies: list[Position3D], faces: list[list[int]]):
        super().__init__(TypeIdentifier("ptPrimitives.Mesh"), position, size, dict())

        self.verticies = verticies.copy()
        self.faces = faces.copy()
        self.behaviors["draw"] = self.draw