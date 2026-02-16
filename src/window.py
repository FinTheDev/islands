import pyglet

class GameWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=800, height=600, caption="Islands", resizable=True)
        pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)

    def on_draw(self):
        self.clear()

    def run(self):
        pyglet.app.run()
