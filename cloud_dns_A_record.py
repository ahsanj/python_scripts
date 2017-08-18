import pyrax
import os
import sys
#import pprint
import re

pyrax.set_setting("identity_type", "rackspace")
cred_file= os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(cred_file)

dns = pyrax.cloud_dns

def list_domains():
    page_size=10
    rx = '\S+[.]\S+'
    count = 0
    domains= dns.list(limit=page_size)
    count += len(domains)
    for domain in domains:
        print domain.name
    #print domains
    print'Total domains in your account', count 
    domain_name= raw_input('Choose the domain by writing? ')
    valid_domain= re.match(rx,domain_name)
    if valid_domain is None:
	print "Not a valid domain"
        sys.exit()
    return domain_name	

def add_domain(mydomain):
    rx= '\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}'
    count_ans=0
    hostname= raw_input('Enter the hostname: ')	
    ip= raw_input("Enter the IP for 'A' record: ")
    valid_ip = re.match(rx,ip)
    if valid_ip is None:
        print "Not a valid IP"
	sys.exit()
    domain= hostname +'.'+ mydomain
    print 'You are adding this record for this domain', domain
    print 'The IP is you added is',ip
    answer= raw_input ("This is the right IP ?  yes or no ? " )
    if answer == 'yes':
        pass
    while answer != 'yes' and count_ans <= 3:
        IP= raw_input('Enter the again IP: ')
        answer= raw_input ("This is the right IP ?  yes or no ? " )
        if answer == 'yes':
            break
        count_ans +=1
        print 'Bye! see you laterss ?'
        sys.exit()
    try:
        dom = dns.find(name=mydomain)
        a_rec = { "type": "A","name": domain, "data": ip , "ttl": 33300 }
        dom.add_records([a_rec])
    except Exception:
        print 'The domain is not present in your Cloud Account'
	sys.exit()

domain_name=list_domains()
add_domain(domain_name)	

#list dns attributes
#pprint.pprint(dir(dns))
