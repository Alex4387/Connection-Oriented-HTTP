from http.HTTPRequest import Request
from http.RequestParsingError import RequestParsingError
import json


class RequestParser:
    @staticmethod
    def toRequestObject(reqRaw):
        reqObj = Request()

        requestLines = reqRaw.split("\r\n")

        try:
            startLine = requestLines[0]
            method, path, httpVersion = tuple(startLine.split())

            header = dict()
            i = 1

            while requestLines[i] != '':
                key, value = requestLines[i].split(": ")

                header[key] = value
                i += 1
            
            body = None
            i += 1
            if i < len(requestLines):
                body = '\r\n'.join(requestLines[i:])

            reqObj.setMethod(method)
            reqObj.setURL(path)
            reqObj.setVersion(httpVersion)

            for key, value in header.items():
                reqObj.setHeader(key, value)

            if body:
                match header["Content-Type"]:
                    case "application/json":
                        body = json.loads(body)
                    case "text/plain":
                        pass
            
                reqObj.setBody(body)

            return reqObj

        except Exception as e:
            return RequestParsingError.InvalidRequestSyntax

if __name__ == "__main__":
    exampleRequest = """GET /example-page.html HTTP/1.1\r\nHost: www.example.com\r\nConnection: keep-alive\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36\r\nAccept-Encoding: gzip, deflate, sdch, br\r\nAccept-Language: en-US,en;q=0.8,ko;q=0.6\r\n"""
    req = RequestParser.toRequestObject(exampleRequest)
    req.method