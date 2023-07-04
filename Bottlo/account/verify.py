# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

os.environ['TWILIO_ACCOUNT_SID'] = 'AC2813737c6aa5bd1545f717a239b19f36'
os.environ['TWILIO_AUTH_TOKEN'] = '6ad54d19d3fe8191a4ebf3e30baeda56'
os.environ['TWILIO_VERIFY_SERVICE_SID'] = 'MG34ac57a818bfc5791fc40f905e177469'

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])


def send(phone):
    service = client.verify.services.create(friendly_name='Bottlo_verify')
    verification = service.verifications.create(to=phone,channel='sms')
    return verification
    

def check(phone,code):
    try:
        result = verify.verification_checks.create(to=phone,code=code)
        print(result)
        return result.status =='approved'    
    except TwilioRestException as e:
        print('Error:',e)
        return False


