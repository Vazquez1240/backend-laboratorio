from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, TokenBackendError
from .models import User
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer
from rest_framework import exceptions
# from .permissions import IsAuthenticatedAndObjUserOrIsStaff
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

class UserViewSet(ModelViewSet):
    parser_classes = [JSONParser]
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticatedAndObjUserOrIsStaff]
    http_method_names = ['get', 'post', 'delete', 'options']

    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        elif self.request.user.is_staff:
            return User.objects.all()
        elif self.request.user.is_authenticated:
            return User.objects.filter(pk=self.request.user.pk)
        else:
            raise exceptions.PermissionDenied('Forbidden')


class RegisterViewSet(viewsets.ViewSet):
    http_method_names = ['post', 'options', 'head']
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data['username'],' data')
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': '201'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AuthTokenViewset(viewsets.ViewSet):
    http_method_names = ['post', 'options', 'head']
    permission_classes = [AllowAny]

    def create(self, request):
        view = TokenObtainPairView.as_view()
        try:
            response = view(request._request)
            data = response.data
            if 'refresh' in data and 'access' in data:
                return Response({
                    'refresh': data['refresh'],
                    'access': data['access'],
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid response from token view'}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidToken as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except TokenBackendError as e:
            return Response({'error': 'Token backend error'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
