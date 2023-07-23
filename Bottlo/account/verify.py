# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

os.environ['TWILIO_ACCOUNT_SID'] = 'AC2813737c6aa5bd1545f717a239b19f36'
os.environ['TWILIO_AUTH_TOKEN'] = 'e388f2889516cb64ba105d2cdcdadfe6'
os.environ['TWILIO_VERIFY_SERVICE_SID'] ='VA8a2f93777d7af0b31a12613f294d0f07'

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.v2.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])


def send(phone):
    verification = verify.verifications.create(to=phone,channel='sms')
    return verification

def check(phone,codes):
    try:
        print(phone,codes)
        result = verify.verification_checks.create(to=phone,code=codes)
        return result.status =='approved'    
    except TwilioRestException as e:
        print('Error:',e)
        return False

 
  

 
 
 
 

