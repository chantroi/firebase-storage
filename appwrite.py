from werkzeug.routing import BaseConverter
from urllib.parse import quote, unquote
import os, json
from deta import Deta

class PathConverter(BaseConverter):
    def to_python(self, value):
        return value
        
deta = Deta(os.getenv("DETA_KEY"))
drive = deta.Drive("storage")
base = deta.Base("storage")

def main(context):
  req_path = context.req.path
  if req_path == "/":
    return context.res.send(files_list(), 200, {"content-type": "text/html"})
  elif req_path == "/api":
    return context.res.json(files_list_api(context.req.url))
  else:
    if context.req.method == "GET":
      filename = req_path.replace("/", "")
      try:
        data, content_type = file_handler(filename)
        return context.res.send(data, 200, {"content-type": content_type})
      except Exception as e:
        return context.res.send(e, 503)
        
    elif context.req.method == "PUT":
      filename = req_path.replace("/", "")
      return context.res.send(file_handler_put(context, filename))
    elif context.req.method == "DELETE":
      filename = req_path.replace("/", "")
      return context.res.send(file_handler_delete(filename))
      
      
  
  
def files_list():
    items = [item['name'] for item in base.fetch().items]
    result = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <style>
            body {
                background-color: white;
            }
            @media (prefers-color-scheme: dark) {
                body {
                    background-color: black;
                }
            }
        </style>
    </head>
    <body>
    """
    for i, item in enumerate(items):
        result += f"{i+1}. <a href='/{quote(item)}'>{item}</a><br><br>"
    result += "</body></html>"
    return result
  
def files_list_api(url):
    url = url.replace('api','')
    items = [f"{url}{quote(item['name'])}" for item in base.fetch().items]
    return items
    
def file_handler(filename):
        data = drive.get(unquote(filename))
        if filename.endswith((".mp4", ".m4u")):
            content_type = "video/mp4"
        elif filename.endswith((".jpg", ".png")):
            content_type = "image/jpeg"
        elif filename.endswith((".mp3", ".ogg")):
            content_type = "audio/mpeg"
        else:
            content_type = "application/octet-stream"
        return data.iter_chunks(), content_type

def file_handler_put(context, filename):
    filename = unquote(filename)
    file = json.dumps(context.req.body())
    drive.put(filename, data=file)
    base.put({"name": filename})
    return f"File {filename} uploaded successfully"

def file_handler_delete(filename):
    filename = unquote(filename)
    drive.delete(filename)
    base_delete(filename)
    return "File deleted successfully"

def base_delete(filename):
    items = base.fetch({"name": filename}).items
    if items:
        item = items[0]
        base.delete(item["key"])