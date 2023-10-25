# accounts/auth_backends.py
from django.contrib.auth.backends import ModelBackend
from .models import User

class UserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if the user is trying to log in with an email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # Check if the user is trying to log in with a username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
