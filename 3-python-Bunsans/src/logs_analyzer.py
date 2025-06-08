from collections import Counter
import datetime
import glob
import re

from loguru import logger
from structures import InputArgs, Log, ResultAnalyze
from parser import ParserLog
from constants import ERROR_APPROX, DEBUG, LOG_PATTERN
import validators
import requests


def _cast_to_datetime_from(datetime_str: str) -> datetime.datetime:
    if datetime_str is None:
        return datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
    return _get_date_time(datetime_str)


def _cast_to_datetime_to(datetime_str: str) -> datetime.datetime:
    if datetime_str is None:
        return datetime.datetime.max.replace(tzinfo=datetime.timezone.utc)
    return _get_date_time(datetime_str)


def _get_date_time(datetime_str: str) -> datetime.datetime:
    formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue
    raise ValueError(
        f'Invalid datetime format: {datetime_str}\nTry to use format: "%Y-%m-%d %H:%M:%S" or "%Y-%m-%d"'
    )


class Analyzer:
    def __init__(
        self,
        datetime_from: str,
        datetime_to: str,
        filter_field,
        filter_value,
    ) -> None:
        self.logs_paths = []
        self.urls = []
        self.datetime_from = _cast_to_datetime_from(datetime_from)
        self.datetime_to = _cast_to_datetime_to(datetime_to)

        if DEBUG:
            logger.debug(
                f"datetime_from: {self.datetime_from}, datetime_to: {self.datetime_to}'"
            )

        if self.datetime_from > self.datetime_to:
            raise ValueError(
                f"from_dt must be less to_dt\n{self.datetime_from} > {self.datetime_to}"
            )

        self.filter_field = filter_field
        self.filter_value = filter_value
        if self.filter_field:
            try:
                # regex = glob.translate(self.filter_value)
                self.filter_value_matcher = re.compile(self.filter_value)
            except TypeError:
                raise ValueError(f"Invalid filter value: {self.filter_value}")

        self.requests_count = 0
        self.resource_counter = Counter()
        self.status_counter = Counter()
        self.response_sizes_sum = 0  # for average
        self.response_sizes_counter = Counter()  # for percintile
        self.hours_counter = Counter()
        self.remote_addr_counter = Counter()

    def add_url(self, url_name: str):
        self.urls.append(url_name)

    def add_log_path(self, log_name: str):
        self.logs_paths.append(log_name)

    def _time_in_border(self, time_local: datetime) -> bool:
        return (
            self.datetime_from.timestamp()
            <= time_local.timestamp()
            <= self.datetime_to.timestamp()
        )

    # remote_addr, remote_user, request[method, url, protocol], status,  body_bytes_sent, http_referer, http_user_agent
    def _filter_field_value(self, log: Log) -> bool:
        if (self.filter_field or self.filter_value) is None:
            return True
        # in this step self.filter_field and self.filter_value must be not None, check in parser_args
        # Maybe should add "in self.filter_value" and filter_value make list
        log_value = getattr(log, self.filter_field)
        match = self.filter_value_matcher.match(str(log_value))
        logger.debug(f"match: {match}, log_value: {log_value}")
        if match:
            return True
        return False

    def _update_response_sizes(self, body_bytes_sent: int):
        # round to number which divisible by ACCURACY_BINS
        body_bytes_sent = round(body_bytes_sent / ERROR_APPROX) * ERROR_APPROX
        self.response_sizes_counter.update([body_bytes_sent])

    def update_statistics(self, log: Log) -> ResultAnalyze:
        logger.debug(
            f"log.time_local: {log.time_local}, {self._filter_field_value(log)}"
        )
        if self._time_in_border(log.time_local) and self._filter_field_value(log):
            self.requests_count += 1
            self.resource_counter.update([log.url])
            self.status_counter.update([log.status])
            self.response_sizes_sum += log.body_bytes_sent
            self._update_response_sizes(log.body_bytes_sent)
            self.hours_counter.update([log.time_local.hour])
            self.remote_addr_counter.update([log.remote_addr])

    def get_result_of_analyze(self) -> ResultAnalyze:
        return ResultAnalyze(
            urls_paths=self.urls,
            logs_paths=self.logs_paths,
            datetime_from=self.datetime_from,
            datetime_to=self.datetime_to,
            requests_count=self.requests_count,
            resource_counter=self.resource_counter,
            status_counter=self.status_counter,
            response_sizes_sum=self.response_sizes_sum,
            response_sizes_counter=self.response_sizes_counter,
            hours_counter=self.hours_counter,
            remote_addr_counter=self.remote_addr_counter,
        )


class LogAnalyzerService:
    def __init__(self, args: InputArgs) -> None:
        self.paths = args.path

        self.parser_log = ParserLog(pattern=LOG_PATTERN)
        self.analyzer = Analyzer(
            datetime_from=args.from_dt,
            datetime_to=args.to_dt,
            filter_field=args.filter_field,
            filter_value=args.filter_value,
        )

    def _update_sets_logs_urls(self):
        for path in self.paths:
            if validators.url(path):
                self.set_of_urls.add(path)
                continue
            # if DEBUG:
            #     logger.debug(f"path in self.paths: {path}")
            file_paths = glob.glob(path, recursive=True)
            # if DEBUG:
            #     logger.debug(f"file_paths: {file_paths}")
            for file_path in file_paths:
                self.set_of_local_paths.add(file_path)
                if DEBUG:
                    logger.debug(f"file_path: {file_path}")

    def _generator_of_logs_line_from_url(self, url):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        for line in response.iter_lines(decode_unicode=True):
            yield line  # тут можно создать log, и сделать update_statistics

    def _analyze_urls(self):
        for url in self.set_of_urls:
            self.analyzer.add_url(url)
            for line in self._generator_of_logs_line_from_url(url):
                log = self.parser_log.parse_line_to_log(line)
                self.analyzer.update_statistics(log)

    def _analyze_local_paths(self):
        for file_path in self.set_of_local_paths:
            self.analyzer.add_log_path(file_path)
            with open(file_path, "r") as file_path:
                while line := file_path.readline():
                    log = self.parser_log.parse_line_to_log(line)
                    self.analyzer.update_statistics(log)

    def run(self) -> ResultAnalyze:
        self.set_of_local_paths = set()
        self.set_of_urls = set()
        if DEBUG:
            logger.debug(f"self.paths: {self.paths}")
        self._update_sets_logs_urls()
        if DEBUG:
            logger.debug(
                f"set_of_logs: {self.set_of_local_paths}\nset_of_urls: {self.set_of_urls}"
            )
        if self.set_of_local_paths:
            self._analyze_local_paths()
        if self.set_of_urls:
            self._analyze_urls()
        return self.analyzer.get_result_of_analyze()
