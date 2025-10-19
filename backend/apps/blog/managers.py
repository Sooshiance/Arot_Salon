from django.db import models


class PublicCommentManager(models.Manager):
    """Manager to retrieve only public comments"""

    def get_queryset(self):
        return super().get_queryset().filter(is_public=True)


class PublicServiceCommentManager(models.Manager):
    """Manager to retrieve only public service comments"""

    def get_queryset(self):
        return super().get_queryset().filter(is_public=True)
