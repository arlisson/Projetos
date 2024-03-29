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
    glColor3f(1.0, 1.0, 1.0)


def translation(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


def scale(x, y, z):
    glPushMatrix()
    glScalef(x, y, z)  # Escala (x,y,z)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


def rotate(a, x, y, z):
    glPushMatrix()
    glRotatef(a, x, y, z)  # (angulo,x,y,z)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


def reflex():
    glPushMatrix()
    glScalef(-1, 1, 1)  # Escala (x,y,z)
    glTranslatef(-2, 0, 0)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


def cis(x=1, y=1, z=1):
    glPushMatrix()
    matriz_cisalhamento = [
        x, 0, 0, 0,
        0, y, 0, 0,
        0, 0, z, 0,
        0, 0, 0, 1
    ]
    glMultMatrixf(matriz_cisalhamento)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


def proj():
    glPushMatrix()
    glTranslatef(3, 0, 0)
    matriz_projecao = [
        1, 0, 0, 0,  # x
        0, 0, 0, 0,  # y
        0, 0, 1, 0,  # z
        0, 0, 0, 1
    ]
    glMultMatrixf(matriz_projecao)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


def ortho():
    glPushMatrix()
    glTranslatef(0, 0, 4)
    glOrtho(-1, 1, -1, 1, 1, 100.0)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


def proj_perspec():
    glPushMatrix()
    glLoadIdentity()  # Resetando a matriz de visualização
    gluPerspective(90, ((1200/800)), 0.1, 50.0)   
    glTranslatef(0.0, 0.0, -3)
    
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()

def camera_projection():
    glPushMatrix()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (1200/ 800), 0.1, 50.0)
    glColor3f(1.0, 0.0, 0.0)
    glMatrixMode(GL_MODELVIEW)

    draw()
    glPopMatrix()

def main():
    pygame.init()
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # (angulo, razão da largura e altura da tela, zNear, zFar )
    #gluPerspective(90, ((display[0]/display[1])), 0.1, 50.0)

    # (left,right,bottom,top,zNear,zFar)
    glOrtho(-5, 5, -5, 5, 0.1, 50.0)

    glTranslatef(0.0, 0.0, -6)
    glRotatef(15, 1, 1, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw()
        #translation(0, -3, 0)
        #rotate(45, 0, 0, 1)
        #scale(2, 2, 2)
        # reflex()
        # cis()
        # proj()
        # ortho()
        #proj_perspec()
        camera_projection()

        pygame.display.flip()
        pygame.time.wait(10)


main()
