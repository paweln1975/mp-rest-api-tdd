from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@test.com', password='password'):
    return get_user_model().objects.create_user(email, password)


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

    def test_invalid_email_raises_error(self):
        with self.assertRaises(ValueError):
            p = "88383883s"
            get_user_model().objects.create_user(
                email=None,
                password=p
            )

    def test_create_superuser(self):
        email = "test@TEST.COM"
        p = "88383883s"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=p
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)
