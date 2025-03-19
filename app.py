import os
import pprint
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import sys
import argparse
from dotenv import load_dotenv
import logging
from _version import __version__

from zammadoo import Client

# Some basic logging 
logging.basicConfig(level=logging.INFO)

# Get current directory with .env
current_dir = os.getcwd()
dotenv_path = os.path.join(current_dir, '.env')

# Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--envfile", type=str, help=f'The ".env" file location (default: {dotenv_path})')
parser.add_argument("-v", "--version", action="version", version=f'slack2zammad: {__version__}')
args = parser.parse_args()
envfile = args.envfile

# Environment File
if envfile == None: 
    load_dotenv(dotenv_path=dotenv_path)

elif envfile == envfile:
    file_exist = os.path.isfile(envfile)

    if file_exist == True:
        #print(envfile)
        load_dotenv(dotenv_path=envfile)
    else:
        print("EnvironmentFile not found")
        exit() 

APPTOKEN = os.environ.get("SLACK_BOT_TOKEN")
BOTTOKEN = os.environ.get("SLACK_APP_TOKEN")
ZAMMAD_URL = os.environ.get("ZAMMAD_URL")
ZAMMAD_USER = os.environ.get("ZAMMAD_USER")
ZAMMAD_PASSWD = os.environ.get("ZAMMAD_PASSWD")

app = App(token=BOTTOKEN)

zamclient = Client(ZAMMAD_URL+"/api/v1/", http_auth=(ZAMMAD_USER, ZAMMAD_PASSWD))

#ticket = zamclient.tickets(28)
#print(f"ticket id: {ticket.id}")
#print(f"ticket number: #{ticket.number}")
#print(f"ticket title: {ticket.title!r}")

@app.shortcut("create_ticket")
def create_ticket(ack, shortcut, client):

    # Acknowledge the shortcut request

    ack()
    #pprint.pp(shortcut["message"]["text"])
    message = shortcut["message"]["text"]
    message_text = message

    pprint.pp(shortcut["message"])

    #pprint.pp(client)
    initial_ticket_title = ""
    if "user_profile" in shortcut["message"]:
        message_user = shortcut["message"]["user_profile"]["display_name"]
        initial_ticket_title = "Issue from " + message_user

    # Call the views_open method using the built-in WebClient
    client.views_open(
        trigger_id=shortcut["trigger_id"],

        view={
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": "Zammad",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Create ticket"
                    }
                },
                {
                    "type": "divider"
                },
                #		{
                #			"type": "section",
                #			"text": {
                #				"type": "mrkdwn",
                #				"text": "*Customer*\nChoose a contact or customer\n\n"
                #			},
                #			"accessory": {
                #				"type": "static_select",
                #				"placeholder": {
                #					"type": "plain_text",
                #					"emoji": True,
                #					"text": "Search"
                #				},
                #				"options": [
                #					{
                #						"text": {
                #							"type": "plain_text",
                #							"emoji": True,
                #							"text": "Edit it"
                #						},
                #						"value": "value-0"
                #					},
                #					{
                #						"text": {
                #							"type": "plain_text",
                #							"emoji": True,
                #							"text": "Read it"
                #						},
                #						"value": "value-1"
                #					},
                #					{
                #						"text": {
                #							"type": "plain_text",
                #							"emoji": True,
                #							"text": "Save it"
                #						},
                #						"value": "value-2"
                #					}
                #				]
                #			}
                #		},
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "inputid_ticket_title",
                        "initial_value": initial_ticket_title
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Ticket title",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "inputid_ticket_text",
                        "initial_value": message_text
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Ticket text",
                        "emoji": True
                    }
                },
                {
                    "type": "divider"
                }
            ]
        }
    )



def get_field_value_from_modal_body(modal_body, field_id):
    for key, value in modal_body['view']['state']['values'].items():
        for key2, value2 in value.items():
            print(key2)
            if key2 == field_id:
                return value2['value']

@app.view("")
def handle_view_submission_events(ack, body, logger):
    ack()

    title = get_field_value_from_modal_body(body, "inputid_ticket_title" )
    text = get_field_value_from_modal_body(body, "inputid_ticket_text" )

    zamclient.tickets.create(title, "Managed Services Supportdesk", ZAMMAD_USER, text)


# Start your app
def main():
    SocketModeHandler(app, APPTOKEN).start()

if __name__ == "__main__":
    main()





