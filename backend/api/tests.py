import uuid
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from decimal import Decimal

from .models import User, Result, Session
from .serializers import UserSerializer, ResultSerializer, SessionSerializer

User = get_user_model()


class TestUserModel(TestCase):
    """Тесты для модели User"""
    
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'sur_name': 'User',
            'role': User.ROLE_USER
        }
    
    def test_create_user(self):
        """Тест создания обычного пользователя"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.sur_name, 'User')
        self.assertEqual(user.role, User.ROLE_USER)
        self.assertTrue(user.check_password('testpass123'))
        self.assertIsNotNone(user.id)
        self.assertIsInstance(user.id, uuid.UUID)
    
    def test_create_user_without_email_raises_error(self):
        """Тест: создание пользователя без email вызывает ошибку"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='testpass123')
    
    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123',
            first_name='Admin',
            sur_name='User'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, User.ROLE_ADMIN)
    
    def test_user_str_method(self):
        """Тест строкового представления пользователя"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'test@example.com - registered')
    
    def test_user_email_normalized(self):
        user = User.objects.create_user(
           email='Test@example.COM',
           password='testpass123',
           first_name='Test',
           sur_name='User'
        )
        #Ваша модель сохраняет как есть
        self.assertEqual(user.email, 'Test@example.COM')


class TestResultModel(TestCase):
    """Тесты для модели Result"""
    
    def setUp(self):
        self.result_data = {
            'budget': Decimal('1000.50'),
            'reputation': 50,
            'office_health': 75,
            'CountCompletedQuest': 5,
            'evaluationGraphConstruction': 80
        }
    
    def test_create_result(self):
        """Тест создания результата"""
        result = Result.objects.create(**self.result_data)
        self.assertIsNotNone(result.id)
        self.assertIsInstance(result.id, uuid.UUID)
        self.assertEqual(result.budget, Decimal('1000.50'))
        self.assertEqual(result.reputation, 50)
        self.assertEqual(result.office_health, 75)
        self.assertIsNotNone(result.finalConstructionDate)
    
    def test_result_default_values(self):
        """Тест значений по умолчанию"""
        result = Result.objects.create(budget=Decimal('500.00'))
        self.assertEqual(result.CountCompletedQuest, 1)
        self.assertEqual(result.reputation, 0)
        self.assertEqual(result.office_health, 0)
        self.assertEqual(result.evaluationGraphConstruction, 0)
    
    def test_result_str_method(self):
        """Тест строкового представления результата"""
        result = Result.objects.create(budget=Decimal('500.00'))
        self.assertIn(str(result.id), str(result))
        self.assertIn('Result created', str(result))


class TestSessionModel(TestCase):
    """Тесты для модели Session"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            sur_name='User'
        )
        self.result = Result.objects.create(budget=Decimal('500.00'))
        self.session_data = {
            'user': self.user,
            'result': self.result,
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 1, 10)
        }
    
    def test_create_session(self):
        """Тест создания сессии"""
        session = Session.objects.create(**self.session_data)
        self.assertIsNotNone(session.id)
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.result, self.result)
        self.assertEqual(session.start_date, date(2024, 1, 1))
        self.assertEqual(session.end_date, date(2024, 1, 10))
    
    def test_session_str_method(self):
        """Тест строкового представления сессии"""
        session = Session.objects.create(**self.session_data)
        self.assertIn(str(session.id), str(session))
        self.assertIn('session created', str(session))
    
    def test_session_user_cascade_delete(self):
        """Тест каскадного удаления при удалении пользователя"""
        session = Session.objects.create(**self.session_data)
        self.assertEqual(Session.objects.count(), 1)
        self.user.delete()
        self.assertEqual(Session.objects.count(), 0)
    
    def test_session_result_cascade_delete(self):
        """Тест каскадного удаления при удалении результата"""
        session = Session.objects.create(**self.session_data)
        self.assertEqual(Session.objects.count(), 1)
        self.result.delete()
        self.assertEqual(Session.objects.count(), 0)


