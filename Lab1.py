#import socket module
import socket
import os
import sys
from socket import *
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Prepare a sever socket
#Fill in start
host = input("Enter IP Host: ")
port = int(input("Enter Port#: "))

serverSocket.bind((host,port))
serverSocket.listen(5)

serverSocket.close()