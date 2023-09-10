import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

vertices = (
    (1, -1, -1),
    (1, -1, 1),
    (-1, -1, 1),
    (-1, -1, -1),
    (0, 1, 0)
)

linhas = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (0, 4),
    (1, 4),
    (2, 4),
    (3, 4)
)

faces = (
    (0, 1, 2, 3),
    (4, 0, 1),
    (4, 1, 2),
    (4, 2, 3),
    (4, 3, 0)
)


def desenhar_piramide():

    glBegin(GL_LINES)
    for linha in linhas:
        for vertice in linha:
            glVertex3fv(vertices[vertice])
    glEnd()


def trans(x, y, z):
    glTranslatef(x, y, z)


def main():
    pygame.init()
    largura, altura = 1600, 800
    tela = pygame.display.set_mode((largura, altura), DOUBLEBUF | OPENGL)

    gluPerspective(90, (largura / altura), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        desenhar_piramide()
        pygame.display.flip()
        pygame.time.wait(10)
        trans(0.01, 0.0, 0.0)


if __name__ == "__main__":
    main()
