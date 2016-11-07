# coding: utf8
# auto: flytrap
import logging
from HTMLParser import HTMLParser

logger = logging.getLogger('parser')


class IndexParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.urls = []
        self.div_num = 0
        self.ul_num = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if len(attrs) == 1 and attrs[0][1] == 'side_nav':
                setattr(self, 'side_nav', 1)
                self.div_num += 1
            if hasattr(self, 'side_nav'):
                self.div_num += 1
        if tag == 'a' and self.div_num == 3:
            if self.ul_num != 0:
                self.urls.append(attrs[0][1])
        if tag == 'ul' and self.div_num == 3:
            if len(attrs) == 1 and attrs[0][1] == 'cate_item':
                self.ul_num += 1

    def handle_endtag(self, tag):
        if tag == 'div' and hasattr(self, 'side_nav'):
            if self.div_num == 0:
                delattr(self, 'side_nav')
            else:
                self.div_num -= 1
        if tag == 'ul' and self.ul_num > 0:
            self.ul_num -= 1


if __name__ == '__main__':
    index_file = '../Log/index.html'
    ip = IndexParser()
    ip.feed(open(index_file).read())
    print ip.urls
