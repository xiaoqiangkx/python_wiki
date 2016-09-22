#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: xiaoqiangkx
@license: xx
@contact: xiaoqiangkx@163.com
@site: http://www.xx.com
@software: PyCharm Community Edition
@file: schedule.py.py
@time: 2016/1/10 19:11
@change_time: 
    1.2016/1/10 19:11
"""


def schedule_op():
    from Queue import Queue

    class Task(object):
        task_id = 0

        def __init__(self, target):
            Task.task_id += 1
            self.tid = Task.task_id
            self.target = target
            self.sendval = None

        def run(self):
            return self.target.send(self.sendval)

    class SystemCall(object):
        def handle(self):
            pass

    class GetTid(SystemCall):
        def handle(self):
            self.task.sendval = self.task.tid
            self.schedule.schedule(self.task)

    class NewTask(SystemCall):
        def __init__(self, target):
            self.target = target

        def handle(self):
            tid = self.schedule.new(self.target)
            self.task.sendval = tid
            self.schedule.schedule(self.task)

    class WaitTask(SystemCall):
        def __init__(self, tid):
            self.tid = tid

        def handle(self):
            result = self.schedule.wait_for_exit(self.task, self.tid)
            self.task.sendval = result
            if not result:
                self.schedule.schedule(self.task)

    class Scheduler(object):
        def __init__(self):
            from collections import defaultdict
            self.task_map = {}
            self.ready = Queue()    # task_map会插入数据，所以遍历ready来执行操作
            self.exit_waiting = defaultdict(lambda: [])

        def new(self, target):
            new_task = Task(target)
            self.task_map[new_task.task_id] = new_task
            self.schedule(new_task)
            return new_task.task_id

        def wait_for_exit(self, task, wait_id):
            if wait_id in self.task_map:
                self.exit_waiting[wait_id].append(task)
                return True
            else:
                return False

        def schedule(self, task):
            self.ready.put(task)

        def exit(self, task_id):
            if task_id in self.task_map:
                del self.task_map[task_id]
                print "finish task_id:", task_id

            for task in self.exit_waiting[task_id]:
                self.schedule(task)

        def main_loop(self):
            while self.task_map:
                task = self.ready.get()
                try:
                    result = task.run()
                    if isinstance(result, SystemCall):
                        result.task = task
                        result.schedule = self
                        result.handle()
                        continue
                except StopIteration:
                    self.exit(task.task_id)
                    continue
                self.schedule(task)

    def foo():
        mytid = yield GetTid()
        for i in xrange(10):
            print "I'm foo", mytid
            yield

    def main():
        child = yield NewTask(foo())
        print "Waiting for child"
        yield WaitTask(child)
        print "child done"

    # sched = Scheduler()
    # sched.new(main())
    # sched.main_loop()

    def handle_client(client, addr):
         print "Connection from", addr

         while True:
            data = client.recv(65536)
            if not data:
                break
            client.send(data)
            client.close()
            print "Client closed"
            yield   # Make the function a generator/coroutine

    def server(port):
        import socket
        print "Server starting"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", port))
        sock.listen(5)
        while True:
            client, addr = sock.accept()
            yield NewTask(handle_client(client, addr))

    def alive():
        while True:
            print "I'm alive!"
            yield

    sched = Scheduler()
    sched.new(alive())
    sched.new(server(9000))
    sched.main_loop()


if __name__ == '__main__':
    schedule_op()