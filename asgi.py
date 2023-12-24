from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from deta import Deta
from urllib.parse import quote
import os

deta = Deta(os.getenv("DETA_KEY"))
drive = deta.Drive("storage")
base = deta.Base("storage")

app = FastAPI()

@app.get("/")
async def home():
  return "Collection"
  
@app.get("/album", response_class=HTMLResponse)
async def files_handler():
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
    result += f"{i+1}. <a href='/{item}'>{item}</a><br><br>"
  result += "</body></html>"
  return result


@app.get("/json")
async def files_handler_api(request: Request):
  url = str(request.url).replace('json', '')
  items = [f"{url}{quote(item['name'])}" for item in base.fetch().items]
  return items


@app.get("/{filename}")
async def file_handler(filename: str, request: Request):
  try:
    file = drive.get(filename)
    media_type = "application/octet-stream"
    if filename.endswith((".mp4", ".m4u")):
      media_type = "video/mp4"
    elif filename.endswith((".jpg", ".png")):
      media_type = "image/jpeg"
    elif filename.endswith((".mp3", ".ogg")):
      media_type = "audio/mpeg"
    return StreamingResponse(file.iter_chunks(), media_type=media_type)
  except:
    return "Not found"


@app.put("/{filename}")
async def files_handler_put(filename: str, request: Request):
  file = await request.body()
  drive.put(filename, data=file)
  base.put({"name": filename})
  return f"File {filename} uploaded successfully"


@app.delete("/{filename}")
async def files_handler_delete(filename: str, request: Request):
  drive.delete(filename)
  base_delete(filename)
  return "File deleted successfully"


def base_delete(filename):
  items = base.fetch({"name": filename}).items
  if items:
    item = items[0]
    base.delete(item["key"])
    