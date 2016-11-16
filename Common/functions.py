# coding: utf8
# auto: flytrap
import hashlib


def make_md5(obj):
    m = hashlib.md5(obj)
    return m.hexdigest()
