import socket
import threading
import time

# TODO
# your partner's IP address
ipPartner = "127.0.0.69"


########################################################################################################################
# receiver
class RecvThread(threading.Thread):
    def __init__(self, port, callback):
        threading.Thread.__init__(self)
        self.port = port
        self.callback = callback
    def run(self):
        print("starting receiver thread on port", self.port)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', self.port))
        while 1:
            data, addr = s.recvfrom(1024)  # 7 bytes needed (4 numbers, 3 blanks)
            self.callback(data)
        print("finishing receiving thread",)

class SendThread(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip, self.port = ip, port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def set_move(self, origin, target):
        self.origin = origin
        self.target = target

    def run(self):
        print("starting sending thread")
        origin = self.origin
        target = self.target
        data = bytearray(str(origin[0]) + " " + str(origin[1]) + " " + str(target[0]) + " " + str(target[1]), "ascii")
        self.s.sendto(data, (self.ip, self.port))
        print("finishing sending thread")
