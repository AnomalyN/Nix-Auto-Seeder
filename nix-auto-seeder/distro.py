# Python imports
import re
import tempfile

from typing import List
from ftplib import FTP

# External libraries
from loguru import logger

# Local imports
import util
from torrents import TorrentPath, TorrentFile


class Distro:

    def __init__(self, **kwargs):
        self.server = kwargs.get('server')
        self.paths = kwargs.get('paths', [])
        self.logger = logger.bind(distro=self)

    def gather(self, **kwargs):
        results = []

        for path in self.paths:
            self.logger.debug("gather torrents from path: {}", path)

            torrent_file_paths = self.gather_torrent_paths(path)
            self.logger.debug("Path contains: {}\n{}", path, torrent_file_paths)
            self.logger.info("Identified {} torrent files in path: {}", len(torrent_file_paths), path)

            torrent_file_paths = self.filter_torrents(torrent_file_paths, **kwargs)
            torrent_files = [self._download(path) for path in torrent_file_paths]

            results += torrent_files

        return results

    def filter_torrents(self, paths, major=0, minor=0, arch=[]):
        """ Filter any TorrentPaths which does not meet requirements

        :param paths: list of TorrentPaths
        :param major: num of major version to download
        :param minor: num of minor version to download
        :param arch: list of architecture types to download
        :return: list of TorrentPaths which fullfills requirements
        """
        dic = dict()

        # Generate dict for sorting
        for torrent_path in paths:
            major_version = torrent_path.major

            # Remove any architecures from dict which are unwanted
            if arch and torrent_path.arch not in arch:
                continue

            if major_version not in dic:
                dic[major_version] = list()

            dic[major_version].append(torrent_path)

        major_lst = sorted(list(dic.keys()), reverse=True)

        # Create subset of major_lst, based on user input
        if major:
            print(major)
            major_lst = major_lst[:major]

        for key in major_lst:
            paths = dic[key]

            # Sort TorrentPaths based on minor version
            paths = sorted(paths, reverse=True)

            if minor:
                paths = paths[:minor]

            for entry in paths:
                yield entry

    def gather_torrent_paths(self, path):
        """ Get all torrent file paths

        :param path: path object (str/dict) to parse for torrent files
        :return list: path of torrent files in path
        """
        # Gather torrent files from single location
        if isinstance(path, str):
            if util.is_directory:

                files = self._list(path)
                return [TorrentPath(path=entry) for entry in util.filter_torrent_files(files)]
            else:
                return TorrentPath(path=path)

        elif isinstance(path, dict):

            paths = []
            path_iter = iter(path)

            cur_path = next(path_iter)
            cur_regex = path[cur_path]

            cur_obj = TorrentPath(path=cur_path)
            files = self._list(cur_obj.path)
            self.logger.trace("Files in path {}: {}", cur_obj.path, files)

            paths += cur_obj.extend(files, cur_regex)

            try:
                while cur_path := next(path_iter):
                    cur_regex = path[cur_path]
                    self.logger.trace("Parsing subdir: {}", cur_path)

                    new_paths = []
                    for p in paths:

                        p.extend_path(cur_path)
                        files = self._list(p.path)

                        new_paths += p.extend(files, cur_regex)

                    paths = new_paths

            except StopIteration:
                pass

            new_paths = []
            for path in paths:

                # Resulting path could still be directory, so get torrent files in those paths
                if util.is_directory(path.path):
                    files = self._list(path.path)
                    new_paths += path.extend_dir(files)

                else:
                    new_paths.append(path)

            paths = new_paths

            return paths

        else:
            raise Exception("Invalid file format used in paths")

    def _list(self, path: str) -> List[str]:
        self.logger.debug("Parent list")
        """ List available files/directories in path

        :return list: list of content in path
        """
        raise NotImplementedError()

    def _download(self, path: str) -> TorrentFile:
        """ Download torrent file from path

        :return TorrentFile: downloaded torrent file
        """

        raise NotImplementedError()

    def __str__(self):
        return self.__class__.__name__

    def __resp__(self):
        num_paths = len(self.paths)
        return f"{self}: [{num_paths}]"

    def __eq__(self, other):
        name = self.__class__.__name__
        if isinstance(other, Distro):
            return name == other.__class__.name

        elif isinstance(other, str):
            return name.lower() == other.lower()

        else:
            return False


class FTPDistro(Distro):

    def __init__(self, **kwargs):
        self.user = kwargs.pop('user', 'anonymous')
        self.pw = kwargs.pop('pass', 'anonymous@domain.com')

        super().__init__(**kwargs)

        self.session = FTP(self.server, self.user, self.pw)

    def _list(self, path: str) -> List[str]:
        return self.session.nlst(path)

    def _download(self, torrent_path: TorrentPath) -> List[str]:
        try:
            tmp_file = tempfile.SpooledTemporaryFile()

            self.logger.trace("Attempting to download: {}", torrent_path)
            self.session.retrbinary(f"RETR {torrent_path.path}", tmp_file.write, 8*1024)

            return TorrentFile(file=tmp_file, torrent_path=torrent_path)

        except Exception as e:
            self.logger.exception(e)
