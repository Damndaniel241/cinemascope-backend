from users.models import User
from .utils import send_email,gen_otp
import core.settings as settings
import logging
import brevo_python
from brevo_python.rest import ApiException
from pprint import pprint


LOGGER = logging.getLogger(__name__)


# def activate_email(recipient_email):
#     try:
#         user = User.objects.only("user_name").get(email=recipient_email)
#         email = {
#             'subject': 'Verify your account ',
#             'from': {'name': 'Faidah from cinemascope', 'email': settings.EMAIL_FROM},
#             'to': [
#                 {'name': f'{user.user_name}', 'email': user.email}
#             ],
#             # "template": {
#             #     'id': '73606',  # ID of the template uploaded in the service. Use this
#             #     # (https://sendpulse.com/integrations/api/bulk-email#template-list)
#             #     # method to get the template ID (use either real_id or id parameter from the reply)
#             #     'variables': {
#             #         'foo': 'value',
#             #         'bar': 'value'
#             #     }
#             # },
#             'html':'<p>this is your otp </p>',
#             'text': '111111'
                
            
#         }
#         send_email(email)
#         LOGGER.info(f"email successfully sent to {recipient_email}")
#     except Exception as e:
#         LOGGER.error(f"Failed to send email to {recipient_email}: {e}")
#         # raise Exception(e)

def activate_email(recipient_email):

    user = User.objects.only("user_name").get(email=recipient_email)
    try:
        subject = "Verify your account"
        sender = {"name":"Faidah from cinemascope","email":"lombardia241@gmail.com"}
        # replyTo = {"name":f"Faidah from cinemascope","email":f"{settings.EMAIL_FROM}"}
        html_content = "<html><body><h1>your otp is {{params.otp}} </h1></body></html>"
        to = [{"email":f"{recipient_email}","name":f"{user.user_name}"}]
        otp = gen_otp()
        params = {"parameter":"My param value","subject":"New Subject","otp":otp}
        send_smtp_email = brevo_python.SendSmtpEmail(to=to,
                                                html_content=html_content, sender=sender, subject=subject,params=params) # SendSmtpEmail | Values to send a transactional email
        # api_response = api_instance.send_transac_email(send_smtp_email)
        # pprint(api_response)
        send_email(send_smtp_email)
        LOGGER.info(f"email successfully sent to {recipient_email}")
    except Exception as e:
        LOGGER.error(f"Failed to send email to {recipient_email}: {e}")
        


# from __future__ import print_function
# import time
# import brevo_python
# from brevo_python.rest import ApiException
# from pprint import pprint

# # Configure API key authorization: api-key
# configuration = brevo_python.Configuration()
# configuration.api_key['api-key'] = 'YOUR_API_KEY'
# # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# # configuration.api_key_prefix['api-key'] = 'Bearer'
# # Configure API key authorization: partner-key
# configuration = brevo_python.Configuration()
# configuration.api_key['partner-key'] = 'YOUR_API_KEY'
# # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# # configuration.api_key_prefix['partner-key'] = 'Bearer'

# # create an instance of the API class
# api_instance = brevo_python.TransactionalEmailsApi(brevo_python.ApiClient(configuration))
# subject = "from the Python SDK!"
# sender = {"name":"Brevo","email":"contact@brrevo.com"}
# replyTo = {"name":"Brevo","email":"contact@brevo.com"}
# html_content = "<html><body><h1>This is my first transactional email </h1></body></html>"
# to = [{"email":"example@example.com","name":"Jane Doe"}]
# params = {"parameter":"My param value","subject":"New Subject"}
# send_smtp_email = brevo_python.SendSmtpEmail(to=to, bcc=bcc, cc=cc, reply_to=reply_to,
#                                              headers=headers, html_content=html_content, sender=sender, subject=subject) # SendSmtpEmail | Values to send a transactional email

# try:
#     # Send a transactional email
#     api_response = api_instance.send_transac_email(send_smtp_email)
#     pprint(api_response)
# except ApiException as e:
#     print("Exception when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)