import argparse
import json
import os
import sys
import requests
from . import services
from .scrapper import info_post
from sys import stderr
from rich import print as print_
from rich.panel import Panel
from typing import Optional


arg = argparse.ArgumentParser(
    prog=f"python3 -m {os.path.dirname(__file__).split('/')[-1]}",
    description='Tiktok Downloader [CLI]'
)

# Services
servgroup = arg.add_argument_group('List Of Services')
serg = servgroup.add_mutually_exclusive_group()
for key in services.keys():
    serg.add_argument(f'--{key}', action='store_true')

# Web Configuration
servconf = arg.add_argument_group('Web Configuration')
servconf.add_argument(
    '--host',
    type=str,
    default='127.0.0.1',
    help='Set host to run this web')
servconf.add_argument(
    '--debug',
    action='store_true',
    help='Set flask mode to debug')
servconf.add_argument('--port', default=8000, type=int, help='Set port')

# Mode Server | CLI
mod = arg.add_argument_group('Mode')
mode = mod.add_mutually_exclusive_group(required=True)
mode.add_argument(
    '--server',
    action='store_true',
    help='Run as web application')
mode.add_argument('--url', type=str, help='Video URL')

# CLI
cli = arg.add_argument_group('Optional')
cli.add_argument(
    '--info',
    action='store_true',
    help='Print info video like author, id & etc')

# Output
outa = arg.add_argument_group('Output Type')
out = outa.add_mutually_exclusive_group()
out.add_argument(
    '--json',
    action='store_true',
    help='Print result to json format')
out.add_argument(
    '--save',
    type=argparse.FileType('wb'),
    help='Write the result to file')
parse = arg.parse_args()


def info(url: str, js: Optional[bool] = False):
    infojson = info_post(url)
    if js:
        print(json.dumps({
            "id": infojson.id,
            "desc": infojson.desc,
            "duration": infojson.duration,
            "author": infojson.author.username,
            "wm": infojson.downloadLink(True),
            "nowm": infojson.downloadLink(False),
            "service": 'TikTok'
        }, indent=4))
    else:
        print_(Panel(
            f'[yellow bold]Id\t: [green bold]{infojson.id}\n'
            f'[yellow bold]Desc\t: [green bold]{infojson.desc}\n'
            f'[yellow bold]Duration: [green bold]{infojson.duration}s\n'
            f'[yellow bold]Author\t: [green bold]@{infojson.author.username}\n'
            f'[yellow bold]URL\t: [green bold]{infojson.downloadLink(True)}',
            title='TikTok Downloader',
            border_style='bold magenta'))


if parse.server:
    from .server import app
    app.run(host=parse.host, port=parse.port, debug=parse.debug)
elif parse.url:
    for key, val in services.items():
        if getattr(parse, key):
            service = val
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
                    if parse.info:
                        info(parse.url, js=parse.json)
                    ok[0].download(parse.save, bar=True)
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
elif parse.info and parse.url:
    info(parse.url, js=False)
else:
    os.system("python3 -m tiktok_downloader --help")
