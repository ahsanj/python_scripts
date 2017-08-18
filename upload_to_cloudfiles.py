#!/usr/bin/env python

import pyrax
import os
import sys
import time

pyrax.set_setting("identity_type", "rackspace")
cred_file= os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(cred_file)

cf = pyrax.cloudfiles

def upload_folder():
    script, directory, cont_name = sys.argv
    ###creating conatiner#####
    cont = cf.create_container(cont_name)
    print "Container",cont

    path= os.path.abspath(directory)
    print 'Path to your folder is: ', path
    folder = os.path.basename(directory)
    folder = os.path.join(directory)
    print folder 
    print 'You are uploading this folder: ',folder
    print "Uploading.........."
    upload_key,total_byte = cf.upload_folder(folder, cont)
    uploaded = 0
    while uploaded < total_byte:
        uploaded = cf.get_uploaded(upload_key)
        time.sleep(1.5)
    return folder, cont
    
def verify_upload(dir):
    print dir[0]
    folder_name = dir[0]
    cont_name = dir[1]
   #print 'Folder uploaded and container', folder_name, cont_name
    nof= cf.get_container_object_names(cont_name)
    print 'Number of files in the container', len(nof)
    
def main():
    if len(sys.argv) != 3:
        print 'usage: python upload_folder_cloudfiles.py Directory Container name'
        sys.exit(1)

if __name__ == '__main__':
    main()
    folder=upload_folder()
    verify_upload(folder)
