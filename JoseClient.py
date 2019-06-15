
import socket as sk
import argparse
import time

class web_client:
    def __init__(self, serverName, serverPort, fileName):
        self.server_name = serverName
        self.server_port = serverPort
        self.fileName = fileName

    def run(self):
        # create a client socket
        clientSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        # connect client socket
        clientSocket.connect((self.server_name, self.server_port))
        try:
            msg = "GET /" + self.fileName + " HTTP/1.1\r\n\r\n" # create msg using filename provided
            send_time = time.time()# used for rtt time calculation
            clientSocket.sendall(bytes(msg, "UTF-8")) # send msg
            print("From Server: ", clientSocket.recv(4096))
            recv_time = time.time() # used for rtt time calculation
            print("rtt:",recv_time - send_time, "\nHost Name: ", self.server_name)
            print("Server Port Number: ", self.server_port, "\nPeer Name: ",clientSocket.getpeername())
            print("Socket Family: ", clientSocket.family,"\nTimeout: ", clientSocket.gettimeout())
            print("Socket Type: ", str(clientSocket.type)[11:])
            clientSocket.close() # close socket
        except IOError:
            clientSocket.close() # close socket

# take arguments through terminal
parser = argparse.ArgumentParser()
parser.add_argument("server_name") # ip address and/or localhost
parser.add_argument("server_port", nargs="?", type=int, default=8080)
parser.add_argument("file_name", nargs="?", default="index.html")
args = parser.parse_args()
client = web_client(args.server_name, args.server_port, args.file_name)
client.run()
