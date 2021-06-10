import time
import random
from threading import Thread
from collections import Counter


class Tetris(Thread):

    figure_temps = [((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)), ((0, 0), (0, 1), (1, 1), (1, 0))]

    def __init__(self, w, h):
        super().__init__()
        self.w = w
        self.h = h
        self.active = None
        self.figures = []
        self.not_free = set()

    def get_array(self):
        mas = [0] * self.h
        for i in range(self.h):
            mas[i] = [0] * self.w
        return mas

    class Figure:
        def __init__(self, figure_id, x, y, maxh, maxw):
            self.id = figure_id
            self.x = x
            self.y = y
            self.h, self.w = maxh, maxw
            self.angle = 0

        def get_all_cords(self):
            return set((self.x + i, self.y + j) for i, j in self.figure_with_angle(Tetris.figure_temps[self.id]))

        def print(self, area):
            for i, j in self.get_all_cords():
                area[j][i] = 1

        def interseption(self, other_cds, is_x=False, is_y=False):
            mas = {(0, 0)}
            if is_x:
                mas |= {(1, 0), (-1, 0)}
            if is_y:
                mas |= {(0, 1), (0, -1)}
            for i, j in self.get_all_cords():
                for tx, ty in mas:
                    if (i + tx, j + ty) in other_cds or (j + ty) > self.h:
                        return True
            return False

        def border(self, d=1, d1=1, is_x=False, is_y=True):
            for i, j in self.get_all_cords():
                if is_x:
                    if (i + d) >= self.w or (i - d1) < 0:
                        return True
                elif is_y:
                    if (j + d) >= self.h or (j - d1) < 0:
                        return True
            return False

        def move(self):
            self.y += 1

        def figure_with_angle(self, figure) -> (int, int):
            new_figure = set()
            for x, y in figure:
                if self.angle == 1:
                    new_figure.add((y, x))
                elif self.angle == 2:
                    new_figure.add((-x, y))
                elif self.angle == 3:
                    new_figure.add((y, -x))
                else:
                    new_figure.add((x, y))
            return new_figure

        def rotate(self, i=1):
            self.angle = (self.angle + i) % 4

    def is_colide(self, **kwargs):
        return self.active.border(1, -1) or self.active.interseption(self.not_free, **kwargs)

    def new_active(self):
        self.figures.append(self.active)
        self.not_free |= self.active.get_all_cords()
        self.active = None

    def full_row(self):
        cells = self.not_free
        for y, count in filter(lambda x: x[1] == self.w, Counter(map(lambda x: x[1], cells)).items()):
            new_free = set()
            for x0, y0 in self.not_free:
                if y0 < y:
                    new_free.add((x0, y0 + 1))
                elif y0 > y:
                    new_free.add((x0, y0))
            self.not_free = new_free

    def on_key(self, key):
        if self.active and not self.is_colide(is_y=True):
            if key == 'up':
                self.active.rotate()
                if self.active.border(0, 0, True, True) or self.is_colide():
                    self.active.rotate(-1)
            elif key == 'left':
                if not self.active.border(-1, 1, True, False):
                    self.active.x -= 1
                    if self.is_colide(is_x=False, is_y=False):
                        self.active.x += 1
                        self.new_active()
            elif key == 'right':
                if not self.active.border(1, -1, True, False):
                    self.active.x += 1
                    if self.is_colide(is_x=False, is_y=False):
                        self.active.x -= 1
                        self.new_active()
            elif key == 'down':
                self.active.y += 1

    def run(self):
        while 1:
            if self.active:
                if self.is_colide(is_y=True):
                    self.new_active()
                    continue
                else:
                    self.active.move()
            else:
                self.active = self.Figure(random.randint(0, len(self.figure_temps) - 1), self.w // 2, 0, self.h, self.w)
            self.full_row()
            time.sleep(1)

    def parse(self):
        arr = self.get_array()
        if self.active:
            self.active.print(arr)
        for x, y in self.not_free:
            arr[y][x] = 1
        # for figure in self.figures:
        #     figure.print(arr)
        return arr

