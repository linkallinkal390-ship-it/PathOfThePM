from rest_framework.pagination import PageNumberPagination
from .responses import paginated_response
from collections import OrderedDict


class SessionPagination(PageNumberPagination):
    """
    Пагинация для сессий с links
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return paginated_response(self, data, message='Sessions retrieved successfully')
    
    def get_paginated_response_schema(self, schema):
        """
        Схема для OpenAPI/Swagger
        """
        return {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean', 'example': True},
                'message': {'type': 'string', 'example': 'Sessions retrieved successfully'},
                'count': {'type': 'integer', 'example': 100},
                'total_pages': {'type': 'integer', 'example': 10},
                'current_page': {'type': 'integer', 'example': 1},
                'page_size': {'type': 'integer', 'example': 10},
                'links': {
                    'type': 'object',
                    'properties': {
                        'self': {
                            'type': 'object',
                            'properties': {
                                'href': {'type': 'string', 'format': 'uri'},
                                'method': {'type': 'string'}
                            }
                        },
                        'next': {
                            'type': 'object',
                            'properties': {
                                'href': {'type': 'string', 'format': 'uri'},
                                'method': {'type': 'string'}
                            }
                        },
                        'previous': {
                            'type': 'object',
                            'properties': {
                                'href': {'type': 'string', 'format': 'uri'},
                                'method': {'type': 'string'}
                            }
                        }
                    }
                },
                'results': {'type': 'array', 'items': {'type': 'object'}}
            }
        }

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'
    page_query_param = 'page'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'message': 'данные успешно получены',
            'total_count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'data': data,
        })
