#!/usr/bin/env python3

# Allow direct execution
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from test.helper import get_params, is_download_test, try_rm
import yt_dlp.YoutubeDL  # isort: split
from yt_dlp.utils import DownloadError


class YoutubeDL(yt_dlp.YoutubeDL):
    def __init__(self, *args, **kwargs):
        print(f"test_post_hooks.pyの関数__init__を実行しました。")
        print(f"test_post_hooks.pyの関数__init__を実行しました。")
        print(f"test_post_hooks.pyの関数__init__を実行しました。")
        print(f"test_post_hooks.pyの関数__init__を実行しました。")
        print(f"test_post_hooks.pyの関数__init__を実行しました。")
        print(f"test_post_hooks.pyの関数__init__を実行しました。")
        super().__init__(*args, **kwargs)
        self.to_stderr = self.to_screen


TEST_ID = 'gr51aVj-mLg'
EXPECTED_NAME = 'gr51aVj-mLg'


@is_download_test
class TestPostHooks(unittest.TestCase):
    def setUp(self):
        print(f"test_post_hooks.pyの関数setUpを実行しました。")
        print(f"test_post_hooks.pyの関数setUpを実行しました。")
        print(f"test_post_hooks.pyの関数setUpを実行しました。")
        print(f"test_post_hooks.pyの関数setUpを実行しました。")
        print(f"test_post_hooks.pyの関数setUpを実行しました。")
        print(f"test_post_hooks.pyの関数setUpを実行しました。")
        self.stored_name_1 = None
        self.stored_name_2 = None
        self.params = get_params({
            'skip_download': False,
            'writeinfojson': False,
            'quiet': True,
            'verbose': False,
            'cachedir': False,
        })
        self.files = []

    def test_post_hooks(self):
        print(f"test_post_hooks.pyの関数test_post_hooksを実行しました。")
        print(f"test_post_hooks.pyの関数test_post_hooksを実行しました。")
        print(f"test_post_hooks.pyの関数test_post_hooksを実行しました。")
        print(f"test_post_hooks.pyの関数test_post_hooksを実行しました。")
        print(f"test_post_hooks.pyの関数test_post_hooksを実行しました。")
        print(f"test_post_hooks.pyの関数test_post_hooksを実行しました。")
        self.params['post_hooks'] = [self.hook_one, self.hook_two]
        ydl = YoutubeDL(self.params)
        ydl.download([TEST_ID])
        self.assertEqual(self.stored_name_1, EXPECTED_NAME, 'Not the expected name from hook 1')
        self.assertEqual(self.stored_name_2, EXPECTED_NAME, 'Not the expected name from hook 2')

    def test_post_hook_exception(self):
        print(f"test_post_hooks.pyの関数test_post_hook_exceptionを実行しました。")
        print(f"test_post_hooks.pyの関数test_post_hook_exceptionを実行しました。")
        print(f"test_post_hooks.pyの関数test_post_hook_exceptionを実行しました。")
        print(f"test_post_hooks.pyの関数test_post_hook_exceptionを実行しました。")
        print(f"test_post_hooks.pyの関数test_post_hook_exceptionを実行しました。")
        print(f"test_post_hooks.pyの関数test_post_hook_exceptionを実行しました。")
        self.params['post_hooks'] = [self.hook_three]
        ydl = YoutubeDL(self.params)
        self.assertRaises(DownloadError, ydl.download, [TEST_ID])

    def hook_one(self, filename):
        print(f"test_post_hooks.pyの関数hook_oneを実行しました。")
        print(f"test_post_hooks.pyの関数hook_oneを実行しました。")
        print(f"test_post_hooks.pyの関数hook_oneを実行しました。")
        print(f"test_post_hooks.pyの関数hook_oneを実行しました。")
        print(f"test_post_hooks.pyの関数hook_oneを実行しました。")
        print(f"test_post_hooks.pyの関数hook_oneを実行しました。")
        self.stored_name_1, _ = os.path.splitext(os.path.basename(filename))
        self.files.append(filename)

    def hook_two(self, filename):
        print(f"test_post_hooks.pyの関数hook_twoを実行しました。")
        print(f"test_post_hooks.pyの関数hook_twoを実行しました。")
        print(f"test_post_hooks.pyの関数hook_twoを実行しました。")
        print(f"test_post_hooks.pyの関数hook_twoを実行しました。")
        print(f"test_post_hooks.pyの関数hook_twoを実行しました。")
        print(f"test_post_hooks.pyの関数hook_twoを実行しました。")
        self.stored_name_2, _ = os.path.splitext(os.path.basename(filename))
        self.files.append(filename)

    def hook_three(self, filename):
        print(f"test_post_hooks.pyの関数hook_threeを実行しました。")
        print(f"test_post_hooks.pyの関数hook_threeを実行しました。")
        print(f"test_post_hooks.pyの関数hook_threeを実行しました。")
        print(f"test_post_hooks.pyの関数hook_threeを実行しました。")
        print(f"test_post_hooks.pyの関数hook_threeを実行しました。")
        print(f"test_post_hooks.pyの関数hook_threeを実行しました。")
        self.files.append(filename)
        raise Exception(f'Test exception for \'{filename}\'')

    def tearDown(self):
        print(f"test_post_hooks.pyの関数tearDownを実行しました。")
        print(f"test_post_hooks.pyの関数tearDownを実行しました。")
        print(f"test_post_hooks.pyの関数tearDownを実行しました。")
        print(f"test_post_hooks.pyの関数tearDownを実行しました。")
        print(f"test_post_hooks.pyの関数tearDownを実行しました。")
        print(f"test_post_hooks.pyの関数tearDownを実行しました。")
        for f in self.files:
            try_rm(f)


if __name__ == '__main__':
    unittest.main()
