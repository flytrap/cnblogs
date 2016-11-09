# coding: utf8
# auto: flytrap
import re
from urlparse import urlparse
from HTMLParser import HTMLParser


class ParserBase(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.num = 0
        self.tag = self.tag if hasattr(self, 'tag') else None
        self.att = self.att if hasattr(self, 'att') else None
        self.att_value = self.att_value if hasattr(self, 'att_value') else None
        self.urls = self.urls if hasattr(self, 'urls') else []

    def check_parser_att(self):
        assert self.tag and self.att and self.att_value, 'Init Error.'

    def handle_starttag(self, tag, attrs):
        if tag == self.tag:
            # other div
            for att, value in attrs:
                if att == self.att and value == self.att_value:
                    setattr(self, self.att_value, 1)
                    break
            if hasattr(self, self.att_value):
                self.num += 1
                if hasattr(self, self.att_value):
                    self.start_doing(attrs)
        if tag == 'a':
            # link
            for att, value in attrs:
                if att == 'href':
                    self.check_url(value)

    def start_doing(self, attrs):
        # custom anything
        pass

    def check_url(self, url):
        # custom url
        self.urls.append(url)

    def handle_endtag(self, tag):
        if tag == self.tag and hasattr(self, self.att_value):
            if self.num == 0:
                delattr(self, self.att_value)
            else:
                self.num -= 1


class ParserUrls(ParserBase):
    def __init__(self, index_url=''):
        ParserBase.__init__(self)
        if index_url:
            assert index_url.startswith('http'), 'Index Url Error'
            self.hostname = urlparse(index_url).hostname
        self.index_url = index_url
        self.filter_dict = {}

    def check_url(self, url):
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
            if url.startswith('/') or (self.hostname and urlparse(url) == self.hostname):
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


class ParserBlog(ParserBase):
    def __init__(self):
        ParserBase.__init__(self)
        self.tag = 'div'
        self.att = 'id'
        self.att_value = 'post_detail'
        self.blog_info = {}

    def start_doing(self, attrs):
        for att, value in attrs:
            # class="postBody" or  id="cnblogs_post_body"
            if (att == 'class' and value == 'postBody') or (att == 'id' and value == 'cnblogs_post_body'):
                setattr(self, 'body', self.num - 1)
                break
            if att == 'class' and value == 'postTitle':
                setattr(self, 'title', self.num - 1)
                break

    def handle_data(self, data):
        if self.num == 3 and hasattr(self, 'title'):
            if hasattr(self, 'title') and len(data.strip()) >= 1:
                self.blog_info['title'] = self.blog_info.get('title', '') + data.strip()
                delattr(self, 'title')
        if hasattr(self, 'body'):
            if hasattr(self, 'body') and self.body >= self.num:
                delattr(self, 'body')
                return
            self.blog_info['body'] = self.blog_info.get('body', '') + data


class ParserBlogUrl(ParserUrls, ParserBlog):
    def __init__(self):
        ParserUrls.__init__(self)
        ParserBlog.__init__(self)

    start_doing = ParserBlog.start_doing
    handle_data = ParserBlog.handle_data


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


if __name__ == '__main__':
    # index_file = '../../Log/index.html'
    # ip = ParserUrls()
    cn_re = re.compile('(^/)|(.*cnblogs\.com.*)')
    # ip.set_filter({'re': cn_re})
    # ip.feed(open(index_file).read())
    # print ip.urls
    # pb = ParserBlog()
    html = open('../../Log/3738115.html').read()
    # pb.feed(html)
    # print pb.blog_info['body']
    bu = ParserBlogUrl()
    bu.set_filter({'re': cn_re})
    bu.feed(html)
    print len(bu.urls)
    print len(bu.blog_info)
