import socket
import sys

#host = input("Enter IP Host: ")
#port = int(input("Enter Port#: "))

host = '169.254.29.2'
port = 8889

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((host,port))

except:
    print("Sorry could not connect")
    sys.exit(0)



print (serverSocket.recv(1024))
serverSocket.close()