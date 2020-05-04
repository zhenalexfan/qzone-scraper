import unittest
from ..encoder import *
from ..models import *

class EncoderTest(unittest.TestCase):
    def test_dict2obj(self):
        pic = {
            "id": "http://b290.photo.store.qq.com/psb?/082ef04e-fa8f-4559-81c7-b6044e75fb36/BUM3ainbRyfIlrEIhSCXShwfsoviEdY*2aXkuBGXJbQ!/b/dCIBAAAAAAAA&bo=OASABwAAAAAREJw!",
            "height": 1920,
            "width": 1080,
            "smallurl": "http://b290.photo.store.qq.com/psb?/082ef04e-fa8f-4559-81c7-b6044e75fb36/BUM3ainbRyfIlrEIhSCXShwfsoviEdY*2aXkuBGXJbQ!/b/dCIBAAAAAAAA&bo=OASABwAAAAAREJw!",
            "url_list": [
                "http://b290.photo.store.qq.com/psb?/082ef04e-fa8f-4559-81c7-b6044e75fb36/BUM3ainbRyfIlrEIhSCXShwfsoviEdY*2aXkuBGXJbQ!/b/dCIBAAAAAAAA&bo=OASABwAAAAAREJw!",
                "http://b290.photo.store.qq.com/psb?/082ef04e-fa8f-4559-81c7-b6044e75fb36/BUM3ainbRyfIlrEIhSCXShwfsoviEdY*2aXkuBGXJbQ!/b/dCIBAAAAAAAA&bo=OASABwAAAAAREJw!",
                "http://b290.photo.store.qq.com/psb?/082ef04e-fa8f-4559-81c7-b6044e75fb36/BUM3ainbRyfIlrEIhSCXShwfsoviEdY*2aXkuBGXJbQ!/b/dCIBAAAAAAAA&bo=OASABwAAAAAREJw!"
            ]
        }
        obj = Encoder.dict2obj(pic, dtype=QzonePicture)
        print(obj)
        assert obj.id is not None