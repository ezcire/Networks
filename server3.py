import socket
import argparse
import threading

connections_array = []
connections_length = 0

parser = argparse.ArgumentParser()
parser.add_argument("PortNumber", nargs = '?' , type = int, default = 8080)

class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal  
    def __str__(self):
        return str(self.id) + " " + str(self.address)

def new_connection(socket):
    while True:
        print("Ready to serve..")
        connectionSocket, addr = socket.accept()
        global connections_length
        connections_array.append(Client(connectionSocket, addr, connections_length, "Name", True))
        connections_array[len(connections_array) - 1].start()
        print("New connection at ID " + str(connections_array[len(connections_array) - 1]))
        connections_length += 1 
        connectionSocket.send(bytes("Connected " + str(connectionSocket.getpeername()), "UTF-8"))

#serverSocket.close()

def main():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

 #host = input("Enter IP Host: ")
 #port = int(input("Enter Port#: "))

 #host = socket.gethostname()
    getPort = parser.parse_args()
    port = getPort.PortNumber
    print("port is ", port)
    serverSocket.bind(("localhost",port))
    serverSocket.listen(1)

    newConnectionsThread = threading.Thread(target = new_connection, args = (serverSocket,))
    newConnectionsThread.start()
main()   










#while True:
#    print("Ready to serve...")
#    connectionSocket, addr = serverSocket.accept()
    #connectionSocket.send(bytes('Connect successful', "UTF-8"))
    
#    connectionSocket.send(bytes("Connected " + str(connectionSocket.getpeername()), "UTF-8"))
#    print("Connected: ", connectionSocket.getpeername())




