from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,permission_classes
from .serializers import ReviewSerializer,RatingSerializer
from users.models import User
from .models import Review,Movie,Rating
from django.db.models import Q



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    try:
        movie_id = request.data['movie']
        user = request.user
        # request.data['user'] = user
        try:
            movie_obj= Movie.objects.get(movie_id=movie_id)
            # print("movie_obj = ",movie_obj)
        except Movie.DoesNotExist:
            # print("movie does not exist")
            movie_obj= Movie.objects.create(movie_id=movie_id)
            # movie_obj.save()

        print("request.data = ",request.data)
        serializer = ReviewSerializer(data=request.data)
        print("serializer = ",serializer)
        if serializer.is_valid(raise_exception=True):
            print("i got here")
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
# @permission_classes([AllowAny])
def get_review(request,pk):
    try:
        try:
            review_obj = Review.objects.filter(pk=pk).first()
        except Review.DoesNotExist:
            pass
        serializer = ReviewSerializer(review_obj)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_review(request,pk):
    try:
        review_obj = Review.objects.filter(pk=pk).first()
        # print("review_obj = ",review_obj)
        
        if review_obj:
            
            serializer = ReviewSerializer(review_obj,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message":"review updated successfully","data":serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request,pk):
    try:
        try:
            review_obj = Review.objects.filter(pk=pk).first()
            if review_obj:
                review_obj.delete()
                return Response({"message":"review deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({"message":"object doesn't exist"},status=status.HTTP_404_NOT_FOUND)

            
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST','PUT'])
@permission_classes([IsAuthenticated])
def rate_movie(request):
    if request.method == "POST":
        print("this has been seen")
        try:
            print("also seen 1")
            try:
                print("also seen 2")
                print("movie= ",request.data["movie"])
                print("user= ",request.user.id)
                movie_obj = Movie.objects.get(movie_id=request.data["movie"])
                
                
                    
            
                # rating_obj = Rating.objects.filter(Q(movie=request.data["movie"]) , Q(user=request.user.id))
            except Movie.DoesNotExist:
                movie_obj = Movie.objects.create(movie_id=request.data["movie"])
                # movie_obj = Movie.objects.get(movie_id=request.data["movie"])
            print("also seen 3, movie_obj= ", movie_obj)
            
            rating_obj = Rating.objects.filter(movie=movie_obj,user=request.user).exists()
            print("rating_obj pleaasseee = ",rating_obj)            
            if rating_obj:
                Rating.objects.update(stars=request.data["stars"])
                return Response({"message":"movie rated successfully","data":serializer.data},status=status.HTTP_200_OK)
            
            print("also seen 4")
            serializer = RatingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({"message":"movie rated successfully","data":serializer.data},status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    else:
        try:
            movie_obj = Movie.objects.get(movie_id=request.data["movie"])
            rating_obj = Rating.objects.filter(movie=movie_obj,user=request.user).first()
            print("rating_obj pleaasseee = ",rating_obj)
            
            if rating_obj:
                serializer = RatingSerializer(rating_obj, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({"message":"movie rating updated successfully","data":serializer.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        
    
    
    #i'm trying to create property methods for movie model