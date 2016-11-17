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
    get = partial(requests.get, proxies=proxies, verify=False)
    post = partial(requests.post, proxies=proxies, verify=False)
else:
    get = requests.get
    post = requests.post

get = partial(get, timeout=3)
if __name__ == '__main__':
    url = 'http://www.cnblogs.com/'
