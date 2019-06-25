import socket
import sys
import argparse
import threading
import http.client

parser = argparse.ArgumentParser()
parser.add_argument("Host_Name")
parser.add_argument("PortNumber", nargs = '?' , type = int, default = 8080)
parser.add_argument("filename" , nargs = '?', default = "index.html")
args = parser.parse_args()

host = args.Host_Name
port = args.PortNumber

def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(4096)
            print('Hostname\t\t: ', socket.getpeername())
            print('Socket family\t\t: ', serverSocket.family) 
            print('Socket protocol\t\t: ', serverSocket.proto)
            print('Socket timeout\t\t: ', serverSocket.gettimeout())
            print('Socket type\t\t: ', serverSocket.type)
            print(data)
            serverSocket.close()  
            signal = False                
        except:
            print("You have been disconnected from the server")
            socket.close()
            signal = False
            break

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((host,port))
    try:
        send_file = "GET /" + args.filename + " HTTP/1.1\r\n\r\n"    
        serverSocket.send(str.encode(send_file))
        
    except IOError:
        print("could not send filename")
        serverSocket.close()
                
except:
    print("Sorry could not connect")
    input("Press enter to quit")
    sys.exit(0)
   

receive_thread = threading.Thread(target = receive, args = (serverSocket, True))
receive_thread.start()

    