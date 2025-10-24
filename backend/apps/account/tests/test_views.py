import random

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import RequestFactory, Client

from faker import Faker


User = get_user_model()


class TestLogin(TestCase):
    def setUp(self):
        self.english_faker = Faker(locale="en-US")

        self.client = Client()
        self.request_factory = RequestFactory()

        self.password = self.english_faker.password(length=10)
        self.user_data = {
            "email": self.english_faker.email(safe=True),
            "phone": f"09123{random.randint(a=1, b=999999)}",
            "password": self.password,
            "username": self.english_faker.user_name(),
        }

        self.user = User.objects.create_user(
            **self.user_data,
        )

        self.login_url = reverse("account:login")

    def test_login_success(self) -> None:
        """"""

        response = self.client.post(
            self.login_url,
            data={
                "phone": self.user_data["phone"],
                "password": self.password,
            },
        )

        self.assertEqual(response.status_code, 302)

    def test_login_failed(self) -> None:
        """"""

        response = self.client.post(
            self.login_url,
            data={
                "phone": self.user_data["phone"],
                "password": f"{self.password}1",
            },
        )

        self.assertEqual(response.status_code, 401)

        messages = list(response.context["messages"])

        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "مشخصات وارد شده اشتباه می باشد، دوباره تلاش کنید"
        )
