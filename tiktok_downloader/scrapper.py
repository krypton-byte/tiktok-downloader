from requests import Session
from re import findall
from typing import Optional, Union
from io import BytesIO
from datetime import datetime
from .Except import InvalidUrl
class Author:
    def __init__(self, ascp: dict):
        self.username = ascp['unique_id']
        self.region = ascp['region']
        self.avatar = ascp['avatar_larger']['url_list'][0]
        self.avatar_thumb = ascp['avatar_thumb']['url_list'][0]
        self.signature = ascp['signature']
        self.unique_id_modify_time = datetime.fromtimestamp(ascp['unique_id_modify_time'])
        self.create_time = datetime.fromtimestamp(ascp['create_time']) if ascp['create_time'] else None
    def __repr__(self):
        return f"<[ @{self.username} ]>"

class info_post(Session):
    def __init__(self, url: str):
        super().__init__()
        self.headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Linux",
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7',
            'Connection': 'keep-alive'
        }
        if 'vt.tiktok.com' in url:
            url = self.get(url, headers=self.headers, allow_redirects=False).text
        if not findall(r'[0-9]{19}', url):
            raise InvalidUrl()
        self.id = findall(r'[0-9]{19}', url)[0]
        self.aweme = self.get('https://api.tiktokv.com/aweme/v1/aweme/detail/', params={'aweme_id': self.id}).json()
        self.height = self.aweme['aweme_detail']['video']['download_addr']['height']
        self.width = self.aweme['aweme_detail']['video']['download_addr']['width']
        self.size = self.aweme['aweme_detail']['video']['download_addr']['data_size']
        self.desc = self.aweme['aweme_detail']['desc']
        self.cover = self.aweme['aweme_detail']['video']['origin_cover']['url_list'][0]
        self.create_time = datetime.fromtimestamp(self.aweme['aweme_detail']['create_time'])
        self.author = Author(self.aweme['aweme_detail']['author'])
        self.music_title = self.aweme['aweme_detail']['music']['title']
        self.music_author = self.aweme['aweme_detail']['music']['author']
        self.music_duration = self.music_author = self.aweme['aweme_detail']['music']['duration']
        self.duration = int(self.aweme['aweme_detail']['video']['duration']/1000)

    def download(self, out:Optional = None, watermark:Optional[bool] = False,chunk_size: int = 1024) -> Union[None, BytesIO]:
        request = self.get(self.aweme['aweme_detail']['video'][['play_addr', 'download_addr'][watermark]]['url_list'][0], stream=True)
        with (open(out,'wb') if isinstance(out, str) else BytesIO()) as stream:
            for i in request.iter_content(chunk_size):
                stream.write(i)
            return None if isinstance(out, str) else stream
    
    def download_music(self, out:Optional = None, chunk_size: int = 1024) -> Union[None, BytesIO]:
        request = self.get(self.aweme['aweme_detail']['music']['play_url']['uri'], stream=True)
        with (open(out,'wb') if isinstance(out, str) else BytesIO()) as stream:
            for i in request.iter_content(chunk_size):
                stream.write(i)
            return None if isinstance(out, str) else stream

    def __repr__(self):
        return f'<[{self.id} {self.duration}s]>'