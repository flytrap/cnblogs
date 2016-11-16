# coding: utf8
# auto: flytrap
import os
import logging
import sqlite3

logger = logging.getLogger('database')


class DatabaseManger(object):
    def __init__(self, db_path):
        assert os.path.exists(os.path.dirname(db_path))
        self.db_path = db_path
        self.con_db = None
        self.cur = self._init_con()
        self.bad_data = []

    def _init_con(self):
        try:
            self.con_db = sqlite3.connect(self.db_path)
            cur = self.con_db.cursor()
            return cur
        except Exception as e:
            logger.exception(e)

    def create_table(self, table, names):
        assert self.cur is not None
        sql = """create table if not exists %s(%s)""" % (table, ','.join(names))
        self.cur.execute(sql)
        self.con_db.commit()

    def create_index(self, table, name):
        sql = """"create index %s on %s(%s)""" % (name, table, name)
        self.cur.execute(sql)
        self.con_db.commit()

    def insert_db(self, table, data_list, filed_list=None):
        assert self.con_db is not None, logger.error('db not init')
        assert isinstance(data_list, (list, tuple)), logger.error('insert type error')
        if len(data_list) == 0 or len(data_list[0]) == 0:
            return
        sql = self._create_insert_sql(table, data_list[0], filed_list)
        self.bad_data = []
        for data in data_list:
            try:
                self._insert_db(data, sql)
            except Exception as e:
                self.bad_data.append(data)
                logger.exception('%s:%s' % (e, data))
        self.con_db.commit()
        return self.cur.lastrowid

    @staticmethod
    def _create_insert_sql(table, data, filed_list=None):
        assert isinstance(data, (list, tuple)), logger.error(str(data))
        if filed_list:
            sql = """insert into %s(%s) values(%s)""" % (table, ', '.join(filed_list), ', '.join('?' * len(filed_list)))
        else:
            sql = """insert into %s values(%s)""" % (table, ', '.join('?' * len(data)))
        return sql

    def _insert_db(self, data, sql):
        self.cur.execute(sql, data)

    def select_db(self, table, filed_list=None, where=None):
        sql = 'select %s from %s' % (', '.join(filed_list) if filed_list else '*', table)
        if where:
            sql += ' where %s' % where
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception as e:
            logger.exception(e)

    def __del__(self):
        self.cur.close()
        self.con_db.close()


class BlogManger(object):
    def __init__(self, db_path):
        self.tables = ['urls', 'tags', 'blog_info', 'blog_tag']
        self.urls = ['id integer primary key autoincrement', 'url unique', 'hash']
        self.tags = ['id integer primary key autoincrement', 'tag']
        self.blog_info = ['id integer primary key autoincrement', 'title', 'blog', 'url']
        self.blog_tag = ['id integer primary key autoincrement', 'blog', 'tag']

        self.db_path = db_path
        self.dm = self.init_db()

    def init_db(self):
        self.dm = DatabaseManger(self.db_path)
        for table in self.tables:
            if self.check_table_default(table):
                self.dm.create_table(table, getattr(self, table))
            else:
                logger.warning('table:%s is not found' % table)
        return self.dm

    def check_table_default(self, table):
        if hasattr(self, table):
            if isinstance(getattr(self, table), (list, tuple)):
                return True
        return False

    def insert_blog(self, blog_info):
        if not isinstance(blog_info, dict) or not blog_info:
            return
        data_list = [blog_info.get('title'), blog_info.get('body'), blog_info.get('url')]
        blog_id = self.dm.insert_db('blog_info', [data_list], self.blog_info[1:])
        tag_ids = self.check_tags(blog_info.get('tags'))
        self.relate_blog_tag(blog_id, tag_ids)

    def check_tags(self, tags):
        assert isinstance(tags, (list, tuple)), logger.error('tags init')
        tag_ids = []
        for tag in tags:
            tag_id = self.dm.select_db('tags', where='tag="%s"' % tag)
            if not tag_id:
                tag_id = self.dm.insert_db('tags', [[tag]], self.tags[1:])
            tag_ids.append(tag_id if isinstance(tag_id, int) else tag_id[0][0])
        return tag_ids

    def relate_blog_tag(self, blog_id, tag_ids):
        assert isinstance(tag_ids, (list, tuple))
        data_list = zip([blog_id] * len(tag_ids), tag_ids)
        self.dm.insert_db('blog_tag', data_list, self.blog_tag[1:])

    def insert_url(self, urls):
        self.dm.insert_db('urls', urls, self.urls[1:])


if __name__ == '__main__':
    blog_info = {'url': 'http:url',
                 'title': 'title',
                 'body': 'body',
                 'tags': ['a', 'b']}
    bm = BlogManger('./test.db')
    bm.insert_blog(blog_info)
    print bm.urls
