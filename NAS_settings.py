from os.path import expanduser

def init():
    #Defining constants here
    
    #Default working directory. Using home since torrents are deleted after being added
    global working_path_NAS
    working_path_NAS = expanduser("~")

    global ubuntu_server
    ubuntu_server = "ftp.mirrorservice.org" #University of Kent
    global ubuntu_path
    ubuntu_path = "sites/releases.ubuntu.com/"
    global ubuntu_user
    ubuntu_user = "anonymous"
    global ubuntu_pass
    ubuntu_pass = "anonymous@domain.com"
 
    global raspian_desktop_software
    raspian_desktop_software = "https://downloads.raspberrypi.org/raspbian_full_latest.torrent"
    global raspian_desktop_only
    raspian_desktop_only = "https://downloads.raspberrypi.org/raspbian_latest.torrent"
    global raspian_lite
    raspian_lite = "https://downloads.raspberrypi.org/raspbian_lite_latest.torrent"
    global noobs_full
    noobs_full = "https://downloads.raspberrypi.org/NOOBS_latest.torrent"
    global noobs_lite
    noobs_lite = "https://downloads.raspberrypi.org/NOOBS_lite_latest.torrent"

    global arch_server
    arch_server = "ftp.mirrorservice.org" #University of Kent
    global arch_path
    arch_path = "sites/ftp.archlinux.org/iso/latest"
    global arch_user
    arch_user = "anonymous"
    global arch_pass
    arch_pass = "anonymous@domain.com"

    global debian_server
    debian_server = "cdimage.debian.org"
    global debian_path
    debian_path = "/debian-cd/current/amd64/bt-cd"
    global debian_path_arm
    debian_path_arm = "/debian-cd/current/arm64/bt-cd"
    global debian_user
    debian_user = "anonymous"
    global debian_pass
    debian_pass = "anonymous@domain.com"

    global centos_server
    centos_server = "ftp.mirrorservice.org"
    global centos_path
    centos_path = "sites/mirror.centos.org/7/isos/x86_64/"
    global centos_user
    centos_user = "anonymous"
    global centos_pass
    centos_pass = "anonymous@domain.com"