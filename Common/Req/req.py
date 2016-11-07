# coding: utf8
# auto: flytrap
from functools import partial
import requests

# proxies = {
#     "http": "http://10.10.1.10:3128",
#     "https": "http://10.10.1.10:1080",
# }
proxies = None
if proxies:
    get = partial(requests.get, proxies=proxies)
    post = partial(requests.post, proxies=proxies)
else:
    get = requests.get
    post = requests.post

if __name__ == '__main__':
    url = 'http://www.cnblogs.com/'