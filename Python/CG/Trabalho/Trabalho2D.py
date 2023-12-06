from operator import truediv
from pickle import TRUE
from turtle import Screen, screensize
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import time
import pygame.font

# Inicializa o Pygame
pygame.init()
pygame.font.init()


# Configurações iniciais
largura, altura = 1200, 800
display = (largura, altura)
'''pygame.display.set_mode(display, DOUBLEBUF | OPENGL )
glViewport(0, 0, largura, altura)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-largura/2, largura/2, -altura/2, altura/2,
        0, 1)  # Define uma nova matriz de projeção

glMatrixMode(GL_MODELVIEW)'''
tela = pygame.display.set_mode(display, DOUBLEBUF | OPENGL | GLUT_DEPTH)
glEnable(GL_DEPTH_TEST)  # Ativa o teste de profundidade

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
# Configura uma projeção em perspectiva
# (angulo, razão da largura e altura da tela, zNear, zFar )
gluPerspective(45, (largura / altura), 0.1, 50.0)
glTranslatef(0.0, 0.0, -20)  # Move a câmera para trás
glMatrixMode(GL_MODELVIEW)

glLoadIdentity()


def draw():
    pontos = ((1, -1), (-1, -1), (-1, 1), (1, 1))
    glBegin(GL_LINE_LOOP)
    glVertex2f(pontos[0][0], pontos[0][1])
    glVertex2f(pontos[1][0], pontos[1][1])
    glVertex2f(pontos[2][0], pontos[2][1])
    glVertex2f(pontos[3][0], pontos[3][1])
    glColor3f(1.0, 1.0, 1.0)
    glEnd()
    return pontos


x, y, z = 0, 0, 0


def translation():
    global x, y, z  # Use a variável global x, y e z
    keys = pygame.key.get_pressed()

    if keys[pygame.K_x] and keys[pygame.K_RIGHT]:
        x += fator
    if keys[pygame.K_y] and keys[pygame.K_UP]:
        y += fator
    if keys[pygame.K_z] and keys[pygame.K_UP]:
        z += fator

    if keys[pygame.K_x] and keys[pygame.K_LEFT]:
        x -= fator
    if keys[pygame.K_y] and keys[pygame.K_DOWN]:
        y -= fator
    if keys[pygame.K_z] and keys[pygame.K_DOWN]:
        z -= fator

    if keys[pygame.K_0]:
        x, y, z = 0, 0, 0

    if keys[pygame.K_1]:
        x, y, z = 0, 0, 0

    font = pygame.font.SysFont('arial', 20)
    text = ['x + Seta Direita(x++)', 'x + Seta Esquerda (x--)', 'y + Seta Cima (y++)', 'y + Seta Baixo (y--)',
            'z + Seta Cima (z++)', 'z + Seta Baixo (z--)', '0 - Reset', '1 - Sair']
    y_offset = 700
    for line in text:
        textSurface = font.render(
            line, True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(10, y_offset)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, textData)
        y_offset -= textSurface.get_height()

    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


x_s, y_s, z_s = 1, 1, 1


def scale():
    global x_s, y_s, z_s  # Use a variável global x, y e z
    keys = pygame.key.get_pressed()

    if keys[pygame.K_x] and keys[pygame.K_RIGHT]:
        x_s += fator
    if keys[pygame.K_y] and keys[pygame.K_UP]:
        y_s += fator
    if keys[pygame.K_z] and keys[pygame.K_UP]:
        z_s += fator

    if keys[pygame.K_x] and keys[pygame.K_LEFT]:
        x_s -= fator
    if keys[pygame.K_y] and keys[pygame.K_DOWN]:
        y_s -= fator
    if keys[pygame.K_z] and keys[pygame.K_DOWN]:
        z_s -= fator

    if keys[pygame.K_0]:
        x_s, y_s, z_s = 1, 1, 1
    if keys[pygame.K_2]:
        x_s, y_s, z_s = 1, 1, 1

    font = pygame.font.SysFont('arial', 20)
    text = ['x + Seta Direita(x++)', 'x + Seta Esquerda (x--)',
            'y + Seta Cima (y++)', 'y + Seta Baixo (y--)', '0 - Reset', '2 - Sair']
    y_offset = 700
    for line in text:
        textSurface = font.render(
            line, True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(10, y_offset)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, textData)
        y_offset -= textSurface.get_height()

    glPushMatrix()
    glScalef(x_s, y_s, z_s)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


