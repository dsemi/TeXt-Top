#!/usr/bin/python2

from flask import Flask
from flask import request

from twilio import twiml
from twilio.rest import TwilioRestClient

import os


app = Flask(__name__)
app.config.from_pyfile('local_settings.py')
if app.config['TWILIO_ACCOUNT_SID'] and app.config['TWILIO_AUTH_TOKEN']:
    app.twilio_client = TwilioRestClient(
            app.config['TWILIO_ACCOUNT_SID'],
            app.config['TWILIO_AUTH_TOKEN'])
else:
    app.twilio_client = None

    
@app.route('/sms', methods=['POST'])
def hello():
    response = twiml.Response()
    texter = in_people(request.form.get('From'))
    if texter:
        group_message('%s: %s' % (texter['name'], request.form.get('Body')), omit=texter['number'])
    else:
        response.sms('You are not verified to send group messages.')
    return str(response)


def group_message(body, omit=None):
    messages = []
    if app.twilio_client:
        for person in app.config['PEOPLE']:
            if person['number'] != omit:
                messages.append(app.twilio_client.sms.messages.create(
                    to=person['number'],
                    from_=app.config['TWILIO_CALLER_ID'],
                    body=body))
    return messages


def in_people(number):
    for person in app.config['PEOPLE']:
        if number == person['number']:
            return person
    return None


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
