import argparse

arg_parser = argparse.ArgumentParser(description="Log statistics")
arg_parser.add_argument(
    "--num-workers", help="number of workers to multiprocess", type=int, default=1
)
arg_parser.add_argument("-p", "--path", help="Path to save image", default="test")
arg_parser.add_argument(
    "-sd",
    "--sample-degree",
    help="Degree of 10 of samples init coordinates",
    default=2e4,
)
arg_parser.add_argument(
    "-i",
    "--iter-degree",
    help="Degree of 10 of iterations",
    default=1e3,
)
arg_parser.add_argument(
    "-s",
    "--symetry_coef",
    help="Coeficient of symetry, if yot don't want symetry, set it to 1",
    type=int,
    default=1,
)
arg_parser.add_argument(
    "--resol_x",
    help="Resolution of x, preferably 1920",
    type=int,
    default=1920,
)
arg_parser.add_argument(
    "--resol_y",
    help="Resolution of y, preferably 1080",
    type=int,
    default=1080,
)
arg_parser.add_argument(
    "-c",
    "--colors_num",
    help="Number of colors",
    type=int,
    default=5,
)


def parse_to_int(str_: str):
    try:
        str_ = int(str_)
    except ValueError:
        base, pow_ = str_.split("e")
        str_ = int(base) * (10 ** int(pow_))
    return str_


def arg_parse_decorator(func):
    def wrapper():
        args = arg_parser.parse_args()
        args.iter_degree = parse_to_int(args.iter_degree)
        args.sample_degree = parse_to_int(args.sample_degree)
        func(args)

    return wrapper
