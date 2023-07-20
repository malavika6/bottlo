# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

os.environ['TWILIO_ACCOUNT_SID'] = 'AC2813737c6aa5bd1545f717a239b19f36'
os.environ['TWILIO_AUTH_TOKEN'] = 'a5add8394cf132aa59f7038d50fb56a4'
os.environ['TWILIO_VERIFY_SERVICE_SID'] ='VA96f1d188e8cf5334562f58b805034933'

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])


# def send(phone):
#     service = client.verify.services.create(friendly_name='Bottlo_verify')
#     print(service,"serv")
#     verification = service.verifications.create(to=phone,channel='sms')
#     print(verification,'ver')
#     return verification

# def check(phone,code):
#     try:
#         print(phone,code,"hi")
        
#         result = verify.verification_checks.create(to=phone,code=code)
#         print(result)
#         print(phone,code)
#     except TwilioRestException:
#         print('no')
#         return False 
#     return result.status == 'approved'

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

