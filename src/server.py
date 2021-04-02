#! /usr/bin/pydoc3
from multiprocessing.connection import (
        Client,
        Listener,
        wait,
        )

from .base import (
        base,
        )

from .client import (
        client
        )
name = "multi_server"

class server(base):
    def __init__(self, host, port = 8055, authkey = b"violas bridge communication", **kwargs):
        base.__init__(self, host, port, authkey, **kwargs)
        self.__listen_thread = None
        self.listener = Listener(self.address, authkey = self.authkey, backlog = 3)

    def __del__(self):
        self.work_stop()
        if self.listend:
            self.listener.close()

    @property
    def listend(self):
        return self.listener is not None

    def parse_msg(self, cmd, conn, listener, call, **kwargs):

        state = call(cmd, conn = conn, listener = self.listener, **kwargs) if call else False
        if state : return True

        if cmd == "disconnect":
            if not conn.closed:
                conn.close()
        elif cmd in ("__shutdown__"):
            self.work_stop()
        else:
            #conn.send(f"{cmd} is invalid")
            return False
        return True
        
    def work(self, call, **kwargs):
        self.working = self.listend
        while self.is_working():
            with self.listener.accept() as conn:
                try:
                     while not conn.closed:
                        cmd = conn.recv()
                        self.parse_msg(cmd, conn, self.listener, call = call, **kwargs)

                        if not self.is_working() or cmd in ("shutdown"):
                            self.show_msg(f"stop {self.name()} thread")
                            return
                except Exception as e:
                     self.show_msg(f"connect error: {e}")
                print(self.is_working())
    
    def start(self, call):
        if self.is_working():
            self.stop()
            self.listen_thread.join()
        self.listen_thread = self.work_thread(self.work, call, **self.kwargs)
        self.listen_thread.start()
        self.listen_thread.join()

    def stop(self):
        try:
            if self.listend and self.is_working():
                client(self.host, self.port, self.authkey, logger = self.logger).send("__shutdown__")
        except Exception as e:
            pass

