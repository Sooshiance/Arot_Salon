# TODO: Need multiple users for `race condition` situation
import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Faker

User = get_user_model()


class BaseReservationTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.english_faker = Faker(locale="en-US")

        self.user_data = {
            "email": self.english_faker.safe_email(),
            "username": f"{self.english_faker.user_name()}_{random.randint(1, 10000)}",
            "phone": f"091{random.randint(1_0000_000, 99_999_999)}",
        }

        self.john_doe = User.objects.create_user(**self.user_data)
        self.mary_ray = User.objects.create_user(**self.user_data)
        self.roy_phil = User.objects.create_user(**self.user_data)
