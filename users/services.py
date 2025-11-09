from users.models import User
from .utils import send_email,gen_otp
import core.settings as settings
import logging
import brevo_python
from brevo_python.rest import ApiException
from pprint import pprint
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token

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

def activate_email(security,domain,recipient_email):

    user = User.objects.only("user_name","pk").get(email=recipient_email)
    try:
        subject = "Activate your account"
        sender = {"name":"Faidah from cinemascope","email":"lombardia241@gmail.com"}
        # replyTo = {"name":f"Faidah from cinemascope","email":f"{settings.EMAIL_FROM}"}
        html_content = "<html><body><h1>click this link to activate your account {{params.security}}://{{params.domain}}/users/activate/{{params.byte_string}}/{{params.token}}/ </h1></body></html>"
        # html_content = "<html><body><h1>your otp is {{params.otp}} </h1></body></html>"
        to = [{"email":f"{recipient_email}","name":f"{user.user_name}"}]
        # otp = gen_otp()
        params = {"security":security,"domain":str(domain),"byte_string":urlsafe_base64_encode(force_bytes(user.pk)),"token":account_activation_token.make_token(user)}
        # params = {"otp":gen_otp()}
        send_smtp_email = brevo_python.SendSmtpEmail(to=to,
                                                html_content=html_content, sender=sender, subject=subject,params=params) # SendSmtpEmail | Values to send a transactional email
        # api_response = api_instance.send_transac_email(send_smtp_email)
        # pprint(api_response)
        send_email_result =send_email(send_smtp_email)
        if send_email_result!=0:
            LOGGER.info(f"email successfully sent to {recipient_email}")
            return 1
        else:
            LOGGER.info("email definitely didn't send")
            return 0
    except Exception as e:
        LOGGER.error(f"Failed to send email to {recipient_email}: {e}")
        return 0
