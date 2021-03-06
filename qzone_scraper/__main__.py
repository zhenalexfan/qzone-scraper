from .parser import QzoneShuoshuoPageParser
from .encoder import Encoder
from .spider import QzoneSpider
from .io import Writer, Reader, ImageDownloader, logger
from .models import *
import os
import json

NAME = 'qzone-scraper'


def check_cwd():
    cwd = os.getcwd()
    try:
        assert os.path.basename(cwd) == NAME
    except Exception as e:
        logger.error(
            f'Current working directory is not `{NAME}`. Please go to the root path of `{NAME}/`')
        logger.debug(f'cwd = {cwd}')
        logger.debug(f'basename(cwd) = {os.path.basename(cwd)}')
        raise e


def clear():
    check_cwd()
    if not (os.path.exists('log/') or os.path.exists('out/')):
        return
    confirm = input(
        'Are you sure you want to clear all the outputs, logs, and configs (log/*, out/*)? [Y/N]\n')
    if (confirm.upper() != 'Y'):
        return
    if not os.path.exists('log/'):
        os.makedirs('log/')
    if not os.path.exists('out/'):
        os.makedirs('out/')
    os.system('rm -r log/*')
    os.system('rm -r out/*')


def scrape(qq, num_posts, download_pics=False):
    spider = QzoneSpider(qq_id=qq, download_pics=download_pics)
    posts = spider.get_posts(num_posts=num_posts)
    Writer.write_shuoshuo_posts(posts)


def parse_from_log_response():
    parser = QzoneShuoshuoPageParser()
    posts = []
    dir = 'log/response/'
    logger.info(f'Start parse shuoshuo from {dir} files')
    for filename in os.listdir(dir):
        data = Reader.read_shuoshuo_response_log(os.path.join(dir, filename))
        page_posts = parser.parse(data).shuoshuo_list
        posts.extend(page_posts)
    Writer.write_shuoshuo_posts(posts)
    # download images
    img_downloader = ImageDownloader()
    logger.info(f'Start downloading images from {len(posts)} posts')
    img_downloader.download_pictures_in_shuoshuo_list(posts)
    img_downloader.write_image_history_map()


if __name__ == "__main__":
    check_cwd()
    clear()
    qq = input('What\'s your QQ number?\n')
    _num_of_posts = input('How many Shuoshuos do you have in total?\n')
    num_of_posts = int(_num_of_posts)
    _download_pics = input('Do you want to download pictures in your Shuoshuos?\n')
    dl_pics = _download_pics.upper().startswith('Y')
    scrape(qq=qq, num_posts=num_of_posts, download_pics=dl_pics)
