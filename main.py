from src.nexus import Nexus

app = Nexus(
  path = "pages"
)

def require_login(req):
  return True

@app.route("/")
def index(req):
    return app.renderFile("index.html", {"title": "Main"})

@app.route("/profile", [require_login])
def profile(req):
    return "Profile"

app.listen("0.0.0.0", 3000)