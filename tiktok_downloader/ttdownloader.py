from httpx import AsyncClient
from requests import Session
import re
from .utils import Download, DownloadAsync


class TTDownloader(Session):
    BASE_URL = 'https://ttdownloader.com/'

    def __init__(self, url: str) -> None:
        super().__init__()
        self.headers: dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 '
            'Safari/537.36',
            'origin': 'https://ttdownloader.com',
            'referer': 'https://ttdownloader.com/',
            'sec-ch-ua': '"Chromium";v="94",'
            '"Google Chrome";v="94", ";'
            'Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Linux",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.url = url

    def get_media(self) -> list[Download]:
        indexsource = self.get(self.BASE_URL)
        token = re.findall(r'value=\"([0-9a-z]+)\"', indexsource.text)
        result = self.post(
            self.BASE_URL+'search/',
            data={'url': self.url, 'format': '', 'token': token[0]}
        )
        nowm, wm, audio = re.findall(
            r'(https?://.*?.php\?v\=.*?)\"', result.text
        )
        return [
            Download(nowm, self, 'video'),
            Download(wm, self, 'video', True),
            Download(audio, self, 'music')
        ]


class TTDownloaderAsync(AsyncClient):
    BASE_URL = 'https://ttdownloader.com/'

    def __init__(self, url: str) -> None:
        super().__init__()
        self.headers: dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 '
            'Safari/537.36',
            'origin': 'https://ttdownloader.com',
            'referer': 'https://ttdownloader.com/',
            'sec-ch-ua': '"Chromium";v="94",'
            '"Google Chrome";v="94", ";'
            'Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Linux",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.url = url

    async def get_media(self) -> list[DownloadAsync]:
        indexsource = await self.get(self.BASE_URL, follow_redirects=True)
        token = re.findall(r'value=\"([0-9a-z]+)\"', indexsource.text)
        result = await self.post(
            self.BASE_URL+'search/',
            data={'url': self.url, 'format': '', 'token': token[0]},
            follow_redirects=True
        )
        nowm, wm, audio = re.findall(
            r'(https?://.*?.php\?v\=.*?)\"', result.text
        )
        return [
            DownloadAsync(nowm, self, 'video'),
            DownloadAsync(wm, self, 'video', True),
            DownloadAsync(audio, self, 'music')
        ]


def ttdownloader(url: str) -> list[Download]:
    return TTDownloader(url).get_media()


async def ttdownloader_async(url: str):
    return await TTDownloaderAsync(url).get_media()
