from users.models import User
from .utils import send_email, gen_otp
import core.settings as settings
import logging
import brevo_python
from brevo_python.rest import ApiException
from pprint import pprint
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from users.tokens import account_activation_token
from users.auth import create_password_reset_token

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
    # print("seett= ",settings.FRONTEND_URL)

    user = User.objects.only("user_name", "pk").get(email=recipient_email)
    try:
        subject = "Activate your account"
        sender = {"name": "cinemascope", "email": settings.EMAIL_FROM}
        # replyTo = {"name":f"Faidah from cinemascope","email":f"{settings.EMAIL_FROM}"}
        # html_content = "<html><body><h1>click this link to activate your account {{params.security}}://{{params.domain}}/users/activate/{{params.byte_string}}/{{params.token}}/ </h1></body></html>"
        params = {
            "byte_string": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "domain": str(settings.FRONTEND_URL),
        }
        # html_content = "<html><body><h1>click this link to activate your account {{params.domain}}/activate-account/{{params.byte_string}}/{{params.token}}/ </h1></body></html>"
        html_content = """ <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Activate Your Account</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0b101b; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; color: #e2e8f0;">

  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #0b101b; padding: 40px 20px;">
    <tr>
      <td align="center">
        
        <table width="100%" max-width="600" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; background-color: #1B2535; border: 1px solid #2c353f; border-radius: 8px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
          
          <tr>
            <td align="center" style="padding: 40px 0 20px 0;">
              <h2 style="margin: 0; color: #ffffff; font-size: 24px; letter-spacing: 2px; text-transform: uppercase;">Cinemascope</h2>
            </td>
          </tr>

          <tr>
            <td style="padding: 20px 40px 30px 40px; text-align: center;">
              <h1 style="margin: 0 0 20px 0; color: #ffffff; font-size: 28px; font-weight: bold;">Welcome to the club.</h1>
              <p style="margin: 0 0 30px 0; color: #94a3b8; font-size: 16px; line-height: 1.6;">
                You're almost ready to start tracking, reviewing, and sharing your favorite films. Click the button below to verify your email address and activate your account.
              </p>

              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="center">
                    <a href="{{params.domain}}/activate-account/{{params.byte_string}}/{{params.token}}/" style="display: inline-block; padding: 14px 32px; background-color: #dc143c; color: #ffffff; text-decoration: none; font-size: 14px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; border-radius: 4px;">
                      Activate Account
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding: 0 40px 40px 40px; text-align: center;">
              <p style="margin: 0; color: #64748b; font-size: 13px; line-height: 1.5;">
                If the button above doesn't work, copy and paste this link into your web browser:<br>
                <a href="{{params.domain}}/activate-account/{{params.byte_string}}/{{params.token}}/" style="color: #40bcf4; word-break: break-all;">
                  {{params.domain}}/activate-account/{{params.byte_string}}/{{params.token}}/
                </a>
              </p>
            </td>
          </tr>

          <tr>
            <td style="background-color: #0b101b; padding: 30px 40px; text-align: center; border-top: 1px solid #2c353f;">
              <p style="margin: 0 0 10px 0; color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">
                &copy; Cinemascope. Made in Ogun, Nigeria.
              </p>
              <p style="margin: 0; color: #475569; font-size: 11px;">
                You received this email because you created an account on our platform. If this wasn't you, please safely ignore this email.
              </p>
            </td>
          </tr>

        </table>
        
      </td>
    </tr>
  </table>

</body>
</html>"""

        # html_content = "<html><body><h1>your otp is {{params.otp}} </h1></body></html>"
        to = [{"email": f"{recipient_email}", "name": f"{user.user_name}"}]

        # params = {"security":security,"domain":str(domain),"byte_string":urlsafe_base64_encode(force_bytes(user.pk)),"token":account_activation_token.make_token(user)}
        # params = {"otp":gen_otp()}
        send_smtp_email = brevo_python.SendSmtpEmail(
            to=to,
            html_content=html_content,
            sender=sender,
            subject=subject,
            params=params,
        )  # SendSmtpEmail | Values to send a transactional email
        # api_response = api_instance.send_transac_email(send_smtp_email)
        # pprint(api_response)
        send_email_result = send_email(send_smtp_email)
        if send_email_result != 0:
            LOGGER.info(f"email successfully sent to {recipient_email}")
            return 1
        else:
            LOGGER.info("email definitely didn't send")
            return 0
    except Exception as e:
        LOGGER.error(f"Failed to send email to {recipient_email}: {e}")
        return 0


