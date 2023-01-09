from src.nexus import Nexus

app = Nexus(
  path = "pages",
  static = "public"
)

@app.route("/")
def index(req):
  res = app.Response()
  res.render("template.html", {
    "title": "Home",
    "content": "index.html",
    "data": {}
  })
  return res

@app.post("/")
def route(req):
  print(req.body)
  return "200: OK"

def online():
  print("server running!")

def offline():
  print("server stopped!")
  
app.listen("0.0.0.0", 3000, online, offline)