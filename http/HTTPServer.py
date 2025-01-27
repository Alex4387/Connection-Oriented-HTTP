import sys
import socket
import threading
import time
from datetime import datetime

from HTTPResponse import Response
from HTTPRequest import Request
from RequestParser import RequestParser

from queue import Queue 

class HTTPServer:
    def __init__(self, serverHost, serverPort, buffSize=16*1024):
        self.SERVER_HOST = serverHost
        self.SERVER_PORT = serverPort
        self.BUFFER_SIZE = buffSize

        self.recvMQ = Queue()
        self.sendMQ = Queue()

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.SERVER_HOST, self.SERVER_PORT))

        self.clientConnectionPool = list()


    def run(self, maxClient=None):
        try:
            if not maxClient:
                self.serverSocket.listen()
            else:
                if type(maxClient) is not int:
                    raise Exception("Invalid maxClient value")
                
                self.serverSocket.listen(maxClient)

            print(f"Server is Listening on {self.SERVER_HOST}:{self.SERVER_PORT}")

            senderThread = threading.Thread(target=self.sendResponse)
            senderThread.daemon = True
            senderThread.start()

            EMGenerator = threading.Thread(target=self.defaultEMGenerator)
            EMGenerator.daemon = True
            EMGenerator.start()

            self.acceptConnection()

        except Exception as e:
            sys.exit()

    def acceptConnection(self):
        try:
            while True:
                clientSocket, addr = self.serverSocket.accept()
                print(f"Accepted connection from {addr[0]}:{addr[1]}")

                self.clientConnectionPool.append(clientSocket)

                clientThread = threading.Thread(target=self.recvRequest, args=(clientSocket, ))
                clientThread.daemon = True
                clientThread.start()
        finally:
            return
        
    def recvRequest(self, clientSocket):
        while True:
            data = clientSocket.recv(self.BUFFER_SIZE).decode("utf-8")

            if not data:
                print(clientSocket.getpeername(), "Client has closed the connection.")
                self.clientConnectionPool.remove(clientSocket)
                break

            req = RequestParser.toRequestObject(data)
            res = Response()

            isEM = self.requestHandle(req, res)
            
            if not isEM:
                self.sendMQ.put((clientSocket, res))
            
    def sendResponse(self):
        try:
            while True:
                messageInfo = self.sendMQ.get()
                clientSocket, res = messageInfo

                clientSocket.sendall(str(res).encode())
                self.sendMQ.task_done()
        finally:
            pass

    def defaultEMGenerator(self):
        while True:
            time.sleep(1)
            # req = Request()
            # req.setMethod("EM")

            # req.setHeader("Content-Type", "text/plain")

            # req.setBody(f"EM 현재 시간은 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            # req.setContentLength()

            for socket in self.clientConnectionPool:
                try:
                    socket.sendall(f"EM: 현재 서버 시간은 {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분 %S초')}".encode())
                except BrokenPipeError:
                    socket.close()
                    self.clientConnectionPool.remove(socket)
                
            
    def requestHandle(self, req, res):
        if req.method == "EM":
            return True
        
        res.setStatus(200)
        res.setBody("Hello!")

        return False
        

if __name__ == "__main__":
    server = HTTPServer("127.0.0.1", 5678)
    server.run()