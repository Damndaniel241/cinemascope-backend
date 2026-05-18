from .views import (
    create_review,
    get_review,
    delete_review,
    update_review,
    rate_movie,
    watch_movie,
    like_movie,
    add_to_watchlist,
    get_movie_user_data,
    comment_review,
    retreive_plat_movie_data,
    test_user_movie_data,
    like_review,
    get_review_user_data,
    edit_comment_review,
    delete_comment_review,
)

from django.urls import path

urlpatterns = [
    path("create/", create_review, name="create-review"),
    path("get/<int:pk>", get_review, name="get-review"),
    path("delete/<int:pk>", delete_review, name="delete-review"),
    path("update/<int:pk>", update_review, name="update-review"),
    path("rate/", rate_movie, name="rate-movie"),
    path("watch/", watch_movie, name="watch-movie"),
    path("like/", like_movie, name="like-movie"),
    path("add-to-watchlist/", add_to_watchlist, name="watchlist-movie"),
    path("movie-user-data/", get_movie_user_data, name="get-movie-user-data"),
    path("review-user-data/", get_review_user_data, name="get-review-user-data"),
    path("comment-review/", comment_review, name="create-review-comment"),
    path("comment-review/<int:pk>", edit_comment_review, name="edit-review-comment"),
    path(
        "comment-review/delete/<int:pk>",
        delete_comment_review,
        name="delete-review-comment",
    ),
    path("like-review/", like_review, name="like-review"),
    path("retrieve-plat-movie-data/", retreive_plat_movie_data, name="movie-activity"),
    path("blackman/", test_user_movie_data),
]
