import re
import json
from .models import *

class Parser():
    def parse(self, body):
        json_dict = json.loads(body)
        return self.parse_json(json_dict)

    def parse_json(self, json_dict):
        pass


class QzoneUserParser(Parser):
    def parse_json(self, json_dict):
        name = json_dict['name']
        uin = json_dict['uin']
        return QzoneUser(name=name, qq=uin)


class QzonePictureParser(Parser):
    def parse_json(self, json_dict):
        picture = QzonePicture()
        picture.id = json_dict['pic_id']
        picture.height = json_dict['height']
        picture.width = json_dict['width']
        picture.smallurl = json_dict['smallurl']
        picture.url_list = [json_dict['url1'],
                            json_dict['url2'], json_dict['url3']]
        return picture


class CommentParser(Parser):
    def __init__(self):
        self.user_parser = QzoneUserParser()
        self.pic_parser = QzonePictureParser()

    def parse_json(self, json_dict):
        # TODO: parse into QzoneShuoshuoComment
        comment = QzoneShuoshuoComment()
        comment.commenter = self.user_parser.parse_json(json_dict)
        comment.content = json_dict['content']
        comment.time = json_dict['create_time']
        # TODO: pictures
        # replies
        replies_data = json_dict.get('list_3')
        if (replies_data):
            comment.replies = [self.parse_json(item) for item in replies_data]
        return comment


class QzoneShuoshuoParser(Parser):
    def __init__(self):
        self.user_parser = QzoneUserParser()
        self.pic_parser = QzonePictureParser()
        self.comment_parser = CommentParser()
    
    def parse_json(self, json_dict):
        shuoshuo = QzoneShuoshuo()
        shuoshuo.id = json_dict['tid']
        shuoshuo.owner = self.user_parser.parse_json(json_dict)
        shuoshuo.content = json_dict['content']
        shuoshuo.time = json_dict['created_time']
        shuoshuo.source = json_dict['source_name']
        # pictures
        picture_dicts = json_dict.get('pic')
        if picture_dicts:
            shuoshuo.pictures = [self.pic_parser.parse_json(
                item) for item in picture_dicts]
        # comments
        comment_dicts = json_dict.get('commentlist')
        if comment_dicts:
            shuoshuo.comments = [self.comment_parser.parse_json(item) for item in comment_dicts]
        return shuoshuo


class QzoneShuoshuoPageParser(Parser):
    def __init__(self):
        self.user_parser = QzoneUserParser()
        self.post_parser = QzoneShuoshuoParser()

    def parse(self, body):
        regex = r'^_preloadCallback\((.*)\);$'
        _posts_json_data = re.search(regex, body, re.DOTALL).group(1)
        posts_data = json.loads(_posts_json_data)
        return self.parse_json(posts_data)
        
    
    def parse_json(self, json_dict):
        user_visitor = self.user_parser.parse_json(json_dict['logininfo'])
        user_host = self.user_parser.parse_json(json_dict['usrinfo'])
        posts = [self.post_parser.parse_json(item)
                 for item in json_dict['msglist']]
        return QzoneShuoshuoPage(user_host=user_host, user_visitor=user_visitor, shuoshuo_list=posts)
    

