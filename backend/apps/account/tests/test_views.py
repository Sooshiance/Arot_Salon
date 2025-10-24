import random

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import RequestFactory, Client

from faker import Faker


User = get_user_model()


class TestBaseAccount(TestCase):
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


class TestLogin(TestBaseAccount):
    def setUp(self):
        super().setUp()

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


class TestLogout(TestBaseAccount):
    def setUp(self) -> None:
        super().setUp()

        self.logout_url = reverse("account:logout")

    def test_logout(self) -> None:
        """"""

        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, 302)


class TestRegister(TestBaseAccount):
    def setUp(self) -> None:
        super().setUp()

        self.register_url = reverse("account:register")

        self.user_password = self.english_faker.password(15)

    # FIXME: {'errors': dict_items([('phone', ['Phone is not an iranian phone number'])])
    def test_create_user_success(self) -> None:
        # Generate a valid 7-digit number for the phone suffix
        phone_suffix = str(random.randint(1000000, 9999999))

        user_data = {
            "email": self.english_faker.email(),
            "phone": f"0912{phone_suffix}",
            "password": self.user_password,
            "password1": self.user_password,
            "password2": self.user_password,
            "username": self.english_faker.texts(nb_texts=9),
            "first_name": self.english_faker.name(),
            "last_name": self.english_faker.name(),
        }

        response = self.client.post(
            self.register_url,
            data={**user_data},
        )

        print(response.context)


    def test_create_user_fail(self) -> None:
        """Test that registration fails when using existing unique field values."""

        # Test cases for each unique field
        test_cases = [
            {
                "name": "duplicate_email",
                "data": {
                    "email": self.user_data["email"],  # Use existing email
                    "phone": f"09123{random.randint(a=1, b=999999)}",  # New phone
                    "password": self.english_faker.password(15),
                    "username": self.english_faker.user_name(),  # New username
                },
                "field": "email",
            },
            {
                "name": "duplicate_phone",
                "data": {
                    "email": self.english_faker.email(safe=True),  # New email
                    "phone": self.user_data["phone"],  # Use existing phone
                    "password": self.english_faker.password(15),
                    "username": self.english_faker.user_name(),  # New username
                },
                "field": "phone",
            },
            {
                "name": "duplicate_username",
                "data": {
                    "email": self.english_faker.email(safe=True),  # New email
                    "phone": f"09123{random.randint(a=1, b=999999)}",  # New phone
                    "password": self.english_faker.password(15),
                    "username": self.user_data["username"],  # Use existing username
                },
                "field": "username",
            },
        ]

        for test_case in test_cases:
            with self.subTest(test_case["name"]):
                response = self.client.post(
                    self.register_url,
                    data=test_case["data"],
                )

                # Registration should fail (not redirect)
                self.assertEqual(response.status_code, 401)
