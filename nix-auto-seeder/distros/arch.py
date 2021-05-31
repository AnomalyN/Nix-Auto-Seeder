from distro import FTPDistro


class Arch(FTPDistro):

    def __init__(self):
        super().__init__(
            server='ftp.mirrorservice.org',
            paths=[
                'sites/ftp.archlinux.org/iso/latest'
            ]
        )
