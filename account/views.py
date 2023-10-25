from django.shortcuts import render,get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model,logout,login
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User,UserProfile
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from reviews.models import Review





class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = self.Meta.model(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()



class UpdateProfileSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False, write_only=True)



class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            # Create a new user if the data is valid
            serializer.save()
            return Response({'message': 'User registered successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username_or_email = serializer.validated_data.get('username_or_email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username_or_email, password=password)
        
            if user:
                if not isinstance(user, AnonymousUser): 
                    login(request, user)
                    token, created = Token.objects.get_or_create(user=user)
                    username = user.username
                    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                    user_reviews = user_profile.user_reviews.all()

                     # Retrieve user_reviews and convert them to a list of IDs
                    user_reviews_ids = list(user_profile.user_reviews.values_list('id', flat=True))

                    # Retrieve followers and convert them to a list of IDs
                    follower_ids = list(user_profile.followers.values_list('id', flat=True))

                    # Create a dictionary representa

                    user_profile_data = {
                    'id': user_profile.id,
                    'followers': follower_ids,
                    # Include any other fields from UserProfile that you need
                    # 'user_reviews': [review.id for review in user_reviews],
                    'user_reviews':user_reviews_ids
                    # You can include IDs or other relevant data from user_reviews
                    }

              
                    return Response({'token': token.key,'username':username,'user_profile':user_profile_data,})
                # return Response({'token': token.key,'username':username,})
                else:
                    return Response({'detail': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
                    
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
           
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user  # Get the authenticated user
            new_username = serializer.validated_data.get('username')
            new_password = serializer.validated_data.get('password')

            if new_username:
                user.username = new_username

            if new_password:
                user.set_password(new_password)

            user.save()
            return Response({'message': 'Profile updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Get the user's token
        user_token = Token.objects.get(user=request.user)

        # Delete the user's token
        user_token.delete()

        # Perform the user logout
        logout(request)

        return Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)
    


class UserProfileDetailView(APIView):
    def get(self, request,username):
        # Get the user object by username
        user = get_object_or_404(User, username=username)

        # Retrieve the UserProfile or create it if it doesn't exist
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Retrieve user_reviews and convert them to a list of IDs
        user_reviews_ids = list(user_profile.user_reviews.values_list('id', flat=True))

        # Retrieve followers and convert them to a list of IDs
        follower_ids = list(user_profile.followers.values_list('id', flat=True))
        # user = User.objects.get(id=user_id)
        # Create a dictionary representation of the UserProfile and related data
        user_profile_data = {
            'id': user_profile.id,
            'followers': follower_ids,
            'user_reviews':  user_reviews_ids,
            # Include any other fields from UserProfile that you need
        }

        return Response({'user_profile': user_profile_data})

class UserProfileDetailViewID(APIView):
    def get(self, request,id):
        # Get the user object by username
        user = get_object_or_404(User, pk=id)

        # Retrieve the UserProfile or create it if it doesn't exist
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Retrieve user_reviews and convert them to a list of IDs
        user_reviews_ids = list(user_profile.user_reviews.values_list('id', flat=True))

        # Retrieve followers and convert them to a list of IDs
        follower_ids = list(user_profile.followers.values_list('id', flat=True))
        # user = User.objects.get(id=user_id)
        # Create a dictionary representation of the UserProfile and related data
        user_profile_data = {
            'id': user_profile.id,
            'followers': follower_ids,
            'user_reviews':  user_reviews_ids,
            # Include any other fields from UserProfile that you need
        }

        return Response({'user_profile': user_profile_data})







def get_user_profile(request, user_id):
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
        # Serialize user_profile to JSON
        user_profile_data = {
            "followers": user_profile.followers.count(),
            "user_reviews": user_profile.user_reviews.count(),
            # Add more fields as needed
        }
        return JsonResponse(user_profile_data)
    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User profile not found"}, status=404)

# serializers.py

# class SignupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'username', 'password']

#     def create(self, validated_data):
#         user = User(**validated_data)
#         user.set_password(validated_data['password'])
#         user.save()

#         # Generate tokens for the new user
#         tokens = get_tokens_for_user(user)

#         return tokens









# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }


# @api_view(['POST'])
# def signup(request):
#     serializer = SignupSerializer(data=request.data)
#     if serializer.is_valid():
#         tokens = serializer.save()

#         return Response(tokens)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def login(request):
#     serializer = LoginSerializer(data=request.data)
#     if serializer.is_valid():
#         user = authenticate(request, username=serializer.validated_data.get('username'), password=serializer.validated_data.get('password'))

#         if user:
#             tokens = get_tokens_for_user(user)
#             username = user.username
#             return Response({"token":tokens,"username":username})
#         else:
#             return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# @api_view(['POST'])
# def logout(request):
#     refresh = request.headers.get('refresh')
#     if refresh:
#         RefreshToken(refresh).blacklist()

#     return Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)



     # if user:
            #     refresh = RefreshToken.for_user(user)
            #     access_token = str(refresh.access_token)
            #     refresh_token = str(refresh)

            #     # Return the access_token and refresh_token to the client
            #     return Response({'access_token': access_token, 'refresh_token': refresh_token})
            # else:
            #     # Handle authentication failure
            #     return Response({'error': 'Invalid credentials'}, status=400) 
