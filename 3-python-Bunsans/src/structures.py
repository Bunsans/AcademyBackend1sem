from collections import Counter
from dataclasses import dataclass
import datetime
from pathlib import Path
from typing import List


@dataclass
class InputArgs:
    path: str
    from_dt: str = None
    to_dt: str = None
    format: str = None
    filter_field: str = None
    filter_value: str = None


@dataclass
class ResultAnalyze:
    urls_paths: List[str]
    logs_paths: List[Path]
    datetime_from: datetime.datetime | None
    datetime_to: datetime.datetime | None

    requests_count: int
    resource_counter: Counter[str, int]
    status_counter: Counter[int, int]
    response_sizes_sum: int  # for average
    response_sizes_counter: Counter[int, int]  # for percintile

    hours_counter: Counter[int, int]
    remote_addr_counter: Counter[str, int]


@dataclass
class Log:
    remote_addr: str
    remote_user: str
    time_local: datetime.datetime
    method: str
    url: str
    protocol: str
    status: int
    body_bytes_sent: int
    http_referer: str
    http_user_agent: str

    # def get(self, key):
    #     return
