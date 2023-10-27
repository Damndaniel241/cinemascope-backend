from django.shortcuts import render,get_object_or_404
from rest_framework import serializers,status
from .models import Review,Movie,Comment,Like,Rating
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from account.models import UserProfile

# Create your views here.


# class ReviewSerializer(serializers.ModelSerializer):
#     user = serializers.CharField(source='user.username', read_only=True)
#     class Meta:
#         model = Review
#         fields = ['user', 'movie', 'content'] 



# class CreateReviewView(generics.CreateAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def perform_create(self, serializer):
#     # Get the user associated with the token from the request
#         user = self.request.user
#         serializer.save(user=user)  



def create_or_update_user_profile(user):
    # Get or create a user profile for the user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Add the user's reviews to the user_reviews field
    user_profile.user_reviews.set(Review.objects.filter(user=user))
    user_profile.liked_reviews.set(Review.objects.filter(user=user))
    user_profile.rated_reviews.set(Review.objects.filter(user=user))

    # Save the user profile
    user_profile.save()

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_review(request):
    if request.method == 'POST':
        data = request.data
        try:
            content = data['content']
            movie_id = data['movie_id']

            try:
                movie = Movie.objects.get(movie_id=movie_id)
            except Movie.DoesNotExist:
                # If the Movie doesn't exist, create it
                movie = Movie(movie_id=movie_id)
                movie.save()

            
            # Create a new review object
            review = Review(user=request.user,movie=movie, content=content)
            review.save()
            # rating = Rating(user=request.user,movie=movie,)
            create_or_update_user_profile(request.user)
            
            return Response({'message': 'Review created successfully'}, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

# class RateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Rating
#         fields = '__all__'



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def like_movie(request):
    if request.method == 'POST':
        data = request.data
        try:
            movie_id = data['movie_id']
            like_status = data.get('like', True)  # Default to True if 'like' is not provided

            try:
                movie = Movie.objects.get(movie_id=movie_id)
            except Movie.DoesNotExist:
                # return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
                 movie = Movie(movie_id=movie_id)
                 movie.save()

            # Check if the user has already liked/disliked the movie
            existing_like, created = Like.objects.get_or_create(user=request.user, movie=movie)
            existing_like.like = like_status

            existing_like.save()
            create_or_update_user_profile(request.user)

            return Response({'message': 'Movie liked/disliked successfully'}, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_like_status(request, movie_id):
    try:
        movie = Movie.objects.get(movie_id=movie_id)
        like = Like.objects.filter(user=request.user, movie=movie).first()
        is_liked = like is not None and like.like
        return Response({'isLiked': is_liked})
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def unlike_movie(request):
    if request.method == 'POST':
        data = request.data
        try:
            movie_id = data['movie_id']

            try:
                movie = Movie.objects.get(movie_id=movie_id)
            except Movie.DoesNotExist:
                return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

            # Check if the user has already liked/disliked the movie
            try:
                existing_like = Like.objects.get(user=request.user, movie=movie)
                existing_like.delete()  # Delete the like from the database
                return Response({'message': 'Movie unliked successfully'}, status=status.HTTP_200_OK)
            except Like.DoesNotExist:
                return Response({'error': 'You have not liked this movie'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def rate_movie(request):
    data = request.data

    try:
        movie_id = data['movie_id']
        # rate_status = data.get('stars', 0)
        stars  = data['stars']
        
        try:
            movie = Movie.objects.get(movie_id=movie_id)
        except Movie.DoesNotExist:
            # return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
                movie = Movie(movie_id=movie_id)
                movie.save()
        
            # Create a new review object
        # rate = Rating(user=request.user,movie=movie, stars=stars)
        # rate.save()
        # rating = Rating(user=request.user,movie=movie,)
        rating, created = Rating.objects.get_or_create(user=request.user, movie=movie)
        if stars is not None:
        
            rating.stars = stars
            rating.save()
        else:
            return Response({'error': 'Stars cannot be null'}, status=status.HTTP_400_BAD_REQUEST)




        
        create_or_update_user_profile(request.user)



        return Response({'message': 'Movie rated successfully'}, status=status.HTTP_201_CREATED)
    except KeyError:
        return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_review(request):
    if request.method == "POST":
        data = request.data

        try:
            content = data['content']
            review = data['review']

        except:
            pass


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

@api_view(['GET'])
def retreive_review(request):
        try: 
            reviews = Review.objects.all().order_by('-created_at')
            serialized_reviews = []

            for review in reviews:
                username = review.user.username
                serialized_review = ReviewSerializer(review).data
                serialized_review['user_username'] = username
                serialized_reviews.append(serialized_review)
            # serializer = ReviewSerializer(reviews,many=True)
            # return Response({"reviews":serializer.data})
            return Response({"reviews":serialized_reviews})
        except:
            return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['GET'])
def get_comments_for_review(request, review_id):
    comments = Comment.objects.filter(review=review_id)
    serialized_comments = []
    for comment in comments:
        username = comment.user.username
        serialized_comment = CommentSerializer(comment).data
        serialized_comment['user_username'] = username
        serialized_comments.append(serialized_comment)
    # serializer = CommentSerializer(comments, many=True)
    return Response(serialized_comments, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_review_object(request,id):
    try:
        # review = Review.objects.get(id=id)
        review = get_object_or_404(Review,id=id)
        
        serializer = ReviewSerializer(review)
        return Response({"review":serializer.data})
    except:
        return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'



@api_view(['GET'])
def get_comment_object(request,id):
    try:
        comment = get_object_or_404(Comment,id=id)

        serializer = CommentSerializer(comment)
        return Response({"comment":serializer.data})
    except:
        return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_comment(request):
    # serializer = CommentSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        data = request.data

        try:
            content = data['content']
            review = data['review']

            review_instance = Review.objects.get(id=int(review))


            comment = Comment(user=request.user,review=review_instance,content=content)
            comment.save()
            create_or_update_user_profile(request.user)
            return Response({'message': 'Commment made successfully'}, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




# @api_view(['GET'])
# def get_comments(request, review_id):
#     comments = Comment.objects.filter(review=review_id)
#     serializer = CommentSerializer(comments, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def delete_rating(request):
#     if request.method == 'POST':
#         data = request.data

#         try:
#             movie_id = data['movie_id']
#             # rate_status = data.get('stars', 0)
#             stars  = data['stars']
           
#             try:
#                 movie = Movie.objects.get(movie_id=movie_id)
#             except Movie.DoesNotExist:
#                 return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#                 #  movie = Movie(movie_id=movie_id)
#                 #  movie.save()
            
#             try:

#                 existing_rating = Rating.objects.get(user=request.user, movie=movie, stars=stars)           
#                 existing_rating.delete()
#                 create_or_update_user_profile(request.user)

            
#                 return Response({'message': 'Movie unrated successfully'}, status=status.HTTP_200_OK)
#             except Rating.DoesNotExist:
#                 return Response({'error': 'You have not liked this movie'}, status=status.HTTP_400_BAD_REQUEST)

        
#         except KeyError:
#             return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)