from reactpy import component, html, hooks

@component
def VideoList(items):
    items = [html.li(html.a(get_file(item))) for item in items]
    return html.ul(items)
    
@component
def VideoPlayer(video_link, video_name):
    source = html.source({"src": video_link, "type":"video/mp4"})
    video = html.video({"id":"player", "playsinline", "controls"},source)