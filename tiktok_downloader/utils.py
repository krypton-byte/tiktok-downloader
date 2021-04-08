class info_videotiktok:
    def __init__(self,  url, headers,request) -> None:
        self.json = url
        self.request = request
        self.headers = headers
    def get_size(self):
        return int(self.request.get(self.json, headers=self.headers, stream=True).headers["Content-Length"])
    def download(self, out=False):
        if isinstance(out, str):
            open(out, "wb").write(self.request.get(self.json,headers=self.headers).content)
        else:
            return BytesIO(self.request.get(self.json,headers=self.headers).content)
    def __str__(self) -> str:
        return f"<[type:video]>"
    def __repr__(self) -> str:
        return self.__str__()