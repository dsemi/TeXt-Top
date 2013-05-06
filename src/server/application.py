from flask import Flask
from flask import request

from twilio import twiml
from twilio.rest import TwilioRestClient

import boto

application = Flask(__name__)
application.config.from_pyfile('local_settings.py')
if application.config['TWILIO_ACCOUNT_SID'] and application.config['TWILIO_AUTH_TOKEN']:
    application.twilio_client = TwilioRestClient(
            application.config['TWILIO_ACCOUNT_SID'],
            application.config['TWILIO_AUTH_TOKEN'])
else:
    application.twilio_client = None

application.sqs = boto.connect_sqs(application.config['AWS_ACCESS_KEY_ID'], application.config['AWS_SECRET_ACCESS_KEY'])
application.s3 = boto.connect_s3(application.config['AWS_ACCESS_KEY_ID'], application.config['AWS_SECRET_ACCESS_KEY'])
application.db = boto.connect_dynamodb(application.config['AWS_ACCESS_KEY_ID'], application.config['AWS_SECRET_ACCESS_KEY'])


def text_handler(**params):
    user = params.get('user')
    message = params.get('message')
    command = message.split(',')
    for i,old in enumerate(command):
        command[i] = old.strip()
    print str(command)
    if not validate(user['Username'], command[0]):
        return error(user, 1)
    add_to_queue(user['Username'], command)


def add_to_queue(username, command):
    queue = application.sqs.get_queue(username)
    queue.write(queue.new_message(','.join(command)))

    
def validate(username, commandname):
    bucket = application.s3.get_bucket('text-top')
    return bucket.get_all_keys(prefix='users/{0}/{1}'.format(username,commandname))
 

def error(user, errno):
    if errno == 1:
        err_message = application.twilio_client.sms.messages.create(
            to=user['Phone Number'],
            from_=application.config['TWILIO_CALLER_ID'],
            body='Invalid command')
    return err_message


@application.route('/sms', methods=['POST'])
def hello():
    response = twiml.Response()
    # Change this to check for user in database
    table = application.db.get_table('Users2')
    try:
        user = table.get_item(request.form.get('From'))
        text_handler(user=user, message=request.form.get('Body'))
    except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
        response.sms('You\'re phone number is not in the system.  Who do you think you are?')
    return str(response)


@application.route('/response', methods=['POST'])
def resp():
    num = request.args.get('phone')
    output = request.args.get('output')
    errcode = request.args.get('error code')
    body = 'Command completed successfully' if not int(errcode) else 'Error'
    if output and not int(errcode):
        body = output
    if application.twilio_client:
        message = application.twilio_client.sms.messages.create(
            to=num,
            from_=application.config['TWILIO_CALLER_ID'],
            body=body)
    return str(message)


def group_message(body, omit=None):
    messages = []
    if application.twilio_client:
        for person in application.config['PEOPLE']:
            if person['number'] != omit:
                messages.append(application.twilio_client.sms.messages.create(
                    to=person['number'],
                    from_=application.config['TWILIO_CALLER_ID'],
                    body=body))
    return messages


def in_people(number):
    for person in application.config['PEOPLE']:
        if number == person['number']:
            return person
    return None


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=80)
