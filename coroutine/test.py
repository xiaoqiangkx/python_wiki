#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: xiaoqiangkx
@file: test.py
@time: 2016/9/22 21:01
@change_time: 
1.2016/9/22 21:01
"""

# -*- coding:utf-8 -*-

import functools
import types
import sys
from copy import copy
import itertools

class Future(object):
	STATE_INIT = 0
	STATE_READY= 1
	STATE_DONE = 2

	instances = {}
	counter = itertools.count()

	@staticmethod
	def next_id():
		return Future.counter.next()

	def __init__(self):
		self.id = Future.next_id()
		Future.instances[self.id] = self
		self.on_result_callback = None
		self.result = None
		self.state = Future.STATE_INIT
		self.exc_info = None

	@staticmethod
	def get_future(future_id):
		future_id = long(future_id)
		return Future.instances.get(future_id)

	@staticmethod
	def run(logger=None):
		for future_id, future in copy(Future.instances).iteritems():
			if future.state == Future.STATE_READY:
				future.on_result()
			elif future.state == Future.STATE_DONE:
				Future.instances.pop(future_id, None)

			if future.exc_info:
				Future.instances.pop(future_id, None)
				if logger:
					logger.error('Exception in Future: %r', future.exc_info)

	def get_id(self):
		return self.id

	def set_result(self, result):
		self.result = result
		self.state = Future.STATE_READY

	def set_on_result_callback(self, callback):
		self.on_result_callback = callback

	def on_result(self):
		if self.on_result_callback:
			self.on_result_callback(self.result)
			self.on_result_callback = None
		self.state = Future.STATE_DONE

	def set_exc_info(self, info):
		self.exc_info = info

	def get_exc_info(self, info):
		return self.exc_info

class Return(Exception):

	def __init__(self, value=None):
		self.value = value

def _co_run(co, future, result):
	if isinstance(result, Future):
		result.set_on_result_callback(lambda r: _co_run(co, future, r))
		return
	try:
		yielded = co.send(result)
	except StopIteration:
		future.set_result(None)
	except Return as e:
		future.set_result(e.value)
	except:
		future.set_exc_info(sys.exc_info())
	else:
		_co_run(co, future, yielded)

def async(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		future = Future()
		co = func(*args, **kwargs)
		if isinstance(co, types.GeneratorType):
			# 是一个generator，启动它
			_co_run(co, future, None)
		else:
			# 不是generator，不能使用async
			raise Exception('%r is not a generator function' % func)
		return future
	return wrapper

################################ test #############################################
def test():
	events = {}
	cur_time = [0]

	def delay(n, f):
		events[cur_time[0]+n] = f

	@async
	def rename(aid, name):
		print "rename start"
		mb = yield get_mb(aid)
		print "mb ", mb, "rename to", name
		mb2 = yield get_mb(aid)
		print "mb2", mb2
		raise Return('mb ' + name)

	@async
	def rename2(aid, name):
		print "rename2 start"
		x = yield rename(aid, name+'_1')
		print "rename2 mid", x
		y = yield rename(aid, name+'_2')
		print "rename2 end", y

	def get_mb(aid):
		future = Future()
		delay(5, lambda: on_get_mb(future.id, aid))
		return future

	def on_get_mb(future_id, aid):
		future = Future.get_future(future_id)
		print "get mailbox of ", aid, future
		future.set_result("mailbox")

	def run_test():
		for i in xrange(1000):
			if i == 0:
				delay(1, lambda: rename2(100, 'newname'))
			event = events.get(cur_time[0])
			if event:
				print "cur_time", cur_time[0], "event", event
				event_result = event()
				print "event_result",  event_result
			cur_time[0] += 1
			Future.run()
			# print "cur_time", cur_time[0]

	run_test()


if __name__ == '__main__':
	test()