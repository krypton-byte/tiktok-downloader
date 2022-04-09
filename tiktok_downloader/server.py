from flask import (
    Flask,
    request,
    render_template,
    Response
)
from typing import List
from . import services
from .snaptik import Snaptik
from .scrapper import info_post
from .utils import info_videotiktok
import json
import os


app = Flask(
    __name__,
    template_folder=os.path.abspath(__file__+'/../templates'),
    static_folder=os.path.abspath(__file__+'/../static')
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auto')
def auto():
    serv = services.copy()
    serv.pop('ssstik')
    try:
        if not request.args.get('url'):
            return Response(
                json.dumps(
                    {'msg': 'url parameter required'},
                    indent=4
                ),
                content_type='application/json'
            )
        for name, service in serv.items():
            try:
                b: List[info_videotiktok] = service(request.args.get('url'))
                if request.args.get('type') in ['direct', 'embed']:
                    for video in filter(
                        lambda v: v.watermark and v.type == 'video',
                        b
                    ):
                        fvid = video.download()
                        return Response(
                            fvid.getvalue(),
                            content_type='video/mp4'
                        )
                else:
                    return Response(
                        json.dumps(
                            list(
                                map(lambda x: {
                                    "url": x.json,
                                    "type": x.type,
                                    "service": name,
                                    "watermark": x.watermark
                                }, b)),
                            indent=4
                        ),
                        content_type='application/json'
                    )
            except Exception as e:
                return Response(
                        json.dumps(
                            {"error": str(e)},
                            indent=4),
                        content_type='application/json'
                    )
        return Response(json.dumps(
                {'msg': 'server busy'},
                indent=4
            ),
            content_type='application/json'
        )
    except Exception:
        return Response(json.dumps(
                {'msg': 'url is invalid'},
                indent=4
            ),
            content_type='application/json'
        )


@app.route('/<path:path>')
def snapt(path):
    if path == 'info':
        try:
            if not request.args.get('url'):
                return json.dumps(
                    {'msg': 'url parameter required'},
                    indent=4
                )
            resp = info_post(request.args['url'])
            return Response(
                    json.dumps(
                        resp.aweme,
                        indent=4
                    ),
                    content_type='application/json'
                )
        except Exception as e:
            print(e)
            return Response(json.dumps({
                'msg': 'Url is invalid'
            }), headers={'Content-Type': 'application/json'})
    elif path not in services:
        return Response(
            json.dumps({'msg': 'Path Not Found'}, indent=4),
            status=404,
            content_type='application/json'
        )
    if request.args.get('url'):
        try:
            service = services.get(path, Snaptik)
            res = service(request.args['url'])
            if request.args.get('type') in ['embed', 'direct']:
                for i in res:
                    if i.type == 'video':
                        return Response(
                            i.download().getvalue(),
                            content_type='video/mp4'
                        )
            return Response(
                json.dumps(
                    [
                        {
                            'type': i.type,
                            'url': i.json,
                            'watermark': i.watermark
                        } for i in res
                    ],
                    indent=4
                ),
                headers={
                    'Content-Type': 'application/json'
                }
            )
        except Exception:
            return Response(
                json.dumps({
                    'msg': 'Url is invalid'
                }, indent=4),
                headers={'Content-Type': 'application/json'}
            )
    else:
        return json.dumps({'msg': 'url parameter required'}, indent=4)
