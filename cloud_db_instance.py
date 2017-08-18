import pyrax
import os
import sys
import time
import getpass

pyrax.set_setting("identity_type", "rackspace")
cred_file= os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(cred_file)
cdb = pyrax.cloud_databases

instances = cdb.list()
cdb = pyrax.cloud_databases
flavors = cdb.list_flavors()

def create_inst():
    inst_name = raw_input('Enter the name for your cloudDB instance: ')

    for pos,flavor in enumerate(flavors):
        #pprint.pprint(dir(flavor))
        print "RAM: %s; ID: %s" % ( flavor.ram,  pos)

    my_flavor = raw_input('\nChoose the cloudDB flavor by ID: ')
    my_flavor= int(my_flavor)
    try:
        my_flavor = flavors[my_flavor]
    except:
        print "Not a valid flavor"
        sys.exit()
    #print 'flavours', flavors
    #print 'printing my_flavor ',my_flavor
    vol_size = raw_input("Enter the volume size in GB between 1 to 50: ")

    instance = cdb.create(inst_name , flavor = my_flavor, volume = vol_size)
    print "Name:", instance.name
    print "ID:", instance.id
    print "Status:", instance.status
    print "Flavor:", instance.flavor.name
    #return instance.name

def add_db():
    #instances = cdb.list()
    #if not instances:
    #    print "you have no db instances"
    #    sys.exit
    #print instances
    instances = cdb.list()
    for pos, inst in enumerate(instances):
        print "%s: %s:" % (pos, inst.name)
    db_sel = raw_input("choose the no of the instance to add DB: ")
    db_sel=int(db_sel) 
    db_sel_number = db_sel
    #print db_sel
    try:
        db_sel = instances[db_sel]
    except:
        print "Not a valid Instance"
    nm = raw_input('Enter the name of the DB: ')

    if db_sel.status == 'BUILD':
       while db_sel.status != 'ACTIVE':
           print 'waiting. Status: {status}'.format(status=db_sel.status)
	   time.sleep(2)
	   _instances = cdb.list()
	   db_sel = _instances[db_sel_number]
	   #print db_sel
    db= inst.create_database(nm)
    #dbs= inst.list_databases()
    #for db in dbs:
    #    print db.name

def add_user():
    instances = cdb.list()
    if not instances:
        print 'No instances'
        sys.exit()
    for pos,inst in enumerate(instances):
        print "Pos=%s: Instance Name=%s Status=%s" % (pos, inst.name, inst.status)
        #print dir(inst)
    try:
        inst_sel= raw_input( "Enter the Pos of the instance to which you want to add the user: ")
        sel_inst = int(inst_sel)
    except:
        print "Invalid, non numeric"
        sys.exit()
    try:
        inst_selected = instances[sel_inst]
    except:
        print "Invalid selection"
        sys.exit() 
    user_name = raw_input('Enter the user name: ')
    user_pass = getpass.getpass("Enter the password for the user: ")
   
    dbs= inst.list_databases()
    
    for pos,db in enumerate(dbs):
        print "Pos=%s DB_name=%s" % (pos, db.name)
    try:
        db_sel = raw_input("Enter the pos no the DB: ")
        db_sel = int(db_sel)
    except:
        print "Invalid non numeric"
        sys.exit
    try:    
        db = dbs[db_sel]
    except:
        print "Invalid selection"
        sys.exit()
    
    user = inst.create_user (user_name,user_pass , database_names= db)
    print 'User %s has been created on %s' %(user_name, inst.name)
   
create_inst()        
add_db()
add_user()

