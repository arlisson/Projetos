import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

# Inicializa o Pygame
pygame.init()

# Configurações iniciais
largura, altura = 1200, 800
display = (largura, altura)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glViewport(0, 0, largura, altura)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, largura, 0, altura, 0, 1)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()


def draw():
    a, b, c = [500, 300], [600, 400], [600, 300]
    glBegin(GL_LINE_LOOP)
    glVertex2f(a[0], a[1])
    #glVertex2f(500, 400)
    glVertex2f(b[0], b[1])
    glVertex2f(c[0], c[1])
    glEnd()
    return a, b, c


def translation(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)  # Ajuste da translação (x, y, z)
    draw()
    glPopMatrix()


def scale(x, y, z):
    a, b, c = draw()
    glPushMatrix()
    # Translação para o centro
    glTranslatef(a[0]+((c[0]-a[0])/2), a[1]+((c[0]-a[0])/2), 0)
    glScalef(x, y, z)  # Escala (x,y,z)
    # Translação de volta para a posição original
    glTranslatef(-(a[0]+((c[0]-a[0])/2)), -(a[1]+((c[0]-a[0])/2)), 0)
    draw()
    glPopMatrix()


def rotate(p, x, y, z):
    a, b, c = draw()
    glPushMatrix()
    # Translação para o centro
    glTranslatef(a[0]+((c[0]-a[0])/2), a[1]+((c[0]-a[0])/2), 0)
    glRotatef(p, x, y, z)     # Rotação
    # Translação de volta para a posição original
    glTranslatef(-(a[0]+((c[0]-a[0])/2)), -(a[1]+((c[0]-a[0])/2)), 0)

    draw()
    glPopMatrix()


def reflex_y():
    a, b, c = draw()
    glPushMatrix()
    draw()
    glBegin(GL_LINE_LOOP)
    glVertex2f(a[0], b[0] - a[1])  # Inverte a coordenada y
    glVertex2f(b[0], b[0] - b[1])
    glVertex2f(c[0], b[0] - c[1])
    glEnd()
    glPopMatrix()


def reflex_x():
    a, b, c = draw()
    glPushMatrix()
    draw()
    glBegin(GL_LINE_LOOP)
    glVertex2f(a[0]+(c[0]-a[0])*2, a[1])  # Inverte a coordenada x
    glVertex2f(b[0], b[1])
    glVertex2f(c[0], c[1])
    glEnd()
    glPopMatrix()


def cis_x():
    a, b, c = draw()
    glPushMatrix()
    draw()
    glBegin(GL_LINE_LOOP)
    glVertex2f(a[0] + 0 * a[1], a[1])  # Cisalha a coordenada x
    glVertex2f(b[0] + 0.5 * b[1], b[1])
    glVertex2f(c[0] + 0.5 * c[1], c[1])
    glEnd()
    glPopMatrix()


# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Limpa a tela
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    draw()
    #translation(50, 100, 0)
    #scale(2, 2, 2)
    #rotate(45, 0, 0, 1)
    # reflex_x()
    cis_x()

    # Atualiza a tela
    pygame.display.flip()
    pygame.time.wait(10)
