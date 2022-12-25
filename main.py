from src.nexus import Nexus

app = Nexus(
  path = "pages",
  static = "public"
)

@app.route("/")
def index(req):
    return app.sendRes(app.renderFile("template.html", {
      "title": "Main",
      "content": "pages/index.html"
    }))

@app.post("/")
def index(req):
    return app.sendRes("200: OK")

def online():
  print("server running!")

def offline():
  print("server stopped!")
  
app.listen("0.0.0.0", 3000, online, offline)