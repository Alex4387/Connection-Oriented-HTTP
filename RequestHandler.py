import http.server
from RequestParser import RequestParser

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes('안녕하세요!\n', 'utf-8'))
        self.wfile.write(bytes('클라이언트가 요청한 경로: ', 'utf-8'))
        self.wfile.write(bytes(self.path, 'utf-8'))
        
        address = ('localhost', 8000)

        listener = http.server.HTTPServer(address, Handler)
        print(f'http://{address[0]}:{address[1]} 주소에서 요청 대기중...')
        listener.serve_forever()
 