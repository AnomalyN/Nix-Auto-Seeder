import util

from ftplib import FTP

from loguru import logger


class Distro:

    def __init__(self, **kwargs):
        self.server = kwargs.get('server')
        self.paths = kwargs.get('paths', [])
        self.user = kwargs.get('user', 'anonymous')
        self.pw = kwargs.get('pass', 'anonymous@domain.com')

    def get_torrents(self):
        with FTP(self.server, self.user, self.pw) as ftp:

            for path in self.paths:
                for f in ftp.nlst(path):
                    print(f)

    def __str__(self):
        return f"{self.__class__.__name__} Distro"

    def __resp__(self):
        num_paths = len(self.pahts)
        return f"{self}: [{num_paths}]"
