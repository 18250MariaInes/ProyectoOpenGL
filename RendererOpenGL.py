"""
Maria Ines Vasquez Figueroa
18250
Gráficas
RendererOpenGL 
Main
"""

import pygame
from pygame.locals import *
import glm
from gl import Renderer, Model
import shaders

deltaTime = 0.0

# Inicializacion de pygame
pygame.init()
clock = pygame.time.Clock()
screenSize = (960, 540)
screen = pygame.display.set_mode(screenSize, DOUBLEBUF | OPENGL)

# Inicializacion de nuestro Renderer en OpenGL
r = Renderer(screen)
r.camPosition.z = 3
r.pointLight.x = 5

r.setShaders(shaders.vertex_shader, shaders.fragment_shader)

fox= Model('fox.obj', 'fox.bmp')
fox.position = glm.vec3(0,-30,-120)
fox.rotation = glm.vec3(0, -90, 0)

nave = Model('space-shuttle-orbiter.obj', 'planespace.bmp')

nave.position = glm.vec3(0,-30,-1000)
nave.rotation = glm.vec3(0, -90, 0)

tiger = Model('tiger.obj', 'tiger-atlas.bmp')
tiger.position = glm.vec3(0,-30,-500)
tiger.rotation = glm.vec3(0, -90, 0)

mill = Model('ukulele.obj', 'uk.jpg')
mill.position = glm.vec3(0,-30,-800)
mill.rotation = glm.vec3(0, 0, 0)


r.modelList.append(tiger)
r.modelList.append(mill)
r.modelList.append(Model('model.obj', 'model.bmp'))
r.modelList.append(nave)
#r.modelList.append(Model('marsRobot.obj', 'metal.bmp'))"""
r.modelList.append(fox)


isPlaying = True
while isPlaying:

    # Para revisar si una tecla esta presionada
    keys = pygame.key.get_pressed()

    # Move cam
    if keys[K_RIGHT]:
        r.camPosition.x += 1 * deltaTime
    if keys[K_LEFT]:
        r.camPosition.x -= 1 * deltaTime
    
    
    """if keys[K_w]:
        r.camPosition.z -= 1 * deltaTime
    if keys[K_s]:
        r.camPosition.z += 1 * deltaTime"""


    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isPlaying = False
        elif ev.type == pygame.KEYDOWN:
            # para revisar en el momento que se presiona una tecla
            if ev.key == pygame.K_1:
                r.filledMode()
            elif ev.key == pygame.K_2:
                r.wireframeMode()
            elif ev.key == pygame.K_ESCAPE:
                isPlaying = False
            elif ev.key == pygame.K_SPACE:
                r.activeModelIndex = (r.activeModelIndex+1)%len(r.modelList)
        
        if ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 4:
               r.camPosition.z -= 1 * deltaTime
            if ev.button == 5:
               r.camPosition.z += 1 * deltaTime

    # Main Renderer Loop
    r.render()

    pygame.display.flip()
    clock.tick(60)
    deltaTime = clock.get_time() / 1000


pygame.quit()
