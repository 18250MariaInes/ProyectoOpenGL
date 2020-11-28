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
from math import sqrt, sin, cos, tan, radians

deltaTime = 0.0
cubeX = 0
cubeY = 0
cubeZ = 0
roll = 0
pitch = 0
yaw = 0
distance = 0

changeY=False
changeX=False

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
camero.position = glm.vec3(0,-0.5,-3)
camero.rotation = glm.vec3(0, -90, 0)


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
        
    #shader de luz de policia
    if keys[K_1]:
        play_step()
        r.setShaders(shaders.vertex_shader, shaders.siren_shader)
    #shader de colores de normal
    if keys[K_2]:
        play_step()
        r.setShaders(shaders.vertex_shader, shaders.rainbow_shader)
    #modelo normal
    if keys[K_3]:
        play_step()
        r.setShaders(shaders.vertex_shader, shaders.fragment_shader)
    #shader de catapulta con cambio de color entre rojo y blanco
    if keys[K_4]:
        play_step()
        r.setShaders(shaders.dance_shader, shaders.ola_shader)
    #shader de explosion 
    if keys[K_5]:
        play_step()
        r.setShaders(shaders.exp_shader, shaders.siren_shader)
    #Para hacer que el objeto explote
    if keys[K_w]:
        r.expl+=10
        play_exp()
    #girar el objeto en el eje horizontal
    if keys[K_x]:
        if (changeY):
            cubeX = 0
            cubeY = 0
            cubeZ = 0
            roll = 0
            pitch = 0
            yaw = 0
            changeY=False
        yaw += 90*deltaTime % 360
        cube_pos = r.modelList[r.activeModelIndex].position
        cam_pos = r.camPosition
        cubeX = sin(radians(yaw))*abs(cube_pos.z)
        cubeZ = cos(radians(yaw))*abs(cube_pos.z) - abs(cube_pos.z) 
        changeX=True
    #girar el objeto en el eje vertical
    if keys[K_y]:
        if (changeX):
            cubeX = 0
            cubeY = 0
            cubeZ = 0
            roll = 0
            pitch = 0
            yaw = 0
            changeX=False
        pitch += 90*deltaTime % 360
        cube_pos = r.modelList[r.activeModelIndex].position
        cubeY = -sin(radians(pitch))*abs(cube_pos.z)
        cubeZ = cos(radians(pitch))*abs(cube_pos.z) - abs(cube_pos.z)
        changeY=True
    

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
            #cambio de modelo
            elif ev.key == pygame.K_SPACE:
                r.expl=0
                cubeX = 0
                cubeY = 0
                cubeZ = 0
                roll = 0
                pitch = 0
                yaw = 0
                r.activeModelIndex = (r.activeModelIndex+1) % len( r.modelList )
        
        if ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.MOUSEBUTTONUP:
            #girar el objeto en el eje horizontal
            if ev.button == 4:
                if (changeY):
                    cubeX = 0
                    cubeY = 0
                    cubeZ = 0
                    roll = 0
                    pitch = 0
                    yaw = 0
                    changeY=False
                yaw += 90*deltaTime % 360
                cube_pos = r.modelList[r.activeModelIndex].position
                cam_pos = r.camPosition
                cubeX = sin(radians(yaw))*abs(cube_pos.z)
                cubeZ = cos(radians(yaw))*abs(cube_pos.z) - abs(cube_pos.z) 
                changeX=True
            #girar el objeto en el eje vertical
            if ev.button == 5:
                if (changeX):
                    cubeX = 0
                    cubeY = 0
                    cubeZ = 0
                    roll = 0
                    pitch = 0
                    yaw = 0
                    changeX=False
                pitch += 90*deltaTime % 360
                cube_pos = r.modelList[r.activeModelIndex].position
                cubeY = -sin(radians(pitch))*abs(cube_pos.z)
                cubeZ = cos(radians(pitch))*abs(cube_pos.z) - abs(cube_pos.z)
                changeY=True

    # Main Renderer Loop
    r.translate_camera(cubeX, cubeY, cubeZ)
    r.roll_camera(roll)
    r.pitch_camera(pitch)
    r.yaw_camera(yaw)
    r.render()

    pygame.display.flip()
    clock.tick(60)
    deltaTime = clock.get_time() / 1000
    r.cont=r.cont+1


pygame.quit()
