import os
import re
import imp
import sys
import inspect
import tempfile
import itertools
import subprocess

from typing import List
from pathlib import Path

from loguru import logger


def get_distros(dir='distros'):
    path = Path('.') / dir

    for pyfile in path.glob('*.py'):
        found_module = imp.find_module(pyfile.stem, [path.resolve()])
        module = imp.load_module(pyfile.stem, found_module[0], found_module[1], found_module[2])

        for mem_name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and inspect.getmodule(obj) is module:
                yield obj()


def filter_torrent_files(files: list, ext: str = '.torrent') -> List[str]:
    """ Select torrent files from list of files

    :param list: list of filenames to filter
    :param ext: extension to verify whether file is torrent file (default `.torrent`)
    :return list: list of filenames which ends with extension
    """
    for entry in filter(lambda f: f.endswith(ext), files):
        yield entry


def run_deluge(t_file):
    try:
        with tempfile.NamedTemporaryFile() as tmp_file:

            # Copy content of torrent file in mem to tmp file
            copy_file(t_file, tmp_file)

            subprocess.run(
                ['deluge-console', 'add', tmp_file.name],
                check=True
            )
    except subprocess.CalledProcessError as cpe:
        logger.error("deluge-console exited with error: {}", cpe)

    except Exception as e:
        logger.error("Failed to run deluge-console: {}", e)


def setup_loguru(verbose):
    # Based on default loguru
    format = str(
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{extra[distro]}</cyan> | "
        "<level>{message}</level>",
    )

    logger.remove()
    logger.configure(extra={'distro': ''})

    # Set logging level based on verbose level
    if verbose == 0:
        logger.add(sys.stderr, format=format, level="INFO", diagnose=False, backtrace=False, catch=False)
    elif verbose == 1:
        logger.add(sys.stderr, format=format, level="DEBUG", diagnose=False, backtrace=True)
    elif verbose >= 2:
        logger.add(sys.stderr, format=format, level="TRACE", diagnose=True, backtrace=True)


def filter_releases(releases, num=0):
    releases = {k: v for k, v in sorted(releases.items(), key=lambda i: i[0], reverse=True)}

    # if num_releases is 0, get all versions
    if num:
        releases = itertools.islice(releases.items(), num)

    return releases


def is_directory(path: str) -> bool:
    """ Verify if path is directory or file

    :param: path to verify
    :return: path is directory
    """
    (head, filename) = os.path.split(path)

    if not filename:
        return True

    else:
        (path, ext) = os.path.splitext(filename)

        return not bool(ext) or (bool(ext) and bool(re.match(r'\.?\d+', ext)))
