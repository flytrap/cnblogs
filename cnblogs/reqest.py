# coding: utf8
# auto: flytrap
import re
import time
import logging
from urlparse import urlparse
import json
from Common.Req import get
from config import TAG_CATEGORIES_URL, AjaxHeader, Header, proxies

int_re = re.compile('\d+')
url_re = re.compile('href="(https?://[\w\./]+)"')
tar_re = re.compile('>(.+)</a>')
logger = logging.getLogger('request')


def get_html(url):
    try:
        req = get(url, headers=Header, proxies=proxies)
        logger.info(url)
    except Exception as e:
        logger.error("%s:%s" % (e, url))
        return
    if req.status_code == 200:
        return req.text
    logger.error(url)


def get_tag_url(url, blog_id):
    tag_info = request_tag_and_categories(url, blog_id)
    if tag_info == url:
        logger.warning(url)
        return
    return tag_info


def request_tag_and_categories(url, blog_id):
    url_parse = urlparse(url)
    path = url_parse.path.split('/')
    if len(path) < 3:
        raise Exception('Url Error')
    try:
        post_id = int_re.search(path[-1]).group(0)
    except Exception as e:
        logger.error(e)
        return
    params = {'blogApp': path[1],
              'postId': str(post_id),
              'blogId': str(blog_id),
              '_': str(time.time())}
    req = get(TAG_CATEGORIES_URL, params, headers=AjaxHeader)
    if req.status_code == 200:
        tag_info = format_tag_url(req.text)
        if tag_info:
            return tag_info
    return url


def format_tag_url(text):
    d = json.loads(text)
    result = {}
    if 'Categories' in d and 'Tags' in d:
        result['url'] = url_re.findall(d['Categories']) + url_re.findall(d['Tags'])
        result['tag'] = tar_re.findall(d['Tags'])
        result['Categories'] = tar_re.findall(d['Categories'])
    return result


if __name__ == '__main__':
    get_tag_url('http://www.cnblogs.com/xjshi/p/6048602.html', '190753')
