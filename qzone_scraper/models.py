import json


class QzoneData():
    pass


class QzoneUser(QzoneData):
    def __init__(self, qq=None, name=None):
        self.qq = qq
        self.name = name

    def __repr__(self):
        return f'User({self.name}[{self.qq}])'

    def __hash__(self):
        return hash(self.qq)

class QzonePicture(QzoneData):
    def __init__(self, id=None, height=None, width=None, smallurl=None, url_list=[]):
        self.id = None
        self.height = height
        self.width = width
        self.smallurl = smallurl
        self.url_list = url_list


class QzoneShuoshuo(QzoneData):
    def __init__(self, id=None, owner=None, time=None, 
            content=None, pictures=None,
            source=None, location=None, 
            visitors=None, likers=None, comments=None):
        self.id = id
        self.owner = owner
        self.time = time
        self.content = content
        self.pictures = pictures
        self.source = source      # Device name (str)
        self.location = location    # Location (str)
        self.visitors = visitors
        self.likers = likers
        self.comments = comments

    def __repr__(self):
        return f'QzoneShuoshuo(#{self.id} @{self.owner}: "{self.content}")'

    def __hash__(self):
        return hash(self.id)


class QzoneRepostShuoshuo(QzoneShuoshuo):
    def __init__(self):
        QzoneShuoshuo.__init__(self)
        self._repost_source = QzoneUser()    # 转发来源
        self._repost_reason = ''                 # 转发理由

    def __str__(self):
        string = QzoneShuoshuo.__str__(self)
        string += 'Repost Source: ' + str(self._repost_source) + '\n'
        string += 'Repost Reason: ' + self._repost_reason + '\n'
        return string

    def __hash__(self):
        return hash(self.id)


class QzoneShuoshuoComment(QzoneData):
    def __init__(self, commenter=None, time=None, content=None, pictures=None, replies=None):
        self.commenter = commenter
        self.time = time
        self.content = content
        self.pictures = pictures
        self.replies = replies

    def __str__(self):
        return f'QzoneShuoshuoComment(@{self.commenter}: "{self.content}")'

    def __hash__(self):
        return hash(self.content)


class QzoneShuoshuoPage():
    def __init__(self, user_visitor=None, user_host=None, shuoshuo_list=None):
        self.user_visitor = user_visitor
        self.user_host = user_host
        self.shuoshuo_list = shuoshuo_list
    
    def __repr__(self):
        shuoshuo_strings = "\n".join([str(x) for x in self.shuoshuo_list])
        return f'QzoneShuoshuoPage({shuoshuo_strings})'
