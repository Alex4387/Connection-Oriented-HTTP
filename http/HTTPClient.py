import socket
import queue
import threading
from .HTTPRequest import Request
from .HTTPResponse import Response
from http.EventMessageHandler import BaseEventMessageHandler
from http.RequestParser import RequestParser 

class HTTPClient:
    def __init__(self, serverHost, serverPort, eventHandler=BaseEventMessageHandler, buffSize = 16*1024):
        self.SERVER_HOST = serverHost
        self.SERVER_PORT = serverPort
        self.BUFFER_SIZE = buffSize

        self.eventHandler = eventHandler()
        self.sendMQ = queue.Queue()
        self.recvMQ = queue.Queue()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.SERVER_HOST, self.SERVER_PORT))

        sender_thread = threading.Thread(target=self.messageSender)
        sender_thread.daemon = True
        sender_thread.start()

        receiver_thread = threading.Thread(target=self.messageReceiver)
        receiver_thread.daemon = True
        receiver_thread.start()


    def sendMessage(self, msg):
        '''
        msg: string
        '''
        req = Request()
        req.setRequest("GET", self.SERVER_HOST, "/", msg)
        self.sendMQ.put(str(req))
    
    def messageSender(self):
        while True:
            item = self.sendMQ.get()
            self.client_socket.sendall(item.encode())
            self.sendMQ.task_done()

    def recvMessage(self):
        originalMsg = self.recvMQ.get()
        res = Response()
        res.setResponse(originalMsg)

        return res

    def messageReceiver(self):
        while True:
            item = self.client_socket.recv(self.BUFFER_SIZE).decode('utf-8')
            
            if item.startswith("EM"):
                req = RequestParser.toRequestObject(item)
                self.eventHandler.processEvent(req)                
            
            else:
                self.recvMQ.put(item)

    def registerEventController(self, url, controller):
        self.eventHandler.registerHandler(url, controller)
    
    def close(self):
        self.client_socket.close()

