from io import BytesIO
from flask import (
    Flask,
    request,
    render_template
)
from flask.wrappers import Response
from typing import List

from tiktok_downloader.scrapper_v2 import VideoInfoV2
from . import services
from .snaptik import Snaptik
from .scrapper import VideoInfo
from .utils import Download
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
                b: List[Download] = service(request.args.get('url'))
                if request.args.get('type') in ['direct', 'embed']:
                    for video in filter(
                        lambda v: v.watermark and v.type == 'video',
                        b
                    ):
                        fvid = video.download()
                        if isinstance(fvid, BytesIO):
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
            if request.args.get('legacy'):
                resp = VideoInfo.get_info(request.args['url'])
                return Response(
                        json.dumps(
                            {'legacy': True, **resp.aweme},
                            indent=4
                        ),
                        content_type='application/json'
                    )
            else:
                resp = VideoInfoV2.get_info(request.args['url'])
                return Response(json.dumps({
                    'id': resp.aweme_id,
                    'author': resp.username,
                    'cover': resp.cover,
                    'caption': resp.caption
                }))
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
                        fvid = i.download()
                        if isinstance(fvid, BytesIO):
                            return Response(
                                fvid.getvalue(),
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
