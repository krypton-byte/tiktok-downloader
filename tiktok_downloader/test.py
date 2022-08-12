import unittest
from .scrapper import VideoInfo
from .snaptik import snaptik
from .tikmate import tikmate
from .mdown import mdown


class TikTok(unittest.TestCase):
    base_url = ('https://www.tiktok.com/' +
                '@tribunsumselcom/' +
                'video/7020708969563917595')

    def test_snaptk(self):
        self.assertTrue(bool(snaptik(self.base_url)))

    def test_info(self):
        self.assertTrue(bool(VideoInfo.get_info(self.base_url)))

    def tikmat(self):
        self.assertTrue(bool(tikmate(self.base_url)))

    def mdown_(self):
        self.assertTrue(bool(mdown(self.base_url)))


if __name__ == '__main__':
    unittest.main()
