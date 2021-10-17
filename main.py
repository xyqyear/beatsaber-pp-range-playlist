import json
import gzip
from typing import Any, Union
import urllib
import argparse


# ! [hash]['diffs'][0]['pp'] is str, need to be converted to float
diff_info_T = dict[str, Union[str, int, float]]
all_maps_T = dict[str, Union[list[diff_info_T], str, int, float]]

beat_star_database_link = "https://cdn.wes.cloud/beatstar/bssb/v2-all.json.gz"

# TODO
def download(url: str) -> bytes:
    return b""


# TODO
def decompress_gz(file_content: bytes) -> bytes:
    return b""


def get_all_maps(
    source: str,
) -> dict[str, all_maps_T]:
    file_content = str()
    if source:
        gz_file = download(beat_star_database_link)
        file_content = decompress_gz(gz_file).decode("utf-8")
    else:
        with open(source, "r", encoding="utf-8") as f:
            file_content = f.read()

    return json.loads(file_content)


def construct_command_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="This script download scraped scoresaber data from beatstardatabase and pick songs that meet specified range to make a playlist."
    )
    parser.add_argument(
        "-l",
        "--lower-bound",
        dest="lower_bound",
        type=float,
        help="the lower bound of the range (decimal, inclusive)",
        default=0,
    )
    parser.add_argument(
        "-u",
        "--upper-bound",
        dest="upper_bound",
        type=float,
        help="the upper bound of the range (decimal, exclusive)",
        default=1e5,
    )
    parser.add_argument(
        "-s", "--source-file", dest="source_file", type=str, help="", default=""
    )
    return parser.parse_args()


# TODO
def filter_map(all_maps: all_maps_T, lower: float, upper: float) -> list[str]:
    return list()


# TODO
def construct_playlist(all_maps: all_maps_T) -> dict[str, Any]:
    return dict()


def main():
    parser = construct_command_parser()


if __name__ == "__main__":
    main()
