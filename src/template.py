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
    template = template.replace(prefix + embed + suffix, rendered)
  return template