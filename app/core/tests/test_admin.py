from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_super_user(
            email='muminfarooq586@gmail.com',
            password='testpass123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test1234@gmail.com',
            password='test123',
            name='test full name'
        )

    def test_users_listed(self):
        """Test that users are listed on the user page"""
        url = reverse('admin:core_myuser_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_page_change(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_myuser_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_page_add(self):
        """Test that new user can be added"""
        url = reverse('admin:core_myuser_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
