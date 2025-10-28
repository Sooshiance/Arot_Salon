import random

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from faker import Faker

from apps.blog.models import Post, Comment, ServiceComment
from apps.service.models import Service

User = get_user_model()


class BaseTestBlog(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.english_faker = Faker(locale="en-US")
        self.password = self.english_faker.password(15)

        self.client = Client()

        self.user_data = {
            "phone": f"09123{random.randint(a=1, b=999999)}",
            "email": self.english_faker.email(),
            "username": self.english_faker.name(),
            "password": self.password,
        }

        self.user = User.objects.create_user(**self.user_data)

        self.word_list = ["Gel", "Massage"]

        self.post = Post.objects.create(
            title=self.english_faker.word(),
            txt=self.english_faker.text(max_nb_chars=10),
        )

        self.service = Service.objects.create(
            title=self.english_faker.word(ext_word_list=self.word_list),
        )

        self.service_comment = ServiceComment.objects.create(
            user=self.user,
            service=self.service,
            txt=self.english_faker.text(max_nb_chars=10),
            vote=random.randint(a=1, b=10),
            is_public=True,
        )


class TestPost(BaseTestBlog):
    def setUp(self) -> None:
        super().setUp()

        self.post = Post.objects.create(
            title=self.english_faker.word(),
            txt=self.english_faker.text(max_nb_chars=10),
        )

        self.post_list_url = reverse("blog:post_list")
        self.post_url = reverse(
            "blog:post",
            kwargs={"pk": self.post.pk},
        )

    def test_post_list(self) -> None:
        """"""

        response = self.client.get(self.post_list_url)

        self.assertEqual(response.status_code, 200)

    def test_post(self) -> None:
        """"""

        response = self.client.get(self.post_url)

        self.assertEqual(response.status_code, 200)


class TestComment(BaseTestBlog):
    def setUp(self) -> None:
        super().setUp()

        self.post = Post.objects.create(
            title=self.english_faker.word(),
            txt=self.english_faker.text(max_nb_chars=10),
        )

        self.comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            txt=self.english_faker.text(max_nb_chars=5),
            is_public=True,
        )

        self.post_url = reverse(
            "blog:post",
            kwargs={"pk": self.post.pk},
        )
        self.create_comment_post_url = reverse(
            "blog:create_comment_post",
            kwargs={"pk": self.post.pk},
        )

    def test_comment_post_list(self) -> None:
        """"""

        response = self.client.get(self.post_url)

        self.assertEqual(response.status_code, 200)

    def test_create_comment_on_post(self) -> None:
        """"""

        self.client.force_login(self.user)

        response = self.client.post(
            self.create_comment_post_url,
            data={
                "txt": self.english_faker.text(5),
            },
        )

        self.assertEqual(response.status_code, 302)
