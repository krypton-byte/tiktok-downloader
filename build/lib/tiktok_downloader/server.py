from flask import Flask, request,render_template
from . import info_post, snaptik, ssstik
import json
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/test')
def test():
    if request.args.get('s') == 't':
        return json.dumps([{'type':'music','url':''},{'type':'video','url':''}])
    elif request.args.get('s') =='i':
        return json.dumps({
            "account": {
                "avatar": "https://p16-sign-sg.tiktokcdn.com/aweme/100x100/tiktok-obj/0c8589b8821e646047ebd34103ae3aea.jpeg?x-expires=1634824800&x-signature=y8keUWmt6%2FBT8SkZXZfXeiV2bI8%3D",
                "username": "tribunsumselcom",
                "nickname": "Tribun Sumsel",
                "signature": "Official Tiktok of Tribunsumsel.com\nYoutube & FB : Tribun Sumsel",
                "create": 1600221674.0,
                "verified": False
            },
            "music": "suara asli - Tribun Sumsel",
            "caption": "#tiktokberita #viral #infoviral #siswatangerangburonan #buronaninternasional",
            "create": 1634636189.0,
            "url": "https://www.tiktok.com/@tribunsumselcom/video/7020708969563917595",
            "id": "7020708969563917595"
        })
    else:
        return json.dumps({'msg':'test'})
@app.route('/<path:path>')
def snapt(path):
    if path == 'info':
        try:
            if not request.args.get('url'):
                return json.dumps({'msg':'url parameter required'}, indent=4)
            resp=info_post(request.args['url'])
            return json.dumps({
            'account':{
                'avatar':resp.account.avatar,
                'username':resp.account.username,
                'nickname':resp.account.nickname,
                'signature':resp.account.signature,
                'create':resp.account.create.timestamp() if resp.account.create else 0,
                'verified':resp.account.verified
            },
            'music':resp.music,
            'cover':resp.cover,
            'caption':resp.caption,
            'create':resp.create.timestamp(),
            'url':resp.url,
            'id':resp.id    }, indent=4)
        except Exception as e:
            print(e)
            return json.dumps({
                'msg':'url tidak valid'
            })
    elif not path in ['snaptik', 'ssstik']:
        return json.dumps({'msg':'path tidak ditemukan'})
    if request.args.get('url'):
        try:
            ok=snaptik(request.args['url']).get_media() if path == 'snaptik' else ssstik().get_media(request.args['url'])
            return json.dumps([{'type':i.type,'url':i.json} for i in ok],indent=4)
        except Exception as e:
            print(e)
            return json.dumps({
                'msg':'url tidak valid'
            })
    else:
        return json.dumps({'msg':'url parameter required'}, indent=4)