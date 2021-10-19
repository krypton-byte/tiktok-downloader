from io import BytesIO
from typing import Union
from requests import Session
class info_videotiktok:
    def __init__(self,  url, Session:Session, type='video') -> None:
        self.json = url
        self.type = type
        self.Session =Session
    def get_size(self)->int:
        return int(self.Session.get(self.json,  stream=True).headers["Content-Length"])
    def download(self, out=False)->Union[None, BytesIO]:
        if isinstance(out, str):
            open(out, "wb").write(self.Session.get(self.json).content)
        else:
            return BytesIO(self.Session.get(self.json).content)
    def __str__(self) -> str:
        return f"<[type:{self.type}]>"
    def __repr__(self) -> str:
        return self.__str__()