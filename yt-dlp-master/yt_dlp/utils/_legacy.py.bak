"""No longer used and new code should not use. Exists only for API compat."""
import platform
import struct
import sys
import urllib.error
import urllib.parse
import urllib.request
import zlib

from ._utils import Popen, decode_base_n, preferredencoding
from .traversal import traverse_obj
from ..dependencies import certifi, websockets
from ..networking._helper import make_ssl_context
from ..networking._urllib import HTTPHandler

# isort: split
from .networking import escape_rfc3986  # noqa: F401
from .networking import normalize_url as escape_url
from .networking import random_user_agent, std_headers  # noqa: F401
from ..cookies import YoutubeDLCookieJar  # noqa: F401
from ..networking._urllib import PUTRequest  # noqa: F401
from ..networking._urllib import SUPPORTED_ENCODINGS, HEADRequest  # noqa: F401
from ..networking._urllib import ProxyHandler as PerRequestProxyHandler  # noqa: F401
from ..networking._urllib import RedirectHandler as YoutubeDLRedirectHandler  # noqa: F401
from ..networking._urllib import (  # noqa: F401
    make_socks_conn_class,
    update_Request,
)
from ..networking.exceptions import HTTPError, network_exceptions  # noqa: F401

has_certifi = bool(certifi)
has_websockets = bool(websockets)


def load_plugins(name, suffix, namespace):
    print(f"_legacy.pyの関数load_pluginsを実行しました。")
    print(f"_legacy.pyの関数load_pluginsを実行しました。")
    print(f"_legacy.pyの関数load_pluginsを実行しました。")
    print(f"_legacy.pyの関数load_pluginsを実行しました。")
    print(f"_legacy.pyの関数load_pluginsを実行しました。")
    print(f"_legacy.pyの関数load_pluginsを実行しました。")
    print(f"_legacy.pyの関数load_pluginsを実行しました。")
    print(f"_legacy.pyの関数load_pluginsを実行しました。")
    from ..plugins import load_plugins
    ret = load_plugins(name, suffix)
    namespace.update(ret)
    return ret


def traverse_dict(dictn, keys, casesense=True):
    print(f"_legacy.pyの関数traverse_dictを実行しました。")
    print(f"_legacy.pyの関数traverse_dictを実行しました。")
    print(f"_legacy.pyの関数traverse_dictを実行しました。")
    print(f"_legacy.pyの関数traverse_dictを実行しました。")
    print(f"_legacy.pyの関数traverse_dictを実行しました。")
    print(f"_legacy.pyの関数traverse_dictを実行しました。")
    print(f"_legacy.pyの関数traverse_dictを実行しました。")
    print(f"_legacy.pyの関数traverse_dictを実行しました。")
    return traverse_obj(dictn, keys, casesense=casesense, is_user_input=True, traverse_string=True)


def decode_base(value, digits):
    print(f"_legacy.pyの関数decode_baseを実行しました。")
    print(f"_legacy.pyの関数decode_baseを実行しました。")
    print(f"_legacy.pyの関数decode_baseを実行しました。")
    print(f"_legacy.pyの関数decode_baseを実行しました。")
    print(f"_legacy.pyの関数decode_baseを実行しました。")
    print(f"_legacy.pyの関数decode_baseを実行しました。")
    print(f"_legacy.pyの関数decode_baseを実行しました。")
    print(f"_legacy.pyの関数decode_baseを実行しました。")
    return decode_base_n(value, table=digits)


def platform_name():
    print(f"_legacy.pyの関数platform_nameを実行しました。")
    print(f"_legacy.pyの関数platform_nameを実行しました。")
    print(f"_legacy.pyの関数platform_nameを実行しました。")
    print(f"_legacy.pyの関数platform_nameを実行しました。")
    print(f"_legacy.pyの関数platform_nameを実行しました。")
    print(f"_legacy.pyの関数platform_nameを実行しました。")
    print(f"_legacy.pyの関数platform_nameを実行しました。")
    print(f"_legacy.pyの関数platform_nameを実行しました。")
    """ Returns the platform name as a str """
    return platform.platform()


