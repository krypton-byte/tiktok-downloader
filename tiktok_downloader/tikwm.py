from httpx import AsyncClient
from requests import Session
from requests.models import InvalidURL
from .utils import Download, DownloadAsync


class TikWM(Session):
    BASE_URL = 'https://www.tikwm.com'

    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url

    def get_media(self) -> list[Download]:
        req = self.post(self.BASE_URL + '/api/', data=dict(url=self.url, count=12, cursor=0, web=1, hd=1))
        res = req.json()
        if res['code'] == 0:
            return [
                Download(
                    self.BASE_URL + res['data'].get('hdplay', res['data']['play']),
                    self,
                    'video'
                ),
                Download(
                    self.BASE_URL + res['data']['wmplay'],
                    self,
                    'video',
                    True
                ),
                Download(
                    self.BASE_URL + res['data']['music'],
                    self,
                    'music'
                )
            ]
        else:
            raise InvalidURL(res['msg'])


class TikWMAsync(AsyncClient):
    BASE_URL = 'https://www.tikwm.com'

    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url

    async def get_media(self) -> list[DownloadAsync]:
        req = await self.post(self.BASE_URL + '/api/', data=dict(url=self.url, count=12, cursor=0, web=1, hd=1))
        res = req.json()
        if res['code'] == 0:
            return [
                DownloadAsync(
                    self.BASE_URL + res['data'].get('hdplay', res['data']['play']),
                    self,
                    'video'
                ),
                DownloadAsync(
                    self.BASE_URL + res['data']['wmplay'],
                    self,
                    'video',
                    True
                ),
                DownloadAsync(
                    self.BASE_URL + res['data']['music'],
                    self,
                    'music'
                )
            ]
        else:
            raise InvalidURL(res['msg'])


def tikwm(url: str) -> list[Download]:
    return TikWM(url).get_media()


async def tikwm_async(url: str) -> list[DownloadAsync]:
    return await TikWMAsync(url).get_media()