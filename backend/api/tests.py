import pytest
import uuid
from decimal import Decimal
from datetime import date, timedelta
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Result, Session


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        'email': 'test@example.com',
        'first_name': 'John',
        'sur_name': 'Doe',
        'password': 'testpass123',
        'password_confirm': 'testpass123',
        'role': 'user'
    }


@pytest.fixture
def admin_user_data():
    return {
        'email': 'admin@example.com',
        'first_name': 'Admin',
        'sur_name': 'User',
        'password': 'adminpass123',
        'password_confirm': 'adminpass123',
        'role': 'admin'
    }


@pytest.fixture
def create_user(db, user_data):
    user = User.objects.create_user(
        email=user_data['email'],
        password=user_data['password'],
        first_name=user_data['first_name'],
        sur_name=user_data['sur_name'],
        role=user_data['role']
    )
    return user


@pytest.fixture
def create_admin_user(db, admin_user_data):
    admin = User.objects.create_superuser(
        email=admin_user_data['email'],
        password=admin_user_data['password'],
        first_name=admin_user_data['first_name'],
        sur_name=admin_user_data['sur_name'],
        role='admin'
    )
    return admin


@pytest.fixture
def authenticated_client(api_client, create_user):
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def admin_authenticated_client(api_client, create_admin_user):
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'email': 'admin@example.com',
        'password': 'adminpass123'
    })
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def result_data():
    return {
        'CountCompletedQuest': 5,
        'reputation': 80,
        'evaluationGraphConstruction': 90,
        'budget': '10000.00',
        'office_health': 85
    }


@pytest.fixture
def create_result(db, result_data):
    result = Result.objects.create(**result_data)
    return result


@pytest.fixture
def session_data(create_user, create_result):
    return {
        'user': create_user.id,
        'result': create_result.id,
        'start_date': '2024-01-01',
        'end_date': '2024-01-31'
    }


@pytest.fixture
def create_session(db, create_user, create_result):
    session = Session.objects.create(
        user=create_user,
        result=create_result,
        start_date='2024-01-01',
        end_date='2024-01-31'
    )
    return session


@pytest.fixture
def multiple_users(db):
    users = []
    for i in range(15):
        user = User.objects.create_user(
            email=f'user{i}@example.com',
            password='testpass123',
            first_name=f'User{i}',
            sur_name=f'Test{i}',
            role='user'
        )
        users.append(user)
    return users


@pytest.fixture
def multiple_sessions(db, create_user, create_result):
    sessions = []
    for i in range(15):
        session = Session.objects.create(
            user=create_user,
            result=create_result,
            start_date=f'2024-{str(i+1).zfill(2)}-01',
            end_date=f'2024-{str(i+1).zfill(2)}-28'
        )
        sessions.append(session)
    return sessions


class TestUserModel:
    
    def test_create_user(self, db, user_data):
        user = User.objects.create_user(**user_data)
        assert user.email == user_data['email']
        assert user.first_name == user_data['first_name']
        assert user.sur_name == user_data['sur_name']
        assert user.role == 'user'
        assert user.check_password(user_data['password'])
        assert user.is_active is True
        assert user.is_staff is False
    
    def test_create_superuser(self, db, admin_user_data):
        admin = User.objects.create_superuser(
            email=admin_user_data['email'],
            password=admin_user_data['password'],
            first_name=admin_user_data['first_name'],
            sur_name=admin_user_data['sur_name']
        )
        assert admin.email == admin_user_data['email']
        assert admin.role == 'admin'
        assert admin.is_staff is True
        assert admin.is_superuser is True
    
    def test_user_str_method(self, create_user):
        expected_str = f'{create_user.email} - registred'
        assert str(create_user) == expected_str
    
    def test_user_without_email_raises_error(self, db):
        with pytest.raises(ValueError):
            User.objects.create_user(email='', password='testpass123')
    
    def test_user_email_normalized(self, db):
        user = User.objects.create_user(
            email='Test@EXAMPLE.com',
            password='testpass123',
            first_name='Test',
            sur_name='User'
        )
        assert user.email == 'Test@example.com'
    
    def test_user_uuid_primary_key(self, create_user):
        assert isinstance(create_user.id, uuid.UUID)


class TestResultModel:
    
    def test_create_result(self, db, result_data):
        result = Result.objects.create(**result_data)
        assert result.CountCompletedQuest == result_data['CountCompletedQuest']
        assert result.reputation == result_data['reputation']
        assert result.budget == Decimal(result_data['budget'])
    
    def test_result_default_values(self, db):
        result = Result.objects.create(budget='5000.00')
        assert result.CountCompletedQuest == 1
        assert result.reputation == 0
        assert result.evaluationGraphConstruction == 0
        assert result.office_health == 0
    
    def test_result_str_method(self, create_result):
        expected_str = f'{create_result.id} - Result created'
        assert str(create_result) == expected_str


