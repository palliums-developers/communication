#! /usr/bin/pydoc3
import time
from multiprocessing.connection import (
        Client,
        Listener,
        wait,
        )

from array import array
from .base import (
        base,
        )

name = "multi_client"

class client(base):
    def __init__(self, host, port = 8055, authkey = b"violas bridge communication", call = None, **kwargs):
        base.__init__(self, host, port, authkey, **kwargs)
        self.conn = Client(self.address, authkey = self.authkey)
        self.__recved = False
        if call:
            self.start(call, **kwargs)

    def __del__(self):
        if self.is_working():
            self.recv_thread.join()

    @property
    def connected(self):
        return self.conn and not self.conn.closed

    def work(self, call, **kwargs):
        try:
            while self.is_working() and self.connected:
                had_data = self.conn.poll(1)
                if had_data and self.connected:
                    self.__recved = True
                    cmd = self.conn.recv()
                    call(cmd, conn = self.conn)
        except Exception as e:
            print(e)

    def start(self, call):
        self.working = self.connected
        self.recv_thread = self.work_thread(self.work, call, **self.kwargs)
        self.recv_thread.start()

    def send(self, cmd):
        if self.connected:
            self.__recved = False
            self.conn.send(cmd)
        else:
            raise Exception(f"not connect to server(self.address)")

    def close(self):
        loop = 0
        while not self.__recved and loop < 10:
            loop += 1
            time.sleep(0.5)

        self.work_stop()
        if self.connected:
            self.conn.close()
