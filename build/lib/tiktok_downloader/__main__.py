import argparse,json, os
import json
from .ssstik import ssstik
from .snaptik import snaptik
from .scrapper import info_post
from sys import stderr
arg=argparse.ArgumentParser(prog=f"python3 -m {os.path.dirname(__file__).split('/')[-1]}", description='Wellcome Maker')
arg.add_argument('--snaptik', action='store_true')
arg.add_argument('--ssstik', action='store_true')
arg.add_argument('--info', action='store_true')
arg.add_argument('--url')
arg.add_argument('--server', action='store_true')
arg.add_argument('--host', type=str, default='0.0.0.0')
arg.add_argument('--debug', action='store_true')
arg.add_argument('--port', default=8000, type=int)
arg.add_argument('--json', action='store_true')
arg.add_argument('--save')
parse=arg.parse_args()
if parse.server:
    from .server import app
    app.run(host=parse.host, port=parse.port, debug=bool(parse.debug))
elif parse.url:
    if parse.snaptik or parse.ssstik:
        try:
            ok=snaptik(parse.url).get_media() if parse.snaptik else ssstik().get_media(parse.url)
            if parse.json or not(parse.save):
                print(json.dumps( [{'type':i.type,'url':i.json} for i in ok],indent=4))
            elif parse.save:
                ok[0].download(parse.save)
            else:
                os.system(f"python3 -m {os.path.dirname(__file__).split('/')[-1]} --help")
        except Exception:
            stderr.write('Post Not Found\n')
            stderr.flush()
    elif parse.info:
        try:
            resp=info_post(parse.url)
            print(json.dumps({
                'account':{
                    'avatar':resp.account.avatar,
                    'username':resp.account.username,
                    'nickname':resp.account.nickname,
                    'signature':resp.account.signature,
                    'create':resp.account.create.timestamp() if resp.account.create else 0,
                    'verified':resp.account.verified
                },
                'music':resp.music,
                'caption':resp.caption,
                'create':resp.create.timestamp(),
                'url':resp.url,
                'id':resp.id    }, indent=4))
        except Exception as e:
            print(e)
            stderr.write('Post Not Found\n')
            stderr.flush()
    else:
        os.system(f"python3 -m {os.path.dirname(__file__).split('/')[-1]} --help")
else:
    os.system(f"python3 -m {os.path.dirname(__file__).split('/')[-1]} --help")