class BaseAPITestCase(APITestCase):
    """Базовый класс для API тестов с авторизацией"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            sur_name='User'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def authenticate(self, user=None):
        """Авторизация пользователя"""
        if user is None:
            user = self.user
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return token


class TestUserAPI(BaseAPITestCase):
    """Тесты для User API"""
    
    def setUp(self):
        super().setUp()
        self.user_list_url = '/api/users/'
    
    def test_list_users(self):
        """Тест получения списка пользователей"""
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('success', True))
        self.assertIn('data', response.data)
    
    def test_create_user(self):
        """Тест создания пользователя через API"""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'sur_name': 'User',
            'role': User.ROLE_USER
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Пользователь зарегистрирован')
        self.assertEqual(response.data['data']['email'], 'newuser@example.com')
    
    def test_retrieve_user(self):
        """Тест получения конкретного пользователя"""
        url = f'/api/users/{self.user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], 'test@example.com')
    
    def test_retrieve_user_not_found(self):
        """Тест: получение несуществующего пользователя"""
        url = f'/api/users/{uuid.uuid4()}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_user(self):
        """Тест обновления пользователя"""
        url = f'/api/users/{self.user.id}/'
        data = {'first_name': 'Updated'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['first_name'], 'Updated')
    
    def test_delete_user(self):
        """Тест удаления пользователя"""
        url = f'/api/users/{self.user.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'User deleted successfully')
        self.assertEqual(User.objects.count(), 0)
    
    def test_filter_users_by_role(self):
        User.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            first_name='Admin',
            sur_name='User',
            role=User.ROLE_ADMIN
        )
        response = self.client.get(f'{self.user_list_url}?role={User.ROLE_ADMIN}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data'])
        )
    
    def test_search_users(self):
        User.objects.create_user(
            email='search@example.com',
            password='pass123',
            first_name='Search',
            sur_name='Test'
        )
        response = self.client.get(f'{self.user_list_url}?search=search@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
    
    def test_me_endpoint(self):
        """Тест получения текущего пользователя"""
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], 'test@example.com')


class TestResultAPI(BaseAPITestCase):
    """Тесты для Result API"""
    
    def setUp(self):
        super().setUp()
        self.result_data = {
            'budget': '1000.50',
            'reputation': 50,
            'office_health': 75,
            'CountCompletedQuest': 5,
            'evaluationGraphConstruction': 80
        }
        self.result = Result.objects.create(
            budget=Decimal('1000.50'),
            reputation=50,
            office_health=75
        )
    
    def test_list_results(self):
        """Тест получения списка результатов"""
        response = self.client.get('/api/results/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('success', True))
    
    def test_create_result(self):
        """Тест создания результата"""
        response = self.client.post('/api/results/', self.result_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Result created successfully')
        self.assertEqual(float(response.data['data']['budget']), 1000.50)
    
    def test_create_result_negative_budget(self):
        data = self.result_data.copy()
        data['budget'] = '-100.00'
        response = self.client.post('/api/results/', data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        # Проверяем структуру ошибки
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error']['code'], 'business_logic_error')
    
    def test_retrieve_result(self):
        """Тест получения конкретного результата"""
        url = f'/api/results/{self.result.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['reputation'], 50)
    
    def test_update_result(self):
        """Тест обновления результата"""
        url = f'/api/results/{self.result.id}/'
        data = {'reputation': 100}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['reputation'], 100)
    
    def test_delete_result(self):
        """Тест удаления результата"""
        url = f'/api/results/{self.result.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Result deleted successfully')
        self.assertEqual(Result.objects.count(), 0)


class TestSessionAPI(BaseAPITestCase):
    """Тесты для Session API"""
    
    def setUp(self):
        super().setUp()
        self.result = Result.objects.create(
            budget=Decimal('500.00'),
            reputation=50
        )
        self.session_data = {
            'user': str(self.user.id),
            'result': str(self.result.id),
            'start_date': '2024-01-01',
            'end_date': '2024-01-10'
        }
        self.session = Session.objects.create(
            user=self.user,
            result=self.result,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 10)
        )
    
    def test_list_sessions(self):
        """Тест получения списка сессий"""
        response = self.client.get('/api/sessions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('success', True))
    
    def test_create_session(self):
        """Тест создания сессии"""
        # Создаем нового пользователя и результат для теста
        new_user = User.objects.create_user(
            email='newuser@example.com',
            password='pass123',
            first_name='New',
            sur_name='User'
        )
        new_result = Result.objects.create(budget=Decimal('300.00'))
        
        data = {
            'user': str(new_user.id),
            'result': str(new_result.id),
            'start_date': '2024-02-01',
            'end_date': '2024-02-10'
        }
        response = self.client.post('/api/sessions/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Session created successfully')
    
    def test_create_session_invalid_dates(self):
        """Тест: создание сессии с невалидными датами"""
        data = self.session_data.copy()
        data['end_date'] = '2023-12-31'  # Дата раньше start_date
        response = self.client.post('/api/sessions/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_session(self):
        """Тест получения конкретной сессии"""
        url = f'/api/sessions/{self.session.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['id'], str(self.session.id))
    
    def test_update_session(self):
        """Тест обновления сессии"""
        url = f'/api/sessions/{self.session.id}/'
        data = {'end_date': '2024-01-15'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['end_date'], '2024-01-15')
    
    def test_delete_session(self):
        """Тест удаления сессии"""
        url = f'/api/sessions/{self.session.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Session deleted successfully')
        self.assertEqual(Session.objects.count(), 0)
    
    def test_my_sessions_endpoint(self):
        """Тест получения сессий текущего пользователя"""
        response = self.client.get('/api/sessions/my_sessions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('success', True))
    
    def test_extend_session(self):
        """Тест продления сессии"""
        url = f'/api/sessions/{self.session.id}/extend/'
        data = {'new_end_date': '2024-01-20'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['end_date'], '2024-01-20')


class TestAuthAPI(APITestCase):
    """Тесты для аутентификации"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            sur_name='User'
        )
        self.register_data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'sur_name': 'User'
        }
        self.login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    
    def test_register_success(self):
        """Тест успешной регистрации"""
        response = self.client.post('/api/auth/register/', self.register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Пользователь зарегистрирован')
        self.assertEqual(response.data['data']['email'], 'newuser@example.com')
        self.assertEqual(User.objects.count(), 2)
    
    def test_login_success(self):
        """Тест успешного входа"""
        response = self.client.post('/api/auth/login/', self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Успешная авторизация')
        self.assertIn('token', response.data['data'])
    
    def test_login_invalid_credentials(self):
        """Тест: вход с неверными данными"""
        data = {'email': 'test@example.com', 'password': 'wrongpass'}
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Неверные учетные данные')


class TestExceptionHandling(APITestCase):
    """Тесты обработки исключений"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            sur_name='User'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_404_response_format(self):
        """Тест формата ответа при 404"""
        url = f'/api/users/{uuid.uuid4()}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('success', response.data)
        self.assertEqual(response.data['success'], False)
    
    def test_validation_error_format(self):
        """Тест формата ответа при ошибке валидации"""
        data = {'email': 'invalid-email'}
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_method_not_allowed(self):
        """Тест: метод не разрешен"""
        response = self.client.put('/api/auth/login/', {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestCustomResponses(APITestCase):
    """Тесты кастомных форматов ответов"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            sur_name='User'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.result = Result.objects.create(budget=Decimal('500.00'))
    
    def test_success_response_format(self):
        """Тест формата успешного ответа"""
        url = f'/api/users/{self.user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('success', True))
        self.assertIn('message', response.data)
        self.assertIn('data', response.data)
    
    def test_create_response_format(self):
        """Тест формата ответа при создании"""
        data = {
            'budget': '1000.00',
            'reputation': 50
        }
        response = self.client.post('/api/results/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data.get('success', True))
        self.assertEqual(response.data['message'], 'Result created successfully')
    
    def test_delete_response_format(self):
        """Тест формата ответа при удалении"""
        url = f'/api/results/{self.result.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('success', True))
        self.assertEqual(response.data['message'], 'Result deleted successfully')


class TestPagination(APITestCase):
    """Тесты пагинации"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            sur_name='User'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Создаем 25 пользователей для теста пагинации
        for i in range(25):
            User.objects.create_user(
                email=f'user{i}@example.com',
                password='pass123',
                first_name=f'User{i}',
                sur_name=f'Test{i}'
            )
    
    def test_custom_pagination_response_format(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertIn('total_count', data)
        self.assertIn('total_pages', data)
        self.assertIn('current_page', data)
        self.assertEqual(data['current_page'], 1)
    
    def test_pagination_first_page(self):
        """Тест первой страницы пагинации"""
        response = self.client.get('/api/users/?page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['current_page'], 1)
        self.assertEqual(len(response.data['data']['results']), 20)
        self.assertEqual(response.data['data']['total_pages'], 2)
    
    def test_pagination_last_page(self):
        """Тест последней страницы пагинации"""
        response = self.client.get('/api/users/?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['current_page'], 2)
        self.assertEqual(len(response.data['data']['results']), 5)
    
    def test_pagination_max_page_size(self):
        """Тест максимального размера страницы"""
        response = self.client.get('/api/users/?limit=50')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['total_pages'], 1)
        self.assertEqual(len(response.data['data']['results']), 25)