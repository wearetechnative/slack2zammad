import os
import pprint
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from dotenv import load_dotenv
load_dotenv()

apptoken = os.environ.get("SLACK_BOT_TOKEN")
bottoken = os.environ.get("SLACK_APP_TOKEN")

app = App(token=bottoken)

@app.shortcut("create_ticket")
def create_ticket(ack, shortcut, client):

    # Acknowledge the shortcut request

    ack()
    #pprint.pp(shortcut["message"]["text"])
    message_text = shortcut["message"]["text"]

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

@app.view("")
def handle_view_submission_events(ack, body, logger):
    ack()
    pprint.pp(body)
    pprint.pp(body['view']['state']['values'])


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, apptoken).start()





