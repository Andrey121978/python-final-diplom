from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from backend.models import User, Shop, Category
from backend.serializers import UserSerializer
import os
import django
from django.conf import settings
from backend.views import str_to_bool

if not settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.netology_pd_diplom.settings")
    django.setup()
# class UserViewTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username="testuser", password="testpassword", email="testuser@example.com")
#         self.client.force_authenticate(user=self.user)
#
#     # /'first_name', 'last_name', 'email', 'password', 'company', 'position'
#     def test_create_user(self):
#         """
#         Tests creating a new user.
#         """
#         # Get the initial count of users
#         initial_count = User.objects.count()
#
#         # Create a new user
#         response = self.client.post(reverse('backend:user-register'), {
#             'first_name': 'newuser1',
#             'last_name': 'newusers1',
#             'email': 'newuser@example.com',
#             'password': 'newPassword1',
#             'company': 'testcompany',
#             'position': 'tester',
#         })
#
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#
#         self.assertIn('id', response.data)
#         self.assertIn('email', response.data)
#
#         self.assertEqual(User.objects.count(), initial_count + 1)
#         self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

class RegisterAccountTests(TestCase):
    def test_register_valid_data(self):
        """
        Tests registering a new user with valid data.
        """
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'TestPassword123',
            'company': 'Test Company',
            'position': 'Tester',
        }
        response = self.client.post(reverse('backend:user-register'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())
        self.assertIn('email', response.json())

    def test_register_invalid_password(self):
        """
        Tests registering a new user with an invalid password.
        """
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'invalid',
            'company': 'Test Company',
            'position': 'Tester',
        }
        response = self.client.post(reverse('backend:user-register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Status'], False)
        self.assertIn('Errors', response.json())
        self.assertIn('password', response.json()['Errors'])

    def test_register_missing_arguments(self):
        """
        Tests registering a new user with missing arguments.
        """
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'TestPassword123',
            'company': 'Test Company',
        }
        response = self.client.post(reverse('backend:user-register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Status'], False)
        self.assertIn('Errors', response.json())
        self.assertEqual(response.json()['Errors'], 'Не указаны все необходимые аргументы')

    def test_register_duplicate_email(self):
        """
        Tests registering a new user with a duplicate email.
        """
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'TestPassword123',
            'company': 'Test Company',
            'position': 'Tester',
        }
        User.objects.create_user(email='testuser@example.com', password='TestPassword123')
        response = self.client.post(reverse('backend:user-register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Status'], False)
        self.assertIn('Errors', response.json())
        self.assertIn('email', response.json()['Errors'])



class AccountDetailsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            company='Test Company',
            position='Tester',
        )
        self.token = Token.objects.create(user=self.user)

    def test_get_account_details_authenticated(self):
        """
        Tests retrieving account details when authenticated.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('backend:user-details'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.json())
        self.assertIn('first_name', response.json())
        self.assertIn('last_name', response.json())
        self.assertIn('company', response.json())
        self.assertIn('position', response.json())

    def test_get_account_details_unauthenticated(self):
        """
        Tests retrieving account details when unauthenticated.
        """
        response = self.client.get(reverse('backend:user-details'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['Status'], False)
        self.assertIn('Error', response.json())

    def test_get_account_details_invalid_token(self):
        """
        Tests retrieving account details with an invalid token.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid-token')
        response = self.client.get(reverse('backend:user-details'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['detail'], 'Invalid token.')
class LoginAccountTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            company='Test Company',
            position='Tester',
            is_active=True,
        )
        self.token = Token.objects.create(user=self.user)

    def test_login_success(self):
        """
        Tests the login endpoint with valid credentials.
        """
        response = self.client.post(
            reverse('backend:user-login'),
            data={
                'email': 'testuser@example.com',
                'password': 'testpassword',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Status'], True)
        self.assertIn('Token', response.json())

    def test_login_invalid_credentials(self):
        """
        Tests the login endpoint with invalid credentials.
        """
        response = self.client.post(
            reverse('backend:user-login'),
            data={
                'email': 'testuser@example.com',
                'password': 'wrongpassword',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Status'], False)
        self.assertIn('Errors', response.json())

    def test_login_missing_arguments(self):
        """
        Tests the login endpoint with missing arguments.
        """
        response = self.client.post(
            reverse('backend:user-login'),
            data={
                'email': 'testuser@example.com',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Status'], False)
        self.assertIn('Errors', response.json())
# class ShopViewTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.shop = Shop.objects.create(name="Test Shop")
#
#     def test_get_shops(self):
#         """
#         Тестирует получение списка магазинов.
#         """
#         response = self.client.get(reverse('shop-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertContains(response, self.shop.name)
#
#     def test_create_shop(self):
#         """
#         Тестирует создание нового магазина.
#         """
#         response = self.client.post(reverse('shop-list'), {
#             'name': 'New Shop',
#         })
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Shop.objects.count(), 2)
#
#     def test_create_shop_without_name(self):
#         """
#         Тестирует создание магазина без имени.
#         """
#         response = self.client.post(reverse('shop-list'), {})
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('name', response.data)
#
#     def test_get_shop_details(self):
#         """
#         Тестирует получение детальной информации о магазине.
#         """
#         response = self.client.get(reverse('shop-detail', kwargs={'pk': self.shop.pk}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], self.shop.name)
# class CategoryViewTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.category = Category.objects.create(name="Test Category")
#
#     def test_get_category(self):
#         """
#         Тестирует получение существующей категории.
#         """
#         response = self.client.get(reverse('category-detail', kwargs={'pk': self.category.pk}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], self.category.name)
#
#     def test_create_category_invalid(self):
#         """
#         Тестирует недопустимое создание категории (например, без названия).
#         """
#         response = self.client.post(reverse('category-list'), {'name': ''})
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
# class UtilityFunctionTests(TestCase):
#     def test_str_to_bool(self):
#         """
#         Тестирует функцию str_to_bool.
#         """
#         true_values = ['yes', 'y', 'true', 't', '1']
#         false_values = ['no', 'n', 'false', 'f', '0']
#
#         for val in true_values:
#             self.assertTrue(str_to_bool(val))
#
#         for val in false_values:
#             self.assertFalse(str_to_bool(val))
#
#         with self.assertRaises(ValueError):
#             str_to_bool('invalid')
# # Create your tests here.
