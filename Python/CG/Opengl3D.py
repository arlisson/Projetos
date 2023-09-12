import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (1, -1, -1),
    (1, -1, 1),
    (-1, -1, 1),
    (-1, -1, -1),
    (0, 1, 0)  # Vértice superior da pirâmide
)

edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (0, 4),
    (1, 4),
    (2, 4),
    (3, 4)
)


def draw():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def translation(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    draw()
    glPopMatrix()


def scale(x, y, z):
    glPushMatrix()
    glScalef(x, y, z)  # Escala (x,y,z)
    draw()
    glPopMatrix()


def rotate(a, x, y, z):
    glPushMatrix()
    glRotatef(a, x, y, z)  # (angulo,x,y,z)
    draw()
    glPopMatrix()


def reflex():
    glPushMatrix()
    glScalef(1, 1, 1)  # Escala (x,y,z)
    glTranslatef(0, 0, -2)
    draw()
    glPopMatrix()


def cis():
    matriz_cisalhamento = [
        1, 0.01, 0, 0,
        0.01, 1, 0, 0,
        0.01, 0, 1, 0,
        0, 0, 0, 1
    ]
    glMultMatrixf(matriz_cisalhamento)


def main():
    pygame.init()
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # (angulo, razão da largura e altura da tela, zNear, zFar )
    #gluPerspective(90, ((display[0]/display[1])), 0.1, 50.0)

    # (left,right,bottom,top,zNear,zFar)
    glOrtho(-5, 5, -5, 5, 0.1, 50.0)

    glTranslatef(0.0, 0.0, -6)
    glRotatef(30, 1, 1, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw()
        #translation(4, 0, 0)
        #rotate(180, 1, 0, 0)
        #scale(2, 2, 2)
        # reflex()
        # cis()

        pygame.display.flip()
        pygame.time.wait(10)


main()
