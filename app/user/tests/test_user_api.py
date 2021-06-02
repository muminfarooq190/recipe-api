from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
CREATE_TOKEN = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """test the users api (public)"""
    def setUp(self):
        self.client = APIClient()

    def test_creat_valid_user_success(self):
        """Test Creating user with valid payload is successfull"""
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """tests that user already exists"""
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test', }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test password must be more tha 5 characters"""
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'pw',
            'name': 'Test', }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """Test that a token is created for a user"""
        payload = {'email': 'testapp@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(CREATE_TOKEN, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created when invalid credentials given"""
        create_user(email='testapp@londonappdev.com', password='testpass')
        payload = {'email': 'testapp@londonappdev.com', 'password': 'wrong'}
        res = self.client.post(CREATE_TOKEN, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created when no user"""
        payload = {'email': 'testapp@londonappdev.com', 'password': 'testpass'}
        res = self.client.post(CREATE_TOKEN, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that token is not created when password or email is missing"""
        payload = {'email': 'testapp@londonappdev.com', 'password': ''}
        res = self.client.post(CREATE_TOKEN, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
