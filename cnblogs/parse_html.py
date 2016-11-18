# coding: utf8
# auto: flytrap
import re
import logging
from urlparse import urlparse
from Common.Parser import ParserUrls, ParserBlogUrl
from config import EXCLUDE_URL
from reqest import get_html, get_tag_url

cn_re = re.compile('(^/)|(.*cnblogs\.com.*)')
blog_re = re.compile('https?:[\/\.\w]+?(\d+).html')  # 寧可殺錯，不許放過
blog_id_re = re.compile('cb_blogId=(\d+)')
logger = logging.getLogger('parser')


def parse_blog(url):
    if not isinstance(url, basestring):
        return
    blog = blog_re.match(url.strip())
    html = get_html(url)
    result = {}
    if not html:
        return result
    if blog:
        bu = parse_blog_url(html)
        result['urls'] = bu.get('urls', [])
        if bu.get('blog_info'):
            blog_id = blog_id_re.findall(html)[0]
            result['blog_info'] = bu.get('blog_info')
            result['blog_info']['url'] = url
            tag_info = get_tag_url(url, blog_id)
            if tag_info:
                result['blog_info']['tags'] = tag_info.get('Tags', [])
                result['blog_info']['tags'].extend(tag_info.get('Categories', []))
                result['urls'].extend(tag_info.get('url', []))
    else:
        u = parse_url(html)
        result.update(u)  # 'urls' in u
    result['urls'] = filter_urls(result['urls'])
    return result


def parse_blog_url(html):
    pbu = ParserBlogUrl()
    pbu.set_filter({'re': cn_re})
    pbu.feed(html)
    if 'body' in pbu.blog_info:
        if 'title' not in pbu.blog_info and hasattr(pbu.blog_info, 'title_text'):
            pbu.blog_info['title'] = pbu.title_text
            logger.info('title change title_text')
    return {'blog_info': pbu.blog_info, 'urls': pbu.urls}


def check_urls(old_url, urls):
    up = urlparse(old_url)
    host = up.scheme + '://' + up.netloc

    def check_url(url):
        if url.startswith('/'):
            url = host + url
        return url

    return map(check_url, urls)


def parse_url(html):
    pu = ParserUrls()
    pu.set_filter({'re': cn_re})
    pu.feed(html)
    return {'urls': pu.urls}


def filter_urls(urls):
    return filter(filter_url, urls)


def filter_url(url):
    up = urlparse(url)
    for exclude_url in EXCLUDE_URL:
        if str(up.hostname).startswith(exclude_url):
            return False
    return url


def get_cn_blog_html_url(html, index_url):
    up = ParserUrls(index_url)
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
    index_file = '../Log/3738115.html'
    # ip = ParserUrls()
    # cn_re = re.compile('(^/)|(.*cnblogs\.com.*)')
    # ip.set_filter({'re': cn_re})
    # ip.feed(open(index_file).read())
    # print ip.urls
    # import time
    #
    # t = time.time()
    # urls = get_cn_blog_html_url(open(index_file).read(), 'http://www.cnblogs.com')
    # print 'get_cn_blog_html_url:%s' % str(time.time() - t)
    # print len(urls)
    # blog_info = parse_blog('http://www.cnblogs.com/binyue/p/6063353.html')
    blog_info = parse_blog('http://www.cnblogs.com/binyue/category/538822.html')
    print len(blog_info)
    # html = get_html('http://www.cnblogs.com/binyue/p/6063353.html')
    # bu = parse_url(html)
    # print len(bu)
