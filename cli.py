from http.HTTPClient import HTTPClient
import time

def printData(req):
    print("[ServerTime Info]", req.body)

conn = HTTPClient("localhost", 5001)
conn.registerEventController('/server/time', printData)

time.sleep(100)