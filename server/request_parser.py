from lark import Lark, Transformer, v_args

grammar = r'''
    request: startline headers?

    startline: METHOD WS URI WS VERSION CR LF
    headers: HEADER_KEY":" WS HEADER_VALUE CR LF

    METHOD: "GET"
    URI: /\/[a-zA-Z0-9\/.]+/
    VERSION: "HTTP/1.1"
    HEADER_KEY: /[a-zA-Z0-9]+/
    HEADER_VALUE: /[a-zA-Z0-9\/]+/

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
    def request(self, startline, headers=None):
        return {
            "method": startline["method"],
            "uri": startline["uri"],
            "http_version": startline["http_version"],
            "headers": headers
        }

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
            header_key: header_value
        }
