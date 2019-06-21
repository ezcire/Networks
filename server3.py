import socket
import argparse
import threading

#get input from terminal as parse 
#if no PORT input, set to default 8080
parser = argparse.ArgumentParser()
parser.add_argument("PortNumber", nargs = '?' , type = int, default = 8080)

connections_array = []  #store clients in arrays
connections_length = 0

#multithread each client
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

    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
                print("actual data is", data)
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections_array.remove(self)
                break
            if data != "":
                print("ID " + str(self.id) + ": Filename :\t" + str(data.decode("utf-8")))
                #open file
                try:
                    filename = str(data.decode("utf-8"))
                    print("filename is ",filename)
                    f = open(filename, "r")
                    print(f.read())
                   
                except:
                    print("oops")    
            for client in connections_array:
                    if client.id != self.id: 
                        client.socket.sendall(data) 
                            

def new_connection(socket):
    while True:
        print("Ready to serve..")
        connectionSocket, addr = socket.accept()
        global connections_length
        
    
        connections_array.append(Client(connectionSocket, addr, connections_length, "Name", True))
        connections_array[len(connections_array) - 1].start()
        print("New connection at ID " + str(connections_array[len(connections_array) - 1]))
        connections_length += 1 
       #connectionSocket.send(bytes("Connected " + str(connectionSocket.getpeername()), "UTF-8"))
        


#serverSocket.close()

def main():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    getPort = parser.parse_args()
    port = getPort.PortNumber
    print("port is ", port) #print for me to see
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




