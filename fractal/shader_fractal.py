import glm
import pxng
from OpenGL.GL import GL_TRIANGLES


def resource(resource):
    from pathlib import Path
    font_path = Path(__file__).parent / 'resources' / resource
    return str(font_path)


class ShaderFractal:
    def __init__(self):
        program = pxng.ShaderProgram('FractalShader')
        program.add_shader(resource('fractal.vert'), pxng.ShaderType.Vertex)
        program.add_shader(resource('fractal.frag'), pxng.ShaderType.Fragment)
        program.compile_and_link()

        program.add_uniform('projection_view', glm.mat4x4)
        program.add_uniform('model', glm.mat4x4)
        program.add_uniform('iterations', glm.ivec1)
        program.add_uniform('fractal_space', glm.dvec4)
        self._program = program

        self._vao = pxng.VertexArrayObject(GL_TRIANGLES)
        self._vao.attach_buffer(pxng.BufferObject(data_type=glm.vec3))  # vertex buffer
        self._vao.attach_buffer(pxng.BufferObject(data_type=glm.vec2))  # texture buffer

        self._vao.add_quad(
            glm.vec3(0, 0, 0),
            glm.vec3(0, 1, 0),
            glm.vec3(1, 1, 0),
            glm.vec3(1, 0, 0),
        )

        self._vao.set_texture(
            glm.vec2(0, 1),
            glm.vec2(0, 0),
            glm.vec2(1, 0),
            glm.vec2(1, 1)
        )

    def create_fractal(self, spaces: pxng.Spaces, pix, frac, iterations):
        spaces.push()
        spaces.model.scale((spaces.width, spaces.height, 1))

        if self._vao.bind():
            self._program.activate()
            self._program.set_uniform('projection_view', spaces.projection_view)
            self._program.set_uniform('model', spaces.model.m)
            self._program.set_uniform('iterations', iterations)
            self._program.set_uniform('fractal_space', glm.dvec4(*frac))
            self._vao.draw()
        spaces.pop()
