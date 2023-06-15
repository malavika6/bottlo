# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

os.environ['TWILIO_ACCOUNT_SID'] = 'AC2813737c6aa5bd1545f717a239b19f36'
os.environ['TWILIO_AUTH_TOKEN'] = '7f3e69c8b9bbe9d0b9c776613311016f'
os.environ['TWILIO_VERIFY_SERVICE_SID'] = 'VA42a0c11c0b5d548f985831d09d2ef290'

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])


def send(phone):
    verify.verifications.create(to=phone, channel='sms')


def check(phone, code):
    try:
        result = verify.verification_checks.create(to=phone, code=code)
    except TwilioRestException:
        print('no')
        return False
    return result.status =='approved'
