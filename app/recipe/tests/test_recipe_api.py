from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Recipe
from ..serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def sample_recipe(user, **params):
    defaults = {
        'title': 'Cheese and Chips',
        'time_minutes': 10,
        'price': 5.2
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)


class PublicAPIRecipesTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAPIRecipesTests(TestCase):

    def setUp(self) -> None:
        self.user = create_user(
            email='test@test.com',
            name='test name',
            password='testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_recipes(self):
        sample_recipe(user=self.user)
        sample_recipe(user=self.user, title="Fried Pork with Vegetables")

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by("-title")
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipes_limited_to_user(self):
        user2 = create_user(
            email='test2@test.com',
            name='test name 2',
            password='testpass 2'
        )
        sample_recipe(user=user2)
        recipe = sample_recipe(user=self.user, title='Eggs and Bacon')

        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], recipe.title)
