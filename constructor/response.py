from enum import IntEnum
from dataclasses import dataclass
from typing import Any


class StatusCode(IntEnum):
    WRONG_MOVE = 100
    MOVE_DONE = 101
    IS_CHECK = 102


@dataclass(frozen=True)
class Response:
    status: StatusCode
    data: Any = None
