# coding: utf8
# auto: flytrap
import os
from pickle_db import BlogManger
from Common.Log import define_logger

urls = []


def init_log():
    define_logger('parser', 'Log/parser.txt')
    define_logger('request', 'Log/request.txt')
    define_logger('database', 'Log/database.txt')
    define_logger('spider', 'Log/spider.txt')


class CNBlogSpider(object):
    def __init__(self):
        self.index_url = 'http://www.cnblogs.com/'
        self.blog_db_path = './cnblogs.db'
        self.bm = self.init_db()

    def init_db(self):
        bm = BlogManger(self.blog_db_path)
        return bm

    def start(self):
        pass


def pickle_html(url_path, html_text):
    filename = os.path.basename(url_path)
    path = os.path.join('Log', filename)
    with open(path, 'w') as f:
        f.write(html_text.encode('utf8'))


if __name__ == '__main__':
    os.chdir('../')
    cn = CNBlogSpider()
