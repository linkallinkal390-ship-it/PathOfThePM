from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

# Создаем роутер
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'results', views.ResultViewSet, basename='result')
router.register(r'sessions', views.SessionViewSet, basename='session')

# URL-паттерны
urlpatterns = [
    path('auth/register/', views.RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auht/merinda/', include(router.urls)),
]

api_urlpatterns = router.urls