#! /usr/bin/pydoc3
from multiprocessing.connection import (
        Client,
        Listener,
        wait,
        )

from .base import (
        base,
        )

name = "multi_server"

class server(base):
    def __init__(self, host, port = 8055, authkey = b"violas bridge communication", **kwargs):
        base.__init__(self, host, port, authkey, **kwargs)
        self.__listen_thread = None
        self.listener = Listener(self.address, authkey = self.authkey)

    def __del__(self):
        self.work_stop()
        if self.listend:
            self.listener.close()

        self.listen_thread.join()

    def listend(self):
        return self.listener and not self.listener.closed

    def parse_msg(self, cmd, conn, listener):
        if cmd == "disconnect":
            if not conn.closed:
                conn.close()
        elif cmd == "shutdown":
            if not conn.closed:
                conn.close()
            if self.listend:
                self.listener.close()
            self.work_stop()
        else:
            conn.send(f"{cmd} is invalid")
            return False
        return True
        
    def work(self, call, **kwargs):
        self.working = self.listend
        while self.is_working():
            with self.listener.accept() as conn:
                  self.show_msg('connection accepted from {}'.format(self.listener.last_accepted))
                  while not conn.closed:
                      try:
                        cmd = conn.recv()
                        ret = call(cmd, conn = conn, listener = self.listener, **kwargs)
                        if not ret:
                            self.parse_msg(cmd, conn, self.listener)
                      except Exception as e:
                          self.show_msg(f"connect error: {e}")
                          break

    
    def start(self, call):
        if self.is_working():
            self.stop()
            self.listen_thread.join()
        self.listen_thread = self.work_thread(self.work, call, **self.kwargs)
        self.listen_thread.start()
        self.listen_thread.join()

    def stop(self):
        self.work_stop()
        if self.listend:
            self.listener.close()

