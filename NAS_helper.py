import urllib.request

def strip_dir_raw(dir_raw_string):
    #Given a directory listing this will return a clean list of folder/files with attributes, links etc
    #Split raw dir info into nice list
    dirlist =[]
    for x in range(0,len(dir_raw_string)):
         words = dir_raw_string[x].split(None, 8)
         filename = words[-1].lstrip()
         dirlist.append(filename.split()[0])  #Strip out the --> code name notation
    return dirlist


def latest_ubuntu(dir_raw_string):
    #Given a directory listing of
    #ftp://mirrors.mit.edu/ubuntu-releases
    #this will return latest version number
    
    #Clean unneeded info
    dirlist = strip_dir_raw(dir_raw_string)
    
    #Cycle through release numbers from 50 down till we hit something incl point releases
    latest = ""
    for x in range(50,17,-1):
        #.10 version with point releases
        for y in range(10,0,-1): #Unlikely to get to x.10.10 point release but try anyway
            if latest == "" and str(x)+".10."+str(y) in dirlist:
                latest = str(x)+".10."+str(y)

        # and try .10 without point release
        if latest == "" and str(x)+".10" in dirlist:
            latest = str(x)+".10"
        
        #.04 version with point releases
        for y in range(10,0,-1): #Unlikely to get to x.04.10 point release but try anyway
            if latest == "" and str(x)+".04."+str(y) in dirlist:
                latest = str(x)+".04."+str(y)

        # and try .04 without point release
        if latest == "" and str(x)+".04" in dirlist:
            latest = str(x)+".04"

    return latest #String with version number. e.g. 18.10


    
def find_torrents(dir_raw_string):
    #Given a directory listing of
    #ftp://mirrors.mit.edu/ubuntu-releases
    #this will return all torrent files found

    torrents =[]
    
    #Clean unneeded info
    dir_list = strip_dir_raw(dir_raw_string)

    for x in range(0,len(dir_list)):
        if ".torrent" in dir_list[x]:
            torrents.append(dir_list[x])
  
    
    return torrents

def grab_file(web_url,destination_path):
    #Download a file
    with urllib.request.urlopen(web_url) as response, open(destination_path, 'wb') as out_file:
        data = response.read() # a `bytes` object
        out_file.write(data)
    