p, x_p, y_p, z_p = 0, 1, 1, 1


def rotate():
    global p, x_p, y_p, z_p  # Use a variável global x, y e z
    keys = pygame.key.get_pressed()

    if keys[pygame.K_x] and keys[pygame.K_RIGHT]:
        p += 1
        x_p, y_p, z_p = 1, 0, 0
    if keys[pygame.K_y] and keys[pygame.K_UP]:
        p += 1
        x_p, y_p, z_p = 0, 1, 0
    if keys[pygame.K_z] and keys[pygame.K_UP]:
        p += 1
        x_p, y_p, z_p = 0, 0, 1

    if keys[pygame.K_x] and keys[pygame.K_LEFT]:
        p -= 1
        x_p, y_p, z_p = 1, 0, 0
    if keys[pygame.K_y] and keys[pygame.K_DOWN]:
        p -= 1
        x_p, y_p, z_p = 0, 1, 0
    if keys[pygame.K_z] and keys[pygame.K_DOWN]:
        p -= 1
        x_p, y_p, z_p = 0, 0, 1

    if keys[pygame.K_0]:
        p, x_p, y_p, z_p = 0, 1, 1, 1
    if keys[pygame.K_3]:
        p, x_p, y_p, z_p = 0, 1, 1, 1

    font = pygame.font.SysFont('arial', 20)
    text = ['x + Seta Direita(x++)', 'x + Seta Esquerda (x--)',
            'y + Seta Cima (y++)', 'y + Seta Baixo (y--)', 'z + Seta Cima (z++)', 'z + Seta Baixo (z--)', '0 - Reset', '3 - Sair']
    y_offset = 700
    for line in text:
        textSurface = font.render(
            line, True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(10, y_offset)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, textData)
        y_offset -= textSurface.get_height()

    glPushMatrix()
    glRotatef(p, x_p, y_p, z_p)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


x_r, y_r, z_r = 0, 0, 0


def reflex():
    global x_r, y_r, z_r  # Use a variável global x, y e z
    keys = pygame.key.get_pressed()

    if keys[pygame.K_x] and keys[pygame.K_RIGHT]:
        x_r, y_r, z_r = 2, 0, 0
    if keys[pygame.K_y] and keys[pygame.K_UP]:
        x_r, y_r, z_r = 0, 2, 0
    if keys[pygame.K_z] and keys[pygame.K_UP]:
        x_r, y_r, z_r = 0, 0, 2

    if keys[pygame.K_x] and keys[pygame.K_LEFT]:
        x_r, y_r, z_r = -2, 0, 0
    if keys[pygame.K_y] and keys[pygame.K_DOWN]:
        x_r, y_r, z_r = 0, -2, 0
    if keys[pygame.K_z] and keys[pygame.K_DOWN]:
        x_r, y_r, z_r = 0, 0, -2

    if keys[pygame.K_0]:
        x_r, y_r, z_r = 0, 0, 0
    if keys[pygame.K_4]:
        x_r, y_r, z_r = 0, 0, 0

    font = pygame.font.SysFont('arial', 20)
    text = ['x + Seta Direita(x++)', 'x + Seta Esquerda (x--)',
            'y + Seta Cima (y++)', 'y + Seta Baixo (y--)', 'z + Seta Cima (z++)', 'z + Seta Baixo (z--)', '0 - Reset', '4 - Sair']
    y_offset = 700
    for line in text:
        textSurface = font.render(
            line, True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(10, y_offset)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, textData)
        y_offset -= textSurface.get_height()

    glPushMatrix()
    glTranslatef(x_r, y_r, z_r)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


