def getMime(path):
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