import requests
import json
import getpass
import sys
import urllib3

instance_flavors = """
Available flavors for cloudDB:
|  1 | 512MB Instance |   512        
|  2 | 1GB Instance   |  1024        
|  3 | 2GB Instance   |  2048        
|  4 | 4GB Instance   |  4096        
|  5 | 8GB Instance   |  8192              
|  6 | 16GB Instance  | 16384              
|  7 | 32GB Instance  | 32768             
|  8 | 64GB Instance  | 65536        
"""

turnoff_quotas = """
If the container was build before 30th Jan 2017 then first run the following commands on the compute\n
# vzquota off CITD -f
# vzquota drop CITD
"""

def resize_container():
    regions = ['ord','dfw','iad','lon']
    region = raw_input("Enter the region: ")

    if region not in regions:
        print "Not a valid region"
        sys.exit()
    
    customer_ddi = raw_input("Enter the customer DDI: ")
    try:
       checking_ddi = int(customer_ddi)
    except ValueError:
        print"Customer DDI should be digits only! "
	sys.exit()
    
    token = getpass.getpass("Enter the Customer impersonation token: ")
    if not token.strip():
        print "You need to enter the customer impersonation token: "
        sys.exit()
   
    instance_id = raw_input("Enter the Trove UUID of the instance to be resized: ")
    
    flavor_id = raw_input("Enter the new flavor ID: ")
    try:
        checking_flavor_id = int(flavor_id)
    except ValueError:
	print"flavor_id should be a single digit "
        sys.exit()

    url = "https://"+region+".databases.api.rackspacecloud.com/v1.0/"+customer_ddi+"/instances/"+instance_id+"/action"
    
    payload = {"resize":
            {"flavorRef": "https://"+region+".databases.api.rackspacecloud.com/v1.0/"+customer_ddi+"/flavors/"+flavor_id}
           }

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
          }

    #print "URL    : "+url
    #print "Headers: "+str(headers) 
    #print "Payload: "+str(payload)
    req=requests.post(url,headers=headers, data=json.dumps(payload))
    if req.status_code not in range(200, 300):
        print "Request didnt go through, status returned: ",req.status_code
    else:
        print "Request accepted: ",req.status_code


def main():
    print instance_flavors
    print turnoff_quotas
    resize_container()

if __name__ == '__main__':
    main()
