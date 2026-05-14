# from django.http import HttpResponse
# from functools import wraps
# from .review_comment import ReviewComment
# from reviews.models import Review
# from rest_framework.response import Response
# from rest_framework import status

# def userCanDeleteReviewComment(user,obj):
#     if user.pk == obj.user.pk:
#         return True
#     return False


# def userDeleteCommentAccessOnly():
#     def decorator(view):
#         @wraps(view)
#         def _wrapped_view(request, *args, **kwargs):
#             review_comment_id = kwargs.get('pk') 
#             review_comment_obj = ReviewComment.objects.filter(pk=review_comment_id).first()
#             if review_comment_obj:
#                 if not userCanDeleteReviewComment(request.user,review_comment_obj):
#                     return Response({"message":"you are not authorized to delete this resource"},status=status.HTTP_401_UNAUTHORIZED)
#             return view(request, *args, **kwargs)
#         return _wrapped_view
#     return decorator

# def userCanDeleteReview(user,obj):
#     if user.pk == obj.user.pk:
#         return True
#     return False


# def userDeleteReviewAccessOnly():
#     def decorator(view):
#         @wraps(view)
#         def _wrapped_view(request, *args, **kwargs):
#             review_id = kwargs.get('pk') 
#             review_obj = Review.objects.filter(pk=review_id).first()
#             if review_obj:
#                 if not userCanDeleteReviewComment(request.user,review_obj):
#                     return Response({"message":"you are not authorized to delete this resource"},status=status.HTTP_401_UNAUTHORIZED)
#             return view(request, *args, **kwargs)
#         return _wrapped_view
#     return decorator


from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def owns_resource_only(model_class):
    """
    A generic decorator to check if the request user owns the resource.
    Works for any model that has a 'user' foreign key.
    """
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            # 1. Get the ID from the URL (usually 'pk')
            resource_id = kwargs.get('pk')
            
            # 2. Fetch the object using the model class passed in
            obj = model_class.objects.filter(pk=resource_id).first()
            
            # 3. Perform the ownership check
            if obj:
                if obj.user.pk != request.user.pk:
                    return Response(
                        {"message": "You are not authorized to access this resource"},
                        status=status.HTTP_403_FORBIDDEN # Use 403 for Permission issues
                    )
            
            # 4. If object doesn't exist, we let the view handle the 404
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator