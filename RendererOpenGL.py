"""
Maria Ines Vasquez Figueroa
18250
Gráficas
ProyectoOpenGL 
Main
"""

import pygame
from pygame.locals import *
import glm
from gl import Renderer, Model
import shaders


deltaTime = 0.0
roll = 0
pitch = 0
yaw = 0

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
nave.position = glm.vec3(0,-30,-500)
nave.rotation = glm.vec3(0, -90, 0)
nave.scale = glm.vec3(0.5,0.5,0.5)

tiger = Model('tiger.obj', 'tiger-atlas.bmp')
tiger.position = glm.vec3(0,-30,-500)
tiger.rotation = glm.vec3(0, -90, 0)

camero = Model('camero.obj','camero.png')
camero.position = glm.vec3(0,-0.5,0)
camero.rotation = glm.vec3(0, 90, 0)


r.modelList.append(tiger)
r.modelList.append(nave)
r.modelList.append(fox)
r.modelList.append(camero)


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
    if keys[K_LEFT]:
        r.camPosition.x -= 100 * deltaTime
        

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
        r.setShaders(shaders.dance_shader, shaders.ola_shader)
    if keys[K_5]:
        play_step()
        r.setShaders(shaders.exp_shader, shaders.siren_shader)
    if keys[K_w]:
        r.expl+=10
        play_exp()
    if keys[K_x]:
        r.modelList[r.activeModelIndex].rotation.y += 30*deltaTime
        #yaw -= 30 * deltaTime
    if keys[K_y]:
        r.modelList[r.activeModelIndex].rotation.x += 30*deltaTime
        #pitch -= 30 * deltaTime
    

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

    r.roll_camera(roll)
    r.pitch_camera(pitch)
    r.yaw_camera(yaw)
    r.render()

    pygame.display.flip()
    clock.tick(60)
    deltaTime = clock.get_time() / 1000
    r.cont=r.cont+1


pygame.quit()
