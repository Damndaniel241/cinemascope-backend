from rest_framework import serializers
from users.models import User,UserProfile
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.db import transaction


# class SocialField(serializers.Field):
#     def to_representation(self, value:Social):
#         return {
#             "title":value.title,
#             "link":value.link
#         }
        
#     def to_internal_value(self, data):
#         return Social.objects.get_or_create(
#             title=data.get("title"),
#             link=data.get("link")
#         )[0]
        
class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)
    profile_cover = serializers.ImageField(required=False)
    class Meta:
        model = UserProfile
        fields = ["user","bio","website","location","profile_image","profile_cover"]
        
        

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="This email address is already in use.")]
    )
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)
    user_profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ["id","email","user_name","is_verified","password","password2","user_profile"]
        read_only_fields = ["is_verified"]
        
        
    def validate(self,attrs):
        password = attrs.get("password")
        password2 = attrs.pop("password2")
        
        if password != password2:
            return serializers.ValidationError({ "password": "Password fields didn't match." })
        return attrs
    
    def validate_user_name(self,value):
        if User.objects.filter(user_name=value).exists():
            raise serializers.ValidationError("a user with this username already exists")
        return value
        
    def create(self,validated_data):
        # print("i got here")
        password = validated_data.pop("password")
        # user_profile_data = validated_data.pop('user_profile',None)
        # print("user_profile_data = ",user_profile_data)
        with transaction.atomic():
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            # if user_profile_data is not None:
                # print("i got here for profile")
            profile = UserProfile.objects.create(user=user)
            profile.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True,required=True)
    
    def validate(self,data):
        user = authenticate(**data)
        if user is not None:
            serializers.ValidationError({"error":"invalid credentials"})
        return data
    
    
