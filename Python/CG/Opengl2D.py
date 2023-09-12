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
glOrtho(-largura/2, largura/2, -altura/2, altura/2,
        0, 1)  # Define uma nova matriz de projeção

glMatrixMode(GL_MODELVIEW)
glLoadIdentity()


def draw():
    pontos = ((0, 0), (100, 100), (100, 0))
    glBegin(GL_LINE_LOOP)
    glVertex2f(pontos[0][0], pontos[0][1])
    #glVertex2f(500, 400)
    glVertex2f(pontos[1][0], pontos[1][1])
    glVertex2f(pontos[2][0], pontos[2][1])
    glEnd()
    return pontos


def translation(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)  # Ajuste da translação (x, y, z)
    draw()
    glPopMatrix()


def scale(x, y, z):

    glPushMatrix()
    glScalef(x, y, z)  # Aplica a escala em relação a origem do plano (0,0,0)
    draw()
    glPopMatrix()


def rotate(p, x, y, z):
    glPushMatrix()
    glRotatef(p, x, y, z)    # Rotação
    draw()
    glPopMatrix()


def reflex_y(positivo=False):
    pontos = draw()
    glPushMatrix()
    if positivo == True:
        glTranslatef(0, 200, 0)
    glBegin(GL_LINE_LOOP)
    for ponto in pontos:
        # Reflete em relação ao eixo y positivo
        glVertex2f(ponto[0], -ponto[1])

    glEnd()
    glPopMatrix()


def reflex_x(positivo=False):
    pontos = draw()
    glPushMatrix()
    if positivo == True:
        glTranslatef(200, 0, 0)  # Ajuste da translação (x, y, z)

    glBegin(GL_LINE_LOOP)
    for ponto in pontos:
        # Reflete em relação ao eixo x positivo
        glVertex2f(-ponto[0], ponto[1])

    glEnd()
    glPopMatrix()


def cis(fator):
    pontos = draw()
    glPushMatrix()
    glBegin(GL_LINE_LOOP)
    for ponto in pontos:
        # Cisalha a coordenada x
        glVertex2f(ponto[0] + fator * ponto[1], ponto[1])
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
    #translation(100, 0, 0)
    #scale(2, 2, 0)
    #rotate(45, 0, 0, 1)
    # reflex_x(positivo=False)
    # reflex_y(positivo=True)
    # cis(1)

    # Atualiza a tela
    pygame.display.flip()
    pygame.time.wait(10)
