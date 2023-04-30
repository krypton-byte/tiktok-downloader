from typing import Generator
from httpx import AsyncClient
from requests.models import InvalidURL
from .decoder import decoder
from .utils import Download, DownloadAsync
from ast import literal_eval
import re
from base64 import b64decode
import requests
import json
import aiohttp



def decodeJWT(resp: str) -> Generator[dict[str, str], None, None]:
    urls = re.findall('https?://snap[\w./?=.&\-]+', resp)
    for i in urls:
        token: str = re.search(r'token=(.*?)&', i).group(0)
        yield {'filename':'tiktok.'+['mp4','mp3'][b'.mp3' in b64decode(token.split('.')[1] + '==========')], 'url': i}
class Tikmate(requests.Session):
    BASE_URL = 'https://tikmate.online/'

    def __init__(self) -> None:
        super().__init__()
        self.headers: dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/86.0.4240.111 Safari/537.36'
        }

    def get_media(self, url: str) -> list[Download]:
        media = self.post(
            self.BASE_URL+'abc.php',
            data={'url': url, **dict(re.findall(
                'name="(token)" value="(.*?)"', self.get(
                    'https://tikmate.online/?lang=id').text))},
            headers={
                "origin": "https://tikmate.online",
                "referer": "https://tikmate.online/",
                "sec-ch-ua": '"Chromium";v="94",\
                    "Google Chrome";v="94", \
                    ";Not A Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "Linux",
                "sec-fetch-dest": "iframe",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/94.0.4606.81 Safari/537.36"
                }
        )
        if "'error_api_get'" in media.text:
            raise InvalidURL()
        tt = re.findall(r'\(\".*?,.*?,.*?,.*?,.*?.*?\)', media.text)
        decode = decodeJWT(decoder(*literal_eval(tt[0])))
        return [
            Download(
                x['url'],
                self,
                type=(['video', 'music'][x['filename'].endswith(
                    '.mp3')])) for x in decode
        ]


class TikmateAsync(AsyncClient):
    BASE_URL = 'https://tikmate.online/'

    def __init__(self) -> None:
        super().__init__()
        self.headers: dict[str, str] = {
            "referer": "https://tikmate.online/",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/94.0.4606.81 Safari/537.36"
        }

    async def get_media(self, url: str) -> list[DownloadAsync]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.BASE_URL+'abc.php',
                data={'url': url, **dict(re.findall(
                    'name="(token)" value="(.*?)"', (
                        await self.get(self.BASE_URL)).text))},
                headers={
                    "Origin": "https://tikmate.online",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "Linux",
                    "sec-fetch-dest": "iframe",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'x-requested-with': 'XMLHttpRequest',
                    **self.headers
                }
            ) as media:
                text = await media.text()
                if "'error_api_get'" in text:
                    raise InvalidURL()
                tt = re.findall(r'\(\".*?,.*?,.*?,.*?,.*?.*?\)', text)
                decode = decodeJWT(decoder(*literal_eval(tt[0])))
                return [
                    DownloadAsync(
                        x['url'],
                        self,
                        type=(['video', 'music'][x['filename'].endswith(
                            '.mp3')])) for x in decode
                ]


def tikmate(url: str):
    return Tikmate().get_media(url)


async def tikmate_async(url: str):
    return await tikmateAsync().get_media(url)
