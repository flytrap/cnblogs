# coding: utf8
# auto: flytrap
import time
from threading import Thread, RLock
from Queue import Queue, Empty, Full
import logging

from pickle_db import BlogManger
from Common.functions import make_md5
from parse_html import parse_blog

logger = logging.getLogger('spider')
urls_queue = Queue(10000)  # spider url
url_queue = Queue(10000)  # db url
blog_queue = Queue(10000)


def check_queue_empty():
    if url_queue.empty() and blog_queue.empty() and urls_queue.empty():
        return True
    return False


class PickleInfo(Thread):
    over = False

    def __init__(self, db_path):
        Thread.__init__(self)
        self._lock = RLock()
        self._lock.acquire()
        self.bm = BlogManger(db_path)
        self._lock.release()

    def pickle_blog(self, blog_info):
        self._lock.acquire()
        self.bm.insert_blog(blog_info)
        self._lock.release()

    def pickle_urls(self, urls):
        if isinstance(urls, basestring):
            urls = [urls]
        data = zip(urls, map(make_md5, urls))
        self._lock.acquire()
        self.bm.insert_url(data)
        self._lock.release()

    def run(self):
        while True:
            try:
                if blog_queue.empty():
                    urls = url_queue.get(timeout=3)
                    self.pickle_urls(urls)
                else:
                    blog_info = blog_queue.get(timeout=3)
                    self.pickle_blog(blog_info)
            except Empty:
                if PickleInfo.over is True and check_queue_empty():
                    logger.info('PickleInfo thread exit.')
                    break


class Parser(Thread):
    url_hash = set()
    over = False

    def __init__(self):
        Thread.__init__(self)

    def start(self):
        while True:
            try:
                url = urls_queue.get(timeout=3)
                self.url_hash.add(make_md5(url))
                result = parse_blog(url)
                self.scheduling(result)
                url_queue.put(url, timeout=3)
            except Empty:
                if self.over is True and check_queue_empty():
                    logger.info('Parser thread exit.')
                    break
            except Full:
                logger.warning('url_queue full:%s' % url_queue.qsize())

    def scheduling(self, result):
        if 'blog_info' in result:
            blog_info = result.get('blog_info')
            try:
                blog_queue.put(blog_info, timeout=5)
            except Full:
                logger.warning('blog queue full:%s' % blog_queue.qsize())
        urls = result.get('urls')
        for url in urls:
            if self.check_url(url):
                urls_queue.put(url)

    def check_url(self, url):
        if make_md5(url) in self.url_hash:
            return False
        return True


class Scheduling(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = object.__new__(cls, args)
        return cls._inst

    def __init__(self, db_path):
        if not hasattr(self, '__is_init'):
            super(Scheduling, self).__init__()
            setattr(self, '__is_init', self)
        self.db_path = db_path
        self.pickle_num = 1
        self.request_num = 3
        self.pickle_thread = {}
        self.parser_thread = {}

    def parser(self, url):
        urls_queue.put(url)
        for i in xrange(self.pickle_num):
            t = PickleInfo(self.db_path)
            self.pickle_thread[i] = t
            t.start()
        for i in xrange(self.request_num):
            t = Parser()
            self.parser_thread[i] = t
            t.start()

    @staticmethod
    def stop():
        Parser.over = True
        PickleInfo.over = True

    def kill(self):
        self.stop()
        qs = [urls_queue, blog_queue]
        for q in qs:
            try:
                q.get(timeout=0.01)
            except Empty:
                pass
        while not check_queue_empty():
            # waite
            time.sleep(3)
        self.waite_thread()

    def waite_thread(self):
        for t in self.pickle_thread.values() + self.parser_thread.values():
            t.join()


if __name__ == '__main__':
    s = PickleInfo('test.db')
    s.start()

    time.sleep(3)
    PickleInfo.over = True
    s.join()
    print s.__class__
