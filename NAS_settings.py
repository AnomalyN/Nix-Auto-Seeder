from os.path import expanduser
from collections import namedtuple
import tempfile

Settings = namedtuple('Settings', [
    'working_path_NAS',
    'output_dir_set',
    'ubuntu_server',
    'ubuntu_path',
    'ubuntu_user',
    'ubuntu_pass',
    'raspian_torrents',
    'arch_server',
    'arch_path',
    'arch_user',
    'arch_pass',
    'debian_server',
    'debian_path',
    'debian_path_arm',
    'debian_user',
    'debian_pass',
    'centos_server',
    'centos_path',
    'centos_user',
    'centos_pass'
])

def create_settings():
    '''Populates a namedtuple with the settings defined for the rest of the program'''
    return Settings(
        working_path_NAS=tempfile.gettempdir(),
        output_dir_set=False,
        ubuntu_server="ftp.mirrorservice.org", #University of Kent
        ubuntu_path="sites/releases.ubuntu.com/",
        ubuntu_user="anonymous",
        ubuntu_pass="anonymous@domain.com",
        raspian_torrents=[
            "https://downloads.raspberrypi.org/raspbian_full_latest.torrent",
            "https://downloads.raspberrypi.org/raspbian_latest.torrent",
            "https://downloads.raspberrypi.org/raspbian_lite_latest.torrent",
            "https://downloads.raspberrypi.org/NOOBS_latest.torrent",
            "https://downloads.raspberrypi.org/NOOBS_lite_latest.torrent"
        ],
        arch_server="ftp.mirrorservice.org", #University of Kent
        arch_path="sites/ftp.archlinux.org/iso/latest",
        arch_user="anonymous",
        arch_pass="anonymous@domain.com",
        debian_server="cdimage.debian.org",
        debian_path="/debian-cd/current/amd64/bt-cd",
        debian_path_arm="/debian-cd/current/arm64/bt-cd",
        debian_user="anonymous",
        debian_pass="anonymous@domain.com",
        centos_server="ftp.mirrorservice.org",
        centos_path="sites/mirror.centos.org/7/isos/x86_64/",
        centos_user="anonymous",
        centos_pass="anonymous@domain.com"
    )
