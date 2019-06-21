import socket
import argparse
import threading
import requests
import sys

#get input from terminal as parse 
#if no PORT input, set to default 8080
parser = argparse.ArgumentParser()
parser.add_argument("PortNumber", nargs = '?' , type = int, default = 8080)

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
        return str(self.id) + " " + str(self.address)

    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
                q = str(data.decode("utf-8"))
                if q == 'q':
                    print("Client " + str(self.address) + " has disconnected")
                    self.signal = False
                    connections_array.remove(self)
                    break
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections_array.remove(self)
                #self.socket.close()
                break
            if data != "":
                #open file
                try:
                    print("ID " + str(self.id) + ": ")
                    filename = str(data.decode("utf-8"))
                    print("filename is ",filename)
                    f = open(filename, "r")
                    print(f.read())
                    print("\n\n")
                    f.close()  
                    #response = requests.get(filename)
                    #print(response.status_code)
                    print("Ready to serve..")
                    
                except IOError:
                    print("404 oops could not read file")
                    print("\n\n")
                    print("Ready to serve..")
                        
            for client in connections_array:
                    if client.id != self.id: 
                        client.socket.sendall(data)
                         
                            

def new_connection(socket):
    while True:
        print("Ready to serve..")
        connectionSocket, addr = socket.accept()
        global connections_length
        connections_array.append(add_client(connectionSocket, addr, connections_length, "Name", True))
        connections_array[len(connections_array) - 1].start()
        print("New client " + str(connections_array[len(connections_array) - 1]))
        connections_length += 1 
    connectionSocket.close()
def main():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    getPort = parser.parse_args()
    port = getPort.PortNumber
   #print("port is ", port) #print for me to see
    serverSocket.bind(("localhost",port))
    serverSocket.listen(1)

    add_new_thread = threading.Thread(target = new_connection, args = (serverSocket,))
    add_new_thread.start()
main()   


