# coding: utf8
# auto: flytrap
import os
import re
from Common.Log import define_logger

urls = []


def init_log():
    define_logger('parser', 'Log/parser.txt')
    define_logger('request', 'Log/request.txt')


class CNBlogSpider(object):
    def __init__(self):
        self.index_url = 'http://www.cnblogs.com/'


def pickle_html(url_path, html_text):
    filename = os.path.basename(url_path)
    path = os.path.join('Log', filename)
    with open(path, 'w') as f:
        f.write(html_text.encode('utf8'))


if __name__ == '__main__':
    os.chdir('../')
    cn = CNBlogSpider()
