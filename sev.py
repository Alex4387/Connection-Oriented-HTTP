from http.HTTPServer import HTTPServer

server = HTTPServer("localhost", 5001)
server.run()

# def printData(req):
#     print("[ServerTime Info]", req.body)

# conn = HTTPClient("localhost", 5001)
# conn.registerEventController('/server/time', printData)

# time.sleep(100)