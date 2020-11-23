"""
Maria Ines Vasquez Figueroa
18250
Gráficas
RendererOpenGL 
Main
"""

import pygame
from pygame.locals import *

from gl import Renderer
import shaders



deltaTime = 0.0

# Inicializacion de pygame
pygame.init()
clock = pygame.time.Clock()
screenSize = (960, 540)
screen = pygame.display.set_mode(screenSize, DOUBLEBUF | OPENGL)

# Inicializacion de nuestro Renderer en OpenGL
r = Renderer(screen)
r.setShaders(shaders.vertex_shader, shaders.fragment_shader)
r.createObjects()

#constantes para mover el cubo en el espacio
cubeX = 0
cubeZ = 0

#ciclo de juego 
isPlaying = True
while isPlaying:

    # Para revisar si una tecla esta presionada
    #funciona con las teclas direccionales <- y ->
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cubeX -= 2 * deltaTime
    if keys[pygame.K_RIGHT]:
        cubeX += 2 * deltaTime

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isPlaying = False
        elif ev.type == pygame.KEYDOWN:
            # para revisar en el momento que se presiona una tecla
            if ev.key == pygame.K_1:
                r.filledMode()
            elif ev.key == pygame.K_2:
                r.wireframeMode
            elif ev.key == pygame.K_ESCAPE:
                isPlaying = False
        #para mover el cubo de atrás hacia adelante con la rueda del mouse
        if ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 4:
               cubeZ -= 2 * deltaTime
            if ev.button == 5:
               cubeZ += 2 * deltaTime

    #movimiento de cubo
    r.translateCube(cubeX, 0, cubeZ)

    # Main Renderer Loop
    r.render()

    #para renderizar cada cierto tiempo
    pygame.display.flip()
    clock.tick(60)
    deltaTime = clock.get_time() / 1000

#cuando renuncia del juego
pygame.quit()
