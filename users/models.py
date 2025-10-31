from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    user_name = models.CharField(max_length=50,unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)
    # verification_datetime = models.DateTimeField(
    #     null=True,
    #     verbose_name="Verification Datetime",
    #     help_text="user's verificcation time")
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['user_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ['-date_joined']
    
    
    # @classmethod
    # def default_admin(cls):
    #     user,created = cls.objects.get_or_create(email="admin2@cs.com",is_superuser=True,is_active=True,user_name="admin")
    #     user.set_password("admin")
    #     return user.pk
    
# class Social(models.Model):
#     title = models.CharField(default="default social")
#     link = models.URLField(max_length = 200,default="https://example.com/default")
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="user_profile")
    bio = models.TextField(max_length=50,null=True,blank=True)
    website = models.URLField(max_length=100,null=True,blank=True)
    location = models.TextField(max_length=100,null=True,blank=True)
    profile_image = models.ImageField(upload_to="users/profile_images/", null=True,blank=True)
    profile_cover = models.ImageField(upload_to="users/profile_covers/", null=True,blank=True)
    
    def __str__(self):
        return f"{self.user}'s profile"