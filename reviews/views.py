from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .serializers import (
    ReviewSerializer,
    RatingSerializer,
    WatchSerializer,
    LikeSerializer,
    WatchListSerializer,
    MovieSerializer,
    ReviewCommentSerializer,
    UserMovieDataSerializer,
    ReviewLikeSerializer,
)
from users.models import User
from .models import Review, Movie, Rating, Watch, WatchList, Like
from django.db.models import Q
from .review_comment import ReviewComment
from .review_like import ReviewLike
from rest_framework.generics import get_object_or_404
from django.http import Http404
from reviews.decorators import owns_resource_only


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review(request):
    try:
        movie_id = request.data["movie"]
        user = request.user
        # request.data['user'] = user
        try:
            movie_obj = Movie.objects.get(movie_id=movie_id)
            # print("movie_obj = ",movie_obj)
        except Movie.DoesNotExist:
            # print("movie does not exist")
            movie_obj = Movie.objects.create(movie_id=movie_id)
            # movie_obj.save()

        print("request.data = ", request.data)
        serializer = ReviewSerializer(data=request.data)
        print("serializer = ", serializer)
        if serializer.is_valid(raise_exception=True):
            print("i got here")
            if Watch.objects.filter(movie=movie_obj, user=request.user) is None:
                Watch.objects.create(movie=movie_obj, user=request.user)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
