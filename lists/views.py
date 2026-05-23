from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .serializers import ListSerializer,ListCommentSerializer,ListLikeSerializer
from .models import List,ListLike,ListComment
from reviews.decorators import owns_resource_only
# Create your views here.



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_list(request):
    try:
        # data = request.data
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message":"you have created a list","data":serializer.data},status=status.HTTP_201_CREATED)
        return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        


    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_list(request):
    try:
        list_id = request.data["list"]
        list_obj = List.objects.get(id=list_id)
        existing_list_like = ListLike.objects.filter(
            list=list_obj, user=request.user
        ).first()
        if existing_list_like:
            existing_list_like.delete()
            return Response(
                {"message": "you have unliked this List"}, status=status.HTTP_200_OK
            )
        else:
            # new_List_like = ListLike.objects.create(user=request.user,List=List_obj)
            # print("nigga i got here",new_List_like)
            serializer = ListLikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(
                    {"message": "you have liked this List"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {
                    "message": "something wromg liking this List",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def comment_list(request):
    try:
        list_id = request.data["list"]
        try:
            list_obj = List.objects.get(id=list_id)
        except List.DoesNotExist:
            return Response(
                {"message": "resource not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ListCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {
                    "message": "you have commented on this list",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_comment_list(request, pk):
    try:
        existing_comment_obj = ListComment.objects.filter(pk=pk).first()
        serializer = ListCommentSerializer(
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
    except ListComment.DoesNotExist:
        return Response(
            {"message": "resource not found"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@owns_resource_only(ListComment)
def delete_comment_list(request, pk):
    try:
        try:
            comment_obj = ListComment.objects.filter(pk=pk).first()
            if comment_obj:
                comment_obj.delete()
            return Response(
                {"message": "list comment deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except List.DoesNotExist:
            return Response(
                {"message": "object doesn't exist"}, status=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
