import time

import numpy
import pyrr
from OpenGL.GL import shaders, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glEnable, GL_DEPTH_TEST, glClear, \
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, glUseProgram, glGetUniformLocation, glUniformMatrix4fv, glGenVertexArrays, \
    glBindVertexArray, glGenBuffers, GL_ELEMENT_ARRAY_BUFFER, glBindBuffer, glBufferData, GL_ARRAY_BUFFER, \
    GL_STATIC_DRAW, glEnableVertexAttribArray, glGetAttribLocation, glVertexAttribPointer, glDrawElements, GL_TRIANGLES, \
    GL_TEXTURE_2D, glBindTexture, GL_UNSIGNED_SHORT, GL_FLOAT, GL_TRUE, GL_FALSE, ctypes, glPixelStorei, glGenTextures, \
    GL_UNPACK_ALIGNMENT, glTexParameterf, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_REPEAT, GL_TEXTURE_MAG_FILTER, \
    GL_LINEAR, GL_TEXTURE_MIN_FILTER, GL_RGBA8, GL_BGRA, glTexImage2D, GL_UNSIGNED_INT_8_8_8_8, GL_UNSIGNED_BYTE, \
    glCompressedTexImage2D, GL_UNSIGNED_INT_8_8_8_8_REV
from OpenGL.raw.GL.EXT.texture_compression_s3tc import GL_COMPRESSED_RGBA_S3TC_DXT1_EXT, GL_COMPRESSED_RGB_S3TC_DXT1_EXT
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QOpenGLWidget
import numpy as np

from installation import Installation

VERTEX_SHADER = \
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

FRAGMENT_SHADER = \
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

        self.camera_position = pyrr.vector3.create(0, -2, 0, np.float32)
        self.camera_rotation = pyrr.euler.create(0, 0, 0, np.float32)

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
        self.projection_matrix = self.axis_correction @ pyrr.matrix44.create_perspective_projection(80, 16 / 9, 0.1,
                                                                                                    1000)

        texture_id = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, 1, 1, 0, GL_BGRA, GL_UNSIGNED_INT_8_8_8_8, [0xFF00FFFF])
        self.textures["NULL"] = texture_id

        QtCore.QTimer.singleShot(33, self.update)

    def resizeGL(self, width, height):
        aspect = width / height
        self.projection_matrix = self.axis_correction @ pyrr.matrix44.create_perspective_projection(80, aspect, 0.1,
                                                                                                    1000)
        self.repaint()

    def paintGL(self):
        for model_name, model in self.model_buffer.items():
            for texture_name in model.textures:
                if texture_name not in self.textures:
                    tex = Installation.find_texture(texture_name, self.window().active_installation)
                    texture_id = glGenTextures(1)
                    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
                    glBindTexture(GL_TEXTURE_2D, texture_id)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, tex.width, tex.height, 0, GL_BGRA, GL_UNSIGNED_INT_8_8_8_8_REV , tex.get_rgba())
                    self.textures[texture_name] = texture_id
            self.models[model_name] = self.load_node_data(model.root_node)
            self.build_node(self.models[model_name], model.root_node)
        self.model_buffer.clear()

        global shader

        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shader)

        rot = pyrr.matrix44.create_from_eulers(self.camera_rotation)
        trans = pyrr.matrix44.create_from_translation(self.camera_position)
        view_matrix = trans @ rot

        projectionMatrixLocation = glGetUniformLocation(shader, "projectionMatrix")
        glUniformMatrix4fv(projectionMatrixLocation, 1, False, self.projection_matrix)

        viewMatrixLocation = glGetUniformLocation(shader, "viewMatrix")
        glUniformMatrix4fv(viewMatrixLocation, 1, False, view_matrix)

        for object in self.objects:
            if object.model_name in self.models:
                transform = pyrr.matrix44.create_from_translation(object.position).T
                self.models[object.model_name].render(transform)

    def load_node_data(self, model_node):
        vertex_data = []
        indices_data = []
        texture = ""

        if model_node.trimesh is not None and model_node.trimesh.render is True and model_node.walkmesh is None:
            texture = model_node.trimesh.texture
            for i in range(len(model_node.trimesh.vertices)):
                vertex_data.append(model_node.trimesh.vertices[i].x)
                vertex_data.append(model_node.trimesh.vertices[i].y)
                vertex_data.append(model_node.trimesh.vertices[i].z)
                if len(model_node.trimesh.texture_uvs) != 0:
                    vertex_data.append(model_node.trimesh.texture_uvs[i].u)
                    vertex_data.append(1.0 - model_node.trimesh.texture_uvs[i].v)
                else:
                    vertex_data.extend([0.0, 0.0])
            for i in range(len(model_node.trimesh.faces)):
                indices_data.append(model_node.trimesh.faces[i][0])
                indices_data.append(model_node.trimesh.faces[i][1])
                indices_data.append(model_node.trimesh.faces[i][2])

        vertex_data = numpy.array(vertex_data, dtype=np.float32)
        indices_data = numpy.array(indices_data, dtype=np.uint16)

        position = pyrr.vector3.create()
        rotation = pyrr.quaternion.create()
        position = pyrr.vector3.create(model_node.local_position.x, model_node.local_position.y, model_node.local_position.z)
        rotation = pyrr.quaternion.create(model_node.local_rotation.x, model_node.local_rotation.y, model_node.local_rotation.z, model_node.local_rotation.w)

        return GLNode(self, position, rotation, vertex_data, indices_data, texture, model_node.name)

    def build_node(self, gl_node, model_node):
        for model_child in model_node.children:
            gl_child = self.load_node_data(model_child)
            gl_node.children.append(gl_child)
            self.build_node(gl_child, model_child)


