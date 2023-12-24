from flask import Flask, request, Response
from werkzeug.routing import BaseConverter
from urllib.parse import quote, unquote
import os
from deta import Deta

class PathConverter(BaseConverter):
    def to_python(self, value):
        return value

app = Flask(__name__)
app.url_map.converters['path'] = PathConverter

deta = Deta(os.getenv("DETA_KEY"))
drive = deta.Drive("storage")
base = deta.Base("storage")

@app.route("/")
def home():
  return "Collection"

@app.route("/album", methods=["GET"])
def files_handler():
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

@app.route("/json", methods=["GET"])
def files_handler_api():
    items = [{item['name']: quote(item['name'])} for item in base.fetch().items]
    return {"items": items}

@app.route("/<path:filename>", methods=["GET"])
def file_handler(filename):
    filename = unquote(filename)
    try:
        file = drive.get(filename)
        media_type = "application/octet-stream"
        if filename.endswith((".mp4", ".m4u")):
            media_type = "video/mp4"
        elif filename.endswith((".jpg", ".png")):
            media_type = "image/jpeg"
        elif filename.endswith((".mp3", ".ogg")):
            media_type = "audio/mpeg"
        response = Response(file.iter_chunks(), content_type=media_type)
        return response
    except:
        return "Not found"

@app.route("/<filename>", methods=["PUT"])
def files_handler_put(filename):
    filename = unquote(filename)
    file = request.get_data()
    drive.put(filename, data=file)
    base.put({"name": filename})
    return f"File {filename} uploaded successfully"

@app.route("/<filename>", methods=["DELETE"])
def files_handler_delete(filename):
    filename = unquote(filename)
    drive.delete(filename)
    base_delete(filename)
    return "File deleted successfully"

def base_delete(filename):
    items = base.fetch({"name": filename}).items
    if items:
        item = items[0]
        base.delete(item["key"])