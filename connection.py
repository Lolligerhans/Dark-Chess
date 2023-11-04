import socket
import threading
import time

# TODO
# your partner's IP address
ipPartner = "192.168.2.100"

def getCommObj(color):
    #create comminucator basaed on color and return
    1

class FuncThread:
    def __init__(self, function, args = None):
        self.f = function
        self.args = args
    def run(self):
        if args is not None:
            self.f(self.args)
        else:
            self.f()

class Communicator:
    def __init__(self, lPort, sPort, callback):
        self.sPort = sPort
        self.lPort = lPort
        self.cb = cb

        # socket startup
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', self.lPort))
            s.listen()
            conn, address = s.accept()
            self.connectionSocket = conn
            print('Connected by', address)

        seld.start_recv_moves()


    def send(self, data):
        conn.sendall( data.encode('ASCII'))

    def recv(self):
        while 1:
            data = conn.recv(1024)
            if not data:
                break
            self.cb(data)

    def start_recv(self):
        t = FuncThread(self.recv_moves)
        t.start()

    def start_send(self, data):
        t = FuncThread(self.send_move, move)
        t.start()

    def close_connection(self):
        start_send('')







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
        # print("finishing receiving thread")

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
