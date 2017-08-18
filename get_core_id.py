# usage exmaple "python core_id.py iad2xxxxxxx"
import sys
import socket
import subprocess

def get_coreid():
    hostname = sys.argv[1]
    host = socket.getfqdn(hostname)
    txt_record= subprocess.Popen(['dig', '-t', 'TXT', host, '+short'], stdout=subprocess.PIPE).communicate()[0]
    if txt_record == "":
        print "Cannot find the Core_ID of this hostname", sys.argv[1]
        sys.exit()
    pos0=txt_record.find(":")
    pos1=txt_record.find(' " ')
    core_id=txt_record[pos0+1:-2]
    print "The Core ID of", sys.argv[1], "is", core_id,


def main():
    if len(sys.argv) != 2:
        print 'usage: python hostname, only takes one argument'
        sys.exit(1)

if __name__ == '__main__':
    main()
    get_coreid()
