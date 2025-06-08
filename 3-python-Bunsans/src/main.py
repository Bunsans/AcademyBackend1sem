# import logging
# import platform
from loguru import logger

# logging.basicConfig()
# logging.getLogger().setLevel(logging.INFO)
# logger = logging.getLogger(__name__)

from argument_parser import arg_parser
from logs_analyzer import LogAnalyzerService
from result_writer import result_writer_mapper

from constants import DEBUG


def arg_parse_decorator(func):
    def wrapper():
        args = arg_parser.parse_args()
        func(args)

    return wrapper


# python main.py -p /Users/al.s.kim/study/AcademyBackend/3-python-Bunsans/tests/logs.txt --from_dt "2015-05-24 14:05:46" --to_dt "2015-05-24 15:15:44" -f adoc
# python main.py -p /Users/al.s.kim/study/AcademyBackend/3-python-Bunsans/tests/test_folder_of_logs/logs.txt /Users/al.s.kim/study/AcademyBackend/3-python-Bunsans/tests/test_folder_of_logs/logs_2.txt  -f adoc --filter-field status --filter-value 200
# python main.py -p /Users/al.s.kim/study/AcademyBackend/3-python-Bunsans/tests/test_folder_of_logs/logs.txt /Users/al.s.kim/study/AcademyBackend/3-python-Bunsans/tests/test_folder_of_logs/logs_2.txt  -f adoc --filter-field method --filter-value GET
@arg_parse_decorator
def main(args) -> None:
    if DEBUG:
        logger.debug(args)

    log_analyzer = LogAnalyzerService(args)
    result_analyze = log_analyzer.run()
    result_witer = result_writer_mapper[args.format](
        result_analyze=result_analyze,
        output_path=args.output_file,
        format=args.format,
        from_dt=args.from_dt,
        to_dt=args.to_dt,
    )
    result_witer.write()


if __name__ == "__main__":
    main()
