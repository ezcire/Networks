import socket
import sys
import argparse

#host = input("Enter IP Host: ")
#port = int(input("Enter Port#: "))

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
    print (serverSocket.recv(1024))
    

except:
    print("Sorry could not connect")
    sys.exit(0)



serverSocket.close()