fator_x = 0
fator_y = 0
fator_z = 0


def cis():
    global fator_x, fator_y, fator_z  # Use a variável global x, y e z
    keys = pygame.key.get_pressed()

    if keys[pygame.K_x] and keys[pygame.K_RIGHT]:
        fator_x += fator
        fator_y = 0
        fator_z = 0

    if keys[pygame.K_x] and keys[pygame.K_LEFT]:
        fator_x -= fator
        fator_y = 0
    if keys[pygame.K_y] and keys[pygame.K_UP]:
        fator_x = 0
        fator_y += fator
        fator_z = 0

    if keys[pygame.K_y] and keys[pygame.K_DOWN]:
        fator_x = 0
        fator_y -= fator
        fator_z = 0

    if keys[pygame.K_z] and keys[pygame.K_UP]:
        fator_x = 0
        fator_z += fator
        fator_y = 0

    if keys[pygame.K_z] and keys[pygame.K_DOWN]:
        fator_x = 0
        fator_z -= fator
        fator_y = 0

    if keys[pygame.K_0]:
        fator_x, fator_y, fator_z = 0, 0, 0

    if keys[pygame.K_5]:
        fator_x, fator_y, fator_z = 0, 0, 0

    font = pygame.font.SysFont('arial', 20)
    text = ['x + Seta Direita(x++)', 'x + Seta Esquerda (x--)',
            'y + Seta Cima (y++)', 'y + Seta Baixo (y--)', 'z + Seta Cima (z++)', 'z + Seta Baixo (z--)', '0 - Reset', '5 - Sair']
    y_offset = 700
    for line in text:
        textSurface = font.render(
            line, True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(10, y_offset)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, textData)
        y_offset -= textSurface.get_height()

    glPushMatrix()
    matriz_projecao = [
        1, fator_y, 0, 0,  # x
        fator_x, 1, 0, 0,  # y
        0, 0, 1, fator_z,  # z
        0, 0, 0, 1
    ]
    glMultMatrixf(matriz_projecao)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


x_pr = 0


def proj():
    global x_pr  # Use a variável global x, y e z
    keys = pygame.key.get_pressed()

    if keys[pygame.K_x] and keys[pygame.K_RIGHT]:
        x_pr -= fator
    if keys[pygame.K_x] and keys[pygame.K_LEFT]:
        x_pr += fator

    if keys[pygame.K_0]:
        x_pr = 0
    if keys[pygame.K_6]:
        x_pr = 0

    font = pygame.font.SysFont('arial', 20)
    text = ['x + Seta Direita(x++)', 'x + Seta Esquerda (x--)',
            '0 - Reset', '6 - Sair']
    y_offset = 700
    for line in text:
        textSurface = font.render(
            line, True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(10, y_offset)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, textData)
        y_offset -= textSurface.get_height()

    glPushMatrix()
    matriz_projecao = [
        x_pr, 0, 0, 0,  # x
        0, x_pr, 0, 0,  # y
        0, 0, 1, 0,  # z
        0, 0, 0, 1
    ]
    glMultMatrixf(matriz_projecao)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


ort_a = 1


def ortho():
    global ort_a  # Use a variável global x, y e z
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        ort_a += fator
    if keys[pygame.K_LEFT]:
        ort_a -= fator

    if keys[pygame.K_0]:
        ort_a = 1
    if keys[pygame.K_7]:
        ort_a = 1

    font = pygame.font.SysFont('arial', 20)
    text = ['Seta Direita(++)', 'Seta Esquerda (--)',
            '0 - Reset', '7 - Sair']
    y_offset = 700
    for line in text:
        textSurface = font.render(
            line, True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(10, y_offset)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, textData)
        y_offset -= textSurface.get_height()

    glPushMatrix()

    # (left,right,bottom,top,near,far)
    glOrtho(ort_a, -ort_a, ort_a, -ort_a, 1, 100)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


