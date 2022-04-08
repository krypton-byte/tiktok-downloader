from .snaptik import snaptik, Snaptik
from .ssstik import ssstik, Ssstik
from .scrapper import info_post
from .tikmate import tikmate, Tikmate
from .mdown import mdown, Mdown
from .Except import InvalidUrl
from .ttdownloader import ttdownloader
from .tikdown import TikDown

__all__ = [
    'snaptik',
    'ssstik',
    'info_post',
    'tikmate',
    'mdown',
    'InvalidUrl',
    'ttdownloader',
    'TikDown'
]
services = {
    'snaptik': Snaptik,
    'ssstik': Ssstik,
    'tikmate': Tikmate,
    'mdown': Mdown,
    'ttdownloader': ttdownloader,
    'tikdown': TikDown,
    'tiktok': info_post.service
}
