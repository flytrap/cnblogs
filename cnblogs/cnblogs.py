# coding: utf8
# auto: flytrap
import os
from Common.Log import define_logger
from Common.Req import get


def init_log():
    define_logger('parser', 'Log/parser.txt')
    # define_logger('requests', 'Log/requests.txt')


class CNBlogSpider(object):
    def __init__(self):
        self.index_url = 'http://www.cnblogs.com/'

    def get_index(self):
        text = self.get_html(self.index_url)
        with open('Log/index.html', 'w') as f:
            f.write(text.encode('utf8'))

    def get_html(self, url_path):
        req = get(url_path)
        if req.status_code == 200:
            return req.text


def pickle_html(url_path, html_text):
    filename = os.path.basename(url_path)
    path = os.path.join('Log', filename)
    with open(path, 'w') as f:
        f.write(html_text.encode('utf8'))


if __name__ == '__main__':
    os.chdir('../')
    cn = CNBlogSpider()
    # cn.get_index()
    # url = 'http://www.cnblogs.com/jialiangliang/p/6044700.html'
    url = 'http://www.cnblogs.com/chengtian/p/3738115.html'
    html = cn.get_html(url)
    pickle_html(url, html)
