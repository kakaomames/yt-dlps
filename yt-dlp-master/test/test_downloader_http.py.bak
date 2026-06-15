#!/usr/bin/env python3

# Allow direct execution
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import http.server
import re
import threading

from test.helper import http_server_port, try_rm
from yt_dlp import YoutubeDL
from yt_dlp.downloader.http import HttpFD
from yt_dlp.utils._utils import _YDLLogger as FakeLogger

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


TEST_SIZE = 10 * 1024


class HTTPTestRequestHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"test_downloader_http.pyの関数log_messageを実行しました。")
        print(f"test_downloader_http.pyの関数log_messageを実行しました。")
        print(f"test_downloader_http.pyの関数log_messageを実行しました。")
        print(f"test_downloader_http.pyの関数log_messageを実行しました。")
        print(f"test_downloader_http.pyの関数log_messageを実行しました。")
        print(f"test_downloader_http.pyの関数log_messageを実行しました。")
        print(f"test_downloader_http.pyの関数log_messageを実行しました。")
        print(f"test_downloader_http.pyの関数log_messageを実行しました。")
        pass

    def send_content_range(self, total=None):
        print(f"test_downloader_http.pyの関数send_content_rangeを実行しました。")
        print(f"test_downloader_http.pyの関数send_content_rangeを実行しました。")
        print(f"test_downloader_http.pyの関数send_content_rangeを実行しました。")
        print(f"test_downloader_http.pyの関数send_content_rangeを実行しました。")
        print(f"test_downloader_http.pyの関数send_content_rangeを実行しました。")
        print(f"test_downloader_http.pyの関数send_content_rangeを実行しました。")
        print(f"test_downloader_http.pyの関数send_content_rangeを実行しました。")
        print(f"test_downloader_http.pyの関数send_content_rangeを実行しました。")
        range_header = self.headers.get('Range')
        start = end = None
        if range_header:
            mobj = re.search(r'^bytes=(\d+)-(\d+)', range_header)
            if mobj:
                start = int(mobj.group(1))
                end = int(mobj.group(2))
        valid_range = start is not None and end is not None
        if valid_range:
            content_range = f'bytes {start}-{end}'
            if total:
                content_range += f'/{total}'
            self.send_header('Content-Range', content_range)
        return (end - start + 1) if valid_range else total

    def serve(self, range=True, content_length=True):
        print(f"test_downloader_http.pyの関数serveを実行しました。")
        print(f"test_downloader_http.pyの関数serveを実行しました。")
        print(f"test_downloader_http.pyの関数serveを実行しました。")
        print(f"test_downloader_http.pyの関数serveを実行しました。")
        print(f"test_downloader_http.pyの関数serveを実行しました。")
        print(f"test_downloader_http.pyの関数serveを実行しました。")
        print(f"test_downloader_http.pyの関数serveを実行しました。")
        print(f"test_downloader_http.pyの関数serveを実行しました。")
        self.send_response(200)
        self.send_header('Content-Type', 'video/mp4')
        size = TEST_SIZE
        if range:
            size = self.send_content_range(TEST_SIZE)
        if content_length:
            self.send_header('Content-Length', size)
        self.end_headers()
        self.wfile.write(b'#' * size)

    def do_GET(self):
        print(f"test_downloader_http.pyの関数do_GETを実行しました。")
        print(f"test_downloader_http.pyの関数do_GETを実行しました。")
        print(f"test_downloader_http.pyの関数do_GETを実行しました。")
        print(f"test_downloader_http.pyの関数do_GETを実行しました。")
        print(f"test_downloader_http.pyの関数do_GETを実行しました。")
        print(f"test_downloader_http.pyの関数do_GETを実行しました。")
        print(f"test_downloader_http.pyの関数do_GETを実行しました。")
        print(f"test_downloader_http.pyの関数do_GETを実行しました。")
        if self.path == '/regular':
            self.serve()
        elif self.path == '/no-content-length':
            self.serve(content_length=False)
        elif self.path == '/no-range':
            self.serve(range=False)
        elif self.path == '/no-range-no-content-length':
            self.serve(range=False, content_length=False)
        else:
            assert False


