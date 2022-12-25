def render(template, data={}):
  prefix = "<%"
  suffix = "%>"

  embeds = []
  start = template.find(prefix)
  end = template.find(suffix)

  while start != -1 and end != -1:
    embed = template[start+len(prefix):end]
    embeds.append(embed)
    start = template.find(prefix, end)
    end = template.find(suffix, start)
  
  for embed in embeds:
    rendered = embed
    for key, value in data.items():
      rendered = rendered.replace("<var>" + key + "</var>", value)
      
    files = findTags("file", rendered)
    for file in files:
        with open(file, "r") as f:
            content = f.read()
        rendered = rendered.replace("<file>" + file + "</file>", content)
    template = template.replace(prefix + embed + suffix, rendered)
  return template


def findTags(name, embed):
  tags = []
  openTag = "<" + name + ">"
  closeTag = "</" + name + ">"
  openPos = embed.find(openTag)
  closePos = embed.find(closeTag)
  while openPos != -1 and closePos != -1:
    tag = embed[openPos+len(openTag):closePos]
    tags.append(tag)
    openPos = embed.find(openTag, closePos)
    closePos = embed.find(closeTag, openPos)
  return tags