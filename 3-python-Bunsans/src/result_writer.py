from abc import ABC, abstractmethod
import os
from typing import Literal
from loguru import logger
from structures import ResultAnalyze
from http.client import responses

from constants import (
    DEBUG,
    NUMBER_MOST_COMMON_HOURS,
    PERCENTILE,
)


class ResultWriter(ABC):
    suffix: Literal["md", "adoc"]

    def __init__(
        self,
        result_analyze: ResultAnalyze,
        from_dt: str,
        to_dt: str,
        output_path: str = "./result",
        most_common_number: int = 5,
    ) -> None:
        self._set_suffix()
        self.output_path = output_path

        self.logs_paths = self._parse_list_of_paths(result_analyze.logs_paths)
        self.urls_paths = self._parse_list_of_paths(result_analyze.urls_paths)

        self.from_dt = from_dt
        self.to_dt = to_dt

        self.requests_count = result_analyze.requests_count
        try:
            self.response_sizes_average = round(
                result_analyze.response_sizes_sum / self.requests_count
            )
        except ZeroDivisionError:
            self.response_sizes_average = 0
        self.most_requested_resources = result_analyze.resource_counter.most_common(
            most_common_number
        )
        self.most_status_codes = result_analyze.status_counter.most_common(
            most_common_number
        )
        self.most_hours = result_analyze.hours_counter.most_common(
            NUMBER_MOST_COMMON_HOURS
        )
        self.most_remote_addr_counter = result_analyze.remote_addr_counter.most_common(
            most_common_number
        )

        self.response_sizes_percintile = self._get_percintile(
            result_analyze.response_sizes_counter,
        )

        if DEBUG:
            logger.debug(
                f"""requests_count: {self.requests_count}
response_sizes_average: {self.response_sizes_average}
most_requested_resources: {self.most_requested_resources}
most_status_codes: {self.most_status_codes}
most_hours: {self.most_hours}
most_remote_addr_counter: {self.most_remote_addr_counter}
response_sizes_percintile: {self.response_sizes_percintile}"""
            )

    def _parse_list_of_paths(self, list_of_paths):
        if list_of_paths:
            return ", ".join([os.path.basename(log_path) for log_path in list_of_paths])
        else:
            return "-"

    def _get_percintile(self, response_sizes_counter):
        quantity_5_percentile = round(self.requests_count / 100 * (100 - PERCENTILE))
        # use reversed sort to find 95 percentile from tail
        for size, quantity_in_bin in sorted(
            response_sizes_counter.items(), reverse=True
        ):
            quantity_5_percentile -= quantity_in_bin
            if quantity_5_percentile <= 0:
                return size

    def _save_to_file(self, string_result: str, output_path: str = "./result") -> None:
        output_path = self.output_path or output_path
        with open(f"{output_path}.{self.suffix}", "w") as f:  # encoding="utf-8"
            f.write(string_result)
            logger.info(f"Result saved to {output_path}.{self.suffix}")

    @abstractmethod
    def _set_suffix(self):
        pass

    @abstractmethod
    def _get_general_info(self):
        pass

    @abstractmethod
    def _get_requested_resources(self):
        pass

    @abstractmethod
    def _get_response_codes(self):
        pass

    @abstractmethod
    def _get_most_common_hours(self):
        pass

    @abstractmethod
    def _get_most_common_remote_addr(self):
        pass

    def write(self) -> None:
        string_result = self._get_general_info()
        string_result += self._get_requested_resources()
        string_result += self._get_response_codes()
        string_result += self._get_most_common_hours()
        string_result += self._get_most_common_remote_addr()
        if DEBUG:
            logger.debug(f"\n{string_result}")
        self._save_to_file(string_result)