class GLNode:
    def __init__(self, renderer, position, rotation, vertex_data, indices_data, texture_name, name):
        self.renderer = renderer
        self.position = pyrr.matrix44.create_from_translation(position).T
        self.rotation = pyrr.matrix44.create_from_quaternion(rotation)
        self.vertex_data = vertex_data
        self.indices_data = indices_data
        self.texture_name = texture_name
        self.name = name
        self.children = []

        self.element_count = len(indices_data)

        self.vao_id = glGenVertexArrays(1)
        glBindVertexArray(self.vao_id)

        self.ebo_id = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo_id)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_data, GL_STATIC_DRAW)

        self.vbo_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_id)
        glBufferData(GL_ARRAY_BUFFER, vertex_data, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        positionAttrib = glGetAttribLocation(shader, 'in_Position')
        coordsAttrib = glGetAttribLocation(shader, 'in_TextureCoord')
        glVertexAttribPointer(positionAttrib, 3, GL_FLOAT, GL_FALSE, 20, None)
        glVertexAttribPointer(coordsAttrib, 2, GL_FLOAT, GL_TRUE, 20, ctypes.c_void_p(12))

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self, parent_transform):
        transform = parent_transform @ self.position @ self.rotation

        texture_id = self.renderer.textures["NULL"]
        if self.texture_name in self.renderer.textures:
            texture_id = self.renderer.textures[self.texture_name]

        modelMatrixLocation = glGetUniformLocation(shader, "modelMatrix")
        glUniformMatrix4fv(modelMatrixLocation, 1, False, transform.T)

        glBindTexture(GL_TEXTURE_2D, texture_id)

        glBindVertexArray(self.vao_id)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo_id)
        glDrawElements(GL_TRIANGLES, self.element_count, GL_UNSIGNED_SHORT, None)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        for child in self.children:
            child.render(transform)


class Object:
    def __init__(self, model_name, position=pyrr.vector3.create(), rotation=pyrr.quaternion.create()):
        self.model_name = model_name
        self.position = position
        self.rotation = rotation
