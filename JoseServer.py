import argparse
import socket as sk
from multiprocessing.dummy import Pool as ThreadPool 


class multithreaded_server:
    def __init__(self, serverPort):
        self.port = serverPort
        
    def run(self):
        # Prepare a server socket
        serverSocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        serverSocket.bind(('localhost', self.port))
        serverSocket.listen(1)
        pool = ThreadPool(4) # Create pool of "workers" for multithreading
        
        while True:
            #Establish the connection
            print ('Ready to serve...')
            (connectionSocket, addr) = serverSocket.accept()
            pool.map(self.new_thread, [connectionSocket]) # create a new thread for each connection socket. 
        pool.close() # properly close all threads
        pool.join()  # properly close all thread continued
        # Close server socket
        serverSocket.close()

    def new_thread(self, connectionSocket):
        try:
            print("Client Port Number: ", connectionSocket.getpeername()[1])
            print("Peer Name: ", connectionSocket.getpeername())
            conn_family = str(connectionSocket.family)
            print("Socket Family: ", conn_family[conn_family.find(".")+1:])
            print("Timeout: ", connectionSocket.gettimeout())
            conn_type = str(connectionSocket.type)
            print("Socket Type: ", conn_type[conn_type.find(".")+1:])
            print("Protocol: IPPROTO_TCP")
            message = connectionSocket.recv(1024)
            print("msg is ", message)
            filename = message.split()[1]
            print("filename is ", filename)
            f = open(filename[1:])
            # store the entire content of the requested file
            outputdata = f.read()
            # Send one HTTP header line into socket
            connectionSocket.sendall(bytes("HTTP/1.1 200 OK\r\n\r\n", "UTF-8"))
            # Send the content of the requested file to the client
            connectionSocket.sendall(bytes(outputdata, "UTF-8"))          
            connectionSocket.close()
        except IOError:
            #Send response message for file not found
            connectionSocket.sendall(bytes("HTTP/1.1 404 Not Found\r\n\r\n", "UTF-8"))
            # for browser output
            connectionSocket.sendall(bytes("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n", "UTF-8"))
            #Close client socket
            connectionSocket.close()

# take arguments through terminal 
parser = argparse.ArgumentParser()
parser.add_argument("serverPort", nargs='?', type=int, default=8080)
args = parser.parse_args()
mt_server = multithreaded_server(args.serverPort)
mt_server.run()
