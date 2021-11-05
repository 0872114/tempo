import pyglet
from time import time


class Tempo(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label('',
                                       font_name='Times New Roman',
                                       font_size=36,
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center',
                                       batch=self.batch)

        self.dot = pyglet.shapes.Circle(x=self.width // 2,
                                        y=self.height // 2 - 72,
                                        radius=8,
                                        color=(178, 11, 12),
                                        batch=self.batch)
        self.prev_time = None
        self.tik = 0
        self.taks = []

        self.flag = False

    def on_draw(self):
        self.clear()
        self.dot.visible = self.flag
        self.batch.draw()

    def update_dot(self, *args, **kwargs):
        if self.tik:
            self.flag = not self.flag
        else:
            self.flag = False

    def on_key_press(self, *args, **kwargs):
        cur_time = time()
        if self.prev_time is None:
            self.prev_time = cur_time
            return

        tak = time() - self.prev_time
        if len(self.taks) > 8:
            self.taks.append((sum(self.taks) / len(self.taks) + tak) / 2)
        else:
            self.taks.append(tak)

        if len(self.taks) > 16:
            self.taks = self.taks[1:]

        if self.tik is None:
            self.tik = tak
            label = 'keep tapping...'
        elif tak >= self.tik * 2:
            self.tik = None
            self.taks = []
            self.prev_time = None
            label = '[reset]'
        elif len(self.taks) > 4:
            self.tik = sum(self.taks) / len(self.taks)
            bpm = round(60 / self.tik, 0)
            label = '{} BPM'.format(bpm)
            pyglet.clock.unschedule(self.update_dot)
            pyglet.clock.schedule_interval(self.update_dot, self.tik)
        else:
            self.tik = (self.tik + tak) / 2
            bpm = round(60 / self.tik, 0)
            label = '~{} BPM'.format(bpm)

        self.label.text = label
        self.prev_time = cur_time

    def on_mouse_press(self, *args, **kwargs):
        self.on_key_press()


if __name__ == '__main__':
    Tempo()
    pyglet.app.run()
