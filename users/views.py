from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import UserSerializer,LoginSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import User
from .services import activate_email
import logging
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from users.tokens import account_activation_token
from django.db import transaction,IntegrityError

# Create your views here.
LOGGER = logging.getLogger(__name__)


@api_view(['GET'])
def test_site(request):
    current_site = get_current_site(request)
    site_name = current_site.name
    site_domain = current_site.domain
    # c = current_site.e
    # ... use site_name and site_domain in your view logic
    return Response(f"Welcome to {site_name} --- ({site_domain})!")


def security_set(request):
    return 'https' if request.is_secure() else 'http'


@api_view(['POST'])
def signup(request):
    try:
        data = request.data
        email = data.get("email")
        with transaction.atomic():
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                activate_email_response = activate_email(security_set(request),get_current_site(request),email)
                # activate_email_response = activate_email(email)
                print("activate-email-response", activate_email_response)
                if activate_email_response != 1:
                    raise IntegrityError("Data is not valid, rolling back.")
                LOGGER.info("Testing info log")
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        LOGGER.warning("Testing warning log")
        LOGGER.error("Testing error log")
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
def signin(request):
    user = User.objects.get(email=request.data["email"])
    data = request.data
    
    # print("before user = ",user)
    try:
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                user_data =UserSerializer(user)
                data = dict(user_data.data)
                data['tokens'] = {"refresh":str(refresh),"access":str(refresh.access_token)}
                return Response({"message":"successful","data":data},status=status.HTTP_200_OK)
            else:
                # refresh = RefreshToken.for_user(user)
                user_data =UserSerializer(user)
                data = dict(user_data.data)
                data['tokens'] = {"refresh":None,"access":None}
                return Response({"message":"you aren't activated yet","data":data},status=status.HTTP_200_OK)
            # raise AuthenticationFailed("User is not active")
            
        return Response({"message":"something went wrong","error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_by_user_name(request):
    # user = User.objects.get(user_name=request.data["user_name"])
    user_name = request.query_params.get("user_name")
    if not user_name:
        return Response({"message":"user_name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(user_name=user_name)
        serializer = UserSerializer(user)
        return Response({"message":"successfully retrieved","data":serializer.data},status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"message":"user doesn't exist"},status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(['GET'])
def activate_account(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)  
    except (TypeError,ValueError,User.DoesNotExist) as error:
        user = None  
    
    if user is not None and not user.is_active and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        return Response({"message":"you have successfully activated your account"},status=status.HTTP_200_OK)
        
        
    
    # except Exception as e:
    #     return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    