"""
Maria Ines Vasquez Figueroa
18250
Gráficas
ProyectoOpenGL 
Funciones GL
"""
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
import numpy as np

from obj import Obj

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

class Model(object):
    def __init__(self, fileName, textureName):
        self.model = Obj(fileName)

        self.createVertBuffer()
        
        #textura del objeto
        self.texture_surface = pygame.image.load(textureName)
        self.texture_data = pygame.image.tostring(self.texture_surface,"RGB",1)
        self.texture = glGenTextures(1)

        self.position = glm.vec3(0,0,0)  #30,-90
        self.rotation = glm.vec3(0,0,0) # pitch, yaw, roll
        self.scale = glm.vec3(1,1,1)

    def getMatrix(self):
        i = glm.mat4(1)
        #View Matrix del objeto para rotarlo
        translate = glm.translate(i, self.position)
        pitch = glm.rotate(i, glm.radians( self.rotation.x ), glm.vec3(1,0,0))
        yaw   = glm.rotate(i, glm.radians( self.rotation.y ), glm.vec3(0,1,0))
        roll  = glm.rotate(i, glm.radians( self.rotation.z ), glm.vec3(0,0,1))
        rotate = pitch * yaw * roll
        scale = glm.scale(i, self.scale)
        return translate * rotate * scale

    def createVertBuffer(self):
        buffer = []
        #creacion del buffer del objeto, coneccion de vertices, caras, normales del objeto
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
        self.VBO = glGenBuffers(1) #Vertex Buffer Object
        self.VAO = glGenVertexArrays(1) #Vertex Array Object


    def renderInScene(self):
      
        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
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
        self.expl=0
        self.modelList = []

        self.activeModelIndex=0

        # View Matrix
        self.camPosition = glm.vec3(0,0,-250)
        self.camRotation = glm.vec3(0,0,0) # pitch, yaw, roll

        #rotation
        self.cam_pitch = 0
        self.cam_yaw = 0
        self.cam_roll = 0

        # Light
        self.pointLight = glm.vec4(-100,0,300,0)

        # Matriz de perspectiva/proyeccion
        self.projection = glm.perspective(glm.radians(60), self.width / self.height, 0.1, 1000)

    def getViewMatrix(self):
        # View Matrix
        # glm.lookAt( eye, center, up)
        i = glm.mat4(1)
        camTranslate = glm.translate(i, self.camPosition)
        cam_pitch = glm.rotate(i, glm.radians(self.cam_pitch), glm.vec3(1, 0, 0))
        cam_yaw = glm.rotate(i, glm.radians(self.cam_yaw), glm.vec3(0, 1, 0))
        cam_roll = glm.rotate(i, glm.radians(self.cam_roll), glm.vec3(0, 0, 1))
        cam_rotate = cam_pitch * cam_yaw * cam_roll
        return glm.inverse( camTranslate * cam_rotate )

    #solo dibujar el esqueleto del objeto
    def wireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    #llenar el objeto cargado
    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    #movimiento de roll para la camara
    def roll_camera(self, x):
        self.cam_roll = x

    #movimiento de pitch para la camara
    def pitch_camera(self, x):
        self.cam_pitch = x

    #movimiento de roll para la camara
    def yaw_camera(self, x):
        self.cam_yaw = x
    
    #funcion para mover la camara
    def translate_camera(self, x, y, z):
        self.camPosition = glm.vec3(x, y, z)


    #establecer shaders desarrollados en los modelos
    def setShaders(self, vertexShader, fragShader):

        if vertexShader is not None or fragShader is not None:
            self.active_shader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
                                                compileShader(fragShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shader = None

        glUseProgram(self.active_shader)

    #funcion para renderizar escena con camara
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
            glUniform1f(glGetUniformLocation(self.active_shader, "expl"), self.expl)

            if self.active_shader:
                glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "model"),
                                   1, GL_FALSE, glm.value_ptr( self.modelList[self.activeModelIndex].getMatrix() ))

            self.modelList[self.activeModelIndex].renderInScene()
