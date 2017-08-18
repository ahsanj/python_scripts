import lefty
import config
import requests
import json
from urlparse import urljoin
from slackclient import SlackClient
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Auth against the encore endpoint
#api = lefty.Lefty(auth_token=config.auth_token,ticket_service=config.ticket_service,auth_endpoint=config.auth_endpoint)
api = lefty.Lefty(config.username, config.SSO, ticket_service=config.ticket_service,auth_endpoint=config.auth_endpoint)

# This is Datastore ops (encore) queue ID xxx-xxxxx
response = api.get_queue_tickets(config.queue)

slack_client = SlackClient(config.slack_bot)

def feedback_received():
    tickets=[]
    for ticket in response.get('tickets', [None]):
        #if ticket['assignee']['value'] != "" and ticket['status'] != 'Solved':
        if ticket['status'] == "Feedback Received":
            url= urljoin('https://encore.rackspace.com/ticketing/ticket/' ,ticket['ticket_id'])
            tickets.append(url)
    text= '\n'.join(tickets)
    return str(text)

def notify_slack(channel,message,username):
        
        slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=message,
        username='Ticket(s) updated by the customer(s)',
        icon_emoji=':robot_face:' )
        
def main():
     message=feedback_received()
     channel = "doc"
     username = "ahsanjaved"
     notify_slack(channel,message,username)
if __name__ == '__main__':
    main()
