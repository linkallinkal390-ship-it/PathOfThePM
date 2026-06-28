from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from rest_framework.serializers import ValidationError

from .models import User, Result, Session
from .serializers import (
    UserSerializer, 
    ResultSerializer, 
    SessionSerializer,
    SessionCreateSerializer,
    SessionUpdateSerializer,
    RegisterSerializer,
    LoginSerializer
)
from .pagination import CustomPageNumberPagination
from .exceptions import (
    SessionNotFoundException,
    SessionValidationError,
    SessionCreateError,
    SessionUpdateError,
    SessionDeleteError,
    ResultNotFoundException,
    UserNotFoundException,
    BusinessLogicError,
    SessionDateConflictError,
    UnauthorizedAccessError,
    ForbiddenAccessError
)
from .responses import (
    success_response,
    created_response,
    updated_response,
    deleted_response,
    error_response,
    validation_error_response,
    not_found_response,
    unauthorized_response,
    forbidden_response,
    server_error_response
)



class RegisterView(APIView):
    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'message': 'Пользователь зарегистрирован',
                'data': {
                    'id': user.id, 
                    'email': user.email,
                    'role': user.role,
                    'first_name': user.first_name,
                    'sur_name': user.sur_name,
                    },
            },
            status=status.HTTP_201_CREATED,
        )

class LoginView(APIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                {'message': 'Неверные учетные данные'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'message': 'Успешная авторизация',
                'data': {'token': token.key},
            },
        )



