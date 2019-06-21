import socket
import sys
import argparse
import threading

#host = input("Enter IP Host: ")
#port = int(input("Enter Port#: "))

def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            print(str(data.decode("utf-8")))
        except:
            print("You have been disconnected from the server")
            signal = False
            break


parser = argparse.ArgumentParser()
parser.add_argument("Host_Name")
parser.add_argument("PortNumber", nargs = '?' , type = int, default = 8080)
parser.add_argument("filename" , nargs = '?', default = "index.html")
args = parser.parse_args()

#host = socket.gethostname()
host = args.Host_Name
port = args.PortNumber
print("hostname is ", host)
print("port is ", port)


try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((host,port))
    try:
        print(args.filename)
        serverSocket.sendall(str.encode(args.filename))
    except:
        print("could not send filename")

        serverSocket.close()    
   # print (serverSocket.recv(1024))
except:
    print("Sorry could not connect")
    input("Press enter to quit")
    sys.exit(0)

receiveThread = threading.Thread(target = receive, args = (serverSocket, True))
receiveThread.start()

#while True:
#    message = args.filename
#    serverSocket.sendall(bytes(message))

#serverSocket.close()