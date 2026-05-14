from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import UserSerializer,LoginSerializer,ChangePasswordSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.token_blacklist import OutstandingToken,BlacklistedToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import User
from .services import activate_email
import logging
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from users.tokens import account_activation_token
from django.db import transaction,IntegrityError
from .tokens import RefreshTokenStore
import hashlib
import bcrypt
from datetime import timedelta
from django.utils import timezone

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


def generate_access_token(user):
    refresh = RefreshToken.for_user(user)
    print("gen ref= ",refresh)
    return str(refresh.access_token)


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
    print("before user = ",request.user)
    try:
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                user_data =UserSerializer(user)
                data = dict(user_data.data)
                # print("refresher = ",str(refresh))
                data['tokens'] = {"access":str(refresh.access_token)}
                token_index = hashlib.sha256(str(refresh).encode()).hexdigest()
                encoded_ref_token = hashlib.sha256(str(refresh).encode()).digest()
                hashed_ref_token = bcrypt.hashpw(encoded_ref_token,bcrypt.gensalt(12))
                RefreshTokenStore.objects.create(user=user,token=hashed_ref_token,token_index=token_index, expires_at=timezone.now() + timedelta(days=7))
                response = Response({"message":"successful","data":data},status=status.HTTP_200_OK)
                if request.data['remember'] == True:
                    response.set_cookie(key="refresh_token",value=str(refresh),httponly=True,secure=True,samesite="Lax",max_age=60 * 60 * 24 * 7)
                else:
                    response.set_cookie(key="refresh_token",value=str(refresh),httponly=True,secure=True,samesite="Lax")
                return response
                # return Response({"message":"successful","data":data},status=status.HTTP_200_OK)
            else:
                # refresh = RefreshToken.for_user(user)
                user_data =UserSerializer(user)
                data = dict(user_data.data)
                data['tokens'] = {"access":None}
                return Response({"message":"you aren't activated yet","data":data},status=status.HTTP_200_OK)
            # raise AuthenticationFailed("User is not active")
            
        return Response({"message":"something went wrong","error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
# @permission_classes([IsAuthenticated,AllowAny])
def token_refresh(request):
    # user = User.objects.get(email=request.user)
    refresh_token = request.COOKIES.get("refresh_token")
    if not refresh_token:
        raise AuthenticationFailed("No refresh token")
    
    print("COOKIE TOKEN:", refresh_token)

    reproduced_token_index = hashlib.sha256(str(refresh_token).encode()).hexdigest()
    print("COOKIE TOKEN:", reproduced_token_index)
    
    token_obj = RefreshTokenStore.objects.filter(
        token_index=reproduced_token_index,
        revoked=False
    ).first()
    
    print("DB MATCH:", token_obj)
    

    if not token_obj or token_obj.expires_at < timezone.now():
        raise AuthenticationFailed("Invalid refresh token")

    user = token_obj.user
    # OPTIONAL: ROTATION (recommended)
    # token_obj.revoked = True
    # token_obj.save()

    # new_refresh_token = RefreshToken.for_user(user)
    # new_refresh_token_index = hashlib.sha256(str(new_refresh_token).encode()).hexdigest()
    # RefreshTokenStore.objects.create(
    #     user=token_obj.user,
    #     token=new_refresh_token,
    #     token_index=new_refresh_token_index,
    #     expires_at=timezone.now() + timedelta(days=7)
    # )

    
        
    new_access_token = generate_access_token(user)

    print(new_access_token)
    response = Response({"access_token": new_access_token})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  #change in prod
        samesite="Lax"
    )

    return response
    

@api_view(['GET'])
def get_by_user_name_or_id(request):
    # user = User.objects.get(user_name=request.data["user_name"])
    # param = request.query_params.get("user_name") or request.query_params.get("id")
    param = None
    # if param is None:
    #     return Response({"message":"user_name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if "user_name" in request.query_params:
        param = request.query_params.get("user_name") 
        try:
            user = User.objects.get(user_name=param)
            serializer = UserSerializer(user)
            return Response({"message":"successfully retrieved","data":serializer.data},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message":"user doesn't exist"},status=status.HTTP_404_NOT_FOUND)
    
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    elif "id" in request.query_params:
        param = request.query_params.get("id")
        try:
            user = User.objects.get(id=param)
            serializer = UserSerializer(user)
            return Response({"message":"successfully retrieved","data":serializer.data},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message":"user doesn't exist"},status=status.HTTP_404_NOT_FOUND)
    
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    elif param is None:
        return Response({"message":"user_name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    
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
    
  
@api_view(['POST'])
@permission_classes([IsAuthenticated])  
# def logout(request):
#     try:
#         token = request.data.get("refresh")
        
#         token = RefreshToken(token) 
#         token.blacklist()
#         return Response({"message":"you have logged out successfully"},status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"message":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
def logout(request):
    try:
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            token = RefreshToken(refresh_token) 
            new_refresh_token_index = hashlib.sha256(refresh_token.encode()).hexdigest()
            token.blacklist()
            RefreshTokenStore.objects.filter(token_index=new_refresh_token_index).update(revoked=True)

        response = Response({"message": "Logged out"},status=status.HTTP_200_OK)
        
        response.delete_cookie("refresh_token")

        return response
    except Exception as e:
        return Response({"message":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    try:
        data =request.data
        user = request.user
        print("user_is_active",user.is_active)
        print("user_is_blacklisted",user.is_blacklisted)
        if user.is_active and not user.is_blacklisted:
            print("Inside the block!") # Add a print here to be SURE
            serializer = ChangePasswordSerializer(request.user,data)
            if serializer.is_valid():
                serializer.save(raise_exception = True)
                return Response({"message":"password successfully updated"},status=status.HTTP_200_OK)
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "You are forbidden"},
                    status=status.HTTP_403_FORBIDDEN # Use 403 for Permission issues
                )
    except Exception as e:
        return Response({"message":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        

    
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def try_user(request):
#     try:
#         user = request.user
#         print("user = ", user)
        
       
#         return Response({"message":"successful"},status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"message":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)