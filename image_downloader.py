import urllib
import requests

class ImageSpider:
    def __init__(self):
        self.posts = []
        self.headers = {
            'host': 'h5.qzone.qq.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'connection': 'keep-alive'
        }
        self.req = requests.Session()

    def scrape_images(self):
        posts_left = set(range(len(self.posts)))
        while len(posts_left) != 0:
            finished_posts = set()
            for post_idx, post in enumerate([self.posts[i] for i in posts_left]):
                if 'pic' in post.keys():
                    try:
                        for pic_idx, item in enumerate(post['pic']):
                            url = item['url1']
                            with open('images/%s-%d.jpg' % (post['tid'], pic_idx), 'wb') as f:
                                f.write(urllib.request.urlopen(url, timeout=5).read())
                                print('Finishing %s', url)
                        finished_posts.add(post_idx)
                    except Exception as e:
                        print(e)
            posts_left = posts_left - finished_posts
            print('posts_left:')

        # urls = set()
        # for post in self.posts:
        #     if 'pic' in post.keys():
        #         for item in post['pic']:
        #             urls.add(item['url1'])
        # while len(urls) != 0:
        #     finished_urls = set()
        #     for url in urls:
        #         with open('img/%s.jpg' % url[url.rfind('/')+1:], 'wb') as f:
        #             try:
        #                 f.write(urllib.request.urlopen(url, timeout=5).read())
        #                 print('Finishing %s', url)
        #                 finished_urls.add(url)
        #             except Exception as e:
        #                 print(e)
        #     urls = urls - finished_urls



# imageSpider = ImageSpider()
# imageSpider.merge_all_posts()
# imageSpider.scrape_images()