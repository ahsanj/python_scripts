import lefty
from lefty.exceptions import LeftyResourceNotFound
import config
import json, ast
import requests
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class color:
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   END = '\033[0m'

# Auth against the  endpoint
api = lefty.Lefty(config.username, config.SSO, ticket_service='https:xxxxxxxxx')

# This is Datastore ops (encore) queue ID xxx-xxxxxx
response = api.get_queue_tickets(config.queue)

def unassigned_tickets():
    print color.YELLOW + "Un-assigned tickets"  + color.END
    count = 0
    for ticket in response.get('tickets', [None]):
        # data returned as unicode following converts in str
        if ast.literal_eval(json.dumps(ticket['assignee']['value'])) == "":
            count = count + 1
            print count,'-', "Ticket: %s is not assigned to anyone!, Subject: %s Status: %s" % (ticket['ticket_id'],ticket['subject'],ticket['status'])
        
def assigned_tickets():
    output=""
    try:
        print color.YELLOW + "Assigned tickets" + color.END
        for ticket in response.get('tickets', [None]): 
            if ticket['assignee']['value'] != "" and ticket['status'] != 'Solved':
                output+="Ticket: %s, Subject: %s Assigned: %s, Status: %s \n" % (ticket['ticket_id'],ticket['subject'],ticket['assignee']['value'],ticket['status'])
        return output
    except LeftyResourceNotFound:
        return "No ticket in the Queue"

def feedback_received():
    output= ""
    try:
        for ticket in response.get('tickets', [None]):
            if ticket['status'] == "Feedback Received":
                output+='Ticket: %s Subject: %s Status: %s\n' % (ticket['ticket_id'], ticket['subject'],ticket['status'])
        return output 
    except:
        return "No ticket in the Queue with the status 'Feedback Received'"


def get_ticket(ticket):
    print color.YELLOW + "Getting the ticket"  + color.END
    try:
        ticket = api.get_ticket_by_id(ticket)
        print 'Ticket: %s Subject: %s Status: %s Created on: %s' % (ticket['ticket_id'], ticket['subject'],ticket['status'],ticket['created'])
    except LeftyResourceNotFound:
        print "Ticket", ticket, "does not exist in encore"

def main():
    if len(sys.argv) != 2:
        print 'usage: ./get_ticket.py {--assigned | --unassigned | --check_tickets_feedback}'
        sys.exit(1)
    option = sys.argv[1]
    if option == '--assigned':
        print assigned_tickets()
    elif option == '--unassigned':
        unassigned_tickets()
    elif option == '--check_tickets_feedback':
        print feedback_received()
    elif option == '--get_ticket':
        ticket= sys.argv[2]
        get_ticket(ticket)
    else:
        print 'unknown option: ' + option
        sys.exit(1)
if __name__ == '__main__':
    main()
