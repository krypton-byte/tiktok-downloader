from io import BytesIO
from typing import Optional, Union
from requests import Session


class info_videotiktok:

    def __init__(
        self,
        url: str,
        Session: Session,
        type='video',
        watermark: bool = False
    ) -> None:
        self.json = url
        self.type = type
        self.Session = Session
        self.watermark = watermark

    def get_size(self) -> int:
        return int(
            self.Session.get(
                self.json,
                stream=True
            ).headers["Content-Length"]
        )

    def download(self, out: Optional[str] = None) -> Union[None, BytesIO]:
        if isinstance(out, str):
            open(out, "wb").write(self.Session.get(self.json).content)
        else:
            return BytesIO(self.Session.get(self.json).content)

    def __str__(self) -> str:
        f = (
            self.type == 'video' and f' \
watermark: {self.watermark}]>') or ']>'
        return f"<[type: \"{self.type}\""+f

    def __repr__(self) -> str:
        return self.__str__()