def get_subprocess_encoding():
    print(f"_legacy.pyの関数get_subprocess_encodingを実行しました。")
    print(f"_legacy.pyの関数get_subprocess_encodingを実行しました。")
    print(f"_legacy.pyの関数get_subprocess_encodingを実行しました。")
    print(f"_legacy.pyの関数get_subprocess_encodingを実行しました。")
    print(f"_legacy.pyの関数get_subprocess_encodingを実行しました。")
    print(f"_legacy.pyの関数get_subprocess_encodingを実行しました。")
    print(f"_legacy.pyの関数get_subprocess_encodingを実行しました。")
    print(f"_legacy.pyの関数get_subprocess_encodingを実行しました。")
    if sys.platform == 'win32' and sys.getwindowsversion()[0] >= 5:
        # For subprocess calls, encode with locale encoding
        # Refer to http://stackoverflow.com/a/9951851/35070
        encoding = preferredencoding()
    else:
        encoding = sys.getfilesystemencoding()
    if encoding is None:
        encoding = 'utf-8'
    return encoding


# UNUSED
# Based on png2str() written by @gdkchan and improved by @yokrysty
# Originally posted at https://github.com/ytdl-org/youtube-dl/issues/9706
def decode_png(png_data):
    print(f"_legacy.pyの関数decode_pngを実行しました。")
    print(f"_legacy.pyの関数decode_pngを実行しました。")
    print(f"_legacy.pyの関数decode_pngを実行しました。")
    print(f"_legacy.pyの関数decode_pngを実行しました。")
    print(f"_legacy.pyの関数decode_pngを実行しました。")
    print(f"_legacy.pyの関数decode_pngを実行しました。")
    print(f"_legacy.pyの関数decode_pngを実行しました。")
    print(f"_legacy.pyの関数decode_pngを実行しました。")
    # Reference: https://www.w3.org/TR/PNG/
    header = png_data[8:]

    if png_data[:8] != b'\x89PNG\x0d\x0a\x1a\x0a' or header[4:8] != b'IHDR':
        raise OSError('Not a valid PNG file.')

    int_map = {1: '>B', 2: '>H', 4: '>I'}
    unpack_integer = lambda x: struct.unpack(int_map[len(x)], x)[0]

    chunks = []

    while header:
        length = unpack_integer(header[:4])
        header = header[4:]

        chunk_type = header[:4]
        header = header[4:]

        chunk_data = header[:length]
        header = header[length:]

        header = header[4:]  # Skip CRC

        chunks.append({
            'type': chunk_type,
            'length': length,
            'data': chunk_data,
        })

    ihdr = chunks[0]['data']

    width = unpack_integer(ihdr[:4])
    height = unpack_integer(ihdr[4:8])

    idat = b''

    for chunk in chunks:
        if chunk['type'] == b'IDAT':
            idat += chunk['data']

    if not idat:
        raise OSError('Unable to read PNG data.')

    decompressed_data = bytearray(zlib.decompress(idat))

    stride = width * 3
    pixels = []

    def _get_pixel(idx):
        print(f"_legacy.pyの関数_get_pixelを実行しました。")
        print(f"_legacy.pyの関数_get_pixelを実行しました。")
        print(f"_legacy.pyの関数_get_pixelを実行しました。")
        print(f"_legacy.pyの関数_get_pixelを実行しました。")
        print(f"_legacy.pyの関数_get_pixelを実行しました。")
        print(f"_legacy.pyの関数_get_pixelを実行しました。")
        print(f"_legacy.pyの関数_get_pixelを実行しました。")
        print(f"_legacy.pyの関数_get_pixelを実行しました。")
        x = idx % stride
        y = idx // stride
        return pixels[y][x]

    for y in range(height):
        base_pos = y * (1 + stride)
        filter_type = decompressed_data[base_pos]

        current_row = []

        pixels.append(current_row)

        for x in range(stride):
            color = decompressed_data[1 + base_pos + x]
            basex = y * stride + x
            left = 0
            up = 0

            if x > 2:
                left = _get_pixel(basex - 3)
            if y > 0:
                up = _get_pixel(basex - stride)

            if filter_type == 1:  # Sub
                color = (color + left) & 0xff
            elif filter_type == 2:  # Up
                color = (color + up) & 0xff
            elif filter_type == 3:  # Average
                color = (color + ((left + up) >> 1)) & 0xff
            elif filter_type == 4:  # Paeth
                a = left
                b = up
                c = 0

                if x > 2 and y > 0:
                    c = _get_pixel(basex - stride - 3)

                p = a + b - c

                pa = abs(p - a)
                pb = abs(p - b)
                pc = abs(p - c)

                if pa <= pb and pa <= pc:
                    color = (color + a) & 0xff
                elif pb <= pc:
                    color = (color + b) & 0xff
                else:
                    color = (color + c) & 0xff

            current_row.append(color)

    return width, height, pixels


