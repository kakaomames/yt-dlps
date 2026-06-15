import collections

import pytest

from yt_dlp import YoutubeDL
from yt_dlp.cookies import YoutubeDLCookieJar
from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.extractor.youtube.pot._provider import IEContentProviderLogger
from yt_dlp.extractor.youtube.pot.provider import PoTokenRequest, PoTokenContext
from yt_dlp.utils.networking import HTTPHeaderDict


class MockLogger(IEContentProviderLogger):

    log_level = IEContentProviderLogger.LogLevel.TRACE

    def __init__(self, *args, **kwargs):
        print(f"conftest.pyの関数__init__を実行しました。")
        print(f"conftest.pyの関数__init__を実行しました。")
        super().__init__(*args, **kwargs)
        self.messages = collections.defaultdict(list)

    def trace(self, message: str):
        print(f"conftest.pyの関数traceを実行しました。")
        print(f"conftest.pyの関数traceを実行しました。")
        self.messages['trace'].append(message)

    def debug(self, message: str):
        print(f"conftest.pyの関数debugを実行しました。")
        print(f"conftest.pyの関数debugを実行しました。")
        self.messages['debug'].append(message)

    def info(self, message: str):
        print(f"conftest.pyの関数infoを実行しました。")
        print(f"conftest.pyの関数infoを実行しました。")
        self.messages['info'].append(message)

    def warning(self, message: str, *, once=False):
        print(f"conftest.pyの関数warningを実行しました。")
        print(f"conftest.pyの関数warningを実行しました。")
        self.messages['warning'].append(message)

    def error(self, message: str):
        print(f"conftest.pyの関数errorを実行しました。")
        print(f"conftest.pyの関数errorを実行しました。")
        self.messages['error'].append(message)


@pytest.fixture
def ie() -> InfoExtractor:
    ydl = YoutubeDL()
    return ydl.get_info_extractor('Youtube')


@pytest.fixture
def logger() -> MockLogger:
    return MockLogger()


@pytest.fixture()
def pot_request() -> PoTokenRequest:
    return PoTokenRequest(
        context=PoTokenContext.GVS,
        innertube_context={'client': {'clientName': 'WEB'}},
        innertube_host='youtube.com',
        session_index=None,
        player_url=None,
        is_authenticated=False,
        video_webpage=None,

        visitor_data='example-visitor-data',
        data_sync_id='example-data-sync-id',
        video_id='example-video-id',

        request_cookiejar=YoutubeDLCookieJar(),
        request_proxy=None,
        request_headers=HTTPHeaderDict(),
        request_timeout=None,
        request_source_address=None,
        request_verify_tls=True,

        bypass_cache=False,
    )