class BaseViewSet(viewsets.ModelViewSet):
    """
    Базовый ViewSet с кастомными методами ответа
    """
    
    def handle_exception(self, exc):
        """
        Обработка исключений
        """
        if isinstance(exc, (SessionNotFoundException, ResultNotFoundException, 
                           UserNotFoundException)):
            return not_found_response(resource_name=exc.default_detail.split(' ')[0])
        
        elif isinstance(exc, (SessionValidationError, SessionCreateError, 
                            SessionUpdateError)):
            return validation_error_response(
                errors=exc.detail.get('error', {}).get('errors', []),
                message=exc.detail.get('error', {}).get('message', 'Validation error')
            )
        
        elif isinstance(exc, SessionDateConflictError):
            return error_response(
                message=str(exc.detail.get('error', {}).get('message', 'Conflict')),
                error_code='date_conflict',
                status_code=status.HTTP_409_CONFLICT
            )
        
        elif isinstance(exc, UnauthorizedAccessError):
            return unauthorized_response()
        
        elif isinstance(exc, ForbiddenAccessError):
            return forbidden_response()
        
        elif isinstance(exc, BusinessLogicError):
            return error_response(
                message=str(exc.detail.get('error', {}).get('message', 'Business logic error')),
                error_code='business_logic_error',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        return super().handle_exception(exc)


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['email', 'first_name', 'sur_name']
    ordering_fields = ['created_at', 'email', 'first_name']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')
        is_active = self.request.query_params.get('is_active')

        if role:
            queryset = queryset.filter(role=role)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data,
            message='User retrieved successfully'
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return created_response(
                data=serializer.data,
                message='User created successfully'
            )
        raise ValidationError(serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return updated_response(
                data=serializer.data,
                message='User updated successfully'
            )
        raise ValidationError(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return deleted_response(message='User deleted successfully')

    @action(detail=False, methods=['get'])
    def me(self, request):
        if not request.user.is_authenticated:
            raise UnauthorizedAccessError()

        serializer = self.get_serializer(request.user)
        return success_response(
            data=serializer.data,
            message='Current user retrieved successfully'
        )

class ResultViewSet(BaseViewSet):
    """
    ViewSet для работы с результатами
    """
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['reputation', 'office_health']
    ordering_fields = ['finalConstructionDate', 'budget', 'reputation']
    ordering = ['-finalConstructionDate']
    
    def retrieve(self, request, *args, **kwargs):
        """
        Получить результат по ID
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return success_response(
                data=serializer.data,
                message='Result retrieved successfully'
            )
        except Result.DoesNotExist:
            raise ResultNotFoundException()
    
    def create(self, request, *args, **kwargs):
        """
        Создать новый результат
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return validation_error_response(
                errors=serializer.errors,
                message='Validation error'
            )
        
        # Проверка бизнес-логики
        budget = serializer.validated_data.get('budget', 0)
        if budget < 0:
            raise BusinessLogicError(
                detail={'error': {'message': 'Budget cannot be negative', 'errors': []}}
            )
        
        self.perform_create(serializer)
        return created_response(
            data=serializer.data,
            message='Result created successfully'
        )
    
    def update(self, request, *args, **kwargs):
        """
        Обновить результат
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            return validation_error_response(
                errors=serializer.errors,
                message='Validation error'
            )
        
        self.perform_update(serializer)
        return updated_response(
            data=serializer.data,
            message='Result updated successfully'
        )
    
    def destroy(self, request, *args, **kwargs):
        """
        Удалить результат
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return deleted_response(message='Result deleted successfully')
    

class SessionViewSet(BaseViewSet):
    """
    ViewSet для работы с сессиями
    """
    queryset = Session.objects.all().select_related('user', 'result')
    serializer_class = SessionSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'result']
    ordering_fields = ['start_date', 'end_date']
    ordering = ['-start_date']
    
    def get_serializer_class(self):
        """
        Разные сериалайзеры для разных действий
        """
        if self.action == 'create':
            return SessionCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SessionUpdateSerializer
        return SessionSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        user_id = self.request.query_params.get('user_id')
        result_id = self.request.query_params.get('result_id')
        
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if result_id:
            queryset = queryset.filter(result_id=result_id)
            
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """
        Получить сессию по ID
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return success_response(
                data=serializer.data,
                message='Session retrieved successfully'
            )
        except Session.DoesNotExist:
            raise SessionNotFoundException()
    
    def create(self, request, *args, **kwargs):
        """
        Создать новую сессию
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Проверка на конфликт дат
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')
            user = serializer.validated_data.get('user')
            
            if start_date and end_date and user:
                conflicting_sessions = Session.objects.filter(
                    user=user,
                    start_date__lte=end_date,
                    end_date__gte=start_date
                )
                if conflicting_sessions.exists():
                    raise SessionDateConflictError(
                        detail='User already has a session in this date range'
                    )
            
            self.perform_create(serializer)
            return created_response(
                data=serializer.data,
                message='Session created successfully'
            )
        raise SessionValidationError(detail='Validation error', errors=serializer.errors)
    
    def update(self, request, *args, **kwargs):
        """
        Обновить сессию
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return updated_response(
                data=serializer.data,
                message='Session updated successfully'
            )
        raise SessionUpdateError(detail='Validation error', errors=serializer.errors)
    
    def destroy(self, request, *args, **kwargs):
        """
        Удалить сессию
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return deleted_response(message='Session deleted successfully')
        except Session.DoesNotExist:
            raise SessionNotFoundException()
        except Exception as e:
            raise SessionDeleteError(detail=str(e))
    
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """
        Получить детальную информацию о сессии
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Дополнительная информация
        detailed_data = serializer.data
        detailed_data['user_details'] = {
            'email': instance.user.email,
            'full_name': f"{instance.user.first_name} {instance.user.sur_name}"
        }
        detailed_data['result_details'] = {
            'reputation': instance.result.reputation,
            'budget': float(instance.result.budget)
        }
        
        return success_response(
            data=detailed_data,
            message='Session details retrieved successfully'
        )
    
    @action(detail=False, methods=['get'])
    def my_sessions(self, request):
        """
        Получить сессии текущего пользователя
        """
        if not request.user.is_authenticated:
            raise UnauthorizedAccessError()
        
        sessions = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(sessions)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(sessions, many=True)
        return success_response(
            data=serializer.data,
            message='My sessions retrieved successfully'
        )
    
    @action(detail=False, methods=['get'])
    def by_date_range(self, request):
        """
        Получить сессии за период
        """
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        
        if not from_date or not to_date:
            return error_response(
                message='from_date and to_date parameters are required',
                error_code='missing_parameters',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        sessions = self.get_queryset().filter(
            start_date__gte=from_date,
            end_date__lte=to_date
        )
        
        page = self.paginate_queryset(sessions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(sessions, many=True)
        return success_response(
            data=serializer.data,
            message=f'Sessions from {from_date} to {to_date} retrieved successfully'
        )
    
    @action(detail=True, methods=['post'])
    def extend(self, request, pk=None):
        """
        Продлить сессию
        """
        instance = self.get_object()
        new_end_date = request.data.get('new_end_date')
        
        if not new_end_date:
            return error_response(
                message='new_end_date is required',
                error_code='missing_parameter',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверка бизнес-логики
        if new_end_date <= str(instance.end_date):
            raise BusinessLogicError(detail='New end date must be after current end date')
        
        instance.end_date = new_end_date
        instance.save()
        
        serializer = self.get_serializer(instance)
        return updated_response(
            data=serializer.data,
            message='Session extended successfully'
        )