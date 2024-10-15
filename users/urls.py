from django.urls import path, include
from apirest.urls import drf_router
from users.viewsets import UserViewSet, RegisterViewSet, AuthTokenViewset

# Configuramos las urls de nuestra app usuarios
urlpatterns = [
]

drf_router.register(r'users', UserViewSet)
drf_router.register(r'register', RegisterViewSet)
drf_router.register(r'login', AuthTokenViewset)