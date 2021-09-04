<p align="center">
<img src="https://avatars.githubusercontent.com/u/52121207" width="25%"><br>
<img src="https://img.shields.io/badge/AUTHOR-KRYPTON--BYTE-brightgreen">
</p>

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# install
```bash
> python3 -m pip install tiktok_downloader
> python3 -m pip install git+https://github.com/krypton-byte/tiktok-downloader
```
# ssstik
```python
>>> from tiktok_downloader import Tiktok
>>> Tiktok.ssstik("url").get_info()
[<[type:video]>, <[type:video]>]
>>> Tiktok.ssstik("url").get_info()[0].download("result.mp4")
```
# snaptik
```python
>>> from tiktok_downloader import Tiktok
>>> Tiktok().snaptik("url").get_info()
[<[type:video]>, <[type:video]>]
>>> Tiktok.snaptik("url").get_info()[0].download("result.mp4")
```
# keeptiktok
```python
>>> from tiktok_downloader import Tiktok
>>> Tiktok.keeptiktok("url").get_info()
[<[type:video]>, <[type:video]>]
>>> Tiktok.keeptiktok("url").get_info()[0].download("result.mp4")
```
# get info video
```python
>>> from tiktok_downloader import Tiktok
>>> info=Tiktok.info_video("url")
>>> info.caption
>>> info.created
>>> info.id
>>> info.music
>>> info.username
>>> info.created
>>> info.signature
>>> info.verified
```
# Donasi
<p align="center"><img src="https://svgur.com/i/Vtt.svg">

</p>
<ul><li><a href="https://saweria.co/kryptonbyte">Saweria</a><li><a href="https://wa.me/6283172366463">Whatsapp</a></li><li><a href="https://trakteer.id/krypton-byte-z8vbo">Trakteer</a></li></ul>
