from django.conf import settings
from django.db import models

from apps.service.models import Service

from .managers import PublicCommentManager, PublicServiceCommentManager

User = settings.AUTH_USER_MODEL


class Post(models.Model):
    """"""

    title = models.CharField(max_length=255)
    txt = models.CharField(max_length=512)

    objects = models.Manager()

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    txt = models.CharField(max_length=512)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    publication = PublicCommentManager()

    def __str__(self) -> str:
        return f"{self.user}->{self.post} wrote {self.txt[:15]}"

    class Meta:
        ordering = ["-created_at"]


class ServiceComment(models.Model):
    """"""

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    txt = models.CharField(max_length=512)
    vote = models.PositiveSmallIntegerField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    publication = PublicServiceCommentManager()

    class Meta:
        verbose_name = "Service Comment"
        verbose_name_plural = "Service Comments"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.service} - {self.user}: {self.txt}"
