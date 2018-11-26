import NAS_helper
import os
from time import sleep

def seed_raspbian(settings):
    for torrent in settings.raspian_torrents:
        local_filename = settings.working_path_NAS + os.sep + torrent.split('/')[-1]
        NAS_helper.grab_file(torrent, local_filename)

        print("Attempting to add: " + local_filename)
        os.system("deluge-console add " + local_filename)

        sleep(1) #Give deluge some time to add it before deleting file
        if os.path.exists(local_filename):
            os.remove(local_filename)
