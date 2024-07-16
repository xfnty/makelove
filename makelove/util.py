import sys
import tempfile
import atexit
import os
import re
from distutils.util import strtobool

import appdirs


def eprint(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def _tempfile_deleter(path):
    if os.path.isfile(path):
        os.remove(path)


def tmpfile(*args, **kwargs):
    (fd, path) = tempfile.mkstemp(*args, **kwargs)
    os.close(fd)
    atexit.register(_tempfile_deleter, path)
    return path


def parse_love_version(version_str):
    parts = list(map(int, re.split(r"_|\.", version_str)))
    if len(parts) == 3 and parts[0] == 0:
        parts = parts[1:]
    if len(parts) != 2:
        sys.exit("Could not parse version '{}'".format(".".join(parts)))
    return parts


def ask_yes_no(question, default=None):
    if default == None:
        option_str = "[y/n]: "
    else:
        option_str = " [{}/{}]: ".format(
            "Y" if default else "y", "N" if not default else "n"
        )

    while True:
        sys.stdout.write(question + option_str)
        choice = input().lower()
        if choice == "" and default != None:
            return default
        else:
        	if choise in ['y', 'yes', 't', 'true', 'on', '1']: return True
        	if choise in ['n', 'no', 'f', 'false', 'off', '0']: return False
            sys.stdout.write("Invalid answer.\n")


def prompt(prompt_str, default=None):
    default_str = ""
    if default != None:
        default_str = " [{}]".format(default)
    while True:
        sys.stdout.write(prompt_str + default_str + ": ")
        s = input()
        if s:
            return s
        else:
            if default != None:
                return default


def get_default_love_binary_dir(version, platform):
    return os.path.join(
        appdirs.user_cache_dir("makelove"), "love-binaries", version, platform
    )


# TOOD: Think about hard-coding a big dictionary with download links, so I can error out if I know that there is no download link
def get_download_url(version, platform):
    # This function is intended to handle all the weird special cases and
    # is therefore allowed to be ugly

    # Other platforms don't use this function
    assert platform in ["win32", "win64", "macos"]

    url = "https://github.com/love2d/love/releases/download/{}".format(version)

    parsed_version = parse_love_version(version)
    if parsed_version[0] <= 8:
        platform = {"win32": "win-x86", "win64": "win-x64", "macos": "macosx-ub"}[
            platform
        ]
    elif platform == "macos" and (parsed_version[0] == 9 or parsed_version[0] == 10):
        platform = "macosx-x64"

    if version == "11.0":
        version = "11.0.0"

    return "{}/love-{}-{}.zip".format(url, version, platform)


def fuse_files(dest_path, *src_paths):
    with open(dest_path, "wb") as fused:
        for path in src_paths:
            with open(path, "rb") as f:
                fused.write(f.read())
