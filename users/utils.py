from pysendpulse.pysendpulse import PySendPulse
import core.settings as settings
import logging
# from __future__ import print_function
import time
# import brevo_python
from brevo_python.rest import ApiException
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv()
LOGGER = logging.getLogger(__name__)

# REST_API_ID = settings.EMAIL_CLIENT_ID
# REST_API_SECRET = settings.EMAIL_CLIENT_SECRET
# TOKEN_STORAGE = 'memcached'
# MEMCACHED_HOST = '127.0.0.1:11211'
# SPApiProxy = PySendPulse(REST_API_ID, REST_API_SECRET, TOKEN_STORAGE, memcached_host=MEMCACHED_HOST)


# def send_email(email):
#     try:
#         response = SPApiProxy.smtp_send_mail(email)
#         LOGGER.info(f"sendpulse response {response}")
#         if not response or not response.get("result"):
#             raise Exception(f"SendPulse email send failed: {response}")

#         return response
#     except Exception as e:
#         LOGGER.error(f"SendPulse failed to send email: {e}")
#         raise


def send_email(send_smtp_email):
    import brevo_python
    configuration = brevo_python.Configuration()
    configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY')
    # configuration.api_key_prefix['api-key'] = 'Bearer'
    api_instance = brevo_python.TransactionalEmailsApi(brevo_python.ApiClient(configuration))
    try:
        # Send a transactional email
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)

def gen_otp():
    import random
    string = ""
    list1 = []
    for i in range(0,6):
        list1.append(str(random.randrange(0,10)))
    string = string.join(list1)
    
    return string


