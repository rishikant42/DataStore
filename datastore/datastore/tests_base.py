import random
import string
import uuid

from store.models import User, Form
from django.test import Client, TestCase


class DataStoreTestCaseBase(TestCase):
    def create_random_text(self, length=8):
        return "".join(random.choices(
            string.ascii_letters + string.digits, k=length)
        )

    def create_random_number(self, length=8):
        return "".join(random.choices(string.digits[1:], k=length))

    def create_random_email(self):
        return (
            "".join(random.choices(string.ascii_letters + string.digits, k=6))
            + "@gmail.com"
        )

    def create_random_uid(self):
        return str(uuid.uuid4())

    def create_random_bool_value(self):
        return random.choice([True, False])

    def create_user(self, name=None, email=None):
        if name is None:
            name = self.create_random_text()

        if email is None:
            email = self.create_random_email()

        return User.objects.create(
            name=name,
            email=email,
        )

    def create_form(self, user_id=None, name=None):
        if user_id is None:
            user_id = self.create_user().id

        if name is None:
            name = self.create_random_text()

        return Form.objects.create(
            user_id=user_id,
            name=name,
        )

    def setUp(self):
        self.client = Client()
