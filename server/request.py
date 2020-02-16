from dataclasses import dataclass
from typing import List, Any

@dataclass
class Request:
    method: str
    uri: str
    http_version: str
    headers: List[dict]
    body: Any
