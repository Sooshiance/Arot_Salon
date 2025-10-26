from django.urls import path

from .views import post_list, post_item, create_comment_post, create_comment_service


app_name = "blog"

urlpatterns = [
    path("post/", post_list, name="post_list"),
    path("post/<int:pk>/", post_item, name="post"),
    path(
        "post/comment/<int:pk>/",
        create_comment_post,
        name="create_comment_post",
    ),
    path(
        "post/service/<int:pk>/",
        create_comment_service,
        name="create_comment_service",
    ),
]
