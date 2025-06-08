import argparse


arg_parser = argparse.ArgumentParser(description="Log statistics")
arg_parser.add_argument(
    "-p",
    "--path",
    help="Path or urls to logs",
    nargs="+",
)
arg_parser.add_argument(
    "--from_dt",
    help="Date time from in format: %Y-%m-%d %H:%M:%S",
)
arg_parser.add_argument(
    "--to_dt",
    help="Date time to in format: %Y-%m-%d %H:%M:%S",
)
arg_parser.add_argument(
    "-f",
    "--format",
    help="Format of output",
)
arg_parser.add_argument(
    "--filter-field",
    help="""Field to filter
    Possible fields:
            remote_addr
            remote_user
            method
            url
            protocol
            status
            body_bytes_sent
            http_referer
            http_user_agent""",
)
arg_parser.add_argument(
    "--filter-value",
    help="Value to filter",
)
arg_parser.add_argument("--output-file", help="Path/Name of output file")
