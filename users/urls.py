from django.urls import path, include
from apirest.urls import drf_router
from users.viewsets import UserViewSet, RegisterViewSet, AuthTokenViewset

# Configuramos las urls de nuestra app users
urlpatterns = [
]

drf_router.register(r'users', UserViewSet, basename='users')
drf_router.register(r'register', RegisterViewSet, basename='register')
drf_router.register(r'login', AuthTokenViewset, basename='login')