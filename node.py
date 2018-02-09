from db import DB
import gossip_pb2
import argparse
import socketserver
import socket
import struct
from tcp_client import TcpClient
from threading import Thread
import time

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--port', type=int, help="listening port")
args = parser.parse_args()
print("arguments: " + str(args))

peers = {}

def add_peer(ip, port):
    global peers
    if (ip, port) not in peers:
        print("adding peer %s:%s" % (ip, port))
        peer = TcpClient(ip, port)
        peers[(ip, port)] = peer
        return peer
    else:
        return peers[(ip, port)]

class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        n_str = self.request.recv(4)
        if n_str is None:
            return
        n = socket.ntohl(struct.unpack('I', n_str)[0])
        bs = self.recv_n(n)
        req = gossip_pb2.Request()
        req.ParseFromString(bs)
        if req.HasField("add_build_request"):
            db.insert_build(req.add_build_request)
        elif req.HasField("registration_request"):
            ip = req.registration_request.ip
            port = req.registration_request.port
            add_peer(ip, port)

    def recv_n(self, n):
        buf = b''
        while n > 0:
            temp = self.request.recv(n)
            if len(temp) == 0:
                print("ERROR: socket.recv returns zero bytes")
                return None
            else:
                buf += temp
                n -= len(temp)
        return buf

server = socketserver.TCPServer(("0.0.0.0", args.port), MyHandler)
thr = Thread(target=server.serve_forever)
thr.start()

db = DB("db")
pool = DB("pool")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
my_host = s.getsockname()[0]

nodelist = open("nodelist.txt", "r").read()
for entry in nodelist.split():
    ip, port = entry.split(":")
    port = int(port)
    if ip == my_host and port == args.port:
        continue
    peer = add_peer(ip, port)
    req = gossip_pb2.Request()
    req.registration_request.ip = my_host
    req.registration_request.port = args.port
    peer.send(req.SerializeToString())

def broadcast(build, peer):
    req = gossip_pb2.Request()
    req.add_build_request = build
    peer.send(req.SerializeToString())

while True:
    for peer in peers:
        for build in pool.get_all_builds():
            broadcast(build, peer)
            db.insert_build(build)
            pool.delete_build(build)
    time.sleep(1)
