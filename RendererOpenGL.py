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
screen = pygame.display.set_mode(screenSize, OPENGLBLIT | DOUBLEBUF | OPENGL)

#backgroung images
bgspace=pygame.image.load('spaceIm.jpg')

# Inicializacion de nuestro Renderer en OpenGL
r = Renderer(screen)
r.camPosition.z = 3
r.pointLight.x = 5

r.setShaders(shaders.vertex_shader, shaders.fragment_shader)

fox= Model('fox.obj', 'fox.bmp')
fox.position = glm.vec3(0,-30,-120)
fox.rotation = glm.vec3(0, -90, 0)

nave = Model('space-shuttle-orbiter.obj', 'planespace.bmp')

nave.position = glm.vec3(0,-30,-900)
nave.rotation = glm.vec3(0, -90, 0)

tiger = Model('tiger.obj', 'tiger-atlas.bmp')
tiger.position = glm.vec3(0,-30,-500)
tiger.rotation = glm.vec3(0, -90, 0)

mill = Model('ukulele.obj', 'uk.jpg')
mill.position = glm.vec3(0,-30,-800)
mill.rotation = glm.vec3(0, 0, 0)


r.modelList.append(tiger)
r.modelList.append(mill)
#r.modelList.append(Model('model.obj', 'model.bmp'))
r.modelList.append(nave)
r.modelList.append(fox)

#play a step sound when moving
def play_step():
    pygame.mixer.music.load('mariostep.mp3')
    pygame.mixer.music.play(0)

def play_exp():
    pygame.mixer.music.load('explosion.mp3')
    pygame.mixer.music.play(0)

isPlaying = True
while isPlaying:


    # Para revisar si una tecla esta presionada
    keys = pygame.key.get_pressed()

    # Move cam
    if keys[K_RIGHT]:
        r.camPosition.x += 100 * deltaTime
        """r.camPosition.z -= 50 * deltaTime
        r.camRotation.y += 50 * deltaTime"""
    if keys[K_LEFT]:
        r.camPosition.x -= 100 * deltaTime
        """r.camPosition.z -= 50 * deltaTime
        r.camRotation.y -= 50 * deltaTime"""

    if keys[K_1]:
        play_step()
        r.setShaders(shaders.vertex_shader, shaders.siren_shader)
    if keys[K_2]:
        play_step()
        r.setShaders(shaders.vertex_shader, shaders.rainbow_shader)
    if keys[K_3]:
        play_step()
        r.setShaders(shaders.vertex_shader, shaders.fragment_shader)
    if keys[K_4]:
        play_step()
        r.setShaders(shaders.dance_shader, shaders.siren_shader)
    if keys[K_5]:
        play_step()
        r.setShaders(shaders.exp_shader, shaders.siren_shader)
    if keys[K_w]:
        r.expl+=10
        play_exp()
    

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isPlaying = False
        elif ev.type == pygame.KEYDOWN:
            # para revisar en el momento que se presiona una tecla
            if ev.key == pygame.K_9:
                r.filledMode()
            elif ev.key == pygame.K_8:
                r.wireframeMode()
            elif ev.key == pygame.K_ESCAPE:
                isPlaying = False
            elif ev.key == pygame.K_SPACE:
                r.activeModelIndex = (r.activeModelIndex+1) % len( r.modelList )
        
        if ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 4:
                if r.camPosition.z>=-44:
                    r.camPosition.z -= 100 * deltaTime
               #print(r.camPosition.z)
            if ev.button == 5:
                if r.camPosition.z<=44:
                    r.camPosition.z += 100 * deltaTime
               #print(r.camPosition.z)


    # Main Renderer Loop
    r.render()

    pygame.display.flip()
    clock.tick(60)
    deltaTime = clock.get_time() / 1000
    r.cont=r.cont+1


pygame.quit()
