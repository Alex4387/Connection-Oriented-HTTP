class BaseEventMessageHandler:
    def __init__(self):
        self.router = dict()

    def registerHandler(self, url, handler):
        self.router[url] = handler

    def processEvent(self, req):
        try:
            handler = self.router[req.url]
            handler(req)
        except Exception as e:
            print(f"Can not find Event Handler for {req.url}")
            return

        