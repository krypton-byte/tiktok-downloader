from requests.models import InvalidURL
from . import snaptik
from .utils import info_videotiktok
from ast import literal_eval
import re
import requests
class tikmate(requests.Session):
    BASE_URL='https://tikmate.online/'
    def __init__(self) -> None:
        super().__init__()
        self.headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    def get_media(self, url):
        token = re.search(r'name\=\"token\".*?value\=\"(.*?)\"',self.get(self.BASE_URL).text).group(1)
        media = self.post(self.BASE_URL+'abc.php', data={'url':url, 'token':token},headers={"origin": "https://tikmate.online","referer": "https://tikmate.online/","sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',"sec-ch-ua-mobile": "?0","sec-ch-ua-platform": "Linux","sec-fetch-dest": "iframe","sec-fetch-mode": "navigate","sec-fetch-site": "same-origin","sec-fetch-user": "?1","upgrade-insecure-requests": "1","user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"})
        if "'error_api_get'" in media.text:
            raise InvalidURL()
        tt=re.findall(r'\(\".*?,.*?,.*?,.*?,.*?.*?\)',media.text)
        d=literal_eval(tt[0]).__str__()
        decode = snaptik.decoder.eval(f'decoder{d}')
        return [info_videotiktok(self.BASE_URL+x, self) for x in re.findall(r'(download.php\?token.*?)\\\\\"',decode)]