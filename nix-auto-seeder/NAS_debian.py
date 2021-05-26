import ftplib
import NAS_helper
import os
from time import sleep

def seed_debian(settings):
    #amd64
    try:
        ftp = ftplib.FTP(settings.debian_server, settings.debian_user,settings.debian_pass)

        #Get debian
        ftp.cwd(settings.debian_path)

        #Get torrent list
        dir_raw = []
        ftp.retrlines("LIST",dir_raw.append)
        torrents = NAS_helper.find_torrents(dir_raw)

        for x in range(0,len(torrents)):
            local_filename = settings.working_path_NAS + os.sep + torrents[x] #Save it in location defined in settings.py
            try:
                lf = open(local_filename, "wb")        
                ftp.retrbinary("RETR " + torrents[x], lf.write, 8*1024)
            finally:
                lf.close()
                print("Attempting to add: "+local_filename)
                if settings.output_dir_set:
                    continue
                os.system("deluge-console add "+local_filename)
                sleep(1) #Give deluge some time to add it before deleting file
                if os.path.exists(local_filename):
                    os.remove(local_filename)
    finally:
        ftp.quit()

    #arm64
    try:
        ftp = ftplib.FTP(settings.debian_server, settings.debian_user,settings.debian_pass)

        #Get debian
        ftp.cwd(settings.debian_path_arm)

        #Get torrent list
        dir_raw = []
        ftp.retrlines("LIST",dir_raw.append)
        torrents = NAS_helper.find_torrents(dir_raw)

        for x in range(0,len(torrents)):
            local_filename = settings.working_path_NAS + os.sep + torrents[x] #Save it in location defined in settings.py
            try:
                lf = open(local_filename, "wb")        
                ftp.retrbinary("RETR " + torrents[x], lf.write, 8*1024)
            finally:
                lf.close()
                print("Attempting to add: "+local_filename)
                os.system("deluge-console add "+local_filename)
                if settings.output_dir_set:
                    continue
                sleep(1) #Give deluge some time to add it before deleting file
                if os.path.exists(local_filename):
                    os.remove(local_filename)
    finally:
        ftp.quit()

    return
