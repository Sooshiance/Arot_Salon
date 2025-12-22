import random
from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from faker import Faker

from apps.booking.models import Schedule
from apps.service.models import Service

User = get_user_model()


class BaseReservationTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.english_faker = Faker(locale="en-US")

        self.user_reserve_service_url = reverse("booking:user_reserve_service_url")

        self.john_doe = User.objects.create_user(
            email=self.english_faker.safe_email(),
            username=self.english_faker.text(15),
            phone=f"091{random.randint(a=10000000, b=99999999)}",
            password=self.english_faker.password(length=15),
        )
        self.mary_ray = User.objects.create_user(
            email=self.english_faker.safe_email(),
            username=self.english_faker.text(15),
            phone=f"091{random.randint(a=10000000, b=99999999)}",
            password=self.english_faker.password(length=15),
        )
        self.roy_phil = User.objects.create_user(
            email=self.english_faker.safe_email(),
            username=self.english_faker.text(15),
            phone=f"091{random.randint(a=10000000, b=99999999)}",
            password=self.english_faker.password(length=15),
        )

        self.service = Service.objects.create(
            title=self.english_faker.texts(10),
        )

        self.schedule = Schedule.objects.create(
            service=self.service,
            date=datetime(2026, 12, 12),
            capacity=2,
        )

    def test_reserve_success(self):
        """Test successful reservation with date selection"""
        self.client.force_login(self.john_doe)

        # Post the date, not the schedule ID
        resp = self.client.post(
            self.user_reserve_service_url,
            data={"date": "2026-12-12"},  # Use string format for date input
        )
        self.assertEqual(resp.status_code, 302)
        print("\n", Schedule.objects.get(pk=self.schedule.pk).capacity)
        # updated_schedule = Schedule.objects.get(pk=self.schedule.pk)
        # self.assertEqual(updated_schedule.capacity, 1)
