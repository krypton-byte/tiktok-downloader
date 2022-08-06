from __future__ import annotations
from requests import Session, get
from re import findall
from typing import Callable, Optional, Union
from io import BytesIO
from datetime import datetime
from .Except import InvalidUrl
from .utils import info_videotiktok
import re


def extract_id(
    initf: Callable[[info_post, str], None]
) -> Callable[[info_post, str], None]:
    subdo_redirect = ['vt', 'vm']

    def regex(url: str) -> str:
        if not findall(r'[0-9]{19}', url):
            raise InvalidUrl()
        return findall(r'[0-9]{19}', url)[0]

    def apply(cls: info_post, url: str):
        subdo = re.findall(r'://(\w+)\.', url)
        if subdo and subdo[0] in subdo_redirect:
            url = get(
                url,
                allow_redirects=False).text
        initf(cls, regex(url))
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


class info_post(Session):
    @extract_id
    def __init__(self, id: str):
        super().__init__()
        self.id = findall(r'[0-9]{19}', id)[0]
        self.aweme = self.get(
            'https://api.tiktokv.com/aweme/v1/aweme/detail/',
            params={'aweme_id': self.id}).json()
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

    def utils(self) -> list[info_videotiktok]:
        return [
            info_videotiktok(
                self.downloadLink(False), self),
            info_videotiktok(
                self.downloadLink(True), self, watermark=True),
            info_videotiktok(
                self.aweme['aweme_detail']['music']['play_url']['uri'],
                self,
                "music"
            )
        ]

    @classmethod
    def service(cls, url: str) -> list[info_videotiktok]:
        return cls(url).utils()

    def downloadLink(self, watermark: Optional[bool] = False) -> str:
        return self.aweme['aweme_detail']['video'][
            ['play_addr', 'download_addr'][watermark]
        ]['url_list'][0]

    def download(
        self,
        out: Optional[str] = None,
        watermark: Optional[bool] = False,
        chunk_size: int = 1024
    ) -> Union[None, BytesIO]:
        request = self.get(self.downloadLink(watermark), stream=True)
        stream = open(out, 'wb') if isinstance(out, str) else BytesIO()
        for i in request.iter_content(chunk_size):
            stream.write(i)
        return None if isinstance(out, str) else stream

    def download_music(
        self,
        out: Optional[str] = None,
        chunk_size: int = 1024
    ) -> Union[None, BytesIO]:
        request = self.get(
            self.aweme['aweme_detail']['music']['play_url']['uri'],
            stream=True)
        stream = open(out, 'wb') if isinstance(out, str) else BytesIO()
        for i in request.iter_content(chunk_size):
            stream.write(i)
        return None if isinstance(out, str) else stream

    def __repr__(self):
        return f'<[{self.id} {self.duration}s]>'
