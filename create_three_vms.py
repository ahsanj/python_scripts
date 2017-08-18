import pyrax
import os

lst=[]
flav=[]

pyrax.set_setting("identity_type", "rackspace")
cred_file= os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(cred_file)

cs= pyrax.cloudservers
server_name1='web1'
server_name2='web2'
server_name3='web3'
for img in cs.images.list():
     #print"Name: %s  ID: %s" % (img.name, img.id)
      if "Ubuntu" in img.name and "14.04" in img.name and "PVHVM" in img.name:
          lst.append(img)
image_name= lst[0]
print image_name

for fla in cs.flavors.list():
    if fla.ram ==512:
      flav.append(fla)
flavor= flav[0]
print flavor

server1 = cs.servers.create(server_name1,image_name.id,flavor.id)
server2 = cs.servers.create(server_name2,image_name.id,flavor.id)
server3 = cs.servers.create(server_name3,image_name.id,flavor.id)

print "Name: ", server1.name,'<---->',server2.name,'<---->',server3.name
print "Server ID: ", server1.id,'<---->',server2.id,'<---->',server3.id
print "Status: ",server1.status,'<---->',server2.status,'<---->',server3.status
print "Admin Password: ", server1.adminPass,'<---->',server2.adminPass,'<---->',server3.adminPass
print "Networks: ",server1.networks,'<---->',server2.networks,'<---->',server3.networks
