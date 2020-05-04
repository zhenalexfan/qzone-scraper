import unittest
from ..parser import *
from ..spider import QzoneSpider
from ..encoder import Encoder
from ..io import Writer

dummyUser = QzoneUser(qq=123, name='Alex')

dummyPicture = QzonePicture(id='pic1', height=600, width=800,
                            smallurl='x.jpg', url_list=['x1.jpg', 'x2.jpg', 'x3.jpg'])

dummyShuoshuoList = [
    QzoneShuoshuo(
        id=1,
        owner=dummyUser,
        time=123,
        content='content',
        pictures=[dummyPicture],
        source='iPhone XR',
        location='Los Angeles',
        visitors=None,
        likers=[dummyUser],
        comments=None
    )
]


class IntegrationTest(unittest.TestCase):
    def test_parse_encode_write(self):
        with open('log/reponse/shuoshuo_reponse_0_20.txt', 'r') as f:
            body = f.readline()
        # print(body)
        parser = QzoneShuoshuoPageParser()
        page = parser.parse(body)
        shuoshuo_dict = Encoder.obj2dict(page.shuoshuo_list)
        Writer.write_shuoshuo_posts(shuoshuo_dict)

    def test_spider_single_page(self):
        spider = QzoneSpider(qq_id='565261370')
        posts = spider.get_posts_within_single_page(start=0, num=20)
        print(posts)

