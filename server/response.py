from dataclasses import dataclass
from typing import List, Any

REASON_PHRASES = {
    200: 'OK',
    204: 'No Content'
}

@dataclass
class Response:
    status_code: int
    reason_phrase: str = 'OK'
    http_version: str = 'HTTP/1.1'

    def serialize(self):
        reason = REASON_PHRASES[self.status_code]
        return f'{self.http_version} {self.status_code} {reason}\r\n'
