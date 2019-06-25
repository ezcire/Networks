import socket
import argparse
import threading
import requests
import sys
import http.client
import os


#get input from terminal as parse 
#if no PORT input, set to default 8080
parser = argparse.ArgumentParser()
parser.add_argument("PortNumber", nargs = '?' , type = int, default = 8080)
args = parser.parse_args()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

getPort = parser.parse_args()
port = getPort.PortNumber
   #print("port is ", port) #print for me to see
serverSocket.bind(("localhost",port))
serverSocket.listen(5)

connections_array = []  #store clients in arrays
connections_length = 0

#multithread each client
class add_client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal 
        
    def __str__(self):
        return str(self.id) + " " + str(self.address) + " " + str(self.socket)

    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(1024)
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections_array.remove(self)
                break
            if data != "":
                #open file
                try:
                    message = data
                    fixed_filename = message.split()[1]
                    f = open(fixed_filename[1:]) 
                    out = f.read()
                   #send message back to client
                    self.socket.sendall(bytes("HTTP/1.1 200 OK\r\n\r\n", "UTF-8"))
                    self.socket.sendall(bytes(out, "UTF-8"))
                   #close the client and file 
                    f.close()    
                    self.socket.close()
    
                    
                except IOError:
                    self.socket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n", "utf-8"))
                    self.socket.close()

def new_connection(socket):
    while True:
        print("Ready to serve..")
        connectionSocket, addr = socket.accept()
        global connections_length
        connections_array.append(add_client(connectionSocket, addr, connections_length, "Name", True))
        connections_array[len(connections_array) - 1].start()
        print("New client " )#+ str(connections_array[len(connections_array) - 1]))
        connections_length += 1 
    

add_new_thread = threading.Thread(target = new_connection, args = (serverSocket,))
add_new_thread.start()

  
  


