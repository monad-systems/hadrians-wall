import socket
import struct

class TcpClient(object):
    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.settimeout(10.0)
        self.socket.connect((ip, port))

    def send(self, msg):
        self.socket.sendall(struct.pack('I', socket.htonl(len(msg))) + msg)

    def recv(self) -> str:
        n_str = self.recv_n(4)
        if n_str is None:
            return None
        n = socket.ntohl(struct.unpack('I', n_str)[0])
        return self.recv_n(n)

    def recv_n(self, n):
        buf = b''
        while n > 0:
            temp = self.socket.recv(n)
            if len(temp) == 0:
                print("ERROR: socket.recv returns zero bytes")
                self.socket.close()
                return None
            else:
                buf += temp
                n -= len(temp)
        return buf

    def close(self):
        self.socket.close()
