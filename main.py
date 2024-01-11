from flask import Flask, request, render_template, send_file, redirect, abort
from urllib.parse import quote, unquote
from storage import list_files, upload_name, get_file, delete_file
from pathlib import Path

app = Flask(__name__, static_folder='static')

@app.route("/")
def home():
    if request.referrer:
    if 'iframe' in request.referrer:
        return "Collection"
    return redirect("/album"), 301

@app.route("/favicon.ico")
def favicon():
    return send_file("static/icons8-favicon.gif", as_attachment=False)

@app.route("/album", methods=["GET"])
def files_handler():
    items = list_files() 
    def get_item(item):
        link = quote(item)
        return item, link
    items = list(map(get_item, items))
    return render_template("index.html", items=items, len=len)

@app.route("/json", methods=["GET"])
def files_handler_api():
    url = str(request.url).replace('json', '')
    items = list_files() 
    def get_item(item):
        link = url + quote(item)
        return link
    items = list(map(get_item, items))
    return {"items": items}

@app.route("/<path:filename>", methods=["GET"])
def file_handler(filename):
    filename = unquote(filename)
    try:
        file = get_file(filename)
        return render_template("video_player.html", video_link=file)
    except:
        abort(404)
    
@app.route("/<filename>", methods=["POST"])
def files_handler_put(filename):
    filename = unquote(filename)
    file_data = request.get_data()
    file = Path(filename)
    file.write_bytes(file_data)
    res = upload_name(filename)
    return str(res)
    
@app.route("/<filename>", methods=["DELETE"])
def files_handler_delete(filename):
    filename = unquote(filename)
    delete_file(filename)
    return f"File {filename} deleted successfully"