x_pr, y_pr = 0, 0


def perspective():
    global x_pr, y_pr  # Use a variável global x, y e z
    keys = pygame.key.get_pressed()

    if keys[pygame.K_x] and keys[pygame.K_RIGHT]:
        x_pr -= fator
        y_pr = 0
    if keys[pygame.K_x] and keys[pygame.K_LEFT]:
        x_pr += fator
        y_pr = 0
    if keys[pygame.K_y] and keys[pygame.K_UP]:
        y_pr -= fator
        x_pr = 0
    if keys[pygame.K_y] and keys[pygame.K_UP]:
        y_pr += fator
        x_pr = 0
    if keys[pygame.K_0]:
        x_pr, y_pr = 0, 0
    if keys[pygame.K_8]:
        x_pr, y_pr = 0, 0

    font = pygame.font.SysFont('arial', 20)
    text = ['x + Seta Direita(x++)', 'x + Seta Esquerda (x--)', 'y + Seta Cima(y++)', 'y + Seta Baixo (y--)',
            '0 - Reset', '8 - Sair']
    y_offset = 700
    for line in text:
        textSurface = font.render(
            line, True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(10, y_offset)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, textData)
        y_offset -= textSurface.get_height()

    glPushMatrix()
    matriz_projecao = [
        1, 0, 0, x_pr,  # x
        0, 1, 0, y_pr,  # y
        0, 0, 1, 0,  # z
        0, 0, 0, 1
    ]
    glMultMatrixf(matriz_projecao)
    glColor3f(1.0, 0.0, 0.0)
    draw()
    glPopMatrix()


camera_x, camera_y, camera_z = 0, 0, -20
camera_rot_x, camera_rot_y = 0, 0
fator = 0.1


