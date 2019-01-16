import qq_init as init
from selenium import webdriver
from urllib import parse
import urllib
import requests
import os
import json
import math

PATH_POST = 'qzone-posts/'

class QzoneSpider:
    def __init__(self):
        '''
        初始化
        '''
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get('https://i.qq.com/')
        self.__username = init.QQ
        self.__password = init.PASSWORD
        self.headers = {
            'host': 'h5.qzone.qq.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'connection': 'keep-alive'
        }
        self.req = requests.Session()
        self.cookies = ''

    def login(self):
        '''
        登录、调用get_g_tk()、get_friends()函数
        :return:
        '''
        self.driver.switch_to.frame('login_frame')
        self.driver.find_element_by_id('switcher_plogin').click()
        self.driver.find_element_by_id('u').clear()
        self.driver.find_element_by_id('u').send_keys(self.__username)
        self.driver.find_element_by_id('p').clear()
        self.driver.find_element_by_id('p').send_keys(self.__password)
        self.driver.find_element_by_id('login_button').click()
        self.driver.get('http://user.qzone.qq.com/{}'.format(self.__username))
        cookie = ''
        for item in self.driver.get_cookies():
            cookie += item["name"] + '=' + item['value'] + ';'
        print('Cookie got! Saved to cookie/cookie.txt')
        print(cookie)
        with open('cookie/cookie.txt', 'w') as f:
            f.write(cookie)
        self.cookies = cookie
        self.headers['cookie'] = self.cookies
        self.get_g_tk()
        self.driver.quit()

    def get_g_tk(self):
        """
        获取g_tk()
        :return: 生成的g_tk
        """
        p_skey = self.cookies[
                 self.cookies.find('p_skey=') + 7: self.cookies.find(';', self.cookies.find('p_skey='))]
        h = 5381
        for i in p_skey:
            h += (h << 5) + ord(i)
        print('g_tk', h & 2147483647)
        self.g_tk = h & 2147483647
        return self.g_tk

    def write_all_post_json(self):
        if not os.path.exists(PATH_POST):
            os.makedirs(PATH_POST)
        num_pages = int(math.ceil(init.NUM_POST / 20))
        num_pages = 2
        for pos in [20*i for i in range(num_pages)]:
            print('Start: pos=%d' % pos)
            url = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?'
            params = {
                'inCharset': 'utf-8',
                'outCharset': 'utf-8',
                'uin': init.QQ,
                'ftype': 0,
                'sort': 0,
                'pos': pos,
                'num': 20,
                'replynum': 100,
                'callback': '_preloadCallback',
                'code_version': 1,
                'format': 'jsonp',
                'need_private_comment': 1,
                'g_tk': self.get_g_tk()
            }
            url = url + parse.urlencode(params)
            posts = self.req.get(url=url, headers=self.headers)
            if '\"message\":\"请先登录空间\"' in posts.text:
                print('pos=%d: FAILED.' % pos)
            else:
                with open(PATH_POST + 'pos-%d' % pos, 'w') as f:
                    f.write(posts.text)
                print('pos=%d: SUCCESSFUL.' % pos)


def merge_all_posts():
    posts = []
    for filename in os.listdir(PATH_POST):
        with open(PATH_POST + filename, 'r') as f:
            data = f.read()[17:-2]
        obj = json.loads(data)
        msglist = obj.get('msglist')
        if type(msglist) == list:
            posts += msglist
    posts = sorted(posts, key=lambda k: k['created_time'])
    return posts


if __name__ == '__main__':
    spider = QzoneSpider()
    spider.login()
    spider.write_all_post_json()
