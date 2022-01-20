from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models


class UserManager(BaseUserManager):
    def _create(self, email, password, name, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, name, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        return self._create(email, password, name, **extra_fields)

    def create_superuser(self, email, password, name, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self._create(email, password, name, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=150, primary_key=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(6, '0123456789')
        if User.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = code
        self.save()

    def send_activation_mail(self, action):
        if action == 'register':
            message = f'http:/localhost:8000/account/activate/{self.activation_code}/'
        else:
            message = f'Ваш код подтверждения: {self.activation_code}'
        send_mail(
            'Активация аккаунта',
            message,
            'test@gmail.com',
            [self.email]
        )

