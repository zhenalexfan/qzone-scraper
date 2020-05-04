import sys
import os
from hashlib import md5
from pathlib import Path
import json
import logging
import requests
from .encoder import Encoder
from .models import *

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(name='qzone_scraper')
logger.addHandler(logging.FileHandler('log/qzone_scraper.log'))
logger.setLevel(level=logging.INFO)

FILE_CONFIG = 'out/config.json'
FILE_SHUOSHUO_LIST = 'out/shuoshuo_list.json'
FILE_IMAGE = lambda image_file : f'out/img/{image_file}'
FILE_IMAGE_HISTORY = 'out/img/download.json'
FILE_POST_RESPONSE_BODY = lambda start, end : f'log/response/shuoshuo_response_{start}_{end}.txt'


class Writer():
    @staticmethod
    def write_file(filename, data):
        dir_path = os.path.dirname(filename)
        if not os.path.exists(dir_path):
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        with open(filename, 'w') as f:
            f.write(data)

    @staticmethod
    def write_config(uin, cookie, g_tk):
        logger.info(
            f'Writing config (uin={uin}, g_tk={g_tk}, etc.) to file `{FILE_CONFIG}`...')
        data = {
            'uin': uin,
            'cookie': cookie,
            'g_tk': g_tk
        }
        with open(FILE_CONFIG, 'w') as f:
            json.dump(data, fp=f)
    
    @staticmethod
    def write_shuoshuo_posts(shuoshuo):
        shuoshuo_dict = Encoder.obj2dict(shuoshuo)
        logger.info(
            f'Writing shuoshuo list to file `{FILE_SHUOSHUO_LIST}`')
        Writer.write_file(FILE_SHUOSHUO_LIST, json.dumps(shuoshuo_dict))

    @staticmethod
    def log_shuoshuo_reponse(data, start, end):
        filepath = FILE_POST_RESPONSE_BODY(start, end)
        logger.info(
            f'Writing shuoshuo response {start}–{end} to file `{filepath}`')
        Writer.write_file(filepath, data)


class Reader():
    @staticmethod
    def read_config():
        if not os.path.exists(FILE_CONFIG):
            return None
        with open(FILE_CONFIG, 'r') as f:
            data = json.load(fp=f)
        logger.info(f'restoring configs: {data}')
        return (data['uin'], data['cookie'], data['g_tk'])

    @staticmethod
    def read_shuoshuo_response_log(fp):
        with open(fp, 'r') as f:
            data = f.read()
        return data 


class ImageDownloader():
    def __init__(self):
        self.headers = {
            'host': 'h5.qzone.qq.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'connection': 'keep-alive'
        }
        self.req = requests.Session()
        self.history = {'success': {}, 'error': {}}

    @staticmethod
    def if_exits(fp):
        if os.path.isfile(fp):
            if os.stat(fp).st_size > 0:
                return True
        return False

    def download_image(self, name, url, fp):
        logger.debug(f'Downloading image to `{fp}` from `{url}`')
        # check existance
        if ImageDownloader.if_exits(fp):
            logger.warning(f'Skip file as it exists: `{fp}`')
            return
        # download
        dir_path = os.path.dirname(fp)
        if not os.path.exists(dir_path):
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        try:
            with open(fp, 'wb') as f:
                img_data = self.req.get(url, stream=True, timeout=10).content
                f.write(img_data)
            if name not in self.history['success']:
                self.history['success'][name] = dict()
            self.history['success'][name][url] = fp
        except:
            if name not in self.history['error']:
                self.history['error'][name] = dict()
            self.history['error'][name][url] = fp
    
    def download_qzone_picture(self, picture: QzonePicture):
        name = None
        if picture.id is not None:
            name = md5(picture.id.encode()).hexdigest()
        elif picture.smallurl is not None:
            name = md5(picture.smallurl.encode()).hexdigest()
        elif picture.url_list is not None and picture.url_list[0] is not None:
            name = md5(picture.url_list[0].encode()).hexdigest()
        else:
            logger.error(f'Cannot generate a name for picture {picture}')
            return
        file_dir = FILE_IMAGE(name)
        # construct all urls with names
        logger.debug(f'picture.smallurl = `{picture.smallurl}`')
        urls = dict()
        urls_set = set()
        if picture.smallurl:
            urls['0'] = picture.smallurl
            urls_set.add(picture.smallurl)
        for i, url in enumerate(picture.url_list):
            if url in urls_set:
                continue
            url_name = str(i + 1)
            urls[url_name] = url
        logger.debug(f'urls = {urls}')
        # download from all urls
        for filename, url in urls.items():
            fp = os.path.join(file_dir, f'{filename}.jpg')
            self.download_image(name=name, url=url, fp=fp)

    def write_image_history_map(self):
        dir_path = os.path.dirname(FILE_IMAGE_HISTORY)
        if not os.path.exists(dir_path):
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        with open(FILE_IMAGE_HISTORY, 'w') as f:
            json.dump(self.history, fp=f)

    def download_pictures_in_shuoshuo_list(self, shuoshuo_list: list):
        length = len(shuoshuo_list)
        for i, shuoshuo in enumerate(shuoshuo_list):
            if shuoshuo.pictures is None:
                logger.debug(f'[{i}/{length}] No picture found')
                continue
            logger.info(f'[{i}/{length}] Downloading {len(shuoshuo.pictures)} pictures in {shuoshuo}')
            for pic in shuoshuo.pictures:
                self.download_qzone_picture(pic)
