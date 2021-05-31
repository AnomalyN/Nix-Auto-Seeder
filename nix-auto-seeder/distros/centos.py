from distro import FTPDistro


class CentOS(FTPDistro):

    def __init__(self):
        super().__init__(
            server='ftp.mirrorservice.org',
            paths=
            [
                {
                    '/sites/mirror.centos.org/': r'(?P<major>\d+)\.(?P<minor>\d+[\.\d]*)',
                    '/isos/': r'(?P<arch>\w+)'
                },
            ]
        )
