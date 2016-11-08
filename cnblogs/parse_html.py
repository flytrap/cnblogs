# coding: utf8
# auto: flytrap
import re
import logging
import urlparse
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


class ParserUrls(HTMLParser):
    def __init__(self, index_url=''):
        HTMLParser.__init__(self)
        self.urls = []
        if index_url:
            assert index_url.startswith('http'), 'Index Url Error'
            self.hostname = urlparse.urlparse(index_url).hostname
        self.index_url = index_url
        self.filter_dict = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for att, value in attrs:
                if att == 'href':
                    self.__filter_url(value)

    def __filter_url(self, url):
        # filter url
        if not isinstance(url, basestring):
            return
        if 'index' in self.filter_dict and 're' in self.filter_dict:
            if self.__filter_index(url):
                url = self.__filter_re(url)
        elif 'index' in self.filter_dict:
            if self.__filter_index(url):
                url = ''
        elif 're' in self.filter_dict:
            url = self.__filter_re(url)
        if url and url not in self.urls:
            self.urls.append(url)

    def __filter_index(self, url):
        if self.index_url:
            if url.startswith('/') or (self.hostname and urlparse.urlparse(url) == self.hostname):
                return True
        return False

    def __filter_re(self, url):
        re_class = self.filter_dict.get('re', '')
        if hasattr(re_class, 'search'):
            url_s = re_class.search(url)
            if url_s:
                return url_s.group(0)
        return False

    def set_filter(self, filter_dict):
        assert isinstance(filter_dict, dict)
        self.filter_dict = filter_dict


class ParserBlog(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.div_num = 0
        self.blog_info = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if len(attrs) == 1 and attrs[0][1] == 'post_detail':
                setattr(self, 'post_detail', 1)
            if hasattr(self, 'post_detail'):
                self.div_num += 1
                if not hasattr(self, 'post_body'):
                    for att, value in attrs:
                        # class="postBody" or  id="cnblogs_post_body"
                        if (att == 'class' and value == 'postBody') or (att == 'id' and value == 'cnblogs_post_body'):
                            setattr(self, 'post_body', self.div_num)
                            break
        if tag == 'a' and self.div_num == 3:
            setattr(self, 'title', '')

    def handle_data(self, data):
        if self.div_num == 3 and hasattr(self, 'title'):
            self.blog_info['title'] = data
            delattr(self, 'title')
        if hasattr(self, 'post_body'):
            self.blog_info['body'] = self.blog_info.get('body', '') + data

    def handle_endtag(self, tag):
        if tag == 'div' and hasattr(self, 'post_detail'):
            if self.div_num == 0:
                delattr(self, 'post_detail')
            else:
                self.div_num -= 1
                if hasattr(self, 'post_body') and self.post_body >= self.div_num:
                    delattr(self, 'post_body')
                    # if tag == 'p':
                    #     if hasattr(self, 'post_body'):
                    #         self.blog_info['body'] = self.blog_info.get('body', '') + '\n'


def get_cn_blog_html_url(html, index_url):
    up = ParserUrls(index_url)
    cn_re = re.compile('(^/)|(.*cnblogs\.com.*)')
    up.set_filter({'re': cn_re})
    up.feed(html)
    result = []
    for url in up.urls:
        if url.startswith('/'):
            if index_url.endswith('/'):
                url = index_url + url[1:]
            else:
                url = index_url + url
        if url not in result:
            result.append(url)
    return result


if __name__ == '__main__':
    index_file = '../Log/index.html'
    # ip = ParserUrls()
    # cn_re = re.compile('(^/)|(.*cnblogs\.com.*)')
    # ip.set_filter({'re': cn_re})
    # ip.feed(open(index_file).read())
    # print ip.urls
    import time

    t = time.time()
    urls = get_cn_blog_html_url(open(index_file).read(), 'http://www.cnblogs.com')
    print 'get_cn_blog_html_url:%s' % str(time.time() - t)
    print len(urls)