# @permission_classes([AllowAny])
def get_review(request, pk):
    try:
        try:
            review_obj = Review.objects.filter(pk=pk).first()
        except Review.DoesNotExist:
            pass
        serializer = ReviewSerializer(review_obj)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_review(request, pk):
    try:
        review_obj = Review.objects.filter(pk=pk).first()
        # print("review_obj = ",review_obj)

        if review_obj:

            serializer = ReviewSerializer(review_obj, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {"message": "review updated successfully", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@owns_resource_only(Review)
def delete_review(request, pk):
    try:
        try:
            review_obj = Review.objects.filter(pk=pk).first()
            if review_obj:
                review_obj.delete()
                return Response(
                    {"message": "review deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )
        except Review.DoesNotExist:
            return Response(
                {"message": "object doesn't exist"}, status=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rate_movie(request):

    # print("this has been seen")
    try:
        # print("also seen 1")

        movie_obj, created = Movie.objects.get_or_create(movie_id=request.data["movie"])

        # print("also seen 3, movie_obj= ", movie_obj)

        print("type of request data", type(request.data["stars"]))

        existing_rating_obj = Rating.objects.filter(
            movie=movie_obj, user=request.user
        ).first()
        # print("rating_obj pleaasseee = ",existing_rating_obj)
        if existing_rating_obj:
            if request.data["stars"] == "0":
                existing_rating_obj.delete()
                return Response(
                    {"message": "zero rating, object deleted"},
                    status=status.HTTP_200_OK,
                )
            else:
                serializer = RatingSerializer(existing_rating_obj, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(
                        {
                            "message": "movie rating updated successfully",
                            "data": serializer.data,
                        },
                        status=status.HTTP_200_OK,
                    )
        elif request.data["stars"] == "0":
            return Response(
                {"message": "you cannot make a rating of zero"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:

            print("also seen 4")
            serializer = RatingSerializer(data=request.data)
            Watch.objects.create(movie=movie_obj, user=request.user)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(
                    {"message": "movie rated successfully", "data": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
    except KeyError:
        return Response(
            {"error": "movie field is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def watch_movie(request):
    try:
        # try:
        #     movie_obj = Movie.objects.get(movie_id=request.data["movie"])
        # except Movie.DoesNotExist:
        #     movie_obj = Movie.objects.create(movie_id = request.data["movie"])

        movie_obj, _ = Movie.objects.get_or_create(movie_id=request.data["movie"])

        existing_watch = Watch.objects.filter(
            user=request.user, movie=movie_obj
        ).first()

        if existing_watch:
            existing_watch.delete()
            return Response(
                {"message": "you have unwatched this movie"}, status=status.HTTP_200_OK
            )
        else:
            watch = Watch.objects.create(movie=movie_obj, user=request.user)
            serializer = WatchSerializer(watch)
            return Response(
                {"message": "you have watched this movie", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        # also works
        # serializer = WatchSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save(user=request.user)
        #     return Response({"message":"you have watched this movie","data":serializer.data},status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_movie(request):
    try:
        movie_obj, _ = Movie.objects.get_or_create(movie_id=request.data["movie"])

        print("did movie object show =", movie_obj)

        existing_like = Like.objects.filter(user=request.user, movie=movie_obj).first()
        print("did existing like show =", existing_like)

        if existing_like:
            existing_like.delete()
            return Response(
                {"message": "you have unliked this movie"}, status=status.HTTP_200_OK
            )
        else:
            print("did i get here =")
            like = Like.objects.create(user=request.user, movie=movie_obj)
            serializer = LikeSerializer(like)
            return Response(
                {"message": "you have liked this movie", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        # also works
        # serializer = WatchSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save(user=request.user)
        #     return Response({"message":"you have liked this movie","data":serializer.data},status=status.HTTP_201_CREATED)

    except KeyError:
        return Response(
            {"error": "movie field is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_watchlist(request):
    try:
        movie_obj, created = Movie.objects.get_or_create(movie_id=request.data["movie"])

        prev_added = WatchList.objects.filter(
            user=request.user, movie=movie_obj
        ).first()
        if prev_added:
            prev_added.delete()
            return Response(
                {"message": "movie removed from watch list"}, status=status.HTTP_200_OK
            )
        else:
            serializer = WatchListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(
                    {"message": "movie added to watchlist", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_movie_user_data(request):
    try:
        movie_obj, _ = Movie.objects.get_or_create(
            movie_id=request.query_params.get("movie")
        )

        review_obj = Review.objects.filter(user=request.user, movie=movie_obj)
        rating_obj = Rating.objects.filter(user=request.user, movie=movie_obj).first()
        watch_obj = Watch.objects.filter(user=request.user, movie=movie_obj).first()
        watch_list_obj = WatchList.objects.filter(
            user=request.user, movie=movie_obj
        ).first()
        like_obj = Like.objects.filter(user=request.user, movie=movie_obj).first()

        review_obj_serializer = ReviewSerializer(review_obj, many=True)
        rating_obj_serializer = RatingSerializer(rating_obj)
        watch_obj_serializer = WatchSerializer(watch_obj)
        watch_list_obj_serializer = WatchListSerializer(watch_list_obj)
        like_obj_serializer = LikeSerializer(like_obj)

        # review_data = dict(review_obj_serializer.data)
        # review_data["comments"] = ReviewCommentSerializer(ReviewComment.objects.filter(review=36).all(),many=True).data

        return Response(
            {
                "data": {
                    "review": review_obj_serializer.data,
                    "watched": watch_obj_serializer.data,
                    "liked": like_obj_serializer.data,
                    "added_to_watchlist": watch_list_obj_serializer.data,
                    "rating": rating_obj_serializer.data,
                }
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_review_user_data(request):
    try:
        review_obj = get_object_or_404(Review, id=request.query_params.get("review_id"))
        print("did you get my object = ", review_obj.pk)
        if review_obj:
            review_like_obj = ReviewLike.objects.filter(
                review=review_obj.pk, user=request.user
            ).first()
            print("did you get my review like object = ", review_like_obj)
            serializer = ReviewLikeSerializer(review_like_obj)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        # return Response({"error":serializer.errors})

    except Http404:
        # Explicitly capture the 404 error and return a 404 status code
        return Response(
            {"error": "No Review matches the given query."},
            status=status.HTTP_404_NOT_FOUND,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def comment_review(request):
    try:
        review_id = request.data["review"]
        try:
            review_obj = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response(
                {"message": "resource not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReviewCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {
                    "message": "you have commented on this review",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_comment_review(request, pk):
    try:
        existing_comment_obj = ReviewComment.objects.filter(pk=pk).first()
        serializer = ReviewCommentSerializer(
            existing_comment_obj,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(
                {"message": "comment updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
    except ReviewComment.DoesNotExist:
        return Response(
            {"message": "resource not found"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@owns_resource_only(ReviewComment)
def delete_comment_review(request, pk):
    try:
        try:
            comment_obj = ReviewComment.objects.filter(pk=pk).first()
            if comment_obj:
                comment_obj.delete()
            return Response(
                {"message": "review comment deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Review.DoesNotExist:
            return Response(
                {"message": "object doesn't exist"}, status=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_review(request):
    try:
        review_id = request.data["review"]
        review_obj = Review.objects.get(id=review_id)
        existing_review_like = ReviewLike.objects.filter(
            review=review_obj, user=request.user
        ).first()
        if existing_review_like:
            existing_review_like.delete()
            return Response(
                {"message": "you have unliked this review"}, status=status.HTTP_200_OK
            )
        else:
            # new_review_like = ReviewLike.objects.create(user=request.user,review=review_obj)
            # print("nigga i got here",new_review_like)
            serializer = ReviewLikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(
                    {"message": "you have liked this review"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {
                    "message": "something wromg liking this review",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def retreive_plat_movie_data(request):
    try:
        movie_obj, _ = Movie.objects.get_or_create(
            movie_id=request.query_params.get("movie")
        )
        # review_objs = Review.objects.filter(movie=movie_obj).all()
        print("i reached here")

        # review_obj_serializer = PlatformMovieDataSerializer(movie_obj,many=True)
        review_obj_serializer = MovieSerializer(movie_obj)
        print("i reached here 2")

        return Response(
            {
                "data": {
                    "reviews": review_obj_serializer.data,
                }
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def test_user_movie_data(request):
    try:
        movie_obj = Movie.objects.get(movie_id=request.query_params.get("movie"))

        # review_obj_serializer = UserMovieDataSerializer(movie_obj)
        # return Response({
        #             "data": {
        #                 "reviews":review_obj_serializer.data,
        #                 }},
        #         status=status.HTTP_200_OK
        #         )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
