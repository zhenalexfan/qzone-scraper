from selenium import webdriver
from urllib import parse
import urllib
import requests
import os
import json
import math
from .parser import QzoneShuoshuoPageParser
from .models import *
from .io import Writer, Reader, ImageDownloader, logger


class QzoneSpider:
    def __init__(self, qq_id, download_pics=False):
        logger.info(f'Initiating with QQ [{qq_id}]')
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.headers = {
            'host': 'h5.qzone.qq.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'connection': 'keep-alive'
        }
        self.req = requests.Session()
        self.download_pics = download_pics
        self.image_downloader = ImageDownloader()
        self.qq_id = qq_id
        self.qq_password = None
        self.cookies = None
        self.g_tk = None
        if self._login_needed():
            self._log_in()

    def _login_needed(self):
        config = Reader.read_config()
        if config is None:
            return True
        uin, cookies, g_tk = config
        if uin != self.qq_id or cookies is None or g_tk is None:
            return True
        self.cookies = cookies
        self.headers['cookie'] = self.cookies
        self.g_tk = g_tk
        logger.debug(f'self.cookies = {self.cookies}')
        logger.debug(f'self.g_tk = {self.g_tk}')
        return False

    def _log_in(self):
        '''
        Log into Qzone and calculate g_tk
        :return: None
        '''
        logger.info('Launching Qzone in Chrome. Please wait...')
        self.driver.get('https://i.qq.com/')
        self.driver.switch_to.frame('login_frame')
        self.driver.find_element_by_id('switcher_plogin').click()
        assert self.qq_id != None
        self.driver.find_element_by_id('u').clear()
        self.driver.find_element_by_id('u').send_keys(self.qq_id)
        input('Please log in with your username and password. Press any key after loggin in...')
        self.driver.get('http://user.qzone.qq.com/{}'.format(self.qq_id))
        # getting cookie
        cookie = ''
        for item in self.driver.get_cookies():
            cookie += item["name"] + '=' + item['value'] + ';'
        self.cookies = cookie
        self.headers['cookie'] = self.cookies
        # getting g_tk
        self._get_g_tk()
        # save cookie and g_tk to file
        Writer.write_config(
            uin=self.qq_id, cookie=self.cookies, g_tk=self.g_tk)
        self.driver.quit()

    def _get_g_tk(self):
        """
        :return: g_tk
        """
        p_skey = self.cookies[
            self.cookies.find('p_skey=') + 7: self.cookies.find(';', self.cookies.find('p_skey='))]
        h = 5381
        for i in p_skey:
            h += (h << 5) + ord(i)
        print('g_tk', h & 2147483647)
        self.g_tk = h & 2147483647
        return self.g_tk

    def get_posts_within_single_page(self, start=0, num=20, replynum=100,):
        """Get a list of Posts in a page that has an offset of {start} and a limit of {num}
        """
        url = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?'
        params = {
            'inCharset': 'utf-8',
            'outCharset': 'utf-8',
            'uin': self.qq_id,
            'ftype': 0,
            'sort': 0,
            'pos': start,
            'num': num,
            'replynum': replynum,
            'callback': '_preloadCallback',
            'code_version': 1,
            'format': 'jsonp',
            'need_private_comment': 1,
            'g_tk': self.g_tk
        }
        url = url + parse.urlencode(params)
        posts_response = self.req.get(url=url, headers=self.headers)
        posts_body = posts_response.text
        if '\"message\":\"请先登录空间\"' in posts_body:
            logger.error(
                f'Failed scraping posts ({start}–{start + num}): {posts_body}')
            raise ConnectionError('Not logged in')
        # TODO: save reponse body to file
        Writer.log_shuoshuo_reponse(
            data=posts_body, start=start, end=start + num)
        # parse response body
        try:
            page: QzoneShuoshuoPage = QzoneShuoshuoPageParser().parse(posts_body)
            shuoshuo_list = page.shuoshuo_list
            if self.download_pics:
                self.image_downloader.download_pictures_in_shuoshuo_list(shuoshuo_list=shuoshuo_list)
            return shuoshuo_list
        except:
            logger.error(f'Error parsing posts ({start}–{start + num})')
            return list()

    def get_posts(self, num_posts,):
        limit_per_page = 20
        limit_of_reply = 100
        posts = []
        num_pages = int(math.ceil(num_posts / limit_per_page))
        for pos in [limit_per_page * i for i in range(num_pages)]:
            logger.info(f'Scraping posts ({pos}—{pos + limit_per_page})...')
            try:
                page_posts = self.get_posts_within_single_page(
                    start=pos, num=limit_per_page, replynum=limit_of_reply)
            except ConnectionError:
                self._log_in()
                page_posts = self.get_posts_within_single_page(
                    start=pos, num=limit_per_page, replynum=limit_of_reply)
            posts.extend(page_posts)
        if self.download_pics:
            self.image_downloader.write_image_history_map()
        return posts


