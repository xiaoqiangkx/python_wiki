# -*- coding: utf-8 -*-
import time
import traceback


class KeyEvent(object):
    KEY_UP = 1
    KEY_DOWN = 2
    KEY_LEFT = 3
    KEY_RIGHT = 4
    KEY_LIST = [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]

    SLEEP_TIME = 5      # 休眠5s钟

    def __init__(self):
        self.key_pressed_dict = {}

    def set_key(self, key, flag):
        """
        翻转key_pressed_list
        :param key:
        :return:
        """
        if flag:
            value = time.time()
        else:
            value = 0
        self.key_pressed_dict[key] = value

    def update_keys(self):
        """
        更新所有的keys
        :return:
        """
        import random
        import time
        while True:
            for key in KeyEvent.KEY_LIST:
                flip_flag = (random.randint(0, 1) == 1)
                self.set_key(key, flip_flag)
            time.sleep(KeyEvent.SLEEP_TIME)

    def get_key_list(self):
        key_list = []
        for key, value in self.key_pressed_dict.iteritems():
            if value != 0:
                key_list.append(key)

        # 处理同时按上下和左右的问题
        try:
            if KeyEvent.KEY_DOWN in key_list and KeyEvent.KEY_UP in key_list:
                if self.key_pressed_dict.get(KeyEvent.KEY_DOWN) < self.key_pressed_dict.get(KeyEvent.KEY_UP):
                    key_list.remove(KeyEvent.KEY_UP)
                else:
                    key_list.remove(KeyEvent.KEY_DOWN)

            if KeyEvent.KEY_LEFT in key_list and KeyEvent.KEY_RIGHT in key_list:
                if self.key_pressed_dict.get(KeyEvent.KEY_LEFT) < self.key_pressed_dict.get(KeyEvent.KEY_RIGHT):
                    key_list.remove(KeyEvent.KEY_RIGHT)
                else:
                    key_list.remove(KeyEvent.KEY_LEFT)
        except KeyError, e:
            print e
            traceback.print_exc()
            return None

        return key_list





