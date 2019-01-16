import qq_init as init
import os
import json
import datetime
import re
from qzone_spider import merge_all_posts


class PostToLatex:
    def __init__(self, posts):
        self.posts = posts
        self.posts = sorted(self.posts, key=lambda k: k['created_time'], reverse=True)

    @staticmethod
    def convert_at_somebody(string):
        ats = re.finditer(r'@{.*nick:(.*),who.*?}', string)
        for at in ats:
            string = string.replace(at.group(0), '@'+at.group(1)+' ')
        return string

    @staticmethod
    def convert_emojicon(string):
        return re.sub(r'\[em\].*?\[/em\]', '[表情]', string)

    @staticmethod
    def preprocess(string):
        string = PostToLatex.convert_at_somebody(string)
        string = PostToLatex.convert_emojicon(string)
        return string

    @staticmethod
    def postprocess(string):
        # \, {,}
        # $, &,  # , ^, _, ~, %
        map = {' ':'\ ', '{':'\{', '}':'\}',
               '$':'\$', '&':'\&', '#':'\#',
               '_':r'\textunderscore ', '^':r'\textasciicircum ',
               '%':'\%', '[':r'\lbrack ', ']':r'\rbrack '}
        for key in map:
            string = string.replace(key, map[key])
        string = string.replace('\n', r'\\')
        return string

    @staticmethod
    def latex_block(string):
        string = PostToLatex.preprocess(string)
        # string = '\\begin{simplechar}%s\\end{simplechar}' % string
        string = PostToLatex.postprocess(string)
        return string

    @staticmethod
    def latex_v(string):
        string = PostToLatex.preprocess(string).replace('\n', '')
        # string = '\\verb|%s|' % string
        string = PostToLatex.postprocess(string)
        return string

    def get_post_latex(self, post):
        post_title = r'{\bf %s} \hfill {\tiny %s}\\[2pt]' \
                     % (post['name'],
                        datetime.datetime.fromtimestamp(post['created_time']).strftime('%Y年%m月%d日 %H:%M:%S'))
        post_content = r'%s ' % (self.latex_block(post['content']))
        post_rt = ''
        if 'rt_con' in post.keys():
            post_rt += r'\begin{addmargin}[2em]{2em}'
            if 'rt_uinname' in post.keys():
                post_rt += r'{\bf %s} \hfill {\tiny %s}\\[2pt]' \
                         % (post['rt_uinname'], post['rt_createTime'])
            post_rt += r'%s' % (self.latex_block(post['rt_con']['content']))
            post_rt += (r'\end{addmargin}' + '\n')
        post_divider = (r'\vspace{1em} \hrule \vspace{1em}' + '\n')
        post_comment = ''
        if 'commentlist' in post.keys():
            for comment in post['commentlist']:
                post_comment += (r'{\bf %s} %s\\' % (PostToLatex.preprocess(comment['name']), self.latex_v(comment['content'])) + '\n')
                if 'list_3' in comment.keys():
                    for subcomment in comment['list_3']:
                        post_comment += (r'\indent {\bf %s} %s\\' % (PostToLatex.preprocess(subcomment['name']), self.latex_v(subcomment['content'])) + '\n')
        end = r'\clearpage' + '\n\n'
        return post_title + post_content + post_rt  + post_divider + post_comment + end

    def to_latex(self):
        with open('doc/book.tex', 'w') as f:
            f.write(r'\documentclass{ctexbook}'
                    r'\usepackage{spverbatim}'
                    r'\usepackage[left=1.2in,top=1.2in,right=1.2in,bottom=1.2in]{geometry}'
                    r'\usepackage{float}\usepackage{scrextend}'
                    r'\newlength\tindent\setlength{\tindent}{\parindent}\setlength{\parindent}{0pt}' 
                    r'\renewcommand{\indent}{\hspace*{\tindent}}' + '\n')
            f.write(r'\begin{document}' + '\n')
            for post in self.posts:
                f.write(self.get_post_latex(post))
            f.write(r'\end{document}')


posts = merge_all_posts()[:]
book = PostToLatex(posts)
book.to_latex()