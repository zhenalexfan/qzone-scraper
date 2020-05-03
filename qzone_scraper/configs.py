# qzone configurations
qzone_emotion_url = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?' \
                    'uin={qq}&ftype=0&sort=0&pos={pos}&num=20&replynum=100&g_tk={gtk}&callback=_preloadCallback' \
                    '&code_version=1&format=jsonp&need_private_comment=1'
qzone_comment_url = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msgdetail_v6?' \
                    'uin={qq}&tid={tid}&ftype=0&sort=0&pos=0&num={num}&g_tk={gtk}&callback=_preloadCallback' \
                    '&code_version=1&format=jsonp&need_private_comment=1'
qzone_like_url = 'https://user.qzone.qq.com/proxy/domain/users.qzone.qq.com/cgi-bin/likes/get_like_list_app?' \
                 'uin={qq1}&unikey=http%3A%2F%2Fuser.qzone.qq.com%2F{qq2}%2Fmood%2F{id}.1&begin_uin=0' \
                 '&query_count=100&if_first_page=1&g_tk={gtk}'
qzone_visitor_url = 'https://h5.qzone.qq.com/proxy/domain/g.qzone.qq.com/cgi-bin/friendshow' \
                    '/cgi_get_visitor_single?uin={qq}&appid=311&blogid={id1}&param={id2}&ref=qzfeeds' \
                    '&beginNum=1&needFriend=1&num=500&g_tk={gtk}'
qzone_message_url = 'https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin={qq1}' \
                    '&hostUin={qq2}&start={pos}&format=jsonp&num=10&inCharset=utf-8&outCharset=utf-8&g_tk={gtk}'
qzone_header = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Referer': 'https://qzs.qq.com/qzone/app/mood_v6/html/index.html'
}
