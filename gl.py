"""
Maria Ines Vasquez Figueroa
18250
Gráficas
RendererOpenGL 
Funciones GL
"""

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
import numpy as np


                     # VERTS           COLOR
rectVerts = np.array([ 0.5, 0.5, 0.5,  1,0,0, 
                       0.5,-0.5, 0.5,  0,1,0, 
                      -0.5,-0.5, 0.5,  0,0,1, 
                      -0.5, 0.5, 0.5,  1,1,0,
                       0.5, 0.5,-0.5,  1,0,1,
                       0.5,-0.5,-0.5,  0,1,1,
                      -0.5,-0.5,-0.5,  1,1,1,
                      -0.5, 0.5,-0.5,  0,0,0 ], dtype=np.float32)


#cube-- it works
rectIndices = np.array([ #front
                         0, 1, 3,
                         1, 2, 3,
                         #left
                         4, 5, 0,
                         5, 1, 0,
                         #back
                         7, 6, 4,
                         6, 5, 4,
                         #right
                         3, 2, 7,
                         2, 6, 7,
                         #top
                         1, 5, 2,
                         5, 6, 2,
                         #bottom
                         4, 0, 7,
                         0, 3, 7], dtype=np.uint32)

#triangle-- working on it
vertex_data = np.array([
    -5, -5, 0.0,
     5, -5, 0.0,
     0.0,  5, 0.0
], dtype=np.uint32)



"""class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        # Matriz de perspectiva/proyeccion
        self.projection = glm.perspective(glm.radians(60), self.width / self.height, 0.1, 1000)

        #posición inicial del cubp
        self.cubePos = glm.vec3(0,0,0)

    #solo dibujar el esqueleto del objeto
    def wireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    #llenar el objeto cargado
    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    #mover el cubo en el espacio
    def translateCube(self, x, y, z):
        self.cubePos = glm.vec3(x,y,z)

    #set shader para objeto
    def setShaders(self, vertexShader, fragShader):

        if vertexShader is not None or fragShader is not None:
            self.active_shader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
                                                compileShader(fragShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shader = None

        glUseProgram(self.active_shader)

    #cargar objeto a visualizar
    def createObjects(self):

        self.VBO = glGenBuffers(1) #Vertex Buffer Object
        self.EBO = glGenBuffers(1) #Element Buffer Object
        self.VAO = glGenVertexArrays(1) #Vertex Array Object

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, rectVerts.nbytes, rectVerts, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, rectIndices.nbytes, rectIndices, GL_STATIC_DRAW)

        # Atributo de posicion de vertices
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Atributo de color de vertices
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(4 * 3))
        glEnableVertexAttribArray(1)

    #funcion de renderizaje
    def render(self):
        glClearColor(0.2, 0.2, 0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

        i = glm.mat4(1)

        #como las matrices vistas en Static rendering
        
        # Model/Object matrix: translate * rotate * scale 
        translate = glm.translate(i, self.cubePos)
        pitch = glm.rotate(i, glm.radians( 0 ), glm.vec3(1,0,0))
        yaw   = glm.rotate(i, glm.radians( 0 ), glm.vec3(0,1,0))
        roll  = glm.rotate(i, glm.radians( 0 ), glm.vec3(0,0,1))
        rotate = pitch * yaw * roll
        scale = glm.scale(i, glm.vec3(1,1,1))
        model = translate * rotate * scale
        
        # View Matrix
        # glm.lookAt( eye, center, up)
        camTranslate = glm.translate(i, glm.vec3( 0, 0, 3))
        camPitch = glm.rotate(i, glm.radians( 0 ), glm.vec3(1,0,0))
        camYaw   = glm.rotate(i, glm.radians( 0 ), glm.vec3(0,1,0))
        camRoll  = glm.rotate(i, glm.radians( 0 ), glm.vec3(0,0,1))
        camRotate = camPitch * camYaw * camRoll
        view = glm.inverse( camTranslate * camRotate )


        if self.active_shader:

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "model"),
                               1, GL_FALSE, glm.value_ptr( model ))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "view"),
                               1, GL_FALSE, glm.value_ptr( view ))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projection"),
                               1, GL_FALSE, glm.value_ptr( self.projection ))


        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
"""

import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
import numpy as np

from obj import Obj

