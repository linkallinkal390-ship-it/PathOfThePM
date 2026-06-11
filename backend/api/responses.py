from rest_framework.response import Response
from rest_framework import status
from collections import OrderedDict


class APIResponse(Response):
    """
    Кастомный Response для API
    """
    def __init__(self, data=None, message=None, status_code=None, 
                 template_name=None, headers=None, exception=False, 
                 content_type=None, **kwargs):
        
        response_data = OrderedDict()
        response_data['success'] = status_code in range(200, 300) if status_code else True
        
        if message:
            response_data['message'] = message
            
        if data is not None:
            if isinstance(data, dict) and 'results' in data:
                # Для пагинированных ответов
                response_data.update(data)
            elif isinstance(data, dict):
                response_data['data'] = data
            elif isinstance(data, list):
                response_data['data'] = data
                response_data['count'] = len(data)
            else:
                response_data['data'] = data
        
        # Добавляем дополнительные поля
        response_data.update(kwargs)
        
        super().__init__(
            data=response_data,
            status=status_code,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )


def success_response(data=None, message='Success', status_code=status.HTTP_200_OK, **kwargs):
    """
    Успешный ответ
    """
    return APIResponse(
        data=data,
        message=message,
        status_code=status_code,
        **kwargs
    )


def created_response(data=None, message='Resource created successfully', **kwargs):
    """
    Ответ при создании ресурса
    """
    return APIResponse(
        data=data,
        message=message,
        status_code=status.HTTP_201_CREATED,
        **kwargs
    )


def updated_response(data=None, message='Resource updated successfully', **kwargs):
    """
    Ответ при обновлении ресурса
    """
    return APIResponse(
        data=data,
        message=message,
        status_code=status.HTTP_200_OK,
        **kwargs
    )


def deleted_response(message='Resource deleted successfully', **kwargs):
    """
    Ответ при удалении ресурса
    """
    return APIResponse(
        data=None,
        message=message,
        status_code=status.HTTP_204_NO_CONTENT,
        **kwargs
    )


def error_response(message='Error occurred', errors=None, error_code='error', 
                   status_code=status.HTTP_400_BAD_REQUEST, **kwargs):
    """
    Ответ с ошибкой
    """
    error_data = {
        'code': error_code,
        'message': message,
        'errors': errors or []
    }
    
    return APIResponse(
        data=None,
        success=False,
        error=error_data,
        status_code=status_code,
        **kwargs
    )


def validation_error_response(errors, message='Validation error', **kwargs):
    """
    Ответ с ошибками валидации
    """
    formatted_errors = []
    
    if isinstance(errors, dict):
        for field, field_errors in errors.items():
            if isinstance(field_errors, list):
                for error in field_errors:
                    formatted_errors.append({
                        'field': field,
                        'message': str(error)
                    })
            else:
                formatted_errors.append({
                    'field': field,
                    'message': str(field_errors)
                })
    elif isinstance(errors, list):
        formatted_errors = errors
    
    return error_response(
        message=message,
        errors=formatted_errors,
        error_code='validation_error',
        status_code=status.HTTP_400_BAD_REQUEST,
        **kwargs
    )


def paginated_response(paginator, data, message='Data retrieved successfully'):
    """
    Ответ с пагинацией
    """
    response_data = OrderedDict([
        ('success', True),
        ('message', message),
        ('count', paginator.page.paginator.count),
        ('total_pages', paginator.page.paginator.num_pages),
        ('current_page', paginator.page.number),
        ('page_size', paginator.get_page_size(paginator.request)),
        ('links', OrderedDict([
            ('self', OrderedDict([
                ('href', paginator.request.build_absolute_uri()),
                ('method', 'GET')
            ])),
            ('first', OrderedDict([
                ('href', paginator.get_first_link()),
                ('method', 'GET')
            ])),
            ('last', OrderedDict([
                ('href', paginator.get_last_link()),
                ('method', 'GET')
            ])),
            ('next', OrderedDict([
                ('href', paginator.get_next_link()),
                ('method', 'GET')
            ])),
            ('previous', OrderedDict([
                ('href', paginator.get_previous_link()),
                ('method', 'GET')
            ]))
        ])),
        ('results', data)
    ])
    
    return Response(response_data)


def not_found_response(resource_name='Resource', **kwargs):
    """
    Ответ "не найдено"
    """
    return error_response(
        message=f'{resource_name} not found',
        error_code='not_found',
        status_code=status.HTTP_404_NOT_FOUND,
        **kwargs
    )


def unauthorized_response(message='Authentication required', **kwargs):
    """
    Ответ "не авторизован"
    """
    return error_response(
        message=message,
        error_code='unauthorized',
        status_code=status.HTTP_401_UNAUTHORIZED,
        **kwargs
    )


def forbidden_response(message='Permission denied', **kwargs):
    """
    Ответ "доступ запрещен"
    """
    return error_response(
        message=message,
        error_code='forbidden',
        status_code=status.HTTP_403_FORBIDDEN,
        **kwargs
    )


def server_error_response(message='Internal server error', **kwargs):
    """
    Ответ "внутренняя ошибка сервера"
    """
    return error_response(
        message=message,
        error_code='server_error',
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        **kwargs
    )