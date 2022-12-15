import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

class Nexus:
    def __init__(self, path=""):
        self.routes = {}
        if not path.endswith("/") and not path == "":
            path = path + "/"
        self.path = path

    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            response = self.server.framework.serve(self)
            type = self.server.framework.get_type(self.path)
            self.send_response(200)
            self.send_header('Content-type', type)
            self.end_headers()
            self.wfile.write(str(response).encode('utf-8'))

    def get_type(self, path):
        type = "text/html"
        if path.endswith(".html"):
            type = "text/html"
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
                    return "501: Unauthorized"
            return view(req)
        elif method == "POST":
            pass
        elif method == "PUT":
            pass
        elif method == "DELETE":
            pass
        else:
            return "405: Method Not Allowed"
      else:
        return "404: Not Found"
      
    def listen(self, host, port):
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
            result = "EJS rendering returned status: " + str(response.status_code)
        return result

    def readFile(self, path):
        with open(self.path + path, "r") as file:
            content = file.read()
            return content

    def renderFile(self, path, data):
        return self.render(self.readFile(path), data)