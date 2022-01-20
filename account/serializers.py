from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


def normalize_email(email):
    """
    Normalize the email address by lowercasing the domain part of it.
    """
    email = email or ''
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError:
        pass
    else:
        email = email_name + '@' + domain_part.lower()
    return email


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    name = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        email = normalize_email(email)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользовтель с этим email'ом уже существует")
        return email

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.pop('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self):#для создан пользователя
        user = User.objects.create_user(**self.validated_data)
        user.create_activation_code()
        user.send_activation_mail()


class ActivationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6, required=True)

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return code

    def activate(self):
        code = self.validated_data.get('code')
        user = User.objects.get(activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        email = normalize_email(email)
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError('Неверный пароль')
        if not user.is_active:
            raise serializers.ValidationError('Аккаунт не активен')
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=6)
    new_pass = serializers.CharField(max_length=6)
    new_pass_confirm = serializers.CharField(max_length=6)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if user.check_password(old_password):
            raise serializers.ValidationError('Укажите верный текущий пароль')
        return old_password

    def validate(self, validated_data):
        new_pass = validated_data.get('new_pass')
        new_pass_confirm = validated_data.get('new_pass_confirm')
        if new_pass != new_pass_confirm:
            raise serializers.ValidationError('Неверный пароль или его подтверждение')
        return validated_data

    def set_new_pass(self):
        new_pass = self.validated_data.get('new_pass')
        user = self.context.get('request').user
        user.set_password(new_pass)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)

    def validate_email(self, email):
        phone = normalize_email(email)
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользовтеля с этим email'ом не существует")
        return email

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.filter(email=email)
        user.create_activation_code()
        user.send_activation_mail()


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)
    new_pass = serializers.CharField(max_length=6)
    new_pass_confirm = serializers.CharField(max_length=6)

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return code

    def validate(self, validated_data):
        new_pass = validated_data.get('new_pass')
        new_pass_confirm = validated_data.get('new_pass_confirm')
        if new_pass != new_pass_confirm:
            raise serializers.ValidationError('Неверный пароль или его подтверждение')
        return validated_data

    def set_new_pass(self):
        code = self.validated_data.get('code')
        new_pass = self.validated_data.get('new_pass')
        user = User.objects.get(activation_code=code)
        user.set_password(new_pass)
        user.save()
