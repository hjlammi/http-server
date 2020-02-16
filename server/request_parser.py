from lark import Lark, Transformer, v_args
from .request import Request

grammar = r'''
    request: startline headers* EMPTY_LINE body?

    startline: METHOD WS URI WS VERSION CR LF
    headers: (headers)* HEADER_KEY":" WS HEADER_VALUE CR LF
    body: BODY CR LF

    METHOD: "GET"
    URI: /\/[a-zA-Z0-9\/.]+/
    VERSION: "HTTP/1.1"
    HEADER_KEY: /[a-zA-Z0-9]+/
    HEADER_VALUE: /[a-zA-Z0-9\/\/.]+/
    EMPTY_LINE: CR LF
    BODY: /[a-zA-Z0-9<>\/]+/

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
            headers[0] if headers else None,
            headers[2] if (headers and len(headers) == 3) else None
        )

    @v_args(inline=True)
    def startline(self, method, ws1, uri, ws2, version, cr, lf):
        return dict(
            method = method.value,
            uri = uri.value,
            http_version = version.value
        )

    @v_args(inline=True)
    def headers(self, *header_args):
        headers = header_args[0]
        if (isinstance(headers, dict)):
            headers.update({header_args[1].value: header_args[3].value})
            return headers
        else:
            return {header_args[0].value: header_args[2].value}

    @v_args(inline=True)
    def EMPTY_LINE(self, *args):
        pass

    @v_args(inline=True)
    def body(self, body, cr, lf):
        return body.value
