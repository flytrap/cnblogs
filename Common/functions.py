# coding: utf8
# auto: flytrap
import hashlib


def make_md5(obj):
    try:
        obj = obj.encode('utf8')
    except (UnicodeEncodeError, TypeError):
        pass
    m = hashlib.md5(obj)
    return m.hexdigest()


if __name__ == '__main__':
    s = 'test'
    print(make_md5(s))
