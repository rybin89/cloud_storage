from django.contrib.auth import logout
from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerilizer,RegisterSerializer


# Create your views here.

class LoginView(views.APIView):
    '''
    Вход
    '''
    permission_classes = [AllowAny] # Доступен всем

    def post(self,request):
        '''
        POST запрос на авторизацию
        :param request:
        :return:
        '''
        serilizer = LoginSerilizer(data=request.data)

        if serilizer.is_valid():
            # получим пользователя
            user = serilizer.validated_data['user']

            # Создаём JWT токен
            refrech = RefreshToken.for_user(user)
            access_token = str(refrech.access_token)

            # Вернуть ответ
            return Response({
                "success": True,
                "message": "Success",
                "token": access_token
            },status=status.HTTP_200_OK)
        ## ПРОВЕРКА ОШИБОК
        else:
            return Response({
                "success": False,
                "message": "Login failed"
            }, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(views.APIView):
    '''
    Регистрация
    '''
    permission_classes = [AllowAny]  # Доступен всем

    def post(self, request):
        serilizer = RegisterSerializer(data=request.data)
        if serilizer.is_valid():
            user = serilizer.save()
            # Создаём JWT токен
            refrech = RefreshToken.for_user(user)
            access_token = str(refrech.access_token)
            return Response({
                "success": True,
                "message": "Success",
                "token": access_token
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "message": "Registration failed",
                "errors": serilizer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
class LogoutView(views.APIView):
    def post(self,request):
        logout(request)
        return Response({
            "success": True,
            "message": "Logout"
        }, status=status.HTTP_200_OK)