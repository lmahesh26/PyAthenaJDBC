# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import codecs
import contextlib
import functools
import os


class Env(object):

    def __init__(self):
        # self.user = os.getenv('AWS_ACCESS_KEY_ID', None)
        # assert self.user, \
        #     'Required environment variable `AWS_ACCESS_KEY_ID` not found.'
        # self.password = os.getenv('AWS_SECRET_ACCESS_KEY', None)
        # assert self.password, \
        #     'Required environment variable `AWS_SECRET_ACCESS_KEY` not found.'
        self.region_name = os.getenv('AWS_DEFAULT_REGION', None)
        assert self.region_name, \
            'Required environment variable `AWS_DEFAULT_REGION` not found.'
        self.s3_staging_dir = os.getenv('AWS_ATHENA_S3_STAGING_DIR', None)
        assert self.s3_staging_dir, \
            'Required environment variable `AWS_ATHENA_S3_STAGING_DIR` not found.'


def with_cursor(fn):
    @functools.wraps(fn)
    def wrapped_fn(self, *args, **kwargs):
        with contextlib.closing(self.connect()) as conn:
            with conn.cursor() as cursor:
                fn(self, cursor, *args, **kwargs)
    return wrapped_fn


def with_engine(fn):
    @functools.wraps(fn)
    def wrapped_fn(self, *args, **kwargs):
        engine = self.create_engine()
        try:
            with contextlib.closing(engine.connect()) as conn:
                fn(self, engine, conn, *args, **kwargs)
        finally:
            engine.dispose()
    return wrapped_fn


def read_query(path):
    with codecs.open(path, 'rb', 'utf-8') as f:
        query = f.read()
    return [q.strip() for q in query.split(';') if q and q.strip()]
