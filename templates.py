from engine import *
import random
import glob
import math
from threading import Thread
import time


class MainMenu(GameArea):
    def __init__(self, main_object):
        super().__init__()
        resolution = main_object.resolution

        bt_new_game = Button(resolution, 20, 20, 60, 10,
                             border_color=(255, 255, 255), border=2)
        bt_new_game.set_color((150, 150, 150))
        bt_new_game.color_on_mouse_down = pygame.Color('gray')
        bt_new_game.set_text('Начать игру', (0, 0, 0))
        bt_new_game.connect_mouse_up(lambda x: (pygame.mixer_music.stop(),
                                                main_object.new_game()))

        bt_settings = Button(resolution, 20, 40, 60, 10,
                             border_color=(255, 255, 255), border=2)
        bt_settings.set_color((150, 150, 150))
        bt_settings.set_text('Настройки', (0, 0, 0))
        bt_settings.color_on_mouse_down = pygame.Color('gray')
        bt_settings.connect_mouse_up(lambda x: main_object.switch_game_area(
            main_object.settings))

        bt_exit = Button(resolution, 20, 60, 60, 10,
                         border_color=(255, 255, 255), border=2)
        bt_exit.set_color((150, 150, 150))
        bt_exit.set_text('Выход', (0, 0, 0))
        bt_exit.color_on_mouse_down = pygame.Color('gray')
        bt_exit.connect_mouse_up(main_object.quit)

        self.add_objects(bt_new_game, bt_settings, bt_exit)


class Settings(GameArea):

    def __init__(self, main_object):
        super().__init__()
        resolution = main_object.resolution

        res_condition = lambda obj, key: key.isdigit() and (
            key != '0' if len(obj.text) == 0 else len(obj.text) < 4)

        te_res_x = TextEdit(resolution, 20, 40, 25, 5, border=2)
        te_res_x.color_default = (200, 200, 200)
        te_res_x.set_color((200, 200, 200))
        te_res_x.color_filling = (160, 160, 160)
        te_res_x.text_condition = res_condition

        te_res_x.set_text(str(resolution[0]))

        te_res_y = TextEdit(resolution, 55, 40, 25, 5, border=2)
        te_res_y.color_default = (200, 200, 200)
        te_res_y.set_color((200, 200, 200))
        te_res_y.color_filling = (160, 160, 160)
        te_res_y.text_condition = res_condition
        te_res_y.set_text(str(resolution[1]))

        lb_res = Object(resolution, 40, 30, 20, 8)
        lb_res.set_text('Разрешение',
                        (255, 255, 255),
                        align='center',
                        valign='center')

        bt_down_color = pygame.Color('red')

        bt_ok = Button(resolution, 60, 60, 20, 5, border=2)
        bt_ok.set_color((200, 200, 200))
        bt_ok.color_on_mouse_down = (100, 100, 100)
        bt_ok.color_on_mouse_up = (200, 200, 200)

        def change_res(obj: Button, load_obj):
            main_object.switch_resolution(int(te_res_x.text),
                                          int(te_res_y.text),
                                          bt_fullscreen.image_enabled)
            main_object.switch_game_area(load_obj)

        bt_ok.connect_mouse_up(lambda e: change_res(e, main_object.main_menu))
        bt_ok.set_text('OK')

        bt_cancel = Button(resolution, 20, 60, 20, 5, border=2)
        bt_cancel.set_color((200, 200, 200))
        bt_cancel.color_on_mouse_down = (100, 100, 100)
        bt_cancel.color_on_mouse_up = (200, 200, 200)
        bt_cancel.connect_mouse_up(lambda e: main_object.switch_game_area(
            main_object.main_menu))
        bt_cancel.set_text('Отмена')

        bt_fullscreen = Button(resolution, 20, 50, 5, 5,
                               adopt_order=0,
                               border_color=(150, 150, 150),
                               border=2)
        bt_fullscreen.set_image('.\\staff\\check_box.jpg', size_mode='%obj')
        bt_fullscreen.image_enabled = main_object.full_screen
        bt_fullscreen.set_color((255, 255, 255))

        def switch_image(e):
            e.image_enabled = not e.image_enabled

        bt_fullscreen.connect_mouse_up(switch_image)
        # bt_fullscreen.image_enabled = False

        lb_fullscreen = Object(resolution, 25, 50, 10, 5)
        lb_fullscreen.set_text('Полный экран', (255, 255, 255), align='left')

        self.add_objects(te_res_x,
                         te_res_y,
                         lb_res,
                         bt_ok,
                         bt_cancel,
                         bt_fullscreen,
                         lb_fullscreen)


class Gaming(GameArea):

    def __init__(self, main_object):
        super().__init__()
        resolution = main_object.resolution
        # self.background = Background(resolution,
        #                              random.choice(glob.glob('.\\galaxes\\*')))
        self.main = main_object
        self.images = glob.glob('.\\planets\\*.png')
        random.shuffle(self.images)

    def update(self, main):
        k = 5
        area = main.tetris.parse()
        self.objects.clear()
        for i in range(len(area)):
            for j in range(len(area[0])):
                if area[i][j]:
                    obj = Object(main.resolution, j * k, i * k, k, k)
                    obj.set_color((255, 0, 0))
                    obj.border = 1
                    obj.border_color = (255, 255, 255)
                    self.add_objects(obj)

    def on_key_down(self, key):
        self.main.tetris.on_key(key)
