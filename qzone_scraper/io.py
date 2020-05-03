import sys
import os
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(name='qzone_scraper')
logger.setLevel(level=logging.DEBUG)

FILE_CONFIG = 'out/config.json'
FILE_SHUOSHUO_LIST = 'out/shuoshuo_list.json'
FILE_POST_RESPONSE_BODY = lambda start, end : f'log/response/shuoshuo_reponse_{start}_{end}.txt'


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
    def write_shuoshuo_posts(shuoshuo_dict):
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
