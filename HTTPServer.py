import sys
import socket
import threading
import time
from datetime import datetime

from HTTPResponse import Response
from HTTPRequest import Request
from RequestParser import RequestParser
from BaseHandler_Server import BaseHTTPMessageHandler

from queue import Queue 

class HTTPServer:
    def __init__(self, serverHost, serverPort, BaseHandler=BaseHTTPMessageHandler, buffSize=16*1024):
        self.SERVER_HOST = serverHost
        self.SERVER_PORT = serverPort
        self.BUFFER_SIZE = buffSize

        self.baseHandler = BaseHandler()

        self.recvMQ = Queue()
        self.eventMQ = Queue()

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

            senderThread = threading.Thread(target=self.eventMessageSender)
            senderThread.daemon = True
            senderThread.start()

            # EMGenerator = threading.Thread(target=self.recvRequest)
            # EMGenerator.daemon = True
            # EMGenerator.start()

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

            isEM = self.classifyMessage(req)
            
            if isEM:
                self.baseHandler.processEvent(req)
            else:
                res = self.baseHandler.requestHandler(req)
                clientSocket.sendall(str(res).encode("utf-8"))
                
    def sendEventMessage(self, em):
        self.eventMQ.put(em)
            
    def eventMessageSender(self):
        try:
            while True:
                message = self.eventMQ.get()
                self.eventMQ.task_done()

                print("EM 전송 준비 완료")

                for socket in self.clientConnectionPool:
                    try:
                        socket.sendall(str(message).encode('utf-8'))
                    except BrokenPipeError:
                        socket.close()
                        self.clientConnectionPool.remove(socket)
        finally:
            pass

    # def defaultEMGenerator(self):
    #     while True:
    #         time.sleep(1)
    #         for socket in self.clientConnectionPool:
    #             try:
    #                 socket.sendall(f"EM /server/time HTTP/1.1\r\nContent-Type: text/plain\r\n\r\n현재 서버 시간은 {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분 %S초')}".encode())
    #             except BrokenPipeError:
    #                 socket.close()
    #                 self.clientConnectionPool.remove(socket)
                
            
    def classifyMessage(self, req):
        if req.method == "EM":
            return True

        return False

    def em(self,url, handler):
        self.baseHandler.em(url, handler)

    def get(self, url, handler):
        self.baseHandler.get(url, handler)

    def put(self, url, handler):
        self.baseHandler.put(url, handler)

    def post(self, url, handler):
        self.baseHandler.post(url, handler)

    def delete(self, url, handler):
        self.baseHandler.delete(url, handler)

if __name__ == "__main__":
    def exampleGetHandler(req):
        res = Response()
        res.setStatus(200)
        res.setBody({"message": "This is JSON Example"})
        res.setContentLength()
        return res
    
    server = HTTPServer("0.0.0.0", 5001)
    server.get('/', handler=exampleGetHandler)

    em = Request()
    em.setMethod("EM")
    em.setHeader("Content-Type", "application/json")
    em.setURL('/server/time')
    em.setBody({"message": f"EM Sent at {datetime.now()}"})
    em.setContentLength()

    def emGener():
        while True:
            time.sleep(3)
            server.sendEventMessage(em)

    emGen = threading.Thread(target=emGener)
    emGen.daemon = True
    emGen.start()

    def emHandler(req):
        print(req)

    server.em('/', emHandler)

    server.run()

