from distro import Distro


class Ubuntu(Distro):

    def __init__(self):
        super().__init__(
            server='ftp.mirrorservice.org',
            paths=[
                'sites/releases.ubuntu.com/'
            ]
        )
