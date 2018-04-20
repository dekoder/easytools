#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gevent
from gevent import monkey
monkey.patch_all()
from gevent.queue import PriorityQueue

class Muiti(object):
    """
    :l: [(arg1, arg2), (arg1, arg2), ...]
    :func: callee function
    :num: coroutine number
    """
    def __init__(self, l, func, num=20):
        self.queue = PriorityQueue()
        for item in l:
            self.queue.put(item)
        self.num = num
        self.func = func
        self.stop = False
        self.results = PriorityQueue()

    def _do(self):
        while not self.stop:
            try:
                item = self.queue.get_nowait()
            except Exception as e:
                self.stop = True
                continue

            value = None
            if type(item) == tuple:
                value = self.func(*item)
            else:
                value = self.func(item)

            self.results.put(value)

    def get_result(self):
        return list(self.results.queue)
        
    def start(self):
        threads = [gevent.spawn(self._do) for i in range(self.num)]
        gevent.joinall(threads)

    def terminate(self):
        self.stop = True

def test():
    def func(i):
        return i+1

    muiti = Muiti([1,2,3], func, 10)
    muiti.start()
    print(muiti.get_result())

if __name__ == "__main__":
    test()