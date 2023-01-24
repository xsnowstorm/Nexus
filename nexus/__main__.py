from . import Nexus

app = Nexus()

@app.route("/")
def route(req):
    res = app.Response("Hello World!")
    return res

@app.route("/post", "POST")
def route(req):
    print(req.body)
    return "Hello!"

def start():
    print("Example server started!")

app.listen(onStart=start)
