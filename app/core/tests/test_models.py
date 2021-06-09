from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@londonappdev.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """Test creating a new user with email successfull"""
        email = "muminfarooq586@gmail.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
                email=email,
                password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email(self):
        """Test to normalize_email for a new user """
        email = "test@LONDONAPPDEV.COM"
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Tests email of a new user """
        email = None
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email, 'test133')

    def test_create_superuser(self):
        email = "muminfarooq586@gmail.com"
        password = "test123"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password(password))

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredients.objects.create(
            user=sample_user(),
            name='Cucumber'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and Mushroom sauce',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)
