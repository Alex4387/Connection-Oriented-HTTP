class BaseHTTPMessageHandler:
    # EM인 경우
    def __init__(self):
        self.router = dict()
        user = ""

    def registerHandler(self, url, handler):
        self.router[url] = handler

    def processEvent(self, req):
        try:
            handler = self.router[req.url]
            handler(req)
        except Exception as e:
            print(f"Can not find Event Handler for {req.url}")
            return
    
    # Request인 경우
    def method_handler(self, req):
        if req.getMethod() == 'GET':
            return req.getBody()
        
        elif req.getMethod() == 'POST':
            # 데이터 추가
            return req.getBody()
        
        elif req.getMethod() == 'PUT':
            # 데이터 수정
            return req.getBody()
        
        elif req.getMethod() == 'DELETE':
            # 데이터 삭제
            return req.getBody()

    # 개발자 정의 함수
    def client_handler(self, client_socket):
        print("Client Address: ", client_socket.getpeername())

