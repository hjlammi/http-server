from dataclasses import dataclass, field
from typing import List, Any

REASON_PHRASES = {
    200: 'OK',
    204: 'No Content'
}

@dataclass
class Response:
    status_code: int
    headers: List[str] = field(default_factory=list)
    body: str = ''
    reason_phrase: str = 'OK'
    http_version: str = 'HTTP/1.1'

    def serialize(self):
        reason = REASON_PHRASES[self.status_code]
        response = f'{self.http_version} {self.status_code} {reason}\r\n'
        if self.headers:
            for header in self.headers:
                response += header
                response += '\r\n'
        response += '\r\n'
        if self.body:
            response += self.body
        response = response.encode()
        return response
