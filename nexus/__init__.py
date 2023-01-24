__all__ = ["Nexus"]

import os
import ast
from http.server import HTTPServer, BaseHTTPRequestHandler
from mimetypes import guess_type
from .template import render as template

class Nexus:
  def __init__(self, path="", static=""):
    if not path.endswith("/") and not path == "":
      path = path + "/"
    if not static.endswith("/") and not static == "":
      static = static + "/"
      
    self.Response.path = path
    self.RequestHandler.static = static
  
  class RequestHandler(BaseHTTPRequestHandler):
    routes = {}
    
    def do_GET(self):
      self.respond()

    def do_POST(self):
      self.respond()

    def do_PUT(self):
      self.respond()

    def do_DELETE(self):
      self.respond()

    def serve(self):
      req = self.server.framework.Request(self)
      Response = self.server.framework.Response

      path = req.path
      method = req.method

      if method == "GET" and not self.static == "":
          if path == "/":
            static = self.static + "index.html"
          else:
            static = self.static + path[1:]
          if os.path.isfile(static):
            res = Response()
            res.readFile(static)
            return res
          
      routes = self.routes.get(method)
      if not routes:
        return Response("501: Not Implemented", 501)
      route = routes.get(path)

      if route:
        view = route.get("view")
        middlewares = route.get("middleware")
        for middleware in middlewares:
          if not middleware(req):
            return Response("401: Unauthorized", 401)
        res = view(req)
        if not isinstance(res, Response):
          res = Response(res)
        return res
      else:
        return Response("404: Not Found", 404)
      
    def respond(self):
      res = self.serve()
      self.send_response(res.code)
      for key, value in res.headers.items():
        self.send_header(key, value)
      self.end_headers()
      self.wfile.write(res.body)

  class Request:
    def __init__(self, handler):
      self.path = handler.path
      self.method = handler.command
      self.headers = handler.headers
      if not self.method == "GET":
        lengthHeader = self.headers.get("Content-length")
        length = int(lengthHeader) if lengthHeader else 0
        bodyStr = handler.rfile.read(length).decode()
        try:
          self.body = ast.literal_eval(bodyStr) if bodyStr else {}
        except
        
  class Response:
    def __init__(self, body="", code=200, headers={"Content-type": "text/plain"}):
      self.body = str(body).encode("utf-8")
      self.code = code
      self.headers = headers

    def readFile(self, path, mode="rb",  render=False, data={}):
      with open(path, mode) as file:
        content = file.read()
        contentType = guess_type(path)
        if render:
          content = str(template(content, data)).encode("utf-8")
        self.body = content
        self.headers["Content-type"] = contentType

    def render(self, path, data={}):
      self.readFile(self.path + path, "r", True, data)
  
  def route(self, path, method="GET", middleware=[]):
    def decorator(f):
      routes = self.RequestHandler.routes.get(method)
      if not routes:
        self.RequestHandler.routes[method] = {}
      self.RequestHandler.routes[method][path] = {"view": f, "middleware": middleware}
    return decorator
      
  def listen(self, host="localhost", port=8080, onStart=None, onStop=None):
    server = HTTPServer((host, port), self.RequestHandler)
    server.framework = self
    if onStart:
      onStart()
    try:
      server.serve_forever()
    except KeyboardInterrupt:
      server.shutdown()
    if onStop:
      onStop()
