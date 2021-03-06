from flask import Flask, request
import requests
import os
import sys
import json
from credentials import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_verification():
    if request.args.get("hub.mode"=="subscribe") and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "Pkeso Sport Town":
            return "Verification token mismatch !", 403
        return request.args["hub.challenge"], 200 
    return "Welcome to Pkeso Page"

@app.route('/', methods=['POST'])
def handle_message():
    data = request.get_json()
    log(data)

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = "Sorry, I cannot read your message let' me think a moment please"
                    if "text" in messaging_event["message"]:
                        message_text = messaging_event["message"]["text"]
                        send_message(sender_id, message_text.encode('ascii', 'ignore').decode('ascii'))
                    else:
                        send_message(sender_id, message_text)
                if messaging_event.get("delivery"):
                    pass

                if messaging_event.get("option"):
                    pass

                if messaging_event.get("postback"):
                    pass

    return "ok", 200

def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    data1 = json.dumps({
        "recipient": {
            "id":recipient_id 
        },
        "sender_action":"typing_on"
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data1)
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)