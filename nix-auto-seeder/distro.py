# Python imports
import tempfile
from ftplib import FTP

# External libraries
from loguru import logger

# Local imports
import util


class Distro:

    def __init__(self, **kwargs):
        self.server = kwargs.get('server')
        self.paths = kwargs.get('paths', [])
        self.user = kwargs.get('user', 'anonymous')
        self.pw = kwargs.get('pass', 'anonymous@domain.com')

    def get_torrents(self, num_releases=1):
        with FTP(self.server, self.user, self.pw) as ftp:

            torrent_files = self.get_torrents_paths(ftp, num_releases)
            logger.info("Got {} torrent_files from {}", len(torrent_files), self)

            for t_file in self.get_torrents_files(ftp, torrent_files):
                yield t_file

    def get_torrents_paths(self, ftp, num_releases=1):
        torrent_files = []

        for path in self.paths:
            files = ftp.nlst(path)
            logger.debug("Identified {} files for path: {}", len(files), path)

            # Filter files to only list torrent files
            logger.trace("[{}] {} FTP files: {}", self, path, files)
            torrent_files += list(filter(util.verify_torrents, files))

        logger.trace("[{}] FTP torrent files: {}", self, torrent_files)
        return torrent_files

    def get_torrents_files(self, ftp, torrent_files):
        for t_file in torrent_files:
            filename = t_file.split('/')[-1]
            tmp_file = tempfile.SpooledTemporaryFile()

            try:
                ftp.retrbinary(f"RETR {t_file}", tmp_file.write, 8*1024)
                yield (filename, tmp_file)
            except Exception as e:
                logger.exception(e)

    def __str__(self):
        return f"{self.__class__.__name__} Distro"

    def __resp__(self):
        num_paths = len(self.pahts)
        return f"{self}: [{num_paths}]"

    def __eq__(self, other):
        name = self.__class__.__name__
        if isinstance(other, Distro):
            return name == other.__class__.name

        elif isinstance(other, str):
            return name.lower() == other.lower()

        else:
            return False
