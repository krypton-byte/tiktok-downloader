import re
from bs4 import BeautifulSoup
import requests
class VideoInfoV2:
    def __init__(self, url: str, caption, comment: str, like: str, cover: str, aweme_id: str, username: str) -> None:
        self.url = url
        self.username = username
        self.comment = comment
        self.caption = caption
        self.like = like
        self.cover = cover
        self.aweme_id = aweme_id
    @classmethod
    def get_info(cls, url: str):
        obj = BeautifulSoup(requests.get(url, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 UOS'}).text)
        caption = obj.title.text
        cover = re.findall(r'cover\":\"(http[\w:/\-\.\?\=&%]+)"', obj.__str__().replace('\\u002F','/'))[0]
        username = re.findall(r'author\":"([\w]+)"', obj.__str__())[0]
        like = obj.find_all('strong', attrs={'data-e2e':'like-count'})[0].text
        comment = obj.find_all('strong', attrs={'data-e2e':'comment-count'})[0].text
        aweme_id = re.findall(r'aweme/detail/([0-9]+)', obj.__str__())[0]
        return cls(url, caption, comment, like, cover, aweme_id, username)