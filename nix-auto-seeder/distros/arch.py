from distro import Distro


class Arch(Distro):

    def __init__(self):
        super().__init__(
            server='ftp.mirrorservice.org',
            paths=[
                'sites/ftp.archlinux.org/iso/latest'
            ]
        )
