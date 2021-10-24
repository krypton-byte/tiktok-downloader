<p align="center">
<img src="tiktok_downloader/static/tiktok.svg"><br>
<img src="https://img.shields.io/badge/AUTHOR-KRYPTON--BYTE-brightgreen">
</p>

[![Unittest](https://github.com/krypton-byte/tiktok-downloader/actions/workflows/unittest.yml/badge.svg)](https://github.com/krypton-byte/tiktok-downloader/actions/workflows/unittest.yml)

[![Upload to PyPi](https://github.com/krypton-byte/tiktok-downloader/actions/workflows/python-publish.yml/badge.svg?branch=0.1.7&event=release)](https://github.com/krypton-byte/tiktok-downloader/actions/workflows/python-publish.yml)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)&nbsp;

[![Downloads](https://static.pepy.tech/personalized-badge/tiktok-downloader?period=total&units=none&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/tiktok-downloader)&nbsp;[![viitor](https://visitor-badge.glitch.me/badge?page_id=krypton-byte.tiktok-downloader)]()
# install

```bash
> python3 -m pip install tiktok_downloader
> python3 -m pip install git+https://github.com/krypton-byte/tiktok-downloader
```

<ul>
<li><h2> ssstik</h2></li>

```python
>>> from tiktok_downloader import ssstik
>>> ssstik().get_media("url")
[<[type:video]>, <[type:music]>]
>>> ssstik().get_media("url")[0].download("result.mp4")
```

<li><h2> snaptik</h2></li>

```python
>>> from tiktok_downloader import snaptik
>>>snaptik("url").get_media()
[<[type:video]>, <[type:video]>]
>>> snaptik("url").get_media()[0].download("result.mp4")
```
<li><h2> get info </h2></li>

```python
>>> from tiktok_downloader import info_video
>>> info=info_video("url")
>>> info.caption
>>> info.created
>>> info.id
>>> info.music
>>> info.username
>>> info.created
>>> info.signature
>>> info.verified
```
</ul>

# Command line
<ul>
<li>ssstik</li>

```bash
$ python3 -m tiktok_downloader --url=https://www.tiktok.com/@xxxx/video/xxxx --ssstik 2>/dev/null

[
    {
        "type": "video",
        "url": "https://ssstik.io/fe67718b?url=xxxxxx"
    },
    {
        "type": "video",
        "url": "https://v16m.tiktokcdn.com/xxxxxxxx"
    },
    {
        "type": "music",
        "url": "https://sf16-ies-music-sg.tiktokcdn.com/obj/tos-alisg-ve-xxxx/xxxxxx"
    }
]

```

<li>snaptik</li>

```bash
$ python3 -m tiktok_downloader --url=https://www.tiktok.com/@xxxx/video/xxxx --snaptik 2>/dev/null
[
    {
        "type": "video",
        "url": "https://tikcdn.net/file/xxxxxxxx.mp4"
    },
    {
        "type": "video",
        "url": "https://snapsave.info/dl.php?token=xxxxxxxxxxxxxxx"
    }
]

```

<li> post info</li>

```bash
$ python3 -m tiktok_downloader --url=https://www.tiktok.com/@xxxx/video/xxxx --info
{
    "account": {
        "username": "",
        "nickname": "",
        "signatur": "",
        "create": 0,
        "verified": true
    },
    "music": "",
    "caption": "",
    "create": 0,
    "url": "",
    "id": ""
}
```
</ul>

# Run as web

```bash
$ python3 -m tiktok_downloader --host=0.0.0.0 --port=8000 --server
```
## Preview
<img src="image/web.png">


# Donasi
<p align="center"><img src="https://svgur.com/i/Vtt.svg">

</p>
<ul><li><a href="https://saweria.co/kryptonbyte">Saweria</a><li><a href="https://wa.me/6283172366463">Whatsapp</a></li><li><a href="https://trakteer.id/krypton-byte-z8vbo">Trakteer</a></li></ul>
