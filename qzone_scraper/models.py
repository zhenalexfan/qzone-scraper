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



# TODO: remove unused models

class QzoneCommentReplyItem(QzoneData):
    def __init__(self):
        self._replier = QzoneUser()      # 回复者
        self._replyto = QzoneUser()      # 回复对象
        self._time = ''                      # 回复时间
        self._content = ''                   # 回复内容

    def __str__(self):
        return self._time + ' ' + self._replier.name + ' reply to ' + self._replyto.name + ': ' + self._content

    def __hash__(self):
        return hash(self._content)

    @property
    def replier(self):
        return self._replier

    @replier.setter
    def replier(self, value):
        if not isinstance(value, str):
            raise TypeError('Attribute \'replier\' should be an instance of type \'str\'. '
                            'Found: %s.' % type(value))
        self._replier = value

    @property
    def replyto(self):
        return self._replyto

    @replyto.setter
    def replyto(self, value):
        if not isinstance(value, str):
            raise TypeError('Attribute \'replyto\' should be an instance of type \'str\'. '
                            'Found: %s.' % type(value))
        self._replyto = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if not isinstance(value, str):
            raise TypeError('Attribute \'time\' should be an instance of type \'str\'. '
                            'Found: %s.' % type(value))
        self._time = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise TypeError('Attribute \'content\' should be an instance of type \'str\'. '
                            'Found: %s.' % type(value))
        self._content = value


class QzoneMessageItem(QzoneData):
    def __init__(self):
        self._id = ''                       # 留言ID
        self._owner = QzoneUser()       # 主人
        self._poster = QzoneUser()      # 留言者
        self._time = ''                     # 留言时间
        self._content = ''                  # 留言内容
        self.replies = []                   # 留言回复列表

    def __str__(self):
        string = ''
        string += 'Owner: ' + str(self._owner) + '\n'
        string += 'Poster: ' + str(self._poster) + '\n'
        string += 'Time: ' + self._time + '\n'
        string += 'Content: ' + self._content + '\n'
        string += 'Replies: ' + \
            '; '.join([str(reply) for reply in self.replies]) + '\n'
        return string

    def __hash__(self):
        return hash(self._id)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, str):
            raise TypeError('Attribute \'id\' should be an instance of type \'str\'. '
                            'Found: %s.' % type(value))
        self._id = value

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if not isinstance(value, QzoneUser):
            raise TypeError('Attribute \'owner\' should be an instance of type \'QzoneUserItem\'. '
                            'Found: %s.' % type(value))
        self._owner = value

    @property
    def poster(self):
        return self._poster

    @poster.setter
    def poster(self, value):
        if not isinstance(value, QzoneUser):
            raise TypeError('Attribute \'poster\' should be an instance of type \'QzoneUserItem\'. '
                            'Found: %s.' % type(value))
        self._poster = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if not isinstance(value, str):
            raise TypeError('Attribute \'time\' should be an instance of type \'str\'. '
                            'Found: %s.' % type(value))
        self._time = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise TypeError('Attribute \'content\' should be an instance of type \'str\'. '
                            'Found: %s.' % type(value))
        self._content = value


class QzoneMessageReplyItem(QzoneData):
    def __init__(self):
        self._replier = QzoneUser()      # 回复者
        self._time = ''                      # 回复时间
        self._content = ''                   # 回复内容

    def __str__(self):
        return self._time + ' ' + self._replier.name + ' replied: ' + self._content

    def __hash__(self):
        return hash(self.content)

    @property
    def replier(self):
        return self._replier

    @replier.setter
    def replier(self, value):
        if not isinstance(value, str):
            raise TypeError('Attribute \'replier\' should be an instance of type \'str\'. '
                            'Found: %s.' % type(value))
        self._replier = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if not isinstance(value, str):
            raise TypeError('Attribute \'time\' should be an instance of type \'str\'. '
                            'Found: %s.' % type(value))
        self._time = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise TypeError('Attribute \'content\' should be an instance of type \'str\'. '
                            'Found: %s.' % type(value))
        self._content = value


class QzoneShuoshuoPage():
    def __init__(self, user_visitor=None, user_host=None, shuoshuo_list=None):
        self.user_visitor = user_visitor
        self.user_host = user_host
        self.shuoshuo_list = shuoshuo_list
    
    def __repr__(self):
        shuoshuo_strings = "\n".join([str(x) for x in self.shuoshuo_list])
        return f'QzoneShuoshuoPage({shuoshuo_strings})'
