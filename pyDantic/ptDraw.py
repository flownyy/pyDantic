from .ptTypes import *
from .ptIdentifier import *

import pygame

from typing import Callable, Union

class Element:
    """
    The base type for all objects
    """
    def __init__(self, type: TypeIdentifier):
        self.type = type
        self.visible: bool = True

        # Not implemented
        self.resources: dict[str, list[any]] = {}

class Element3D(Element):
    """
    The base type for all 3D objects.
    """
    def __init__(self, type: TypeIdentifier, position: Position3D, size: Size3D, behaviors: dict[str, list[Callable[['Element3D'], list[any]]]]):
        super().__init__(type)
        self.position: Position3D = position
        self.size: Size3D = size
        self.posize: PositionAndSize3D = position + size
        self.type: TypeIdentifier = type
        self.behaviors = behaviors.copy()
    
    def set_position(self, new_pos: Position3D):
        self.position = new_pos
        self.posize = new_pos + self.posize[3:]

class Element2D(Element):
    """
    The base type for all 2D objects.
    """
    def __init__(self, type: TypeIdentifier, position: Position2D, size: Size2D, behaviors: dict[str, list[Callable[['Element2D'], list[any]]]]):
        super().__init__(type)
        self.position: Position2D = position
        self.size: Size2D = size
        self.posize: PositionAndSize2D = position + size
        self.type: TypeIdentifier = type
        self.behaviors = behaviors.copy()
    
    def set_position(self, new_pos: Position2D):
        self.position = new_pos
        self.posize = new_pos + self.posize[2:]

class RendererType(Enum):
    TwoDimensional = "2D"
    ThreeDimensional = "3D"

class Renderer2D:
    """
    The 2D renderer used by the Workspace.
    """
    def __init__(self, draw_target: pygame.Surface):
        self.draw_target: pygame.Surface = draw_target
        self.elements: list[Element2D] = []
        self.active = True
    
    def draw(self, unhandled_events: list[pygame.event.Event] = []):
        if not self.active: return

        for element in self.elements:
            if not element.visible: continue

            element.behaviors["draw"]((self.draw_target, None))

            for event in unhandled_events:
                if "handle_event" in element.behaviors and element.behaviors["handle_event"](element, (event, None)):
                    unhandled_events.remove(event)

Renderer2D.Type = RendererType.TwoDimensional

class Workspace:
    """
    A window.
    """
    def __init__(self, width: int, height: int, title: str = "Window", fps: int = 60, clear_color: Color = Color("#333")):
        self.width: int = width
        self.height: int = height
        self.size: Size2D = (width, height)
        self.title: int = title
        self.fps: int = fps

        self.window: pygame.Surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)

        self.renderer2d: Renderer2D = Renderer2D(self.window)

        self.clear_color: Color = clear_color

        self.active = True
    
    def add_elem(self, element: Union[Element2D, Element3D]):
        # if isinstance(element, Element2D):
        #     self.renderer2d.elements.append(element)
        # else:
        #     raise NotImplementedError
        self.renderer2d.elements.append(element)
    
    def draw(self):
        unhandled_events: list[pygame.event.Event] = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                self.active = False
                continue
            unhandled_events.append(event)

        # self.renderer3d.draw(unhandled_events)
        self.renderer2d.draw(unhandled_events)

        pygame.display.update()
        # pygame.time.wait(round(1 / float(self.fps) * 1000))

        self.renderer2d.draw_target.fill(self.clear_color.pygame())

    def quit(self):
        return