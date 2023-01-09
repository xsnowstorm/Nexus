def render(template, data={}):
  prefix = "{%"
  suffix = "%}"

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
    rendered = str(eval(embed))
    template = template.replace(prefix + embed + suffix, rendered)
  return template

def file(name, data={}):
  with open(name, "r") as f:
    return render(f.read(), data)