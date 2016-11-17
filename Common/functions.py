# coding: utf8
# auto: flytrap
import hashlib


def make_md5(obj):
    try:
        obj = str.encode(obj, 'utf8', errors='ignore')
    except UnicodeDecodeError:
        pass
    m = hashlib.md5(obj)
    return m.hexdigest()


if __name__ == '__main__':
    s = 'test'
    print(make_md5(s))