def send_reset_password(recipient_email):
    user = User.objects.only("user_name", "pk").get(email=recipient_email)

    try:
        subject = "reset your password"
        sender = {"name": "cinemascope", "email": settings.EMAIL_FROM}
        params = {"token": create_password_reset_token(user), "domain": str(settings.FRONTEND_URL),}
        # replyTo = {"name":f"Faidah from cinemascope","email":f"{settings.EMAIL_FROM}"}
        # html_content = "<html><body><h1>click this link to reset your password, if it wasn't you please, ignore it {{settings.FRONTEND_URL}}/users/reset_confirm/{{params.token}}/ </h1></body></html>"
        # html_content = "<html><body><h1>your otp is {{params.otp}} </h1></body></html>"
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reset Your Password</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0b101b; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; color: #e2e8f0;">

  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #0b101b; padding: 40px 20px;">
    <tr>
      <td align="center">
        
        <table width="100%" max-width="600" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; background-color: #1B2535; border: 1px solid #2c353f; border-radius: 8px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
          
          <tr>
            <td align="center" style="padding: 40px 0 20px 0;">
              <h2 style="margin: 0; color: #ffffff; font-size: 24px; letter-spacing: 2px; text-transform: uppercase;">Cinemascope</h2>
            </td>
          </tr>

          <tr>
            <td style="padding: 20px 40px 30px 40px; text-align: center;">
              <h1 style="margin: 0 0 20px 0; color: #ffffff; font-size: 26px; font-weight: bold;">Password Reset Request</h1>
              <p style="margin: 0 0 30px 0; color: #94a3b8; font-size: 16px; line-height: 1.6;">
                We received a request to reset the password for your Cinemascope account. Click the button below to securely set up a new password.
              </p>

              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="center">
                    <a href="{{params.domain}}/users/reset_confirm/{{params.token}}/" style="display: inline-block; padding: 14px 32px; background-color: #dc143c; color: #ffffff; text-decoration: none; font-size: 14px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; border-radius: 4px;">
                      Reset Password
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td style="padding: 0 40px 40px 40px; text-align: center;">
              <p style="margin: 0; color: #64748b; font-size: 13px; line-height: 1.5;">
                If the button above doesn't work, copy and paste this link into your web browser:<br>
                <a href="{{params.domain}}/users/reset_confirm/{{params.token}}/" style="color: #40bcf4; word-break: break-all;">
                  {{params.domain}}/users/reset_confirm/{{params.token}}/
                </a>
              </p>
            </td>
          </tr>

          <tr>
            <td style="background-color: #0b101b; padding: 30px 40px; text-align: center; border-top: 1px solid #2c353f;">
              <p style="margin: 0 0 10px 0; color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">
                &copy; Cinemascope Security
              </p>
              <p style="margin: 0; color: #475569; font-size: 11px; line-height: 1.5;">
                If you did not request a password reset, please safely ignore this email. Your password will remain unchanged and your account is secure.
              </p>
            </td>
          </tr>

        </table>
        
      </td>
    </tr>
  </table>

</body>
</html>"""
        to = [{"email": f"{recipient_email}", "name": f"{user.user_name}"}]
        # otp = gen_otp()
      
        # params = {"otp":gen_otp()}
        send_smtp_email = brevo_python.SendSmtpEmail(
            to=to,
            html_content=html_content,
            sender=sender,
            subject=subject,
            params=params,
        )  # SendSmtpEmail | Values to send a transactional email
        # api_response = api_instance.send_transac_email(send_smtp_email)
        # pprint(api_response)
        send_email_result = send_email(send_smtp_email)
        if send_email_result != 0:
            LOGGER.info(f"email successfully sent to {recipient_email}")
            return 1
        else:
            LOGGER.info("email definitely didn't send")
            return 0

    except Exception as e:
        LOGGER.error(f"Failed to send email to {recipient_email}: {e}")
        return 0
