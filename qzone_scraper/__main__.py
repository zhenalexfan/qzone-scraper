from .parser import QzoneShuoshuoPageParser
from .encoder import Encoder
from .spider import QzoneSpider
from .io import Writer, Reader
from .models import *
import json

dummyUser = QzoneUser(qq=123, name='Alex')

dummyPicture = QzonePicture(id='pic1', height=600, width=800, smallurl='x.jpg', url_list=['x1.jpg', 'x2.jpg', 'x3.jpg'])

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


def clear():
    import os
    os.system('rm log/response/*')
    os.system('rm out/config.json')

def test_io():
    Writer.write_file('log/response/1.txt', 'blah blah')
    Writer.log_shuoshuo_reponse('blah blah', 1, 10)


def test_encoder():
    # print(dummyShuoshuoList[0])
    # print(dummyShuoshuoList[0].__dict__.items())
    data_dict = Encoder.obj2dict(dummyShuoshuoList)
    assert isinstance(data_dict, dict) or isinstance(data_dict, list)
    print(data_dict)


def test_parser():
    with open('log/pos-0', 'r') as f:
        body = f.readline()
    # print(body)
    parser = QzoneShuoshuoPageParser()
    page = parser.parse(body)
    shuoshuo_dict = Encoder.obj2dict(page.shuoshuo_list)
    Writer.write_shuoshuo_posts(shuoshuo_dict)


def test_spider_single_page():
    spider = QzoneSpider(qq_id='565261370')
    posts = spider.get_posts_within_single_page(start=0, num=20)
    print(posts)



if __name__ == "__main__":
    # test_io()
    # test_spider_single_page()
    # test_encoder()
    test_parser()
