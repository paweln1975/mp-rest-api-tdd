from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Tag, Ingredient, Recipe, recipe_image_file_path
from unittest.mock import patch


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
        tag = Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        ingredient = Ingredient.objects.create(
            user=sample_user(),
            name='Butter'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        recipe = Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushrooms',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_filename_uuid(self, mock_uuid):
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)
