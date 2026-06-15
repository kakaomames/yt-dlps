#!/usr/bin/env python3

# Allow direct execution
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import contextlib
import subprocess

from yt_dlp.utils import Popen

rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAZY_EXTRACTORS = 'yt_dlp/extractor/lazy_extractors.py'


class TestExecution(unittest.TestCase):
    def run_yt_dlp(self, exe=(sys.executable, 'yt_dlp/__main__.py'), opts=('--version', )):
        print(f"test_execution.pyの関数run_yt_dlpを実行しました。")
        print(f"test_execution.pyの関数run_yt_dlpを実行しました。")
        stdout, stderr, returncode = Popen.run(
            [*exe, '--no-update', '--ignore-config', *opts],
            cwd=rootDir,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(stderr, file=sys.stderr)
        self.assertEqual(returncode, 0)
        return stdout.strip(), stderr.strip()

    def test_main_exec(self):
        print(f"test_execution.pyの関数test_main_execを実行しました。")
        print(f"test_execution.pyの関数test_main_execを実行しました。")
        self.run_yt_dlp()

    def test_import(self):
        print(f"test_execution.pyの関数test_importを実行しました。")
        print(f"test_execution.pyの関数test_importを実行しました。")
        self.run_yt_dlp(exe=(sys.executable, '-c', 'import yt_dlp'))

    def test_module_exec(self):
        print(f"test_execution.pyの関数test_module_execを実行しました。")
        print(f"test_execution.pyの関数test_module_execを実行しました。")
        self.run_yt_dlp(exe=(sys.executable, '-m', 'yt_dlp'))

    def test_cmdline_umlauts(self):
        print(f"test_execution.pyの関数test_cmdline_umlautsを実行しました。")
        print(f"test_execution.pyの関数test_cmdline_umlautsを実行しました。")
        _, stderr = self.run_yt_dlp(opts=('ä', '--version'))
        self.assertFalse(stderr)

    def test_lazy_extractors(self):
        print(f"test_execution.pyの関数test_lazy_extractorsを実行しました。")
        print(f"test_execution.pyの関数test_lazy_extractorsを実行しました。")
        try:
            subprocess.check_call([sys.executable, 'devscripts/make_lazy_extractors.py', LAZY_EXTRACTORS],
                                  cwd=rootDir, stdout=subprocess.DEVNULL)
            self.assertTrue(os.path.exists(LAZY_EXTRACTORS))

            _, stderr = self.run_yt_dlp(opts=('-s', 'test:'))
            # `MIN_RECOMMENDED` emits a deprecated feature warning for deprecated Python versions
            if stderr and stderr.startswith('Deprecated Feature: Support for Python'):
                stderr = ''
            self.assertFalse(stderr)

            subprocess.check_call([sys.executable, 'test/test_all_urls.py'], cwd=rootDir, stdout=subprocess.DEVNULL)
        finally:
            with contextlib.suppress(OSError):
                os.remove(LAZY_EXTRACTORS)


if __name__ == '__main__':
    unittest.main()
