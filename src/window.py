import pyglet
from pyglet import gl
from src.renderer import Renderer

class GameWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=800, height=600, caption="Islands", resizable=True)

        gl.glEnable(gl.GL_DEPTH_TEST)

        self.renderer = Renderer(self.width, self.height)

    def on_draw(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.renderer.draw()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        gl.glViewport(0, 0, width, height)
        self.renderer.width = width
        self.renderer.height = height
        self.renderer._create_matrices()

    def run(self):
        pyglet.app.run()
