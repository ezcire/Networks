import socket
import sys
import argparse
import threading

def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            print(str(data.decode("utf-8")))
            q = str(data.decode("utf-8"))
            if q == 'q':
                print("disconnet\n")
                serverSocket.close()
                signal = False
                break
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
except:
    print("Sorry could not connect")
    input("Press enter to quit")
    sys.exit(0)

receive_thread = threading.Thread(target = receive, args = (serverSocket, True))
receive_thread.start()

while True:
    print("Enter filename\nPress q to quit")
    message = input()
    if message == 'q':
        serverSocket.sendall(str.encode(message))
        input("Press enter to quit")
        serverSocket.close()
        break
    serverSocket.sendall(str.encode(message))
