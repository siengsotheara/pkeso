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

    
    return "ok", 200

'''
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
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)

'''
def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)