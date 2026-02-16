from pyglet import gl
import ctypes
import numpy as np
import math
from src.math_utils import perspective, identity

class Renderer:
    def __init__(self, width, height):
        self.program = self.create_shader_program()
        self.width = width
        self.height = height

        self._create_cube()
        self._create_matrices()

    def create_shader_program(self):
        def load_shader(path, shader_type):
            with open(path, "r") as f:
                source = f.read()

            shader = gl.glCreateShader(shader_type)

            src_buffer = ctypes.create_string_buffer(source.encode())
            ptr = ctypes.cast(
                ctypes.pointer(ctypes.pointer(src_buffer)),
                ctypes.POINTER(ctypes.POINTER(gl.GLchar))
            )
            length = ctypes.c_int(len(source))

            gl.glShaderSource(shader, 1, ptr, ctypes.byref(length))
            gl.glCompileShader(shader)

            status = gl.GLint()
            gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS, ctypes.byref(status))
            if not status.value:
                log_length = gl.GLint()
                gl.glGetShaderiv(shader, gl.GL_INFO_LOG_LENGTH, ctypes.byref(log_length))
                log = ctypes.create_string_buffer(log_length.value)
                gl.glGetShaderInfoLog(shader, log_length, None, log)
                raise RuntimeError(log.value.decode())

            return shader

        vertex = load_shader("assets/shaders/vertex.glsl", gl.GL_VERTEX_SHADER)
        fragment = load_shader("assets/shaders/fragment.glsl", gl.GL_FRAGMENT_SHADER)

        program = gl.glCreateProgram()
        gl.glAttachShader(program, vertex)
        gl.glAttachShader(program, fragment)
        gl.glLinkProgram(program)

        status = gl.GLint()
        gl.glGetProgramiv(program, gl.GL_LINK_STATUS, ctypes.byref(status))
        if not status.value:
            log_length = gl.GLint()
            gl.glGetProgramiv(program, gl.GL_INFO_LOG_LENGTH, ctypes.byref(log_length))
            log = ctypes.create_string_buffer(log_length.value)
            gl.glGetProgramInfoLog(program, log_length, None, log)
            raise RuntimeError(log.value.decode())

        gl.glDeleteShader(vertex)
        gl.glDeleteShader(fragment)

        return program

    def _create_cube(self):
        self.vao = gl.GLuint()
        gl.glGenVertexArrays(1, ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)

        vertices = [
            -0.5, -0.5, -0.5,
             0.5, -0.5, -0.5,
             0.5,  0.5, -0.5,
             0.5,  0.5, -0.5,
            -0.5,  0.5, -0.5,
            -0.5, -0.5, -0.5,
        ]

        vertex_data = (gl.GLfloat * len(vertices))(*vertices)

        self.vbo = gl.GLuint()
        gl.glGenBuffers(1, ctypes.byref(self.vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        size = gl.GLsizeiptr(ctypes.sizeof(vertex_data))
        gl.glBufferData(gl.GL_ARRAY_BUFFER, size, vertex_data, gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

    def _create_matrices(self):
        aspect = self.width / self.height
        self.projection = perspective(math.radians(70), aspect, 0.1, 100.0)
        self.view = identity()
        self.model = identity()

        self.view[2][3] = -2.0

    def _set_matrix(self, name, matrix):
        location = gl.glGetUniformLocation(self.program, name.encode())
        gl.glUniformMatrix4fv(
            location,
            1,
            gl.GL_TRUE,
            matrix.ctypes.data_as(ctypes.POINTER(gl.GLfloat))
        )

    def draw(self):
        gl.glUseProgram(self.program)

        self._set_matrix("projection", self.projection)
        self._set_matrix("view", self.view)
        self._set_matrix("model", self.model)

        gl.glBindVertexArray(self.vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
