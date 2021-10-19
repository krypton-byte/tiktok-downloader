from sys import stderr
from .snaptik_utils import PyJsHoisted_decoder_
from .utils import info_videotiktok
from .Except import InvalidUrl
from requests import Session
from re import findall
class snaptik(Session):
    '''
    :param tiktok_url:
    ```python
    >>> tik=snaptik('url')
    >>> tik.get_media()
    [<[type:video]>, <[type:video]>]
    ```
    '''
    def __init__(self, tiktok_url:str) -> None:
        super().__init__()
        self.resp = self.get('https://snaptik.app/abc.php', params={'url':tiktok_url,'lang':'en'}, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'})
        if 'error_api_web;' in self.resp.text or 'Error:' in self.resp.text:
            raise InvalidUrl()
    def get_media(self)->list[info_videotiktok]:
        '''
        ```python
        >>> <snaptik object>.get_media()
        [<[type:video]>, <[type:video]>]
        ```
        '''
        stderr.write('[*] decoding\n')
        stderr.flush()
        dec = PyJsHoisted_decoder_(*eval(findall('\(\".*?,.*?,.*?,.*?,.*?.*?\)',self.resp.text)[0]))
        stderr.write('[*] decoded\n')
        stderr.flush()
        return [info_videotiktok(i, self) for i in set(map(lambda x:x[0].strip('\\'),findall('\"(https?://(tikcdn\.net|snapsave\.info).*?)\"',dec.value)))]