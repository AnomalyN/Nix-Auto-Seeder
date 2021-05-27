from distro import Distro


class CentOS(Distro):

    def __init__(self):
        super().__init__(
            server='ftp.mirrorservice.org',
            paths=[
                'sites/mirror.centos.org/7/isos/x86_64/'
            ]
        )
