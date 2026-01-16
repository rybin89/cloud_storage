from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.



class UserManager(BaseUserManager):
      '''
      Кастомный менеджер управления пользователями
      '''
      def create_user(self,email,password, **extra_filds):
          '''
          Метод создания и сохранения пользоватеоля
          :param email:
          :param password:
          :param extar_filds:
          :return:
          '''
          if not email:
              raise ValueError('Вы не ввели свой Email')
          email = self.normalize_email(email)
          user = self.model(email=email, **extra_filds)
          user.set_password(password)
          user.save()
          return user
      def create_superuser(self,email,password, **extra_filds):
          '''
                   Метод создания и сохранения суперпользоватеоля
                   :param email:
                   :param password:
                   :param extar_filds:
                   :return:
            '''
          extra_filds.setdefault('is_staff',True)
          extra_filds.setdefault('is_superuser',True)
          extra_filds.setdefault('is_active',True)
          if extra_filds.get('is_staff') is not True:
              raise ValueError("Суперпользоватль должен is_staff = True")
          if extra_filds.get('is_superuser') is not True:
              raise ValueError("Суперпользоватль должен is_superuser = True")
          return self.create_user(email,password,**extra_filds)


# Создание своей модели User
class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # Заменить username на email
    username = None  # убрал username
    USERNAME_FIELD = 'email'  # Для входа надо ввести email
    REQUIRED_FIELDS = ['first_name', 'last_name']  # для суперпользователя

    objects = UserManager()

    # Сохраняем данные пользователя в БД
    def save(self, *args, **kwargs):
        # Хешируем пароль если он не хеширован
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    # Метод преобразует email в строку
    def __str__(self):
        return self.email