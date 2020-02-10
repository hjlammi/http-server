from lark import Lark, Transformer, v_args

grammar = r'''
    request: METHOD URI VERSION

    METHOD: "GET" | "PUT"
    URI: /\/[a-zA-Z0-9\/.]+/
    VERSION: "HTTP/1.1"

    %import common.WS
    %ignore WS
'''

request_parser = Lark(grammar, start='request')

def parse_request(request):
    result = request_parser.parse(request)
    return TreeToRequest().transform(result)

class TreeToRequest(Transformer):
    @v_args(inline=True)
    def request(self, method, uri, version):
        return dict(
            method = method.value,
            uri = uri.value,
            http_version = version.value
        )
