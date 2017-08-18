import pyrax

pyrax.set_setting("identity_type", "rackspace")
cred_file= os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(cred_file)

cf = pyrax.cloudfiles

cont_name= raw_input('Enter the container name: ')
cont = cf.create_container(cont_name)

print 'Conatiner', cont
print 'cdn_enabled', cont.cdn_enabled
print 'cdn_url', cont.cdn_uri

cont.make_public(ttl=1200)

print ''

print 'Conatiner', cont
print 'cdn_enabled', cont.cdn_enabled
print 'cdn_url', cont.cdn_uri

