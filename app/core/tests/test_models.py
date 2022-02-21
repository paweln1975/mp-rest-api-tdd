from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email(self):
        email = "test@test.com"
        p = "838928"
        user = get_user_model().objects.create_user(
            email=email,
            password=p
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(p))

    def test_email_normalized(self):
        email = "test@TEST.COM"
        p = "88383883s"
        user = get_user_model().objects.create_user(
            email=email,
            password=p
        )
        self.assertEqual(user.email, email.lower())
