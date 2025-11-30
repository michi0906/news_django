from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    # email と password でユーザーをDBに保存するための役割。Django認証が参照するレイヤーとして確定。
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("email required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # パスワードはハッシュ化され保存される → 平文では保存されない仕様として確定
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # emailをusernameとして使う設計。Django認証仕様で照合キーとして使う位置が確定している。
    email = models.EmailField(unique=True)  # 重複を許さない確定仕様。Userテーブルの照合キーになる。
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # Django authenticate() が拾う照合キーの名称として確定
    REQUIRED_FIELDS = []  # 追加で必須フィールドは無し → 提出適正を満たす確定仕様

    def __str__(self):
        return self.email
