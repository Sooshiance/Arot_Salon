from django.shortcuts import render, get_object_or_404, redirect
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.core.exceptions import FieldDoesNotExist

from apps.blog.models import Post, Comment, ServiceComment
from .forms import CommentForm, ServiceCommentForm
from apps.service.models import Service


def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.all()
    return render(
        request,
        "blog/post_list.html",
        {"posts": posts},
    )


def post_item(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        post = Post.objects.get(pk=pk)
    except FieldDoesNotExist as ex:
        raise str(ex)
    comments = Comment.publication.filter(post__exact=post)
    return render(
        request,
        "blog/post_item.html",
        {"post": post, "comments": comments},
    )


def create_comment_post(
    request: HttpRequest,
    pk: int,
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    try:
        post = Post.objects.get(pk=pk)
    except FieldDoesNotExist as ex:
        raise str(ex)
    if not request.user.is_authenticated:
        return redirect("account:login")
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            txt = form.cleaned_data["txt"]
            Comment.objects.create(
                post=post,
                user=request.user,
                txt=txt,
            ).save()
            return redirect("blog:post_list")
        else:
            return redirect("blog:post")
    else:
        form = CommentForm()
    return render(
        request,
        "blog/create_comment_post.html",
        {"form": form},
    )


def create_comment_service(
    request: HttpRequest,
    pk: int,
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    service = get_object_or_404(Service, pk)
    if not request.user.is_authenticated:
        return redirect("account:login")
    if request.method == "POST":
        form = ServiceCommentForm(request.POST)
        if form.is_valid():
            txt = form.cleaned_data["txt"]
            ServiceComment.objects.create(
                service=service,
                user=request.user,
                txt=txt,
            ).save()
            return redirect("service:home")
        else:
            return redirect("service:service")
    else:
        form = ServiceCommentForm()
    return render(
        request,
        "blog/create_comment_service.html",
        {"form": form},
    )