class TestSessionModel:
    
    def test_create_session(self, db, create_user, create_result):
        session = Session.objects.create(
            user=create_user,
            result=create_result,
            start_date='2024-01-01',
            end_date='2024-01-31'
        )
        assert session.user == create_user
        assert session.result == create_result
        assert session.start_date == date(2024, 1, 1)
        assert session.end_date == date(2024, 1, 31)
    
    def test_session_str_method(self, create_session):
        expected_str = f'{create_session.id} - session created'
        assert str(create_session) == expected_str
    
    def test_session_user_cascade_delete(self, db, create_user, create_result):
        session = Session.objects.create(
            user=create_user,
            result=create_result,
            start_date='2024-01-01',
            end_date='2024-01-31'
        )
        create_user.delete()
        assert Session.objects.filter(id=session.id).count() == 0
    
    def test_session_result_cascade_delete(self, db, create_user, create_result):
        session = Session.objects.create(
            user=create_user,
            result=create_result,
            start_date='2024-01-01',
            end_date='2024-01-31'
        )
        create_result.delete()
        assert Session.objects.filter(id=session.id).count() == 0


class TestUserAPI:
    
    def test_list_users(self, api_client, multiple_users):
        url = reverse('user-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) > 0
    
    def test_list_users_pagination(self, api_client, multiple_users):
        url = reverse('user-list')
        response = api_client.get(url, {'page_size': 5})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) <= 5
        assert 'links' in response.data
        assert 'next' in response.data['links']
    
    def test_create_user(self, api_client, user_data):
        url = reverse('user-list')
        response = api_client.post(url, user_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['email'] == user_data['email']
    
    def test_create_user_invalid_data(self, api_client):
        url = reverse('user-list')
        invalid_data = {
            'email': 'invalid-email',
            'password': 'short',
        }
        response = api_client.post(url, invalid_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_retrieve_user(self, api_client, create_user):
        url = reverse('user-detail', kwargs={'pk': create_user.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['email'] == create_user.email
    
    def test_retrieve_user_not_found(self, api_client):
        url = reverse('user-detail', kwargs={'pk': uuid.uuid4()})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_user(self, authenticated_client, create_user):
        url = reverse('user-detail', kwargs={'pk': create_user.id})
        updated_data = {
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'sur_name': 'Name'
        }
        response = authenticated_client.put(url, updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
    
    def test_delete_user(self, authenticated_client, create_user):
        url = reverse('user-detail', kwargs={'pk': create_user.id})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_filter_users_by_role(self, api_client, create_user, create_admin_user):
        url = reverse('user-list')
        response = api_client.get(url, {'role': 'admin'})
        assert response.status_code == status.HTTP_200_OK
        for user in response.data['results']:
            assert user['role'] == 'admin'
    
    def test_search_users(self, api_client, create_user):
        url = reverse('user-list')
        response = api_client.get(url, {'search': 'John'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1


class TestResultAPI:
    
    def test_list_results(self, api_client, create_result):
        url = reverse('result-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
    
    def test_create_result(self, api_client, result_data):
        url = reverse('result-list')
        response = api_client.post(url, result_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['reputation'] == result_data['reputation']
    
    def test_create_result_negative_budget(self, api_client, result_data):
        url = reverse('result-list')
        result_data['budget'] = '-1000.00'
        response = api_client.post(url, result_data, format='json')
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY]
    
    def test_retrieve_result(self, api_client, create_result):
        url = reverse('result-detail', kwargs={'pk': create_result.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['id'] == str(create_result.id)
    
    def test_update_result(self, api_client, create_result):
        url = reverse('result-detail', kwargs={'pk': create_result.id})
        updated_data = {
            'reputation': 95,
            'budget': '15000.00',
            'CountCompletedQuest': 10,
            'evaluationGraphConstruction': 88,
            'office_health': 90
        }
        response = api_client.put(url, updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
    
    def test_delete_result(self, api_client, create_result):
        url = reverse('result-detail', kwargs={'pk': create_result.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestSessionAPI:
    
    def test_list_sessions(self, api_client, create_session):
        url = reverse('session-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
    
    def test_create_session(self, api_client, session_data):
        url = reverse('session-list')
        response = api_client.post(url, session_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['start_date'] == session_data['start_date']
    
    def test_create_session_invalid_dates(self, api_client, create_user, create_result):
        url = reverse('session-list')
        invalid_data = {
            'user': create_user.id,
            'result': create_result.id,
            'start_date': '2024-12-31',
            'end_date': '2024-01-01'
        }
        response = api_client.post(url, invalid_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_retrieve_session(self, api_client, create_session):
        url = reverse('session-detail', kwargs={'pk': create_session.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['id'] == str(create_session.id)
    
    def test_update_session(self, api_client, create_session):
        url = reverse('session-detail', kwargs={'pk': create_session.id})
        updated_data = {
            'start_date': '2024-02-01',
            'end_date': '2024-02-28'
        }
        response = api_client.put(url, updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
    
    def test_delete_session(self, api_client, create_session):
        url = reverse('session-detail', kwargs={'pk': create_session.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_filter_sessions_by_user(self, api_client, create_user, create_session):
        url = reverse('session-list')
        response = api_client.get(url, {'user_id': create_user.id})
        assert response.status_code == status.HTTP_200_OK
    
    def test_filter_sessions_by_date_range(self, api_client, create_session):
        url = reverse('session-list')
        response = api_client.get(url, {
            'start_date': '2024-01-01',
            'end_date': '2024-12-31'
        })
        assert response.status_code == status.HTTP_200_OK
    
    def test_session_pagination(self, api_client, multiple_sessions):
        url = reverse('session-list')
        response = api_client.get(url, {'page_size': 5})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) <= 5
        assert 'links' in response.data
        assert 'next' in response.data['links']
        assert 'previous' in response.data['links']
        assert 'first' in response.data['links']
        assert 'last' in response.data['links']


class TestPagination:
    
    def test_custom_pagination_response_format(self, api_client, multiple_sessions):
        url = reverse('session-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'success' in response.data
        assert response.data['success'] is True
        assert 'count' in response.data
        assert 'total_pages' in response.data
        assert 'current_page' in response.data
        assert 'page_size' in response.data
        assert 'links' in response.data
        assert 'results' in response.data
    
    def test_pagination_first_page_no_previous(self, api_client, multiple_sessions):
        url = reverse('session-list')
        response = api_client.get(url, {'page': 1, 'page_size': 5})
        assert response.data['links']['previous']['href'] is None
        assert response.data['links']['first']['href'] is None
    
    def test_pagination_last_page_no_next(self, api_client, multiple_sessions):
        url = reverse('session-list')
        response = api_client.get(url, {'page': 1, 'page_size': 5})
        total_pages = response.data['total_pages']
        response = api_client.get(url, {'page': total_pages, 'page_size': 5})
        assert response.data['links']['next']['href'] is None
        assert response.data['links']['last']['href'] is None
    
    def test_pagination_max_page_size(self, api_client, multiple_sessions):
        url = reverse('session-list')
        response = api_client.get(url, {'page_size': 1000})
        assert response.data['page_size'] <= 100


class TestAuthAPI:
    
    def test_login_success(self, api_client, create_user):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_login_invalid_credentials(self, api_client):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_token_refresh(self, api_client, create_user):
        login_url = reverse('token_obtain_pair')
        login_response = api_client.post(login_url, {
            'email': 'test@example.com',
            'password': 'testpass123'
        }, format='json')
        
        refresh_url = reverse('token_refresh')
        refresh_response = api_client.post(refresh_url, {
            'refresh': login_response.data['refresh']
        }, format='json')
        
        assert refresh_response.status_code == status.HTTP_200_OK
        assert 'access' in refresh_response.data
    
    def test_access_protected_endpoint_without_auth(self, api_client, create_user):
        url = reverse('user-detail', kwargs={'pk': create_user.id})
        response = api_client.put(url, {}, format='json')
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


class TestExceptionHandling:
    
    def test_404_response_format(self, api_client):
        url = reverse('user-detail', kwargs={'pk': uuid.uuid4()})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'success' in response.data
        assert response.data['success'] is False
    
    def test_validation_error_format(self, api_client):
        url = reverse('session-list')
        response = api_client.post(url, {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'success' in response.data
        assert response.data['success'] is False
    
    def test_method_not_allowed(self, api_client):
        url = reverse('session-list')
        response = api_client.put(url, {}, format='json')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestCustomResponses:
    
    def test_success_response_format(self, api_client, create_session):
        url = reverse('session-detail', kwargs={'pk': create_session.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'success' in response.data
        assert response.data['success'] is True
        assert 'message' in response.data
        assert 'data' in response.data
    
    def test_create_response_format(self, api_client, session_data):
        url = reverse('session-list')
        response = api_client.post(url, session_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'success' in response.data
        assert response.data['success'] is True
        assert 'message' in response.data
        assert 'data' in response.data
    
    def test_delete_response_format(self, api_client, create_session):
        url = reverse('session-detail', kwargs={'pk': create_session.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT