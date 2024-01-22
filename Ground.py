import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

class Ground:

    def __init__(self, vertices, boundary_1, boundary_2):
        glBegin(GL_QUADS)
        for vertex in vertices:
            glColor3fv((0.64,0.16,0.16))
            glVertex3fv(vertex)

        for vertex in boundary_1:
            glColor3fv((0.5, 0.16, 0.16))
            glVertex3fv(vertex)

        for vertex in boundary_2:
            glColor3fv((0.5, 0.16, 0.16))
            glVertex3fv(vertex)


        glEnd()

    # def expandGrounf(self, vertices):

