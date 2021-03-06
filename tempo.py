import pyglet
from time import time, sleep
from pysinewave import SineWave
import threading


class Tempo(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sinewave = SineWave(pitch = 12, pitch_per_second = 10)

        self.batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label('start tapping',
                                       font_name='Times New Roman',
                                       font_size=36,
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center',
                                       batch=self.batch)

        self.dot = pyglet.shapes.Circle(x=self.width // 2,
                                        y=self.height // 2 - 72,
                                        radius=8,
                                        color=(255, 255, 255),
                                        batch=self.batch)
        self.prev_time = None
        self.tik = 0
        self.taks = []

        self.flag = False

    def on_draw(self):
        self.clear()
        self.dot.visible = self.flag
        self.batch.draw()

    def play_sound(self, *args, **kwargs):
        self.sinewave.play()
        sleep(1/60)
        self.sinewave.stop()

    def update_dot(self, *args, **kwargs):
        self.flag = not self.flag
        if time() - self.prev_time > self.tik * 1.5 and self.flag and self.tik > 1/30:
            t = threading.Thread(target=self.play_sound)
            t.start()

    def on_key_press(self, *args, **kwargs):

        label = '...'
        cur_time = time()
        if self.prev_time is None:
            self.prev_time = cur_time
            return

        tak = time() - self.prev_time
        self.taks.append(tak)

        if not self.tik:
            self.tik = tak
            self.taks = []
            label = 'keep tapping...'
        elif tak >= self.tik * 2:
            self.tik = None
            self.taks = []
            self.prev_time = None
            label = '[reset]'
            pyglet.clock.unschedule(self.update_dot)
            self.flag = False
        elif len(self.taks):
            self.tik = sum(self.taks) / len(self.taks)
            bpm = round(60 / self.tik, 0)
            label = '{} BPM'.format(bpm)
            pyglet.clock.unschedule(self.update_dot)
            pyglet.clock.schedule_interval(self.update_dot, self.tik / 2)

        self.label.text = label
        self.prev_time = cur_time

    def on_mouse_press(self, *args, **kwargs):
        self.on_key_press()


if __name__ == '__main__':
    Tempo()
    pyglet.app.run()
