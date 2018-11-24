import NAS_helper
import NAS_settings
import os
from time import sleep

def seed_raspbian():

    #Seed the full raspbian with desktop and recommended software
    local_filename = NAS_settings.working_path_NAS + os.sep + "raspbian_full_latest.torrent"
    NAS_helper.grab_file(NAS_settings.raspian_desktop_software,local_filename)
    print("Attempting to add: "+local_filename)
    os.system("deluge-console add "+local_filename)
    sleep(1) #Give deluge some time to add it before deleting file
    if os.path.exists(local_filename):
        os.remove(local_filename)

    #Seed the full raspbian with desktop only
    local_filename = NAS_settings.working_path_NAS + os.sep + "raspbian_latest.torrent"
    NAS_helper.grab_file(NAS_settings.raspian_desktop_only,local_filename)
    print("Attempting to add: "+local_filename)
    os.system("deluge-console add "+local_filename)
    sleep(1) #Give deluge some time to add it before deleting file
    if os.path.exists(local_filename):
        os.remove(local_filename)

    #Seed the lite raspbian
    local_filename = NAS_settings.working_path_NAS + os.sep + "raspbian_lite_latest.torrent"
    NAS_helper.grab_file(NAS_settings.raspian_lite,local_filename)
    print("Attempting to add: "+local_filename)
    os.system("deluge-console add "+local_filename)
    sleep(1) #Give deluge some time to add it before deleting file
    if os.path.exists(local_filename):
        os.remove(local_filename)

    #Seed the NOOBS
    local_filename = NAS_settings.working_path_NAS + os.sep + "NOOBS_latest.torrent"
    NAS_helper.grab_file(NAS_settings.noobs_full,local_filename)
    print("Attempting to add: "+local_filename)
    os.system("deluge-console add "+local_filename)
    sleep(1) #Give deluge some time to add it before deleting file
    if os.path.exists(local_filename):
        os.remove(local_filename)

    #Seed the NOOBS lite
    local_filename = NAS_settings.working_path_NAS + os.sep + "NOOBS_lite_latest.torrent"
    NAS_helper.grab_file(NAS_settings.noobs_lite,local_filename)
    print("Attempting to add: "+local_filename)
    os.system("deluge-console add "+local_filename)
    sleep(1) #Give deluge some time to add it before deleting file
    if os.path.exists(local_filename):
        os.remove(local_filename)