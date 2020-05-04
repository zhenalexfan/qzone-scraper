import unittest
from ..parser import *
from ..encoder import Encoder

class ParserTest(unittest.TestCase):
    def test_qzone_shuoshuo_page_test(self):
        with open('log/response/shuoshuo_reponse_0_20.txt', 'r') as f:
            body = f.readline()
            # print(body)
        parser = QzoneShuoshuoPageParser()
        page = parser.parse(body)
        shuoshuo_dict = Encoder.obj2dict(page.shuoshuo_list)
        print(shuoshuo_dict[:2])
