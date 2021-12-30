from flask import (
    Flask,
    request,
    render_template,
    Response
)
from .mdown import Mdown
from .snaptik import Snaptik
from .ssstik import Ssstik
from .tikmate import Tikmate
from .scrapper import info_post
from .ttdownloader import ttdownloader
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


@app.route('/<path:path>')
def snapt(path):
    if path == 'info':
        for i in range(10):
            try:
                if not request.args.get('url'):
                    return json.dumps(
                        {'msg': 'url parameter required'},
                        indent=4
                    )
                resp = info_post(request.args['url'])
                js = Response(
                    json.dumps(
                        {
                            'account': {
                                'avatar': resp.account.avatar,
                                'username': resp.account.username,
                                'nickname': resp.account.nickname,
                                'signature': resp.account.signature,
                                'create': (
                                    (
                                        resp.account.create
                                        and
                                        resp.account.create.timestamp()
                                    ) or 0),
                                'verified': resp.account.verified
                            },
                            'music': resp.music,
                            'cover': resp.cover,
                            'caption': resp.caption,
                            'create': resp.create.timestamp(),
                            'url': resp.url,
                            'id': resp.id
                        },
                        indent=4
                    )
                )
                js.headers['Content-Type'] = 'application/json'
                return js
            except Exception as e:
                print(e)
                continue
        else:
            return Response(json.dumps({
                'msg': 'Url is invalid'
            }), headers={'Content-Type': 'application/json'})
    elif path not in ['snaptik', 'ssstik', 'tikmate', 'mdown', 'ttdownloader']:
        return Response(
            json.dumps({'msg': 'Path Not Found'}, indent=4),
            status=404,
            content_type='application/json'
        )
    if request.args.get('url'):
        try:
            service = ({
                'snaptik': Snaptik,
                'ssstik': Ssstik,
                'tikmate': Tikmate,
                'mdown': Mdown,
                'ttdownloader': ttdownloader
            }).get(path, Snaptik)
            res = service(request.args['url'])
            if request.args.get('type') == 'embed':
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
                            'url': i.json
                        } for i in res
                    ],
                    indent=4
                ),
                headers={
                    'Content-Type': 'application/json'
                }
            )
        except Exception as e:
            print(e)
            return Response(
                json.dumps({
                    'msg': 'Url is invalid'
                }, indent=4),
                headers={'Content-Type': 'application/json'}
            )
    else:
        return json.dumps({'msg': 'url parameter required'}, indent=4)
