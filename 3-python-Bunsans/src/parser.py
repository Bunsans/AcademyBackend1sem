import datetime
import re

from loguru import logger
from structures import Log


class ParserLog:
    def __init__(self, pattern: re.Pattern) -> None:
        self.pattern = pattern

    def parse_line_to_log(self, line: str) -> Log:
        match = self.pattern.search(line.strip())

        if match is None:
            raise ValueError("Line does not match NGINX log pattern")
        try:
            (
                remote_addr,
                remote_user,
                time_local,
                request,
                status,
                body_bytes_sent,
                http_referer,
                http_user_agent,
            ) = match.groups()
        except ValueError:
            logger.error("Line does not match NGINX log pattern")

        try:
            request = request.split()
            method, url, protocol = request
        except ValueError:
            method, url, protocol = request[0], request[1], request[2]
            logger.error(f"Error parsing request: {request}")

        time_local = self._to_datetime(time_local)
        log = Log(
            remote_addr,
            remote_user,
            time_local,
            method,
            url,
            protocol,
            int(status),
            int(body_bytes_sent),
            http_referer,
            http_user_agent,
        )
        return log

    def _to_datetime(self, time_local: str) -> datetime.datetime:
        return datetime.datetime.strptime(time_local, "%d/%b/%Y:%H:%M:%S %z")
