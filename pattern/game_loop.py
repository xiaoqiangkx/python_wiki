# -*- coding: utf-8 -*-
import time
import random


class Game(object):
    def __init__(self):
        pass

    def process_input(self):
        rand_time = float(random.randint(1, 6))
        time.sleep(rand_time/10.0)

    def update(self):
        """
        entity等移动根据elapsed来更新
        """
        print "update status"

    def render(self):
        rand_time = float(random.randint(1, 10))
        time.sleep(rand_time/10.0)

    def run(self, fps):
        """
        FPS: 循环的速度；由程序程序复杂度以及硬件共同决定；只要循环代码在1/FPS时间内完成，帧率固定。
        :return:
        """
        last_time = time.time()
        lag = 0.0
        while True:
            current_time = time.time()
            elapsed = current_time - last_time
            lag += elapsed  # 积累的时间
            last_time = current_time

            self.process_input()    # 处理输入

            while lag >= 1.0 / fps:
                self.update()   # 当运行了一帧时间时，开始更新
                lag -= 1.0 / fps

            self.render()

if __name__ == '__main__':
    game = Game()
    FPS = 1
    game.run(FPS)