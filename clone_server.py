import pyrax
import os
import sys

lst=list()
server_id=list()
server_flavor=list()
server_name= 'cloned_server'
pyrax.set_setting("identity_type", "rackspace")
cred_file= os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(cred_file)
cs_ord = pyrax.connect_to_cloudservers(region="ORD")
cs_dfw = pyrax.connect_to_cloudservers(region="DFW")
cs_iad = pyrax.connect_to_cloudservers(region="IAD")

dfw_servers = cs_dfw.list()
ord_servers = cs_ord.list()
iad_servers = cs_iad.list()
all_servers = dfw_servers + ord_servers + iad_servers

dfw_flavors= cs_dfw.flavors.list()
ord_flavors = cs_ord.flavors.list()
iad_flavors= cs_ord.flavors.list()
all_flavors = dfw_flavors + iad_flavors + ord_flavors

dfw_image = cs_dfw.images.list()
ord_image = cs_ord.images.list()
iad_image = cs_iad.images.list()
all_image = dfw_image + ord_image + iad_image

cs= pyrax.cloudservers

def get_vm():
    count = 0
    for server in all_servers:
        if server.status =='ACTIVE':
             lst.append(server.name)
    if not lst:
        print "You dont have any servers"
    else:
        for i in lst:
            count = count + 1
            print count,'->',i
    vm =raw_input("Select the VM name to clone, so that we can spin up a new VM using this image: ")
    if not vm in lst:
        print "Sorry VM with this name does not exits"
        sys.exit()
        print '\n','You have chossen this VM',vm
    return vm

def create_image(vm):
    for server in all_servers:
    # pprint(dir(server))
         if server.name==vm:
             server_id.append(server.id)
    image_name= raw_input("enter the name for the image: ")
    vm_id = server_id[0]

    #print '\n',vm_id
    #print '\n', image_name

    #cs_ord.servers equal is cs.servers, if cs_ord=cs_ord = pyrax.connect_to_cloudservers(region="ORD") is not assigned
    image_id= cs_ord.servers.create_image(vm_id,image_name)
    print 'Image %r  is being created and its ID is %r' % (image_name, image_id)
    return image_id


def create_server(image_id):
    print "Available flavor: "
    for fla in all_flavors:
        print fla.ram,'RAM'
    vm_ram=raw_input("please choose the flavor for VM: ")
    flavor= int(vm_ram)
    for fla in all_flavors:
        if fla.ram ==flavor:
            server_flavor.append(fla)
    flavor= server_flavor[0]
       #else:
            #print "No such flavor"
            #sys.exit()
       #print flavor
       #print type(flavor)
    server_name=raw_input('please enter the name for the server: ')
    # The wait_until function requires an object. The create_image function returns a string. This requires another request to get the object just to use wait_until
    image = cs_ord.images.get(image_id)
    pyrax.utils.wait_until(image, "status", ["ACTIVE", "ERROR"], attempts=0, verbose=True)
    server= cs_ord.servers.create(server_name, image.id,flavor.id)
    print "Name: ", server.name,
    print "Server ID: ", server.id
    print "Status: ", server.status
    print "Admin Password: ", server.adminPass 
   
vm = get_vm()
print "this is the vm name", vm	
image= create_image(vm)
print "this is the image id", image
create_server(image)
