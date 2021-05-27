import tempfile

from ftplib import FTP

from loguru import logger

import util


class Distro:

    def __init__(self, **kwargs):
        self.server = kwargs.get('server')
        self.paths = kwargs.get('paths', [])
        self.user = kwargs.get('user', 'anonymous')
        self.pw = kwargs.get('pass', 'anonymous@domain.com')

    def get_torrents(self):
        with FTP(self.server, self.user, self.pw) as ftp:

            torrent_files = self.get_torrents_paths(ftp)
            logger.info("Got {} torrent_files from {}", len(torrent_files), self)

            for t_file in self.get_torrents_files(ftp, torrent_files):
                yield t_file

    def get_torrents_paths(self, ftp):
        for path in self.paths:
            files = ftp.nlst(path)
            logger.debug("Identified {} files", len(files))

            # Filter files to only list torrent files
            torrent_files = list(filter(util.verify_torrents, files))
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
