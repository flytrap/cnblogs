# coding: utf8
# auto: flytrap
from Common.Log import define_logger
from Common.Req import get


def init_log(log_path):
    define_logger('parser', 'Log/parser.txt')
    # define_logger('requests', 'Log/requests.txt')


class CNBlogSpider(object):
    def __init__(self):
        self.index_url = 'http://www.cnblogs.com/'

    def get_index(self):
        html = self.get_html(self.index_url)
        with open('../Log/index.html', 'w') as f:
            f.write(html.encode('utf8'))

    def get_html(self, url):
        req = get(url)
        if req.status_code == 200:
            return req.text


if __name__ == '__main__':
    cn = CNBlogSpider()
    cn.get_index()