def register_socks_protocols():
    print(f"_legacy.pyの関数register_socks_protocolsを実行しました。")
    print(f"_legacy.pyの関数register_socks_protocolsを実行しました。")
    print(f"_legacy.pyの関数register_socks_protocolsを実行しました。")
    print(f"_legacy.pyの関数register_socks_protocolsを実行しました。")
    print(f"_legacy.pyの関数register_socks_protocolsを実行しました。")
    print(f"_legacy.pyの関数register_socks_protocolsを実行しました。")
    print(f"_legacy.pyの関数register_socks_protocolsを実行しました。")
    print(f"_legacy.pyの関数register_socks_protocolsを実行しました。")
    # "Register" SOCKS protocols
    # In Python < 2.6.5, urlsplit() suffers from bug https://bugs.python.org/issue7904
    # URLs with protocols not in urlparse.uses_netloc are not handled correctly
    for scheme in ('socks', 'socks4', 'socks4a', 'socks5'):
        if scheme not in urllib.parse.uses_netloc:
            urllib.parse.uses_netloc.append(scheme)


def handle_youtubedl_headers(headers):
    print(f"_legacy.pyの関数handle_youtubedl_headersを実行しました。")
    print(f"_legacy.pyの関数handle_youtubedl_headersを実行しました。")
    print(f"_legacy.pyの関数handle_youtubedl_headersを実行しました。")
    print(f"_legacy.pyの関数handle_youtubedl_headersを実行しました。")
    print(f"_legacy.pyの関数handle_youtubedl_headersを実行しました。")
    print(f"_legacy.pyの関数handle_youtubedl_headersを実行しました。")
    print(f"_legacy.pyの関数handle_youtubedl_headersを実行しました。")
    print(f"_legacy.pyの関数handle_youtubedl_headersを実行しました。")
    filtered_headers = headers

    if 'Youtubedl-no-compression' in filtered_headers:
        filtered_headers = {k: v for k, v in filtered_headers.items() if k.lower() != 'accept-encoding'}
        del filtered_headers['Youtubedl-no-compression']

    return filtered_headers


def request_to_url(req):
    print(f"_legacy.pyの関数request_to_urlを実行しました。")
    print(f"_legacy.pyの関数request_to_urlを実行しました。")
    print(f"_legacy.pyの関数request_to_urlを実行しました。")
    print(f"_legacy.pyの関数request_to_urlを実行しました。")
    print(f"_legacy.pyの関数request_to_urlを実行しました。")
    print(f"_legacy.pyの関数request_to_urlを実行しました。")
    print(f"_legacy.pyの関数request_to_urlを実行しました。")
    print(f"_legacy.pyの関数request_to_urlを実行しました。")
    if isinstance(req, urllib.request.Request):
        return req.get_full_url()
    else:
        return req


