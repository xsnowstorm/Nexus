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

app.listen("0.0.0.0", 3000)