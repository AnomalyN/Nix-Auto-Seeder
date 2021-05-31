import os
import re
import copy
import tempfile
import contextlib

from typing import List

from dataclasses import dataclass

from loguru import logger

import util


@dataclass
class TorrentPath:
    """ Data class containing info regarding path to torrent file
    """

    path: str
    major: str = None
    minor: str = None
    arch: str = None

    @property
    def version(self):
        return f"{self.major}.{self.minor}"

    @property
    def filename(self):
        (head, filename) = os.path.split(self.path)
        return filename

    def extend_path(self, path: str):
        """ Add a new sub path to current path

        :param path: subpath to add to path of TorrentPath
        """
        path = path.lstrip('/')
        self.path = os.path.join(self.path, path)

    def extend(self, files, regex):
        """ Generate new TorrentPaths from files and regex

        :param files: list of filenames in path
        :param regex: regex used to filter filenames
        :return: list of new TorrentPaths generated from filter
        """

        regex = re.compile(regex)

        for file in files:
            (head, name) = os.path.split(file)
            match = regex.search(name)

            if not match:
                continue

            groups = match.groupdict()

            new_obj = copy.copy(self)
            new_obj.extend_path(name)

            for param in ['minor', 'major', 'arch']:
                if param in groups:
                    setattr(new_obj, param, groups[param])

            yield new_obj

    def extend_dir(self, files: List):
        """ Generate new TorrentPath for all torrent files in current TorrentPath directory

        :param: list of files
        :yield: new TorrentPath for torrent files
        """

        for torrent_file in util.filter_torrent_files(files):
            (head, filename) = os.path.split(torrent_file)
            new_obj = copy.copy(self)
            new_obj.extend_path(filename)

            yield new_obj

    def __lt__(self, other):
        if self.major == other.major:
            if self.minor == other.minor:
                return self.arch > other.arch
            else:
                return self.minor > other.minor
        else:
            return self.major > self.major

@dataclass
class TorrentFile:
    """ Data class containing actual torrent file
    """

    file: object
    torrent_path: TorrentPath = None

    @property
    def filename(self):
        return self.torrent_path.filename

    def copy_content_to(self, output):
        self.file.seek(0)
        output.write(self.file.read())

    @contextlib.contextmanager
    def local_file(self):
        """ Write content of torrent file to filesystem accessible file

            Due to context manager local file is automatically deleted after this function is run

            :return: filename of local file
        """
        with tempfile.NamedTemporaryFile() as tmp_file:
            self.copy_content_to(tmp_file)
            yield tmp_file.name

    def __str__(self):
        return self.filename
