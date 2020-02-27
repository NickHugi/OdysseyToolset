import time

import numpy
import pyrr
from OpenGL.GL import shaders, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QOpenGLWidget
import numpy as np


VERTEX_SHADER =\
"""
#version 330 core

uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;

layout (location=0) in vec3 in_Position;
layout (location=1) in vec2 in_TextureCoord;

out vec2 pass_TextureCoord;

void main(void) {
   gl_Position = vec4(in_Position, 1);
   gl_Position = projectionMatrix * viewMatrix * modelMatrix * gl_Position;

   pass_TextureCoord = in_TextureCoord;
}
"""

FRAGMENT_SHADER =\
"""
#version 330 core

uniform sampler2D texture_diffuse;

in vec2 pass_TextureCoord;

out vec4 out_Color;

void main(void) {
   out_Color = texture2D(texture_diffuse, pass_TextureCoord);
}
"""

shader = None


class ModelRenderer(QOpenGLWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.models = {}
        self.textures = {}

        self.model_buffer = {}

        self.objects = []

        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.last_update = time.time()
        self.delta_time = 0

    def update(self):
        self.delta_time = time.time() - self.last_update
        self.last_update = time.time()

        self.repaint()

        pause = int(33 - self.delta_time)
        if pause < 1: pause = 1
        QtCore.QTimer.singleShot(1, self.update)

    def initializeGL(self):
        global VERTEX_SHADER
        global FRAGMENT_SHADER
        global shader

        vertex_shader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        shader = shaders.compileProgram(vertex_shader, fragment_shader)

        self.axis_correction = numpy.array([[-1, 0, 0, 0],
                                            [0, 0, 1, 0],
                                            [0, 1, 0, 0],
                                            [0, 0, 0, 1]], dtype=np.float32)
        self.projection_matrix = self.axis_correction @ pyrr.matrix44.create_perspective_projection(80, 16 / 9, 0.1, 1000)

        QtCore.QTimer.singleShot(33, self.update)

    def resizeGL(self, width, height):
        aspect = width / height
        self.projection_matrix = self.axis_correction @ pyrr.matrix44.create_perspective_projection(80, aspect, 0.1, 1000)
        self.repaint()

    def paintGL(self):
        pass