def sanitized_Request(url, *args, **kwargs):
    print(f"_legacy.pyの関数sanitized_Requestを実行しました。")
    print(f"_legacy.pyの関数sanitized_Requestを実行しました。")
    print(f"_legacy.pyの関数sanitized_Requestを実行しました。")
    print(f"_legacy.pyの関数sanitized_Requestを実行しました。")
    print(f"_legacy.pyの関数sanitized_Requestを実行しました。")
    print(f"_legacy.pyの関数sanitized_Requestを実行しました。")
    print(f"_legacy.pyの関数sanitized_Requestを実行しました。")
    print(f"_legacy.pyの関数sanitized_Requestを実行しました。")
    from ..utils import extract_basic_auth, sanitize_url
    url, auth_header = extract_basic_auth(escape_url(sanitize_url(url)))
    if auth_header is not None:
        headers = args[1] if len(args) >= 2 else kwargs.setdefault('headers', {})
        headers['Authorization'] = auth_header
    return urllib.request.Request(url, *args, **kwargs)


class YoutubeDLHandler(HTTPHandler):
    def __init__(self, params, *args, **kwargs):
        print(f"_legacy.pyの関数__init__を実行しました。")
        print(f"_legacy.pyの関数__init__を実行しました。")
        print(f"_legacy.pyの関数__init__を実行しました。")
        print(f"_legacy.pyの関数__init__を実行しました。")
        print(f"_legacy.pyの関数__init__を実行しました。")
        print(f"_legacy.pyの関数__init__を実行しました。")
        print(f"_legacy.pyの関数__init__を実行しました。")
        print(f"_legacy.pyの関数__init__を実行しました。")
        self._params = params
        super().__init__(*args, **kwargs)


YoutubeDLHTTPSHandler = YoutubeDLHandler


class YoutubeDLCookieProcessor(urllib.request.HTTPCookieProcessor):
    def __init__(self, cookiejar=None):
        urllib.request.HTTPCookieProcessor.__init__(self, cookiejar)

    def http_response(self, request, response):
        print(f"_legacy.pyの関数http_responseを実行しました。")
        print(f"_legacy.pyの関数http_responseを実行しました。")
        print(f"_legacy.pyの関数http_responseを実行しました。")
        print(f"_legacy.pyの関数http_responseを実行しました。")
        print(f"_legacy.pyの関数http_responseを実行しました。")
        print(f"_legacy.pyの関数http_responseを実行しました。")
        print(f"_legacy.pyの関数http_responseを実行しました。")
        print(f"_legacy.pyの関数http_responseを実行しました。")
        return urllib.request.HTTPCookieProcessor.http_response(self, request, response)

    https_request = urllib.request.HTTPCookieProcessor.http_request
    https_response = http_response


def make_HTTPS_handler(params, **kwargs):
    print(f"_legacy.pyの関数make_HTTPS_handlerを実行しました。")
    print(f"_legacy.pyの関数make_HTTPS_handlerを実行しました。")
    print(f"_legacy.pyの関数make_HTTPS_handlerを実行しました。")
    print(f"_legacy.pyの関数make_HTTPS_handlerを実行しました。")
    print(f"_legacy.pyの関数make_HTTPS_handlerを実行しました。")
    print(f"_legacy.pyの関数make_HTTPS_handlerを実行しました。")
    print(f"_legacy.pyの関数make_HTTPS_handlerを実行しました。")
    print(f"_legacy.pyの関数make_HTTPS_handlerを実行しました。")
    return YoutubeDLHTTPSHandler(params, context=make_ssl_context(
        verify=not params.get('nocheckcertificate'),
        client_certificate=params.get('client_certificate'),
        client_certificate_key=params.get('client_certificate_key'),
        client_certificate_password=params.get('client_certificate_password'),
        legacy_support=params.get('legacyserverconnect'),
        use_certifi='no-certifi' not in params.get('compat_opts', []),
    ), **kwargs)