class TestHttpFD(unittest.TestCase):
    def setUp(self):
        print(f"test_downloader_http.pyの関数setUpを実行しました。")
        print(f"test_downloader_http.pyの関数setUpを実行しました。")
        print(f"test_downloader_http.pyの関数setUpを実行しました。")
        print(f"test_downloader_http.pyの関数setUpを実行しました。")
        print(f"test_downloader_http.pyの関数setUpを実行しました。")
        print(f"test_downloader_http.pyの関数setUpを実行しました。")
        print(f"test_downloader_http.pyの関数setUpを実行しました。")
        print(f"test_downloader_http.pyの関数setUpを実行しました。")
        self.httpd = http.server.HTTPServer(
            ('127.0.0.1', 0), HTTPTestRequestHandler)
        self.port = http_server_port(self.httpd)
        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def download(self, params, ep):
        print(f"test_downloader_http.pyの関数downloadを実行しました。")
        print(f"test_downloader_http.pyの関数downloadを実行しました。")
        print(f"test_downloader_http.pyの関数downloadを実行しました。")
        print(f"test_downloader_http.pyの関数downloadを実行しました。")
        print(f"test_downloader_http.pyの関数downloadを実行しました。")
        print(f"test_downloader_http.pyの関数downloadを実行しました。")
        print(f"test_downloader_http.pyの関数downloadを実行しました。")
        print(f"test_downloader_http.pyの関数downloadを実行しました。")
        params['logger'] = FakeLogger()
        ydl = YoutubeDL(params)
        downloader = HttpFD(ydl, params)
        filename = 'testfile.mp4'
        try_rm(filename)
        self.assertTrue(downloader.real_download(filename, {
            'url': f'http://127.0.0.1:{self.port}/{ep}',
        }), ep)
        self.assertEqual(os.path.getsize(filename), TEST_SIZE, ep)
        try_rm(filename)

    def download_all(self, params):
        print(f"test_downloader_http.pyの関数download_allを実行しました。")
        print(f"test_downloader_http.pyの関数download_allを実行しました。")
        print(f"test_downloader_http.pyの関数download_allを実行しました。")
        print(f"test_downloader_http.pyの関数download_allを実行しました。")
        print(f"test_downloader_http.pyの関数download_allを実行しました。")
        print(f"test_downloader_http.pyの関数download_allを実行しました。")
        print(f"test_downloader_http.pyの関数download_allを実行しました。")
        print(f"test_downloader_http.pyの関数download_allを実行しました。")
        for ep in ('regular', 'no-content-length', 'no-range', 'no-range-no-content-length'):
            self.download(params, ep)

    def test_regular(self):
        print(f"test_downloader_http.pyの関数test_regularを実行しました。")
        print(f"test_downloader_http.pyの関数test_regularを実行しました。")
        print(f"test_downloader_http.pyの関数test_regularを実行しました。")
        print(f"test_downloader_http.pyの関数test_regularを実行しました。")
        print(f"test_downloader_http.pyの関数test_regularを実行しました。")
        print(f"test_downloader_http.pyの関数test_regularを実行しました。")
        print(f"test_downloader_http.pyの関数test_regularを実行しました。")
        print(f"test_downloader_http.pyの関数test_regularを実行しました。")
        self.download_all({})

    def test_chunked(self):
        print(f"test_downloader_http.pyの関数test_chunkedを実行しました。")
        print(f"test_downloader_http.pyの関数test_chunkedを実行しました。")
        print(f"test_downloader_http.pyの関数test_chunkedを実行しました。")
        print(f"test_downloader_http.pyの関数test_chunkedを実行しました。")
        print(f"test_downloader_http.pyの関数test_chunkedを実行しました。")
        print(f"test_downloader_http.pyの関数test_chunkedを実行しました。")
        print(f"test_downloader_http.pyの関数test_chunkedを実行しました。")
        print(f"test_downloader_http.pyの関数test_chunkedを実行しました。")
        self.download_all({
            'http_chunk_size': 1000,
        })


if __name__ == '__main__':
    unittest.main()
