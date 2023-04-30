from httpx import AsyncClient
from requests import Session
import re
from .utils import Download, DownloadAsync
from base64 import b64decode


class SsstikIO(Session):
    def get_media(self, url: str) -> list[Download]:
        ses = self.get('https://ssstik.io')
        resp = self.post(
            'https://ssstik.io/abc?url=dl', data={
                'id': url,
                'locale': 'en',
                'tt': re.findall(r'tt:\'([\w\d]+)\'', ses.text)[0],
            },
            headers={
                'hx-current-url': 'https://ssstik.io/id',
                'hx-request': 'true',
                'hx-target': 'target',
                'hx-trigger': '_gcaptcha_pt',
                'origin': 'https://ssstik.io',
                'pragma': 'no-cache',
                'referer': 'https://ssstik.io/id',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", '
                '"Google Chrome";v="102"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': "Linux",
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) '
                'AppleWebKit/537.36 (KHTML, like Gecko)'
                ' Chrome/102.0.5059.159 Safari/537.36'
                }
        )
        return [Download(
            res, self, [
                'video', 'music']['music' in res]
                ) for res in [(b64decode(
                    '/'.join(x.split('/')[5:])
                    ).decode() if 'ssscdn.io' in x else x
                    ) for x in set(re.findall('href="(.*?)"', resp.text))]]


class SsstikAIO(AsyncClient):
    async def get_media(self, url: str):
        ses = await self.get('https://ssstik.io', follow_redirects=True)
        resp = await self.post(
            'https://ssstik.io/abc?url=dl', data={
                'id': url,
                'locale': 'id',
                'tt': re.findall(r'tt:\'([\w\d]+)\'', ses.text)[0],
            },
            headers={
                'hx-current-url': 'https://ssstik.io/id',
                'hx-request': 'true',
                'hx-target': 'target',
                'hx-trigger': '_gcaptcha_pt',
                'origin': 'https://ssstik.io',
                'pragma': 'no-cache',
                'referer': 'https://ssstik.io/id',
                'sec-ch-ua': '" Not A;Brand";v="99", '
                '"Chromium";v="102", "Google Chrome";v="102"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': "Linux",
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': (
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/102.0.5059.159Safari/537.36')
                }
        )
        return [DownloadAsync(
            res,
            self,
            ['video', 'music']['music' in res]) for res in [(
                b64decode(
                    '/'.join(
                        x.split('/')[5:])).decode() if 'ssscdn.io' in x else x
                        ) for x in set(
                            re.findall('href="(.*?)"', resp.text))]]


def ssstik(url: str):
    return SsstikIO().get_media(url)


async def ssstik_async(url: str):
    return await SsstikAIO().get_media(url)
