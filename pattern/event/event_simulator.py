# -*- coding: utf-8 -*-

from key_event import KeyEvent

class EventSimulator(object):

    def __init__(self):
        self.key_event = KeyEvent()

    def simulate_keys(self):
        self.key_event.update_keys()

    def start_simulate(self):
        """
            开启模拟事件
        """
        import thread
        thread.start_new_thread(self.simulate_keys, ())

    def get_key_event(self):
        return self.key_event

