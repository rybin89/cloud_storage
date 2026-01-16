# сериализатор - это класс преобразующий данные для API
from rest_framework import  serializers
from django.contrib.auth import authenticate
from .models import User

class LoginSerilizer(serializers.Serializer):
    '''
    Преобразует данные при авторизации
    '''
    email = serializers.EmailField(required=True) # Преобразует введеённый пользователем email и проверит его наличе
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        '''
        Проверяет учётные данные пользователя
        Возвращает словарь с данными, если проверка прошла успешно
        :param data:
        :return:
        '''
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError({
                'success': False,
                'message': {
                    "email": ["Вы не ввели email" if not email else ''],
                    "password": ["field password can not be blank" if not password else '']
                }
            })
        # Аутентификация (для кастомной модели User с USERNAME_FIELD='email' используем username=email)
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                {
                    'success': False,
                    "message": "Login failed"
                }
            )
        # Довить пользователя в Валидные данные
        data['user'] = user
        return data

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)  # Преобразует введеённый пользователем email и проверит его наличе
    password = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def validate(self, data):
        '''
        Проверяет данные при регистрации
        '''
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if not email or not password or not first_name or not last_name:
            raise serializers.ValidationError({
                'success': False,
                'message': {
                    "email": ["Вы не ввели email" if not email else ''],
                    "password": ["field password can not be blank" if not password else ''],
                    "first_name": ["field first_name can not be blank" if not first_name else ''],
                    "last_name": ["field last_name can not be blank" if not last_name else ''],
                }
            })
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        return user