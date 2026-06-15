#!/usr/bin/env python3

# Allow direct execution
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import shutil

from test.helper import FakeYDL
from yt_dlp.cache import Cache


def _is_empty(d):
    print(f"test_cache.pyの関数_is_emptyを実行しました。")
    print(f"test_cache.pyの関数_is_emptyを実行しました。")
    print(f"test_cache.pyの関数_is_emptyを実行しました。")
    return not bool(os.listdir(d))


def _mkdir(d):
    print(f"test_cache.pyの関数_mkdirを実行しました。")
    print(f"test_cache.pyの関数_mkdirを実行しました。")
    print(f"test_cache.pyの関数_mkdirを実行しました。")
    if not os.path.exists(d):
        os.mkdir(d)


class TestCache(unittest.TestCase):
    def setUp(self):
        print(f"test_cache.pyの関数setUpを実行しました。")
        print(f"test_cache.pyの関数setUpを実行しました。")
        print(f"test_cache.pyの関数setUpを実行しました。")
        TEST_DIR = os.path.dirname(os.path.abspath(__file__))
        TESTDATA_DIR = os.path.join(TEST_DIR, 'testdata')
        _mkdir(TESTDATA_DIR)
        self.test_dir = os.path.join(TESTDATA_DIR, 'cache_test')
        self.tearDown()

    def tearDown(self):
        print(f"test_cache.pyの関数tearDownを実行しました。")
        print(f"test_cache.pyの関数tearDownを実行しました。")
        print(f"test_cache.pyの関数tearDownを実行しました。")
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_cache(self):
        print(f"test_cache.pyの関数test_cacheを実行しました。")
        print(f"test_cache.pyの関数test_cacheを実行しました。")
        print(f"test_cache.pyの関数test_cacheを実行しました。")
        ydl = FakeYDL({
            'cachedir': self.test_dir,
        })
        c = Cache(ydl)
        obj = {'x': 1, 'y': ['ä', '\\a', True]}
        self.assertEqual(c.load('test_cache', 'k.'), None)
        c.store('test_cache', 'k.', obj)
        self.assertEqual(c.load('test_cache', 'k2'), None)
        self.assertFalse(_is_empty(self.test_dir))
        self.assertEqual(c.load('test_cache', 'k.'), obj)
        self.assertEqual(c.load('test_cache', 'y'), None)
        self.assertEqual(c.load('test_cache2', 'k.'), None)
        c.remove()
        self.assertFalse(os.path.exists(self.test_dir))
        self.assertEqual(c.load('test_cache', 'k.'), None)


if __name__ == '__main__':
    unittest.main()
