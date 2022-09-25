from __future__ import annotations
from httpx import AsyncClient
from requests import Session, get
from re import findall
from typing import Callable, Optional, Union
from io import BufferedWriter, BytesIO
from datetime import datetime
import requests
from .Except import InvalidUrl
from .utils import Download, DownloadAsync
import re


def extract_id(
    initf: Callable[[VideoInfo, str], VideoInfo]
) -> Callable[[VideoInfo, str], VideoInfo]:
    subdo_redirect = ['vt', 'vm']

    def regex(url: str) -> str:
        if not findall(r'[0-9]{19}', url):
            raise InvalidUrl()
        return findall(r'[0-9]{19}', url)[0]

    def apply(cls: VideoInfo, url: str) -> VideoInfo:
        subdo = re.findall(r'://(\w+)\.', url)
        if subdo and subdo[0] in subdo_redirect:
            url = get(
                url,
                allow_redirects=False).text
        return initf(cls, regex(url))
    return apply


class Author:
    def __init__(self, ascp: dict):
        self.username = ascp['unique_id']
        self.region = ascp['region']
        self.avatar = ascp['avatar_larger']['url_list'][0]
        self.avatar_thumb = ascp['avatar_thumb']['url_list'][0]
        self.signature = ascp['signature']
        self.unique_id_modify_time = datetime.fromtimestamp(
            ascp['unique_id_modify_time'])
        self.create_time = datetime.fromtimestamp(
            ascp['create_time']) if ascp['create_time'] else None

    def __repr__(self):
        return f"<[ @{self.username} ]>"


class VideoInfoAsync(AsyncClient):
    def __init__(self, js: dict, id: str):
        super().__init__()
        self.id = id
        self.aweme = js
        self.height = (
            js['aweme_detail']['video']
            ['download_addr']['height'])
        self.width = (
            js['aweme_detail']['video']
            ['download_addr']['width'])
        self.size = (
            js['aweme_detail']
            ['video']['download_addr']['data_size'])
        self.desc = js['aweme_detail']['desc']
        self.cover = (
            js['aweme_detail']
            ['video']['origin_cover']['url_list'][0])
        self.create_time = datetime.fromtimestamp(
            js['aweme_detail']['create_time'])
        self.author = Author(js['aweme_detail']['author'])
        self.music_title = js['aweme_detail']['music']['title']
        self.music_author = js['aweme_detail']['music']['author']
        self.music_duration = js['aweme_detail']['music']['duration']
        self.duration = int(
            js['aweme_detail']['video']['duration']/1000)

    @classmethod
    async def url_to_id(cls, url: str, client: AsyncClient):
        ids = findall(r'[0-9]{19}', url)
        if ids:
            return ids[0]
        url_ = (await client.get(url, follow_redirects=True)).url.__str__()
        ids = findall(r'[0-9]{19}', url_)
        if ids:
            return ids[0]
        raise InvalidUrl()

    @classmethod
    async def get_info(cls, url: str):
        client = AsyncClient()
        id = await cls.url_to_id(url, client)
        return cls((await client.get(
            'https://api.tiktokv.com/aweme/v1/aweme/detail/',
            params={'aweme_id': id})).json(), id)

    def downloadLink(self, watermark: bool = False) -> str:
        return self.aweme['aweme_detail']['video'][
            ['play_addr', 'download_addr'][watermark]
        ]['url_list'][0]

    def utils(self) -> list[DownloadAsync]:
        return [
            DownloadAsync(
                self.downloadLink(False), self),
            DownloadAsync(
                self.downloadLink(True), self, watermark=True),
            DownloadAsync(
                self.aweme['aweme_detail']['music']['play_url']['uri'],
                self,
                "music"
            )
        ]

    def __repr__(self):
        return f'<[{self.id} {self.duration}s]>'


class VideoInfo(Session):
    def __init__(self, js: dict, id: str):
        super().__init__()
        self.id = id
        self.aweme = js
        self.height = (
            self.aweme['aweme_detail']['video']
            ['download_addr']['height'])
        self.width = (
            self.aweme['aweme_detail']['video']
            ['download_addr']['width'])
        self.size = (
            self.aweme['aweme_detail']
            ['video']['download_addr']['data_size'])
        self.desc = self.aweme['aweme_detail']['desc']
        self.cover = (
            self.aweme['aweme_detail']
            ['video']['origin_cover']['url_list'][0])
        self.create_time = datetime.fromtimestamp(
            self.aweme['aweme_detail']['create_time'])
        self.author = Author(self.aweme['aweme_detail']['author'])
        self.music_title = self.aweme['aweme_detail']['music']['title']
        self.music_author = self.aweme['aweme_detail']['music']['author']
        self.music_duration = self.aweme['aweme_detail']['music']['duration']
        self.duration = int(
            self.aweme['aweme_detail']['video']['duration']/1000)

    @classmethod
    @extract_id
    def get_info(cls, id: str) -> VideoInfo:
        print('id: ', id)
        return cls((requests.get(
            'https://api.tiktokv.com/aweme/v1/aweme/detail/',
            params={'aweme_id': id})).json(), id)

    def utils(self) -> list[Download]:
        return [
            Download(
                self.downloadLink(False), self),
            Download(
                self.downloadLink(True), self, watermark=True),
            Download(
                self.aweme['aweme_detail']['music']['play_url']['uri'],
                self,
                "music"
            )
        ]

    @classmethod
    def service(cls, url: str) -> list[Download]:
        return cls.get_info(url).utils()

    def downloadLink(self, watermark: bool = False) -> str:
        return self.aweme['aweme_detail']['video'][
            ['play_addr', 'download_addr'][watermark]
        ]['url_list'][0]

    def download(
        self,
        out: Optional[str] = None,
        watermark: bool = False,
        chunk_size: int = 1024
    ) -> Union[None, BytesIO, BufferedWriter]:
        request = self.get(self.downloadLink(watermark), stream=True)
        stream = open(out, 'wb') if isinstance(out, str) else BytesIO()
        for i in request.iter_content(chunk_size):
            stream.write(i)
        return None if isinstance(out, str) else stream

    def download_music(
        self,
        out: Optional[str] = None,
        chunk_size: int = 1024
    ) -> Union[None, BytesIO, BufferedWriter]:
        request = self.get(
            self.aweme['aweme_detail']['music']['play_url']['uri'],
            stream=True)
        stream = open(out, 'wb') if isinstance(out, str) else BytesIO()
        for i in request.iter_content(chunk_size):
            stream.write(i)
        return None if isinstance(out, str) else stream

    def __repr__(self):
        return f'<[{self.id} {self.duration}s]>'
