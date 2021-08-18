import random

from django.utils import timezone
from faker import Faker
from typing import List
from uuid import uuid4

from home.models import Account, DailyWalk, Device, IntentionalWalk


class AccountGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate(self, n: int, **kwargs):
        for _ in range(n):
            params = {**self.random_params(), **kwargs}
            yield Account.objects.create(**params)

    def random_params(self):
        return dict(
            email=self.fake.email(),
            name=self.fake.name(),
            zip=self.fake["en-US"].postcode(),
            age=random.randint(10, 100),
        )


class DeviceGenerator:
    def __init__(self, accounts: List[Account]):
        if not accounts:
            raise InputError("Must provide a non-empty list of accounts")
        self.accounts = accounts

    def generate(self, n: int, **kwargs):
        for _ in range(n):
            params = {**self.random_params(), **kwargs}
            yield Device.objects.create(**params)

    def random_params(self):
        return dict(
            device_id=uuid4(),
            account=random.choice(self.accounts),
        )


class DailyWalkGenerator:
    # Requires a list of device ids
    def __init__(self, devices: List[str]):
        self.fake = Faker()
        if not devices:
            raise InputError("Must provide a non-empty list of device ids")
        self.devices = devices

    def generate(self, n: int, **kwargs):
        for _ in range(n):
            params = {**self.random_params(), **kwargs}
            yield DailyWalk.objects.create(**params)

    def random_params(self):
        return dict(
            date=self.fake.date(),
            steps=random.randint(100, 10000),
            distance=random.randint(100, 10000),  # up to 10 km
            device=random.choice(self.devices),
        )

class IntentionalWalkGenerator:
    # Requires a list of device ids
    def __init__(self, devices: List[str]):
        self.fake = Faker()
        if not devices:
            raise InputError("Must provide a non-empty list of device ids")
        self.devices = devices

    def generate(self, n: int, **kwargs):
        for _ in range(n):
            params = {**self.random_params(), **kwargs}
            yield IntentionalWalk.objects.create(**params)

    def random_params(self):
        tz = timezone.get_default_timezone()

        return dict(
            event_id="event_" + str(self.fake.unique.random_int()),
            start=tz.localize(self.fake.date_time()),
            end=tz.localize(self.fake.date_time()),
            steps=random.randint(10, 10000),
            pause_time=random.randint(10, 3600),  # up to 1 hour
            distance=random.randint(100, 10000),  # up to 10 km
            device=random.choice(self.devices),
        )
