import argparse
from pathlib import Path


def get_headers(*args) -> dict:
    return dict([tuple(arg.split(":", 1)) for arg in args if arg])  # noqa


def get_command_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="Directory path", type=Path)
    return parser.parse_args()
