import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#host = input("Enter IP Host: ")
#port = int(input("Enter Port#: "))

host = '169.254.29.2'
port = 8889


serverSocket.bind((host,port))
serverSocket.listen(5)


while True:
    print("Ready to serve...")
    connectionSocket, addr = serverSocket.accept()
    connectionSocket.send(b'Connect successful')
serverSocket.close()