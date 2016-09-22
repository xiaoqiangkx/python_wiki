# -*- coding: utf-8 -*-


class Command(object):
    """
    命令基类
    """
    def __init__(self):
        pass

    def execute(self, entity):
        pass

    def undo(self, entity):
        pass


class JumpCommand(object):
    """
    跳跃命令
    """
    def __init__(self):
        pass

    def execute(self, entity):
        entity.jump()

    def undo(self, entity):
        entity.undo()


class InputHandler(object):
    """
    输入handler
    """
    def __init__(self):
        pass

    def handler_input(self, key_list):
        from event.key_event import KeyEvent
        commands = []
        for key in key_list:
            if key == KeyEvent.KEY_UP:
                commands.append((JumpCommand(), "execute"))
            elif key == KeyEvent.KEY_DOWN:
                commands.append((JumpCommand(), "undo"))

        return commands


if __name__ == '__main__':
    # EventSimulator模拟所有的事件
    from event.event_simulator import EventSimulator
    from entity.player import Player

    event_simulator = EventSimulator()
    event_simulator.start_simulate()
    key_event = event_simulator.get_key_event()
    player = Player()

    input_handler = InputHandler()
    import time
    while True:
        key_list = key_event.get_key_list()
        print "key_list:", key_list
        time.sleep(2)

        commands = input_handler.handler_input(key_list)
        for command, func in commands:
            getattr(command, func)(player)

        print player.get_position()
