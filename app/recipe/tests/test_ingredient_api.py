from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Ingredient, Recipe
from ..serializers import IngredientSerializer
from decimal import Decimal

INGREDIENTS_URL = reverse('recipe:ingredient-list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def sample_recipe(user, **params):
    defaults = {
        'title': 'Cheese and Chips',
        'time_minutes': 10,
        'price': Decimal('1.51')
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)


class PublicAPIIngredientTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAPIIngredientTests(TestCase):

    def setUp(self) -> None:
        self.user = create_user(
            email='test@test.com',
            name='test name',
            password='testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_ingredients(self):
        Ingredient.objects.create(user=self.user, name='Onion')
        Ingredient.objects.create(user=self.user, name='Tomato')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        user2 = create_user(
            email='test2@test.com',
            name='test name 2',
            password='testpass 2'
        )
        Ingredient.objects.create(user=user2, name='Onion')
        ingredient = Ingredient.objects.create(user=self.user, name="Tomato")

        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_success(self):
        payload = {
            'name': 'Cabbage'
        }
        self.client.post(INGREDIENTS_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_failure(self):
        payload = {
            'name': ''
        }
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_ingredients_assigned_to_recipes(self):
        ingredient1 = Ingredient.objects.create(user=self.user, name="Onion")
        ingredient2 = Ingredient.objects.create(user=self.user, name="Carrot")
        recipe = sample_recipe(user=self.user)
        recipe.ingredients.add(ingredient1)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_get_ingredients_assigned_unique(self):
        ingredient = Ingredient.objects.create(user=self.user, name="Apple")
        Ingredient.objects.create(user=self.user, name="Pinch")
        recipe1 = sample_recipe(user=self.user)
        recipe1.ingredients.add(ingredient)
        recipe2 = sample_recipe(user=self.user, title="Pancakes")
        recipe2.ingredients.add(ingredient)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)
