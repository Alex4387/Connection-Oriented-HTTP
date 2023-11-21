import json

class Request:
    def __init__(self):
        self.method = None
        self.url = None
        self.version = "HTTP/1.1"
        self.header = dict()

        self.body = None

    def setRequest(self, method, host, url, body=None):
        self.method = method
        self.url = url
        self.version = "HTTP/1.1"

        self.setHeader("Host", host)
        self.setHeader("Accept", "*/*")

        self.setBody(body)
        self.setHeader("Content-Type", "application/json")
        self.setContentLength()

    def setReq(self, req):
        data = req.split("\r\n\r\n")
        header = data[0].split("\r\n")
        startLine = header[0].split()
        self.method = startLine[0]
        self.url = startLine[1]
        self.version = startLine[2]

        for i in range(1, len(header)):
            key, value = tuple(header[i].split(": "))
            self.header[key] = value

        if self.header["Content-Type"] == "application/json":
            self.body = json.loads(data[1])

        elif self.header["Content-Type"] == "text/plain":
            self.body = data[1]

    def setMethod(self, method):
        self.method = method

    def getMethod(self):
        return self.method

    def setHost(self, host):
        self.header["Host"] = host

    def setURL(self, url):
        self.url = url

    def setVersion(self, version):
        self.version = version

    def setBody(self, bodyData):
        self.body = bodyData
        
    def setHeader(self, key, value):
        self.header[key] = value

    def setContentLength(self):
        if self.body is None:
            return
        
        if self.header["Content-Type"] == "application/json":
            data = json.dumps(self.body, ensure_ascii=False)

        else:
            data = self.body

        self.header["Content-Length"] = len(data)

    def encode_data(self):
        if type(self.body) is str:
            self.body = self.body.encode("utf-8")
    
    def __str__(self):
        request = ""
        request += f"{self.method} {self.url} {self.version}\r\n"
        
        for key, item in self.header.items():
            request += f"{key}: {item}\r\n"
        
        if self.body:
            request += "\r\n"
            request += f"{json.dumps(self.body, ensure_ascii=False)}"

        return request

