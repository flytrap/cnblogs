# coding: utf8
# auto: flytrap
EXCLUDE_URL = ['group', 'passport', 'job', 'ing', 'msg', 'i']
TAG_CATEGORIES_URL = 'http://www.cnblogs.com/mvc/blog/CategoriesTags.aspx'

proxies = {}
Header = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8'}

AjaxHeader = {'X-Requested-With': 'XMLHttpRequest',
              'Accept': 'application/json, text/javascript, */*; q=0.01'}.update(Header)
