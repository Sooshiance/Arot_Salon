from django import forms

from apps.blog.models import Comment, ServiceComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("txt",)


class ServiceCommentForm(forms.ModelForm):
    class Meta:
        model = ServiceComment
        fields = ("txt", "vote")
