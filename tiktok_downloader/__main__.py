import argparse
import json
import os
import sys
import requests
from . import services
from .snaptik import Snaptik
from .scrapper import info_post
from sys import stderr


arg = argparse.ArgumentParser(
    prog=f"python3 -m {os.path.dirname(__file__).split('/')[-1]}",
    description='Tiktok Downloader [CLI]'
)

# Services
servgroup = arg.add_argument_group('list of services')
for key in services.keys():
    servgroup.add_argument(f'--{key}', action='store_true')

arg.add_argument('--info', action='store_true')
arg.add_argument('--url', type=str)
arg.add_argument('--server', action='store_true')
arg.add_argument('--host', type=str, default='127.0.0.1')
arg.add_argument('--debug', action='store_true')
arg.add_argument('--port', default=8000, type=int)
arg.add_argument('--json', action='store_true')
arg.add_argument('--save')
parse = arg.parse_args()
if parse.server:
    from .server import app
    app.run(host=parse.host, port=parse.port, debug=parse.debug)
elif parse.url:
    for key, val in services.items():
        if getattr(parse, key):
            service = val
            break
    else:
        service = Snaptik
    try:
        ok = service(parse.url)
        if parse.json or not(parse.save):
            print(
                json.dumps(
                    [
                        {
                            'type': i.type,
                            'url': i.json,
                            'watermark': i.watermark
                        } for i in ok
                    ],
                    indent=4
                )
            )
        elif parse.save:
            ok[0].download(parse.save)
        else:
            os.system("python3 -m tiktok_downloader --help")
    except Exception as e:
        print(e)
        stderr.write('Post Not Found\n')
        stderr.flush()
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        stderr.write('[x] offline\n')
        stderr.flush()
        sys.exit(1)
    except (KeyError, AttributeError):
        stderr.write('Post Not Found\n')
        stderr.flush()
        sys.exit(1)
else:
    os.system("python3 -m tiktok_downloader --help")
