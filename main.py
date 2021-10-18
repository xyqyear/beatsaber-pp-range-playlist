import json
import gzip
from typing import TypedDict, Union
import urllib
import argparse


# ! [hash]['diffs'][0]['pp'] is str, need to be converted to float
Diff = TypedDict(
    "Diff",
    {
        "bmb": int,
        "diff": str,
        "len": int,
        "njs": int,
        "njt": int,
        "nts": int,
        "obs": int,
        "pp": str,
        "scores": str,
        "star": str,
        "type": int,
    },
)
Map = TypedDict(
    "Map",
    {
        "automapper": Union[str, None],
        "bpm": int,
        "diffs": list[Diff],
        "downVotes": int,
        "downloadCount": int,
        "heat": float,
        "key": str,
        "mapper": str,
        "rating": float,
        "song": str,
        "upVotes": int,
        "uploaddate": str,
    },
)
PlaylistSongDiff = TypedDict("PlaylistSongDiff", {"characteristic": str, "name": str})
PlaylistSong = TypedDict(
    "PlaylistSong", {"hash": str, "difficulties": list[PlaylistSongDiff]}
)
Playlist = TypedDict(
    "Playlist",
    {
        "playlistTitle": str,
        "playlistAuthor": str,
        "playlistDescription": str,
        "songs": list[PlaylistSong],
        "image": str,
    },
)

beat_star_database_link = "https://cdn.wes.cloud/beatstar/bssb/v2-all.json.gz"


# TODO
def download(url: str) -> bytes:
    return b""


# TODO
def image_bytes_to_data_url(image_bytes: bytes) -> str:
    return ""


# TODO
def decompress_gz(file_content: bytes) -> bytes:
    return b""


def get_all_maps(
    source: str,
) -> dict[str, Map]:
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
        "-s",
        "--source-file",
        dest="source_file",
        type=str,
        help="the path of the beat star data file",
        default="",
    )
    parser.add_argument(
        "-o",
        "--save-as",
        dest="save_as",
        type=str,
        help="save playlist as",
        default="playlist.json",
    )
    return parser.parse_args()


def filter_map(
    all_maps: dict[str, Map], lower: float, upper: float
) -> list[tuple[str, list[str]]]:
    map_hash_list: list[tuple[str, list[str]]] = list()
    for map_hash, map_info in all_maps.items():
        diffs: list[str] = list()
        for diff in map_info["diffs"]:
            if lower <= float(diff["pp"]) < upper:
                if diff["diff"] == "Expert+":
                    diffs.append("ExpertPlus")
                else:
                    diffs.append(diff["diff"])
        map_hash_list.append((map_hash, diffs))
    return map_hash_list


def construct_playlist(
    map_hash_list: list[tuple[str, list[str]]],
    image: bytes,
    title: str = "playlist",
    author: str = "",
    description: str = "",
) -> Playlist:
    song_list: list[PlaylistSong] = list()
    for song_hash, diffs in map_hash_list:
        diff_list: list[PlaylistSongDiff] = []
        for diff in diffs:
            diff_list.append({"characteristic": "Standard", "name": diff})
        song_list.append({"hash": song_hash, "difficulties": diff_list})
    return {
        "playlistTitle": title,
        "playlistAuthor": author,
        "playlistDescription": description,
        "songs": song_list,
        "image": image_bytes_to_data_url(image),
    }


def main():
    args = construct_command_parser()
    all_maps = get_all_maps(args.source_file)
    map_hash_list = filter_map(all_maps, args.lower_bound, args.upper_bound)
    playlist = construct_playlist(map_hash_list, b"")
    with open(args.save_as, "w", encoding="utf-8") as f:
        f.write(json.dumps(playlist))


if __name__ == "__main__":
    main()
