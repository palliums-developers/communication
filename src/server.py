#! /usr/bin/pydoc3
from multiprocessing.connection import (
        Client,
        Listener,
        wait,
        )

from src.base import (
        base,
        )

name = "multi_server"

class server(base):
    def __init__(self, host, port = 8055, authkey = b"violas bridge communication"):
        base.__init__(self, host, port, authkey)
        self.__listen_thread = None
        self.listener = Listener(self.address, authkey = self.authkey)

    def __del__(self):
        if self.listend:
            self.listener.close()

        self.listen_thread.join()

    def listend(self):
        return self.listend and not self.listener.closed

    def parse_msg(self, cmd, conn, listener):
        if cmd == "disconnect":
            if not conn.closed:
                conn.close()
            return True
        elif cmd == "shutdown":
            if not conn.closed:
                conn.close()
            if self.listend:
                self.listener.close()
            self.close()
            return True
        return False 
        
    def work(self, call, **kwargs):
        try:
            self.working = self.listend
            while self.is_working():
                with self.listener.accept() as conn:
                      print('connection accepted from', self.listener.last_accepted)
                      while not conn.closed:
                          try:
                            cmd = conn.recv()
                            ret = call(cmd, conn = conn, listener = self.listener)
                            if not ret:
                                self.parse_msg(cmd, conn, self.listener)
                          except Exception as e:
                              print(f"connect error: {e}")
                              break
        except Exception as e:
            parse_except(e)
    
    def start_listen(self, call, **kwargs):
        self.listen_thread = self.work_thread(self.work, call, **kwargs)
        
        self.listen_thread.start()

    def close(self):
        self.stop_work()