def camera():
    global camera_x, camera_y, camera_z, camera_rot_x, camera_rot_y

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (largura / altura), 0.1, 50.0)

    glTranslatef(camera_x, camera_y, camera_z)
    glRotatef(camera_rot_x, 1, 0, 0)
    glRotatef(camera_rot_y, 0, 1, 0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        camera_z += fator
    if keys[pygame.K_s]:
        camera_z -= fator
    if keys[pygame.K_a]:
        camera_x -= fator
    if keys[pygame.K_d]:
        camera_x += fator

    if keys[pygame.K_UP]:
        camera_rot_x -= 1
    if keys[pygame.K_DOWN]:
        camera_rot_x += 1
    if keys[pygame.K_LEFT]:
        camera_rot_y -= 1
    if keys[pygame.K_RIGHT]:
        camera_rot_y += 1

    if keys[pygame.K_0]:  # Resetar posição
        camera_x, camera_y, camera_z = 0, 0, -20
        camera_rot_x, camera_rot_y = 0, 0

    if keys[pygame.K_9]:  # Resetar posição
        camera_x, camera_y, camera_z = 0, 0, -20
        camera_rot_x, camera_rot_y = 0, 0

    font = pygame.font.SysFont('arial', 20)
    text = ['W - Profundidade (++)', 'S - Profundidade (--)', 'A - Eixo x--', 'D - Eixo x ++', 'Seta Cima - Rotação em x ++',
            'Seta Baixo - Rotação em x --', 'Seta Esquerda - Rotação em y--', 'Seta Direita - Rotação em y++', '0 - Reset', '9 - Sair']
    y_offset = 700
    for line in text:
        textSurface = font.render(
            line, True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(10, y_offset)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, textData)
        y_offset -= textSurface.get_height()


def exibir_menu():
    font = pygame.font.SysFont('arial', 20)
    text = ['1 - Translação', '2 - Escala', '3 - Rotação', '4 - Reflexão',
            '5 - Cisalhamento', '6 - Matriz genérica de projeção', '7 - Projeção Ortogonal', '8 - Projeção em perspectiva', '9 - Câmera Digital']
    y_offset = 700
    for line in text:
        textSurface = font.render(
            line, True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(10, y_offset)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, textData)
        y_offset -= textSurface.get_height()


translacao_ativa = False
scale_ativa = False
rotate_ativa = False
reflex_ativa = False
cis_ativa = False
proj_ativa = False
ort_ativa = False
perspective_ativa = False
camera_ativa = False
menu = True
# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Limpa a tela
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if menu:
        exibir_menu()

    draw()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_1]:
        time.sleep(1)
        translacao_ativa = not translacao_ativa  # Inverte o estado da translação
        menu = True

    if keys[pygame.K_2]:
        time.sleep(1)
        scale_ativa = not scale_ativa
        menu = True

    if keys[pygame.K_3]:
        time.sleep(1)
        rotate_ativa = not rotate_ativa
        menu = True

    if keys[pygame.K_4]:
        time.sleep(1)
        reflex_ativa = not reflex_ativa
        menu = True

    if keys[pygame.K_5]:
        time.sleep(1)
        cis_ativa = not cis_ativa
        menu = True

    if keys[pygame.K_6]:
        time.sleep(1)
        proj_ativa = not proj_ativa
        menu = True

    if keys[pygame.K_7]:
        time.sleep(1)
        ort_ativa = not ort_ativa
        menu = True

    if keys[pygame.K_8]:
        time.sleep(1)
        perspective_ativa = not perspective_ativa
        menu = True

    if keys[pygame.K_9]:
        time.sleep(1)
        camera_ativa = not camera_ativa
        menu = True

    if translacao_ativa:
        translation()
        menu = False
        scale_ativa = False
        rotate_ativa = False
        reflex_ativa = False
        cis_ativa = False
        proj_ativa = False
        ort_ativa = False
        perspective_ativa = False
        camera_ativa = False

    if scale_ativa:
        scale()
        menu = False
        translacao_ativa = False
        rotate_ativa = False
        reflex_ativa = False
        cis_ativa = False
        proj_ativa = False
        ort_ativa = False
        perspective_ativa = False
        camera_ativa = False

    if rotate_ativa:
        rotate()
        menu = False
        translacao_ativa = False
        scale_ativa = False
        reflex_ativa = False
        cis_ativa = False
        proj_ativa = False
        ort_ativa = False
        perspective_ativa = False
        camera_ativa = False

    if reflex_ativa:
        reflex()
        menu = False
        translacao_ativa = False
        scale_ativa = False
        rotate_ativa = False
        cis_ativa = False
        proj_ativa = False
        ort_ativa = False
        perspective_ativa = False
        camera_ativa = False

    if cis_ativa:
        cis()
        menu = False
        translacao_ativa = False
        scale_ativa = False
        rotate_ativa = False
        reflex_ativa = False
        proj_ativa = False
        ort_ativa = False
        perspective_ativa = False
        camera_ativa = False

    if proj_ativa:
        proj()
        menu = False
        translacao_ativa = False
        scale_ativa = False
        rotate_ativa = False
        reflex_ativa = False
        cis_ativa = False
        ort_ativa = False
        perspective_ativa = False
        camera_ativa = False
    if ort_ativa:
        ortho()
        menu = False
        translacao_ativa = False
        scale_ativa = False
        rotate_ativa = False
        reflex_ativa = False
        cis_ativa = False
        proj_ativa = False
        perspective_ativa = False
        camera_ativa = False

    if perspective_ativa:
        perspective()
        menu = False
        translacao_ativa = False
        scale_ativa = False
        rotate_ativa = False
        reflex_ativa = False
        cis_ativa = False
        proj_ativa = False
        ort_ativa = False
        camera_ativa = False

    if camera_ativa:
        camera()
        menu = False
        translacao_ativa = False
        scale_ativa = False
        rotate_ativa = False
        reflex_ativa = False
        cis_ativa = False
        proj_ativa = False
        ort_ativa = False
        perspective_ativa = False

    # Atualiza a tela
    pygame.display.flip()
    pygame.time.wait(10)