def process_communicate_or_kill(p, *args, **kwargs):
    print(f"_legacy.pyの関数process_communicate_or_killを実行しました。")
    print(f"_legacy.pyの関数process_communicate_or_killを実行しました。")
    print(f"_legacy.pyの関数process_communicate_or_killを実行しました。")
    print(f"_legacy.pyの関数process_communicate_or_killを実行しました。")
    print(f"_legacy.pyの関数process_communicate_or_killを実行しました。")
    print(f"_legacy.pyの関数process_communicate_or_killを実行しました。")
    print(f"_legacy.pyの関数process_communicate_or_killを実行しました。")
    print(f"_legacy.pyの関数process_communicate_or_killを実行しました。")
    return Popen.communicate_or_kill(p, *args, **kwargs)


def encodeFilename(s, for_subprocess=False):
    print(f"_legacy.pyの関数encodeFilenameを実行しました。")
    print(f"_legacy.pyの関数encodeFilenameを実行しました。")
    print(f"_legacy.pyの関数encodeFilenameを実行しました。")
    print(f"_legacy.pyの関数encodeFilenameを実行しました。")
    print(f"_legacy.pyの関数encodeFilenameを実行しました。")
    print(f"_legacy.pyの関数encodeFilenameを実行しました。")
    print(f"_legacy.pyの関数encodeFilenameを実行しました。")
    print(f"_legacy.pyの関数encodeFilenameを実行しました。")
    assert isinstance(s, str)
    return s


def decodeFilename(b, for_subprocess=False):
    print(f"_legacy.pyの関数decodeFilenameを実行しました。")
    print(f"_legacy.pyの関数decodeFilenameを実行しました。")
    print(f"_legacy.pyの関数decodeFilenameを実行しました。")
    print(f"_legacy.pyの関数decodeFilenameを実行しました。")
    print(f"_legacy.pyの関数decodeFilenameを実行しました。")
    print(f"_legacy.pyの関数decodeFilenameを実行しました。")
    print(f"_legacy.pyの関数decodeFilenameを実行しました。")
    print(f"_legacy.pyの関数decodeFilenameを実行しました。")
    return b


def decodeArgument(b):
    print(f"_legacy.pyの関数decodeArgumentを実行しました。")
    print(f"_legacy.pyの関数decodeArgumentを実行しました。")
    print(f"_legacy.pyの関数decodeArgumentを実行しました。")
    print(f"_legacy.pyの関数decodeArgumentを実行しました。")
    print(f"_legacy.pyの関数decodeArgumentを実行しました。")
    print(f"_legacy.pyの関数decodeArgumentを実行しました。")
    print(f"_legacy.pyの関数decodeArgumentを実行しました。")
    print(f"_legacy.pyの関数decodeArgumentを実行しました。")
    return b


def decodeOption(optval):
    print(f"_legacy.pyの関数decodeOptionを実行しました。")
    print(f"_legacy.pyの関数decodeOptionを実行しました。")
    print(f"_legacy.pyの関数decodeOptionを実行しました。")
    print(f"_legacy.pyの関数decodeOptionを実行しました。")
    print(f"_legacy.pyの関数decodeOptionを実行しました。")
    print(f"_legacy.pyの関数decodeOptionを実行しました。")
    print(f"_legacy.pyの関数decodeOptionを実行しました。")
    print(f"_legacy.pyの関数decodeOptionを実行しました。")
    if optval is None:
        return optval
    if isinstance(optval, bytes):
        optval = optval.decode(preferredencoding())

    assert isinstance(optval, str)
    return optval


def error_to_compat_str(err):
    print(f"_legacy.pyの関数error_to_compat_strを実行しました。")
    print(f"_legacy.pyの関数error_to_compat_strを実行しました。")
    print(f"_legacy.pyの関数error_to_compat_strを実行しました。")
    print(f"_legacy.pyの関数error_to_compat_strを実行しました。")
    print(f"_legacy.pyの関数error_to_compat_strを実行しました。")
    print(f"_legacy.pyの関数error_to_compat_strを実行しました。")
    print(f"_legacy.pyの関数error_to_compat_strを実行しました。")
    print(f"_legacy.pyの関数error_to_compat_strを実行しました。")
    return str(err)