class ResultWriterMD(ResultWriter):
    def _set_suffix(self):
        self.suffix = "md"

    # [str(log_path.name) for log_path in self.logs_names]}
    def _get_general_info(self) -> str:
        return f"""#### Общая информация
| Метрика | Значение |
|:---------------------:|-------------:|
| Файл(-ы) | `{self.logs_paths}` |
| Url(-ы) | `{self.urls_paths}` |
| Начальное время | {"-" if self.from_dt is None else self.from_dt} |
| Конечное время | {"-" if self.to_dt is None else self.to_dt} |
| Количество запросов | {self.requests_count} |
| Средний размер ответа | {self.response_sizes_average}b |
| 95p размера ответа | {self.response_sizes_percintile}b |
"""

    def _get_requested_resources(self) -> str:
        result_string = "#### Запрашиваемые ресурсы\n\n| Ресурс | Количество |\n|:------------------------------:|-----------:|\n"
        for resource, quantity in self.most_requested_resources:
            result_string += f"| `{resource}` | {quantity} |\n"
        return result_string

    def _get_response_codes(self) -> str:
        result_string = "#### Коды ответа\n\n| Код | Имя | Количество |\n|:---:|:---------------------:|-----------:|\n"
        for status_code, quantity in self.most_status_codes:
            result_string += (
                f"| {status_code} | {responses[status_code]} | {quantity} |\n"
            )
        return result_string

    def _get_most_common_hours(self) -> str:
        result_string = "#### Наиболее загруженные часы\n\n| Час | Количество |\n|:---:|-----------:|\n"
        for hour, quantity in self.most_hours:
            result_string += f"| {hour} | {quantity} |\n"
        return result_string

    def _get_most_common_remote_addr(self) -> str:
        result_string = "#### Наиболее частые IP-адреса\n\n| IP-адрес | Количество |\n|:-------------------:|-----------:|\n"
        for remote_addr, quantity in self.most_remote_addr_counter:
            result_string += f"| {remote_addr} | {quantity} |\n"
        return result_string


class ResultWriterADOC(ResultWriter):
    def _set_suffix(self):
        self.suffix = "adoc"

    def _get_general_info(self) -> str:
        return f"""[cols="<,<",options="header"]
|====
|Метрика|Значение
| Файл(-ы) | `{self.logs_paths}`
| Url(-ы) | `{self.urls_paths}`
| Начальное время | {"-" if self.from_dt is None else self.from_dt}
| Конечное время | {"-" if self.to_dt is None else self.to_dt}
| Количество запросов | {self.requests_count}
| Средний размер ответа | {self.response_sizes_average}b
| 95p размера ответа | {self.response_sizes_percintile}b
|====\n
"""

    def _get_requested_resources(self) -> str:
        result_string = """[cols="<,<",options="header"]\n|====\n|Ресурс|Количество """
        for resource, quantity in self.most_requested_resources:
            result_string += f"| `{resource}` | {quantity}\n"
        result_string += "|====\n\n"
        return result_string

    def _get_response_codes(self) -> str:
        result_string = (
            """[cols="<,<,<",options="header"]\n|====\n|Код|Имя|Количество"""
        )
        for status_code, quantity in self.most_status_codes:
            result_string += (
                f"| {status_code} | {responses[status_code]} | {quantity}\n"
            )
        result_string += "|====\n\n"
        return result_string

    def _get_most_common_hours(self) -> str:
        result_string = """[cols="<,<",options="header"]\n|====\n|Час|Количество"""
        for hour, quantity in self.most_hours:
            result_string += f"| {hour} | {quantity}\n"
        result_string += "|====\n\n"
        return result_string

    def _get_most_common_remote_addr(self) -> str:
        result_string = """[cols="<,<",options="header"]\n|====\n|IP-адрес|Количество"""
        for remote_addr, quantity in self.most_remote_addr_counter:
            result_string += f"| {remote_addr} | {quantity}\n"
        result_string += "|====\n\n"
        return result_string


result_writer_mapper: dict[str, type[ResultWriter]] = {
    "markdown": ResultWriterMD,
    "adoc": ResultWriterADOC,
}
