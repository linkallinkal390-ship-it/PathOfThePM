from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Создаем роутер
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'results', views.ResultViewSet, basename='result')
router.register(r'sessions', views.SessionViewSet, basename='session')

# URL-паттерны
urlpatterns = [
    path('auth/register/', views.RegisterView.as_view()),
    path('auth/login/', views.LoginView.as_view()),
    path('', include(router.urls)),
]

api_urlpatterns = router.urls