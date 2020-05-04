import unittest
from ..io import Writer, Reader, ImageDownloader
from ..models import *

class IoTest(unittest.TestCase):
    def test_download_qzone_picture(self):
        pic = QzonePicture()
        pic.id = "httpb290.photo.store.qq.com/psb?/082ef04e-fa8f-4559-81c7-b6044e75fb36/BUM3ainbRyfIlrEIhSCXShwfsoviEdY*2aXkuBGXJbQ!/b/dCIBAAAAAAAA&bo=OASABwAAAAAREJw!"
        pic.height = 1920
        pic.width = 1080
        pic.smallurl = "http://b290.photo.store.qq.com/psb?/082ef04e-fa8f-4559-81c7-b6044e75fb36/BUM3ainbRyfIlrEIhSCXShwfsoviEdY*2aXkuBGXJbQ!/b/dCIBAAAAAAAA&bo=OASABwAAAAAREJw!"
        pic.url_list = [
            "http://b290.photo.store.qq.com/psb?/082ef04e-fa8f-4559-81c7-b6044e75fb36/BUM3ainbRyfIlrEIhSCXShwfsoviEdY*2aXkuBGXJbQ!/b/dCIBAAAAAAAA&bo=OASABwAAAAAREJw!",
            "http://b290.photo.store.qq.com/psb?/082ef04e-fa8f-4559-81c7-b6044e75fb36/BUM3ainbRyfIlrEIhSCXShwfsoviEdY*2aXkuBGXJbQ!/b/dCIBAAAAAAAA&bo=OASABwAAAAAREJw!",
            "http://b290.photo.store.qq.com/psb?/082ef04e-fa8f-4559-81c7-b6044e75fb36/BUM3ainbRyfIlrEIhSCXShwfsoviEdY*2aXkuBGXJbQ!/b/dCIBAAAAAAAA&bo=OASABwAAAAAREJw!"
        ]
        img_downloader = ImageDownloader()
        img_downloader.download_qzone_picture(picture=pic)
        img_downloader.write_image_history_map()
