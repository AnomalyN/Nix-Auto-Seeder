import re
import itertools

from loguru import logger

import util
from distro import Distro


class Ubuntu(Distro):

    def __init__(self):
        self.version_re = re.compile(r'\d+\.\d+(\.\d+)?')

        super().__init__(
            server='ftp.mirrorservice.org',
            paths=[
                'sites/releases.ubuntu.com/'
            ]
        )

    def get_torrents_paths(self, ftp, num_releases=1):
        torrent_files = []

        for path in self.paths:
            releases = dict()
            releases_raw = ftp.nlst(path)

            for release in releases_raw:
                match = self.version_re.search(release)

                # If no match, then dir is not related to Ubuntu release
                if not match:
                    continue

                # Get version info
                version = match.group()
                releases[version] = release

            # Sort releases by version
            releases = {k: v for k, v in sorted(releases.items(), key=lambda i: i[0], reverse=True)}
            logger.debug("Found Ubuntu releases: {}", ', '.join((releases.keys())))

            # if num_releases is 0, get all versions
            if num_releases:
                releases = itertools.islice(releases.items(), num_releases)

            for version, path in releases:
                files = ftp.nlst(path)
                logger.trace("[{}] {} FTP files: {}", self, path, files)
                torrent_files += list(filter(util.verify_torrents, files))

        logger.trace("[{}] FTP torrent files: {}", self, torrent_files)
        return torrent_files
