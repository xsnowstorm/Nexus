from nexus import Nexus

app = Nexus()

@app.route("/")
def index(req):
  res = app.Response()
  res.readFile("README")
  return res

@app.route("/", "POST")
def route(req):
  print(req.body)
  return "200: OK"

def online():
  print("server running!")

def offline():
  print("server stopped!")
  
app.listen("localhost", 8080, online, offline)
