from distro import FTPDistro


class Ubuntu(FTPDistro):

    def __init__(self):
        super().__init__(
            server='ftp.mirrorservice.org',
            paths=[
                [
                    ('sites/releases.ubuntu.com/', r'(?P<major>\d+\.\d+)\.(?P<minor>\d+)?'),
                    ('.', r'(?P<arch>\w+)\.iso\.torrent')
                ]
            ]
        )
