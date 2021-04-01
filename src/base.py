#! /usr/bin/pydoc3
import threading
from .exception_ext import (
        ReadonlyException,
        )


class base(object):
    __NAME = "comm"
    def __init__(self, host, port = 8055, authkey = b"violas bridge communication", **kwargs):
        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.authkey = authkey
        self.working = False
        self.logger = kwargs.get("logger")
        self.kwargs = kwargs
        self.__name = kwargs.get("name", self.__NAME)
        self.show_msg(f"start communication host = {self.host} port = {self.port}")
        

    def __del__(self):
        self.show_msg("close")

    def name(self):
        return self.__name

    class work_thread(threading.Thread):
        def __init__(self, call, parse_msg, **kwargs):
            threading.Thread.__init__(self)
            self.__kwargs = kwargs
            self.__call = call
            self.__parse_msg = parse_msg

        def run(self):
            self.__call(self.__parse_msg, **self.__kwargs)

    @property
    def can_read_write(self):
        return ("working", "listener", "conn", "call")

    
    def can_write(self, name):
        if name not in self.__dict__ or name in self.can_read_write:
            return True
        return False

    def __setattr__(self, name, value):
        if not self.can_write(name):
            raise ReadonlyException(name)
        else:
            object.__setattr__(self, name, value)

    def rmproperty(self, name):
        if name in self.__dict__:
            del self.__dict__[name]

    def is_working(self):
        return self.working

    def work_stop(self):
        self.working = False

    def show_msg(self, msg):
        if self.logger:
            self.logger.debug(msg)
        else:
            print(msg)
        
    def call(self, cmd, conn = None, listener = None, **kwargs):
        pass


