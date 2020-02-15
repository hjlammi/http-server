from lark import Lark, Transformer, v_args
from .request import Request

grammar = r'''
    request: startline headers*

    startline: METHOD WS URI WS VERSION CR LF
    headers: HEADER_KEY":" WS HEADER_VALUE CR LF

    METHOD: "GET"
    URI: /\/[a-zA-Z0-9\/.]+/
    VERSION: "HTTP/1.1"
    HEADER_KEY: /[a-zA-Z0-9]+/
    HEADER_VALUE: /[a-zA-Z0-9\/\/.]+/
    EMPTY_LINE: CR LF

    %ignore EMPTY_LINE

    %import common.WS
    %import common.CR
    %import common.LF
'''

request_parser = Lark(grammar, start='request')

def parse_request(request):
    result = request_parser.parse(request)
    return TreeToRequest().transform(result)

class TreeToRequest(Transformer):
    @v_args(inline=True)
    def request(self, startline, *headers):
        return Request(
            startline["method"],
            startline["uri"],
            startline["http_version"],
            tuple_to_dict(headers)
        )

    @v_args(inline=True)
    def startline(self, method, ws1, uri, ws2, version, cr, lf):
        return dict(
            method = method.value,
            uri = uri.value,
            http_version = version.value
        )

    @v_args(inline=True)
    def headers(self, header_key, ws, header_value, cr, lf):
        return {
            header_key.value: header_value.value
        }

def tuple_to_dict(headers):
    headers_in_dict = {}
    for header in headers:
        headers_in_dict = {**headers_in_dict, **header}
    return headers_in_dict
