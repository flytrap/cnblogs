# coding: utf8
# auto: flytrap
import os
import unittest
from cnblogs.parse_html import ParserBlog


class TestPasser(unittest.TestCase):
    def test_parser(self):
        pb = ParserBlog()
        # html = open('../Log/6044700.html').read()
        html = open('../Log/3738115.html').read()
        pb.feed(html)
        print pb.blog_info['body']


if __name__ == '__main__':
    os.chdir('../')
    unittest.main()
