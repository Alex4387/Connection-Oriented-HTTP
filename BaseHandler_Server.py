from HTTPResponse import Response

class BaseHTTPMessageHandler:
    # EM인 경우
    def __init__(self):
        self.EMrouter = dict()
        self.getRouter = dict()
        self.postRouter = dict()
        self.putRouter = dict()
        self.deleteRouter = dict()

    def em(self,url, handler):
        self.EMrouter[url] = handler

    def get(self, url, handler):
        self.getRouter[url] = handler

    def post(self, url, handler):
        self.postRouter[url] = handler

    def put(self, url, handler):
        self.putRouter[url] = handler

    def delete(self, url, handler):
        self.deleteRouter[url] = handler

    def processEvent(self, req):
        try:
            handler = self.EMrouter[req.url]
            handler(req)
        except Exception as e:
            print(f"Can not find Event Handler for {req.url}")
            return
    
    # Request인 경우
    def requestHandler(self, req):
        try:
            match req.getMethod():
                case "GET":
                    handler = self.getRouter[req.url]
                case "POST":
                    handler = self.postRouter[req.url]
                case "PUT":
                    handler = self.putRouter[req.url]
                case "DELETE":
                    handler = self.deleteRouter[req.url]
                case _:
                    raise Exception("Not Supported Method")
        except Exception as e:
            res = Response()
            res.setStatus(404)
            res.setBody({"message": f"Not Found about {req.url}"})
            res.setContentLength()
            return res
            
        res = handler(req)
        return res
