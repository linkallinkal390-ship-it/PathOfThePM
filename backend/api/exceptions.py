# Цель №3
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    APIException, 
    ValidationError, 
    NotFound, 
    PermissionDenied,
    AuthenticationFailed,
    NotAuthenticated,
    MethodNotAllowed,
    Throttled
)
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from collections import OrderedDict


class BaseCustomException(APIException):
    """
    Базовое кастомное исключение
    """
    default_code = 'error'
    
    def __init__(self, detail=None, code=None, errors=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
            
        self.detail = {
            'success': False,
            'error': {
                'code': code,
                'message': detail,
                'errors': errors or []
            }
        }


class SessionNotFoundException(BaseCustomException):
    """
    Сессия не найдена
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Session not found'
    default_code = 'session_not_found'


class SessionValidationError(BaseCustomException):
    """
    Ошибка валидации сессии
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Session validation error'
    default_code = 'session_validation_error'


class SessionCreateError(BaseCustomException):
    """
    Ошибка создания сессии
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error creating session'
    default_code = 'session_create_error'


class SessionUpdateError(BaseCustomException):
    """
    Ошибка обновления сессии
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error updating session'
    default_code = 'session_update_error'


class SessionDeleteError(BaseCustomException):
    """
    Ошибка удаления сессии
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error deleting session'
    default_code = 'session_delete_error'


class ResultNotFoundException(BaseCustomException):
    """
    Результат не найден
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Result not found'
    default_code = 'result_not_found'


class ResultValidationError(BaseCustomException):
    """
    Ошибка валидации результата
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Result validation error'
    default_code = 'result_validation_error'


class UserNotFoundException(BaseCustomException):
    """
    Пользователь не найден
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'User not found'
    default_code = 'user_not_found'


class UserValidationError(BaseCustomException):
    """
    Ошибка валидации пользователя
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User validation error'
    default_code = 'user_validation_error'


class BusinessLogicError(BaseCustomException):
    """
    Ошибка бизнес-логики
    """
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'Business logic error'
    default_code = 'business_logic_error'


class SessionDateConflictError(BaseCustomException):
    """
    Конфликт дат сессии
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Session dates conflict with existing session'
    default_code = 'session_date_conflict'


class UnauthorizedAccessError(BaseCustomException):
    """
    Неавторизованный доступ
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Authentication credentials were not provided'
    default_code = 'unauthorized'


class ForbiddenAccessError(BaseCustomException):
    """
    Доступ запрещен
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action'
    default_code = 'forbidden'


class RateLimitExceeded(BaseCustomException):
    """
    Превышен лимит запросов
    """
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'Rate limit exceeded. Please try again later'
    default_code = 'rate_limit_exceeded'


class ServerError(BaseCustomException):
    """
    Внутренняя ошибка сервера
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Internal server error'
    default_code = 'server_error'


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'success': False,
            'error': {
                'code': get_error_code(exc, response),
                'message': get_error_message(exc, response),
                'errors': get_error_details(exc, response),
                'path': context.get('request', {}).path if hasattr(context.get('request', {}), 'path') else None,
                'method': context.get('request', {}).method if hasattr(context.get('request', {}), 'method') else None
            }
        }
        
        response.data = custom_response_data
        
    return response


def get_error_code(exc, response):
    """
    Получить код ошибки
    """
    if hasattr(exc, 'default_code'):
        return exc.default_code
    elif hasattr(exc, 'code'):
        return exc.code
    else:
        return 'error'
    
    
def get_error_message(exc, response):
    """
    Получить сообщение ошибки
    """
    if hasattr(exc, 'detail'):
        if isinstance(exc.detail, dict):
            return 'Validation error'
        elif isinstance(exc.detail, list):
            return exc.detail[0] if exc.detail else 'Error'
        return str(exc.detail)
    return str(exc)


def get_error_details(exc, response):
    """
    Получить детали ошибки
    """
    errors = []
    
    if hasattr(exc, 'detail'):
        if isinstance(exc.detail, dict):
            # Ошибки валидации по полям
            for field, field_errors in exc.detail.items():
                if isinstance(field_errors, list):
                    for error in field_errors:
                        errors.append({
                            'field': field,
                            'message': str(error)
                        })
                else:
                    errors.append({
                        'field': field,
                        'message': str(field_errors)
                    })
        elif isinstance(exc.detail, list):
            for error in exc.detail:
                if isinstance(error, dict):
                    for field, field_errors in error.items():
                        errors.append({
                            'field': field,
                            'message': str(field_errors)
                        })
                else:
                    errors.append({
                        'field': 'non_field_errors',
                        'message': str(error)
                    })
    
    return errors