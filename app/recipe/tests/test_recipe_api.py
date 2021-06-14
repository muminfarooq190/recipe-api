from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredients, Tag
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPE_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """Create a sample recipe and return it"""
    defaults = {
        'title': 'Sample Recipe',
        'time_minutes': 10,
        'price': 10.00
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)


def sample_tag(user, name='Main Course'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Cinammon'):
    """Create and return a sample ingrdeient"""
    return Ingredients.objects.create(user=user, name=name)


def detail_url(recipe_id):
    """Return the url for specific recipe"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


class PublicRecipeApi(TestCase):
    """Test Unauthenticated Recipe Access"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to access recipe"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApi(TestCase):
    """Test Authorised Reicpe Access"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'test123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe(self):
        """Test retrieving recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipe = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipe, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_recipe_for_limited_user(self):
        """Test retrieve recipe for authenticated user only"""

        user_two = get_user_model().objects.create_user(
            'another@appdev.com',
            'another123'
        )
        recipe = sample_recipe(user=self.user)
        sample_recipe(user=user_two)

        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], recipe.title)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
