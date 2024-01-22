import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

class Cube:
    vertices = (  # koordynaty wierzchokow
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
    )

    edges = (  # krawedzie
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7)
    )

    surfaces = (  # powierzchnie
        (0, 1, 2, 3),
        (3, 2, 7, 6),
        (6, 7, 5, 4),
        (4, 5, 1, 0),
        (1, 5, 7, 2),
        (4, 0, 3, 6)
    )

    colors = (  # kolorki
        (1, 1, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 0, 0),
        (1, 1, 1),
        (0, 1, 1),
    )

    def __init__(self, vertices):

        glBegin(GL_QUADS)

        for surface in self.surfaces:
            x = 0
            for vertex in surface:
                x += 1
                glColor3fv(self.colors[x])  # daj kolor na element (wierzcholek)
                glTexCoord(0,0)
                glVertex3fv(vertices[vertex])
        glEnd()

        glBegin(GL_LINES)  # zawsze opengl metody tak zaczynamy i konczymy - (uzywamy GL_LINES - linii)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])  # bierze punkt i (lacznie z glbegin) rysuje linie
        glEnd()



