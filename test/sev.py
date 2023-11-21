from http.HTTPServer import HTTPServer

server = HTTPServer("localhost", 5001)
server.run()