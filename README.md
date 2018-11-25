For those with too much server capacity lying around...

I built a tool that automatically finds & seeds torrents for the latest release of linux distros. Thus far these are supported:

    Ubuntu

    Arch

    Raspbian

    NOOBS

    Debian

https://github.com/AnomalyN/Nix-Auto-Seeder

You need python 3 installed and deluge-console needs to work from the command line. i.e. this needs to work:

    deluge-console add XYZ.torrent

I'd also suggest boosting the number of concurrent torrents seeding etc in this file, else it's just going to be queued forever. You'll also need to set the allow remote setting to true, else the above add line doesn't work.

    ~/.config/deluge/core.conf

Assuming deluge is set up correctly running it is just a case of

    python3 main.py

NB - this downloads 11 gigabyte of data & can generate significant network traffic over time so make sure you ISP/university/roommate/parents/dog is OK with that.

Once off run only so to add new ones you'll need to add it to a cron job or startup script. This only adds, doesn't remove so over time it'll accumulate.

Also, this is an amateur coding project so apologies in advance if something gives an error...
