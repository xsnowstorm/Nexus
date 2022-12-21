import os
import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

class Nexus:
    def __init__(self, path="", static=False):
        self.routes = {}
        if not path.endswith("/") and not path == "":
            path = path + "/"
        if not static.endswith("/") and not static == "":
            static = static + "/"
        self.path = path
        self.static = static

    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            res = self.server.framework.serve(self)
            body = res["body"]
            self.send_response(res["code"])
            self.send_header("Content-type", body["type"])
            self.end_headers()
            self.wfile.write(body["content"])

    def getType(self, path):
        type = "text/plain"
        if path.endswith(".html"):
            type = "text/html"
        elif path.endswith(".css"):
            type = "text/css"
        elif path.endswith(".js") or path.endswith(".mjs"):
            type = "text/javascript"
        elif path.endswith(".ico"):
            type = "image/x-icon"
        elif path.endswith(".png"):
            type = "image/png"
        return type
      
    def route(self, path, middleware=[]):
        def decorator(f):
            self.routes[path] = {"view": f, "middleware": middleware}
        return decorator

    def sendRes(self, body="", code=200):
      if not type(body) is dict:
          body = {"content": str(body).encode("utf-8"), "type": "text/plain"}
      return {"body": body, "code": code}

    def serve(self, req):
      path = req.path
      method = req.command
      functions = self.routes.get(path)
      if functions:
        view = functions["view"]
        middleware = functions["middleware"]
        
        if method == "GET":
            for middleware_function in middleware:
                if not middleware_function(req):
                    return self.sendRes("401: Unauthorized", 401)
            return view(req)
        else:
            return self.sendRes("405: Method Not Allowed", 405)
      else:
        if method == "GET" and self.static:
            if path == "/":
                static = self.static + "index.html"
            else:
                static = self.static + path[1:]
            if os.path.isfile(static):
                return self.sendRes(self.readFile(static))
            else:
                return self.sendRes("404: Not Found", 404)
      
    def listen(self, host="localhost", port=8080):
        server = HTTPServer((host, port), self.RequestHandler)
        server.framework = self
        server.serve_forever()
  
    def render(self, template, data={}):
        renderer = "https://ejs-renderer.xsnowstorm.repl.co/"
        template = json.dumps(template)
        data = json.dumps(data)
        body = {
          "code": template,
          "data": data
        }
    
        requests.get(renderer)
        response = requests.post(renderer, json=body);
        if response.status_code == 200:
            result = response.json()
        else:
            result = "EJS rendering returned status: " + response.status_code
        return str(result).encode("utf-8")

    def readFile(self, path, mode="rb",  render=False, data={}):
        with open(path, mode) as file:
            content = file.read()
            if render:
                content = self.render(content, data)
            contentType = self.getType(path)
            return {
              "content": content,
              "type": contentType
            }

    def renderFile(self, path, data={}):
        return self.readFile(self.path + path, "r", True, data)