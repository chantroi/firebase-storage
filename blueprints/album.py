from reactpy import component, html, hooks
from reactpy.backend.flask import configure
from flask import Flask
from storage import list_items, get_file

app = Flask(__name__, static_folder="static")

@component
def Head():
    return html.head(
        html.meta({"name":"viewport","content":"width=device-width, initial-scale=1.0"}),
        html.link({"rel":"stylesheet", "href":"static/list.css"}),
        html.link({"rel":"stylesheet", "href":"static/Videoplayer.css"}),
        html.link({"rel":"stylesheet","href":"static/darkmode.css"}),
        html.link({"rel":"stylesheet","href":"https://cdn.plyr.io/3.6.8/plyr.css"}),
        html.script({"src":"static/darkmode.js"}),
        html.script({"src":"https://cdn.plyr.io/3.6.8/plyr.js"}))

@component
def VideoPlayer(video_link, video_name):
    source = html.source({"src": video_link, "type":"video/mp4"})
    video = html.video({"id":"player", "playsinline", "controls"},source)
    
@component
def VideoList(items):
    video, change_video = hooks.use_state({"",""})
    page, change_page = hooks.use_state(1)
    return html.div(
        VideoPlayer(video[0],video[1]),
        html.strong([html.a({"on_click": lambda _: change_page(i)}, i) for i in range(0,len(items),17)]),
        html.button({"on_click":lambda _: change_page(page-1)}, Trang trước),
        html.button({"on_click":lambda _: change_page(page+1)}, Trang sau),
        html.div(
            html.ul([html.li(html.a({"on_click": lambda event: change_video({get_file(item),item})}, item) for item in item])
        )))
   
@component
def App():
    items = list_items()
    return html._(
        "<!DOCTYPE html>",
        Head(),
        VideoList(items)
        )
        
configure(album, App)