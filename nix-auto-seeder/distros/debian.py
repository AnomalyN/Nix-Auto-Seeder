from distro import FTPDistro


class Debian(FTPDistro):

    def __init__(self):
        super().__init__(
            server='ftp.mirrorservice.org',
            paths=[
                [
                    ('/sites/cdimage.debian.org/debian-cd/', r'(?P<major>\d+)\.(?P<minor>\d+[\.\d]*)'),
                    ('.', r'(?P<arch>\w+)'),
                    ('.', r'bt')
                ]
            ]
        )