class Model(object):
    def __init__(self, fileName, textureName):
        self.model = Obj(fileName)

        self.createVertBuffer()
        
        self.texture_surface = pygame.image.load(textureName)
        self.texture_data = pygame.image.tostring(self.texture_surface,"RGB",1)
        self.texture = glGenTextures(1)

        self.position = glm.vec3(0,0,0)  #30,-90
        self.rotation = glm.vec3(0,0,0) # pitch, yaw, roll
        self.scale = glm.vec3(1,1,1)

    def getMatrix(self):
        i = glm.mat4(1)
        translate = glm.translate(i, self.position)
        pitch = glm.rotate(i, glm.radians( self.rotation.x ), glm.vec3(1,0,0))
        yaw   = glm.rotate(i, glm.radians( self.rotation.y ), glm.vec3(0,1,0))
        roll  = glm.rotate(i, glm.radians( self.rotation.z ), glm.vec3(0,0,1))
        rotate = pitch * yaw * roll
        scale = glm.scale(i, self.scale)
        return translate * rotate * scale

    def createVertBuffer(self):
        buffer = []

        for face in self.model.faces:
            for i in range(3):
                #verts
                buffer.append(self.model.vertices[face[i][0] - 1][0])
                buffer.append(self.model.vertices[face[i][0] - 1][1])
                buffer.append(self.model.vertices[face[i][0] - 1][2])
                buffer.append(1)

                #norms
                buffer.append(self.model.normals[face[i][2] - 1][0])
                buffer.append(self.model.normals[face[i][2] - 1][1])
                buffer.append(self.model.normals[face[i][2] - 1][2])
                buffer.append(0)

                #texcoords
                buffer.append(self.model.texcoords[face[i][1] - 1][0])
                buffer.append(self.model.texcoords[face[i][1] - 1][1])

        self.vertBuffer = np.array( buffer, dtype=np.float32)


    def renderInScene(self):

        VBO = glGenBuffers(1) #Vertex Buffer Object
        VAO = glGenVertexArrays(1) #Vertex Array Object

        glBindVertexArray(VAO)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertBuffer.nbytes, self.vertBuffer, GL_STATIC_DRAW)

        # Atributo de posicion de vertices
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * 10, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Atributo de normal de vertices
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 4 * 10, ctypes.c_void_p(4 * 4))
        glEnableVertexAttribArray(1)

        ## Atributo de uvs de vertices
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 4 * 10, ctypes.c_void_p(4 * 8))
        glEnableVertexAttribArray(2)

        # Dar textura
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.texture_surface.get_width(), self.texture_surface.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, self.texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        glDrawArrays(GL_TRIANGLES, 0, len(self.model.faces) * 3)



class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        self.temp = 0
        self.cont=0 
        self.modelList = []

        self.activeModelIndex=0

        # View Matrix
        self.camPosition = glm.vec3(0,0,0)
        self.camRotation = glm.vec3(0,0,0) # pitch, yaw, roll

        # Light
        self.pointLight = glm.vec4(-100,0,300,0)

        # Perspective Projection Matrix
        self.projection = glm.perspective(glm.radians(60), self.width / self.height, 0.1, 1000)

    def getViewMatrix(self):
        i = glm.mat4(1)
        camTranslate = glm.translate(i, self.camPosition)
        camPitch = glm.rotate(i, glm.radians( self.camRotation.x ), glm.vec3(1,0,0))
        camYaw   = glm.rotate(i, glm.radians( self.camRotation.y ), glm.vec3(0,1,0))
        camRoll  = glm.rotate(i, glm.radians( self.camRotation.z ), glm.vec3(0,0,1))
        camRotate = camPitch * camYaw * camRoll
        return glm.inverse( camTranslate * camRotate )

    def wireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


    def setShaders(self, vertexShader, fragShader):

        if vertexShader is not None or fragShader is not None:
            self.active_shader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
                                                compileShader(fragShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shader = None

        glUseProgram(self.active_shader)


    def render(self):

        glClearColor(0.2, 0.2, 0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        cont=0

        if self.active_shader:
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "view"),
                               1, GL_FALSE, glm.value_ptr( self.getViewMatrix() ))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projection"),
                               1, GL_FALSE, glm.value_ptr( self.projection ))

            glUniform4f(glGetUniformLocation(self.active_shader, "light"), 
                        self.pointLight.x, self.pointLight.y, self.pointLight.z, self.pointLight.w)

            glUniform4f(glGetUniformLocation(self.active_shader, "color"), 
                        1, 1, 1, 1)
            
            glUniform1f(glGetUniformLocation(self.active_shader, "time"), self.cont)

        #for model in self.modelList:

            if self.active_shader:
                glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "model"),
                                   1, GL_FALSE, glm.value_ptr( self.modelList[self.activeModelIndex].getMatrix() ))

            self.modelList[self.activeModelIndex].renderInScene()
