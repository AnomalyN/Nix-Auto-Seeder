from distro import Distro


class Debian(Distro):

    def __init__(self):
        super().__init__(
            server='cdimage.debian.org',
            paths=[
                '/debian-cd/current/amd64/bt-cd',
                '/debian-cd/current/arm64/bt-cd'
            ]
        )
